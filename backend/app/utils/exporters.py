"""
Módulo para exportação de horários em diferentes formatos (HTML, CSV)
"""
from typing import List, Dict
from io import StringIO
import csv
from datetime import datetime


class HorarioExporter:
    """Classe para exportar horários em diferentes formatos"""
    
    def __init__(self, horario_data: Dict, aulas: List[Dict]):
        self.horario_data = horario_data
        self.aulas = aulas
        self.dias_semana = ["SEGUNDA", "TERCA", "QUARTA", "QUINTA", "SEXTA", "SABADO"]
    
    def to_html_turma(self, turma_id: int, turma_nome: str) -> str:
        """Exporta horário de uma turma para HTML"""
        aulas_turma = [a for a in self.aulas if a['turma_id'] == turma_id]
        
        # Organizar aulas por dia e horário
        grade = self._organizar_grade(aulas_turma)
        
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Horário - {turma_nome}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2c3e50;
            margin: 10px 0;
        }}
        .header p {{
            color: #7f8c8d;
            margin: 5px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: center;
            font-weight: bold;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
            vertical-align: top;
        }}
        .horario {{
            background-color: #ecf0f1;
            font-weight: bold;
            width: 100px;
        }}
        .aula {{
            background-color: #e8f5e9;
            min-height: 60px;
        }}
        .disciplina {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        .professor {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .ambiente {{
            color: #95a5a6;
            font-size: 0.85em;
            margin-top: 5px;
        }}
        .vazio {{
            background-color: #fafafa;
        }}
        @media print {{
            body {{
                margin: 0;
                background-color: white;
            }}
            table {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Horário de Aulas - {turma_nome}</h1>
        <p>{self.horario_data.get('nome', 'Horário')} - {self.horario_data.get('ano_letivo', '')}</p>
        <p>Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th class="horario">Horário</th>
"""
        
        # Cabeçalho com dias da semana
        for dia in self.dias_semana:
            html += f"                <th>{self._formatar_dia(dia)}</th>\n"
        
        html += """            </tr>
        </thead>
        <tbody>
"""
        
        # Linhas com horários
        for slot, horario in grade['slots'].items():
            html += f"""            <tr>
                <td class="horario">{horario}</td>
"""
            for dia in self.dias_semana:
                aula = grade['grade'].get(dia, {}).get(slot)
                if aula:
                    html += f"""                <td class="aula">
                    <div class="disciplina">{aula['disciplina_nome']}</div>
                    <div class="professor">{aula['professor_nome']}</div>
                    <div class="ambiente">{aula['ambiente_nome']}</div>
                </td>
"""
                else:
                    html += """                <td class="vazio">-</td>
"""
            html += """            </tr>
"""
        
        html += """        </tbody>
    </table>
</body>
</html>
"""
        return html
    
    def to_html_professor(self, professor_id: int, professor_nome: str) -> str:
        """Exporta horário de um professor para HTML"""
        aulas_prof = [a for a in self.aulas if a['professor_id'] == professor_id]
        
        # Organizar aulas por dia e horário
        grade = self._organizar_grade(aulas_prof)
        
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Horário - {professor_nome}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2c3e50;
            margin: 10px 0;
        }}
        .header p {{
            color: #7f8c8d;
            margin: 5px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #e74c3c;
            color: white;
            padding: 12px;
            text-align: center;
            font-weight: bold;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
            vertical-align: top;
        }}
        .horario {{
            background-color: #ecf0f1;
            font-weight: bold;
            width: 100px;
        }}
        .aula {{
            background-color: #ffeaa7;
            min-height: 60px;
        }}
        .disciplina {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        .turma {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .ambiente {{
            color: #95a5a6;
            font-size: 0.85em;
            margin-top: 5px;
        }}
        .vazio {{
            background-color: #fafafa;
        }}
        @media print {{
            body {{
                margin: 0;
                background-color: white;
            }}
            table {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Horário de Aulas - Prof. {professor_nome}</h1>
        <p>{self.horario_data.get('nome', 'Horário')} - {self.horario_data.get('ano_letivo', '')}</p>
        <p>Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th class="horario">Horário</th>
"""
        
        # Cabeçalho com dias da semana
        for dia in self.dias_semana:
            html += f"                <th>{self._formatar_dia(dia)}</th>\n"
        
        html += """            </tr>
        </thead>
        <tbody>
"""
        
        # Linhas com horários
        for slot, horario in grade['slots'].items():
            html += f"""            <tr>
                <td class="horario">{horario}</td>
"""
            for dia in self.dias_semana:
                aula = grade['grade'].get(dia, {}).get(slot)
                if aula:
                    html += f"""                <td class="aula">
                    <div class="disciplina">{aula['disciplina_nome']}</div>
                    <div class="turma">{aula['turma_nome']}</div>
                    <div class="ambiente">{aula['ambiente_nome']}</div>
                </td>
"""
                else:
                    html += """                <td class="vazio">-</td>
"""
            html += """            </tr>
"""
        
        html += """        </tbody>
    </table>
</body>
</html>
"""
        return html
    
    def to_csv_turma(self, turma_id: int) -> str:
        """Exporta horário de uma turma para CSV"""
        aulas_turma = [a for a in self.aulas if a['turma_id'] == turma_id]
        grade = self._organizar_grade(aulas_turma)
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho
        header = ['Horário'] + [self._formatar_dia(dia) for dia in self.dias_semana]
        writer.writerow(header)
        
        # Dados
        for slot, horario in grade['slots'].items():
            row = [horario]
            for dia in self.dias_semana:
                aula = grade['grade'].get(dia, {}).get(slot)
                if aula:
                    cell = f"{aula['disciplina_nome']} - {aula['professor_nome']} ({aula['ambiente_nome']})"
                    row.append(cell)
                else:
                    row.append('-')
            writer.writerow(row)
        
        return output.getvalue()
    
    def to_csv_professor(self, professor_id: int) -> str:
        """Exporta horário de um professor para CSV"""
        aulas_prof = [a for a in self.aulas if a['professor_id'] == professor_id]
        grade = self._organizar_grade(aulas_prof)
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho
        header = ['Horário'] + [self._formatar_dia(dia) for dia in self.dias_semana]
        writer.writerow(header)
        
        # Dados
        for slot, horario in grade['slots'].items():
            row = [horario]
            for dia in self.dias_semana:
                aula = grade['grade'].get(dia, {}).get(slot)
                if aula:
                    cell = f"{aula['disciplina_nome']} - {aula['turma_nome']} ({aula['ambiente_nome']})"
                    row.append(cell)
                else:
                    row.append('-')
            writer.writerow(row)
        
        return output.getvalue()
    
    def _organizar_grade(self, aulas: List[Dict]) -> Dict:
        """Organiza aulas em uma estrutura de grade por dia e horário"""
        grade = {}
        slots = {}
        
        for aula in aulas:
            dia = aula['dia_semana']
            horario = f"{aula['horario_inicio']} - {aula['horario_fim']}"
            ordem = aula['ordem']
            
            if dia not in grade:
                grade[dia] = {}
            
            grade[dia][ordem] = aula
            slots[ordem] = horario
        
        return {'grade': grade, 'slots': dict(sorted(slots.items()))}
    
    def _formatar_dia(self, dia: str) -> str:
        """Formata nome do dia da semana"""
        dias = {
            'SEGUNDA': 'Segunda-feira',
            'TERCA': 'Terça-feira',
            'QUARTA': 'Quarta-feira',
            'QUINTA': 'Quinta-feira',
            'SEXTA': 'Sexta-feira',
            'SABADO': 'Sábado'
        }
        return dias.get(dia, dia)
