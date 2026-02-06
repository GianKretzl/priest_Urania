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
        
        # 8. Respeitar horas-atividade
        self._adicionar_restricoes_horas_atividade()
        
        # 9. Considerar deslocamento entre sedes
        self._adicionar_restricoes_deslocamento()
    
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
    
    def _adicionar_restricoes_horas_atividade(self):
        """Garante que professores tenham tempo para horas-atividade"""
        for prof_id, professor in self.professores.items():
            if professor.horas_atividade > 0:
                # Calcular total de aulas do professor na semana
                vars_total = []
                for dia_idx in range(len(self.dias_semana)):
                    for slot in range(self.slots_por_dia):
                        for grade in self.grades:
                            if grade.professor_id == prof_id:
                                for aula_num in range(grade.aulas_por_semana):
                                    for ambiente in self.ambientes:
                                        var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                                        if var_name in self.variaveis:
                                            vars_total.append(self.variaveis[var_name])
                
                if vars_total:
                    # Converter duração de aula (minutos) para horas
                    duracao_aula_horas = self.duracao_aula / 60
                    
                    # Carga horária máxima - horas atividade = horas disponíveis para aulas
                    horas_disponiveis_aulas = professor.carga_horaria_maxima - professor.horas_atividade
                    max_aulas_semana = int(horas_disponiveis_aulas / duracao_aula_horas)
                    
                    # Garantir que o total de aulas não ultrapasse o limite
                    self.model.Add(sum(vars_total) <= max_aulas_semana)
    
    def _adicionar_restricoes_deslocamento(self):
        """Considera tempo de deslocamento entre sedes diferentes"""
        # Mapear ambientes por sede
        ambientes_por_sede = {}
        for ambiente in self.ambientes:
            if ambiente.sede_id not in ambientes_por_sede:
                ambientes_por_sede[ambiente.sede_id] = []
            ambientes_por_sede[ambiente.sede_id].append(ambiente)
        
        # Se houver apenas uma sede, não há necessidade de deslocamento
        if len(ambientes_por_sede) <= 1:
            return
        
        for prof_id, professor in self.professores.items():
            if professor.tempo_deslocamento == 0:
                continue
            
            # Calcular quantos slots são necessários para deslocamento
            slots_deslocamento = (professor.tempo_deslocamento + self.duracao_aula - 1) // self.duracao_aula
            
            if slots_deslocamento == 0:
                slots_deslocamento = 1  # No mínimo 1 slot de intervalo
            
            # Para cada dia, verificar aulas consecutivas em sedes diferentes
            for dia_idx in range(len(self.dias_semana)):
                for slot in range(self.slots_por_dia - slots_deslocamento):
                    # Para cada par de sedes diferentes
                    for sede1_id, ambientes_sede1 in ambientes_por_sede.items():
                        for sede2_id, ambientes_sede2 in ambientes_por_sede.items():
                            if sede1_id >= sede2_id:
                                continue  # Evitar duplicação
                            
                            # Variáveis para aulas na sede 1 no slot atual
                            vars_sede1_slot = []
                            for ambiente in ambientes_sede1:
                                for grade in self.grades:
                                    if grade.professor_id == prof_id:
                                        for aula_num in range(grade.aulas_por_semana):
                                            var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot}_amb{ambiente.id}"
                                            if var_name in self.variaveis:
                                                vars_sede1_slot.append(self.variaveis[var_name])
                            
                            # Variáveis para aulas na sede 2 nos próximos slots (dentro do tempo de deslocamento)
                            for slot_offset in range(1, slots_deslocamento + 1):
                                slot_futuro = slot + slot_offset
                                if slot_futuro >= self.slots_por_dia:
                                    break
                                
                                vars_sede2_slot = []
                                for ambiente in ambientes_sede2:
                                    for grade in self.grades:
                                        if grade.professor_id == prof_id:
                                            for aula_num in range(grade.aulas_por_semana):
                                                var_name = f"g{grade.id}_a{aula_num}_d{dia_idx}_s{slot_futuro}_amb{ambiente.id}"
                                                if var_name in self.variaveis:
                                                    vars_sede2_slot.append(self.variaveis[var_name])
                                
                                # Se há aula na sede 1 no slot atual, não pode haver na sede 2 no slot futuro próximo
                                if vars_sede1_slot and vars_sede2_slot:
                                    for var1 in vars_sede1_slot:
                                        for var2 in vars_sede2_slot:
                                            # Se var1 = 1, então var2 = 0 (não ambas podem ser 1)
                                            self.model.Add(var1 + var2 <= 1)
    
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
    
    def _detectar_pendencias(self):
        """Detecta pendências e gera sugestões de resolução"""
        self.pendencias = []
        
        # Verificar aulas não alocadas
        total_aulas = sum(g.aulas_por_semana for g in self.grades)
        if self.horario.aulas_alocadas < total_aulas:
            aulas_faltantes = total_aulas - self.horario.aulas_alocadas
            
            # Analisar possíveis causas
            self._analisar_disponibilidade_professores()
            self._analisar_capacidade_ambientes()
            self._analisar_conflitos_deslocamento()
            
            self.pendencias.insert(0, {
                "tipo": "AULAS_NAO_ALOCADAS",
                "severidade": "ALTA",
                "mensagem": f"{aulas_faltantes} aula(s) não foram alocadas",
                "detalhes": f"Taxa de alocação: {(self.horario.aulas_alocadas/total_aulas)*100:.1f}%"
            })
    
    def _analisar_disponibilidade_professores(self):
        """Analisa se falta de disponibilidade está causando problemas"""
        for prof_id, professor in self.professores.items():
            # Contar grades do professor
            grades_prof = [g for g in self.grades if g.professor_id == prof_id]
            if not grades_prof:
                continue
            
            total_aulas_prof = sum(g.aulas_por_semana for g in grades_prof)
            
            # Contar horários disponíveis
            if prof_id in self.disponibilidades:
                slots_bloqueados = 0
                for disp in self.disponibilidades[prof_id]:
                    if not disp.disponivel:
                        slots_bloqueados += self.slots_por_dia  # Simplificado
                
                slots_disponiveis = len(self.dias_semana) * self.slots_por_dia - slots_bloqueados
                
                if total_aulas_prof > slots_disponiveis * 0.8:
                    self.pendencias.append({
                        "tipo": "DISPONIBILIDADE_INSUFICIENTE",
                        "severidade": "MEDIA",
                        "mensagem": f"Professor {professor.nome} tem poucos horários disponíveis",
                        "sugestao": f"Considere liberar alguns horários bloqueados ou reduzir a carga horária",
                        "professor_id": prof_id
                    })
    
    def _analisar_capacidade_ambientes(self):
        """Analisa se falta de ambientes está causando problemas"""
        total_aulas = sum(g.aulas_por_semana for g in self.grades)
        capacidade_total = len(self.ambientes) * len(self.dias_semana) * self.slots_por_dia
        
        taxa_ocupacao = (total_aulas / capacidade_total) * 100
        
        if taxa_ocupacao > 80:
            self.pendencias.append({
                "tipo": "CAPACIDADE_AMBIENTES",
                "severidade": "MEDIA",
                "mensagem": f"Taxa de ocupação de ambientes muito alta ({taxa_ocupacao:.1f}%)",
                "sugestao": "Considere adicionar mais salas de aula ou distribuir turmas em outros turnos"
            })
    
    def _analisar_conflitos_deslocamento(self):
        """Analisa se restrições de deslocamento estão causando problemas"""
        # Verificar se há múltiplas sedes
        sedes_usadas = set(amb.sede_id for amb in self.ambientes)
        
        if len(sedes_usadas) > 1:
            # Verificar professores com tempo de deslocamento alto
            for prof_id, professor in self.professores.items():
                if professor.tempo_deslocamento > 45:  # Mais de 45 minutos
                    grades_prof = [g for g in self.grades if g.professor_id == prof_id]
                    if len(grades_prof) > 0:
                        self.pendencias.append({
                            "tipo": "DESLOCAMENTO_PROBLEMATICO",
                            "severidade": "BAIXA",
                            "mensagem": f"Professor {professor.nome} tem tempo de deslocamento alto ({professor.tempo_deslocamento}min)",
                            "sugestao": "Considere alocar aulas do professor em apenas uma sede ou reduzir o tempo de deslocamento",
                            "professor_id": prof_id
                        })
    
    def _calcular_qualidade(self) -> int:
        """Calcula um score de qualidade do horário gerado (0-100)"""
        if self.horario.total_aulas == 0:
            return 0
        
        score = 0
        
        # 1. Taxa de alocação (40 pontos)
        taxa_alocacao = (self.horario.aulas_alocadas / self.horario.total_aulas)
        score += int(taxa_alocacao * 40)
        
        # 2. Distribuição de aulas (30 pontos)
        score += self._avaliar_distribuicao()
        
        # 3. Janelas minimizadas (20 pontos)
        score += self._avaliar_janelas()
        
        # 4. Respeito às preferências (10 pontos)
        score += self._avaliar_preferencias()
        
        return min(100, score)
    
    def _avaliar_distribuicao(self) -> int:
        """Avalia a distribuição uniforme de aulas na semana"""
        aulas_por_dia = {dia: 0 for dia in range(len(self.dias_semana))}
        
        for var_name, var in self.variaveis.items():
            if self.solver.Value(var) == 1:
                parts = var_name.split('_')
                dia_idx = int(parts[2][1:])
                aulas_por_dia[dia_idx] += 1
        
        if not aulas_por_dia:
            return 0
        
        # Calcular desvio padrão
        media = sum(aulas_por_dia.values()) / len(aulas_por_dia)
        variancia = sum((v - media) ** 2 for v in aulas_por_dia.values()) / len(aulas_por_dia)
        desvio = variancia ** 0.5
        
        # Quanto menor o desvio, melhor (mais uniforme)
        score = max(0, 30 - int(desvio * 5))
        return score
    
    def _avaliar_janelas(self) -> int:
        """Avalia a quantidade de janelas (horários vagos) dos professores"""
        total_janelas = 0
        
        for prof_id in self.professores:
            for dia_idx in range(len(self.dias_semana)):
                aulas_dia = []
                for slot in range(self.slots_por_dia):
                    tem_aula = False
                    for var_name, var in self.variaveis.items():
                        if f"_d{dia_idx}_s{slot}_" in var_name and self.solver.Value(var) == 1:
                            parts = var_name.split('_')
                            grade_id = int(parts[0][1:])
                            grade = next((g for g in self.grades if g.id == grade_id), None)
                            if grade and grade.professor_id == prof_id:
                                tem_aula = True
                                break
                    aulas_dia.append(tem_aula)
                
                # Contar janelas: False entre dois True
                for i in range(1, len(aulas_dia) - 1):
                    if not aulas_dia[i] and (aulas_dia[i-1] or aulas_dia[i+1]):
                        if aulas_dia[i-1] and aulas_dia[i+1]:
                            total_janelas += 1
        
        # Quanto menos janelas, melhor
        max_janelas_esperadas = len(self.professores) * len(self.dias_semana) * 2
        score = max(0, 20 - int((total_janelas / max(1, max_janelas_esperadas)) * 20))
        return score
    
    def _avaliar_preferencias(self) -> int:
        """Avalia o respeito às preferências (placeholder para futura implementação)"""
        # Por enquanto, retorna 10 pontos fixos
        # Futuramente pode considerar preferências de horário dos professores
        return 10
    
    def refinar_solucao(self):
        """Fase de refinamento para melhorar a qualidade pedagógica do horário"""
        if self.horario.aulas_alocadas == 0:
            return
        
        # Tentar redistribuir aulas para melhorar qualidade
        # Esta é uma versão simplificada - pode ser expandida
        
        # 1. Identificar dias com muita sobrecarga
        # 2. Tentar mover aulas para balancear
        # 3. Recalcular score de qualidade
        
        pass  # Implementação futura mais sofisticada
    
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
                
                # 7. Detectar pendências e gerar sugestões
                self._detectar_pendencias()
                
                # 8. Fase de refinamento
                if status == cp_model.OPTIMAL:
                    self.refinar_solucao()
                
                # Salvar pendências no banco
                self.horario.pendencias = self.pendencias
                self.db.commit()
                
                mensagem = "Horário gerado com sucesso!"
                if self.pendencias:
                    mensagem += f" ({len(self.pendencias)} pendência(s) detectada(s))"
                
                return {
                    "success": True,
                    "message": mensagem,
                    "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
                    "total_aulas": self.horario.total_aulas,
                    "aulas_alocadas": aulas_criadas,
                    "qualidade_score": self.horario.qualidade_score,
                    "tempo_geracao": tempo_decorrido,
                    "pendencias": self.pendencias
                }
            else:
                # Gerar pendências detalhadas quando não há solução
                self._detectar_pendencias()
                
                if not self.pendencias:
                    self.pendencias.append({
                        "tipo": "INFEASIBLE",
                        "severidade": "ALTA",
                        "mensagem": "Restrições muito restritivas ou dados incompatíveis",
                        "sugestao": "Revise as restrições de disponibilidade, carga horária e deslocamento dos professores"
                    })
                
                return {
                    "success": False,
                    "message": "Não foi possível gerar um horário válido",
                    "status": "INFEASIBLE",
                    "tempo_geracao": tempo_decorrido,
                    "pendencias": self.pendencias
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao gerar horário: {str(e)}",
                "tempo_geracao": 0
            }
