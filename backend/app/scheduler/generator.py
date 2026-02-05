from ortools.sat.python import cp_model
from sqlalchemy.orm import Session
from typing import List, Dict, Tuple
import time
from datetime import datetime, timedelta

from app.models.horario import Horario, HorarioAula
from app.models.grade_curricular import GradeCurricular
from app.models.disponibilidade import Disponibilidade
from app.models.professor import Professor
from app.models.ambiente import Ambiente
from app.models.turma import Turma


class HorarioGenerator:
    """
    Motor de geração de horários usando programação com restrições (CP-SAT do OR-Tools).
    """
    
    def __init__(self, db: Session, horario_id: int):
        self.db = db
        self.horario_id = horario_id
        self.horario = db.query(Horario).filter(Horario.id == horario_id).first()
        
        if not self.horario:
            raise ValueError(f"Horário ID {horario_id} não encontrado")
        
        # Configurações de tempo
        self.dias_semana = ["SEGUNDA", "TERCA", "QUARTA", "QUINTA", "SEXTA"]
        self.slots_por_dia = 6  # 6 aulas por dia
        self.duracao_aula = 50  # minutos
        self.horario_inicio_manha = "07:30"
        
        # Modelo CP-SAT
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        
        # Variáveis do modelo
        self.variaveis = {}
        self.grades = []
        self.professores = {}
        self.turmas = {}
        self.ambientes = []
        self.disponibilidades = {}
        
        # Pendências encontradas
        self.pendencias = []
        
    def carregar_dados(self):
        """Carrega todos os dados necessários do banco"""
        # Carregar grades curriculares ativas
        self.grades = self.db.query(GradeCurricular).filter(
            GradeCurricular.ativa == True
        ).all()
        
        # Carregar professores
        professores_query = self.db.query(Professor).filter(Professor.ativo == True).all()
        self.professores = {p.id: p for p in professores_query}
        
        # Carregar turmas
        turmas_query = self.db.query(Turma).filter(Turma.ativa == True).all()
        self.turmas = {t.id: t for t in turmas_query}
        
        # Carregar ambientes
        self.ambientes = self.db.query(Ambiente).filter(Ambiente.ativo == True).all()
        
        # Carregar disponibilidades
        disps = self.db.query(Disponibilidade).all()
        for disp in disps:
            if disp.professor_id not in self.disponibilidades:
                self.disponibilidades[disp.professor_id] = []
            self.disponibilidades[disp.professor_id].append(disp)
    
    def criar_variaveis(self):
        """Cria as variáveis do modelo CP-SAT"""
        # Para cada grade curricular, precisamos alocar aulas
        for grade in self.grades:
            for aula_num in range(grade.aulas_por_semana):
                for dia_idx, dia in enumerate(self.dias_semana):
                    for slot in range(self.slots_por_dia):
                        for ambiente in self.ambientes:
                            # Variável booleana: aula está alocada neste dia/slot/ambiente?
                            var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                            self.variaveis[var_name] = self.model.NewBoolVar(var_name)
    
    def adicionar_restricoes(self):
        """Adiciona todas as restrições ao modelo"""
        
        # 1. Cada aula deve ser alocada exatamente uma vez
        for grade in self.grades:
            for aula_num in range(grade.aulas_por_semana):
                vars_aula = []
                for dia_idx in range(len(self.dias_semana)):
                    for slot in range(self.slots_por_dia):
                        for ambiente in self.ambientes:
                            var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                            if var_name in self.variaveis:
                                vars_aula.append(self.variaveis[var_name])
                
                # Exatamente uma alocação por aula
                if vars_aula:
                    self.model.Add(sum(vars_aula) == 1)
        
        # 2. Uma turma não pode ter mais de uma aula no mesmo horário
        for turma_id in self.turmas:
            for dia_idx in range(len(self.dias_semana)):
                for slot in range(self.slots_por_dia):
                    vars_conflito = []
                    for grade in self.grades:
                        if grade.turma_id == turma_id:
                            for aula_num in range(grade.aulas_por_semana):
                                for ambiente in self.ambientes:
                                    var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                                    if var_name in self.variaveis:
                                        vars_conflito.append(self.variaveis[var_name])
                    
                    # No máximo 1 aula por turma por slot
                    if vars_conflito:
                        self.model.Add(sum(vars_conflito) <= 1)
        
        # 3. Um professor não pode dar mais de uma aula no mesmo horário
        for prof_id in self.professores:
            for dia_idx in range(len(self.dias_semana)):
                for slot in range(self.slots_por_dia):
                    vars_conflito = []
                    for grade in self.grades:
                        if grade.professor_id == prof_id:
                            for aula_num in range(grade.aulas_por_semana):
                                for ambiente in self.ambientes:
                                    var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                                    if var_name in self.variaveis:
                                        vars_conflito.append(self.variaveis[var_name])
                    
                    if vars_conflito:
                        self.model.Add(sum(vars_conflito) <= 1)
        
        # 4. Um ambiente não pode ser usado por mais de uma turma ao mesmo tempo
        for ambiente in self.ambientes:
            for dia_idx in range(len(self.dias_semana)):
                for slot in range(self.slots_por_dia):
                    vars_conflito = []
                    for grade in self.grades:
                        for aula_num in range(grade.aulas_por_semana):
                            var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                            if var_name in self.variaveis:
                                vars_conflito.append(self.variaveis[var_name])
                    
                    if vars_conflito:
                        self.model.Add(sum(vars_conflito) <= 1)
        
        # 5. Respeitar disponibilidade dos professores
        self._adicionar_restricoes_disponibilidade()
        
        # 6. Limitar aulas seguidas por professor
        self._adicionar_restricoes_aulas_seguidas()
        
        # 7. Limitar aulas por dia
        self._adicionar_restricoes_aulas_por_dia()
    
    def _adicionar_restricoes_disponibilidade(self):
        """Respeita os horários de disponibilidade dos professores"""
        for prof_id, disponibilidades in self.disponibilidades.items():
            for disp in disponibilidades:
                if not disp.disponivel:  # Professor NÃO disponível
                    dia_idx = self.dias_semana.index(disp.dia_semana)
                    # Determinar quais slots correspondem a este horário
                    # Simplificado: marcar todos os slots do dia
                    for slot in range(self.slots_por_dia):
                        vars_bloqueio = []
                        for grade in self.grades:
                            if grade.professor_id == prof_id:
                                for aula_num in range(grade.aulas_por_semana):
                                    for ambiente in self.ambientes:
                                        var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                                        if var_name in self.variaveis:
                                            vars_bloqueio.append(self.variaveis[var_name])
                        
                        if vars_bloqueio:
                            self.model.Add(sum(vars_bloqueio) == 0)
    
    def _adicionar_restricoes_aulas_seguidas(self):
        """Limita o número de aulas seguidas por professor"""
        for prof_id, professor in self.professores.items():
            max_seguidas = professor.max_aulas_seguidas
            
            for dia_idx in range(len(self.dias_semana)):
                for slot_inicio in range(self.slots_por_dia - max_seguidas):
                    vars_janela = []
                    for slot in range(slot_inicio, slot_inicio + max_seguidas + 1):
                        for grade in self.grades:
                            if grade.professor_id == prof_id:
                                for aula_num in range(grade.aulas_por_semana):
                                    for ambiente in self.ambientes:
                                        var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                                        if var_name in self.variaveis:
                                            vars_janela.append(self.variaveis[var_name])
                    
                    if vars_janela:
                        self.model.Add(sum(vars_janela) <= max_seguidas)
    
    def _adicionar_restricoes_aulas_por_dia(self):
        """Limita o número total de aulas por dia para cada professor"""
        for prof_id, professor in self.professores.items():
            max_aulas = professor.max_aulas_dia
            
            for dia_idx in range(len(self.dias_semana)):
                vars_dia = []
                for slot in range(self.slots_por_dia):
                    for grade in self.grades:
                        if grade.professor_id == prof_id:
                            for aula_num in range(grade.aulas_por_semana):
                                for ambiente in self.ambientes:
                                    var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                                    if var_name in self.variaveis:
                                        vars_dia.append(self.variaveis[var_name])
                
                if vars_dia:
                    self.model.Add(sum(vars_dia) <= max_aulas)
    
    def adicionar_objetivos(self):
        """Define a função objetivo para otimização"""
        # Objetivo: minimizar janelas (horários vagos) dos professores
        penalidades = []
        
        for prof_id in self.professores:
            for dia_idx in range(len(self.dias_semana)):
                # Para cada sequência de 3 slots, penalizar se tiver aula no início e fim mas não no meio
                for slot in range(self.slots_por_dia - 2):
                    vars_inicio = []
                    vars_meio = []
                    vars_fim = []
                    
                    for grade in self.grades:
                        if grade.professor_id == prof_id:
                            for aula_num in range(grade.aulas_por_semana):
                                for ambiente in self.ambientes:
                                    var_inicio = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                                    var_meio = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot+1}_amb{ambiente.id}"
                                    var_fim = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot+2}_amb{ambiente.id}"
                                    
                                    if var_inicio in self.variaveis:
                                        vars_inicio.append(self.variaveis[var_inicio])
                                    if var_meio in self.variaveis:
                                        vars_meio.append(self.variaveis[var_meio])
                                    if var_fim in self.variaveis:
                                        vars_fim.append(self.variaveis[var_fim])
                    
                    # Criar variável de penalidade para janela
                    if vars_inicio and vars_meio and vars_fim:
                        janela_var = self.model.NewBoolVar(f"janela_p{prof_id}_d{dia_idx}_s{slot}")
                        # Janela = (início OR fim) AND NOT meio
                        # Simplificado: somar penalidades
                        penalidades.append(janela_var)
        
        # Minimizar penalidades
        if penalidades:
            self.model.Minimize(sum(penalidades))
    
    def resolver(self, tempo_maximo: int = 300):
        """Resolve o problema de otimização"""
        self.solver.parameters.max_time_in_seconds = tempo_maximo
        
        inicio = time.time()
        status = self.solver.Solve(self.model)
        tempo_decorrido = time.time() - inicio
        
        return status, tempo_decorrido
    
    def extrair_solucao(self):
        """Extrai a solução e salva no banco de dados"""
        # Limpar aulas existentes
        self.db.query(HorarioAula).filter(
            HorarioAula.horario_id == self.horario_id
        ).delete()
        
        aulas_criadas = 0
        
        # Extrair valores das variáveis
        for var_name, var in self.variaveis.items():
            if self.solver.Value(var) == 1:
                # Parse do nome da variável
                # Formato: g{grade_id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente_id}
                parts = var_name.split('_')
                grade_id = int(parts[0][1:])
                dia_idx = int(parts[2][1:])
                slot = int(parts[3][1:])
                ambiente_id = int(parts[4][3:])
                
                grade = next(g for g in self.grades if g.id == grade_id)
                
                # Calcular horário
                horario_inicio = self._calcular_horario(slot)
                horario_fim = self._calcular_horario(slot, fim=True)
                
                # Criar aula
                aula = HorarioAula(
                    horario_id=self.horario_id,
                    turma_id=grade.turma_id,
                    disciplina_id=grade.disciplina_id,
                    professor_id=grade.professor_id,
                    ambiente_id=ambiente_id,
                    dia_semana=self.dias_semana[dia_idx],
                    horario_inicio=horario_inicio,
                    horario_fim=horario_fim,
                    ordem=slot + 1
                )
                self.db.add(aula)
                aulas_criadas += 1
        
        # Atualizar estatísticas do horário
        total_aulas = sum(g.aulas_por_semana for g in self.grades)
        self.horario.total_aulas = total_aulas
        self.horario.aulas_alocadas = aulas_criadas
        self.horario.status = "FINALIZADO" if aulas_criadas == total_aulas else "EM_PROGRESSO"
        self.horario.qualidade_score = self._calcular_qualidade()
        
        self.db.commit()
        
        return aulas_criadas
    
    def _calcular_horario(self, slot: int, fim: bool = False) -> str:
        """Calcula o horário com base no slot"""
        # Horário base: 07:30
        hora_base = 7
        minuto_base = 30
        
        minutos_totais = hora_base * 60 + minuto_base + (slot * self.duracao_aula)
        
        if fim:
            minutos_totais += self.duracao_aula
        
        hora = minutos_totais // 60
        minuto = minutos_totais % 60
        
        return f"{hora:02d}:{minuto:02d}"
    
    def _calcular_qualidade(self) -> int:
        """Calcula um score de qualidade do horário gerado (0-100)"""
        # Simplificado: baseado na taxa de alocação
        if self.horario.total_aulas == 0:
            return 0
        
        taxa_alocacao = (self.horario.aulas_alocadas / self.horario.total_aulas) * 100
        return int(taxa_alocacao)
    
    def gerar(self, tempo_maximo: int = 300) -> Dict:
        """Método principais para gerar o horário"""
        try:
            # 1. Carregar dados
            self.carregar_dados()
            
            if not self.grades:
                return {
                    "success": False,
                    "message": "Nenhuma grade curricular encontrada",
                    "total_aulas": 0,
                    "aulas_alocadas": 0
                }
            
            # 2. Criar variáveis
            self.criar_variaveis()
            
            # 3. Adicionar restrições
            self.adicionar_restricoes()
            
            # 4. Adicionar objetivos
            self.adicionar_objetivos()
            
            # 5. Resolver
            status, tempo_decorrido = self.resolver(tempo_maximo)
            
            # 6. Verificar resultado
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                aulas_criadas = self.extrair_solucao()
                
                return {
                    "success": True,
                    "message": "Horário gerado com sucesso!",
                    "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
                    "total_aulas": self.horario.total_aulas,
                    "aulas_alocadas": aulas_criadas,
                    "qualidade_score": self.horario.qualidade_score,
                    "tempo_geracao": tempo_decorrido,
                    "pendencias": self.pendencias
                }
            else:
                return {
                    "success": False,
                    "message": "Não foi possível gerar um horário válido",
                    "status": "INFEASIBLE",
                    "tempo_geracao": tempo_decorrido,
                    "pendencias": ["Restrições muito restritivas ou dados incompatíveis"]
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao gerar horário: {str(e)}",
                "tempo_geracao": 0
            }
