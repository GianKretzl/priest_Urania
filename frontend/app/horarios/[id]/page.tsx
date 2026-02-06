'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { horarioService, turmaService, professorService, disciplinaService, HorarioAula, Horario, Turma, Professor, Disciplina } from '@/lib/api';
import { FaDownload, FaCalendarAlt, FaChalkboardTeacher } from 'react-icons/fa';

export default function HorarioDetalhesPage() {
  const params = useParams();
  const horarioId = Number(params.id);

  const [horario, setHorario] = useState<Horario | null>(null);
  const [aulas, setAulas] = useState<HorarioAula[]>([]);
  const [turmas, setTurmas] = useState<Turma[]>([]);
  const [professores, setProfessores] = useState<Professor[]>([]);
  const [disciplinas, setDisciplinas] = useState<Disciplina[]>([]);
  const [visualizacao, setVisualizacao] = useState<'turma' | 'professor'>('turma');
  const [selecionado, setSelecionado] = useState<number | null>(null);

  const diasSemana = ['SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA'];
  const horarios = ['07:30', '08:20', '09:10', '10:00', '10:50', '11:40'];

  useEffect(() => {
    carregarDados();
  }, [horarioId]);

  const carregarDados = async () => {
    try {
      const [horarioResp, aulasResp, turmasResp, professoresResp, disciplinasResp] = await Promise.all([
        horarioService.getById(horarioId),
        horarioService.getAulas(horarioId),
        turmaService.getAll(),
        professorService.getAll(),
        disciplinaService.getAll(),
      ]);

      setHorario(horarioResp.data);
      setAulas(aulasResp.data);
      setTurmas(turmasResp.data);
      setProfessores(professoresResp.data);
      setDisciplinas(disciplinasResp.data);

      if (turmasResp.data.length > 0) {
        setSelecionado(turmasResp.data[0].id);
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      alert('Erro ao carregar dados do horário');
    }
  };

  const getAula = (dia: string, ordem: number): HorarioAula | undefined => {
    if (!selecionado) return undefined;

    return aulas.find((aula) => {
      if (visualizacao === 'turma') {
        return aula.dia_semana === dia && aula.ordem === ordem + 1 && aula.turma_id === selecionado;
      } else {
        return aula.dia_semana === dia && aula.ordem === ordem + 1 && aula.professor_id === selecionado;
      }
    });
  };

  const getDisciplinaNome = (disciplinaId: number): string => {
    const disciplina = disciplinas.find(d => d.id === disciplinaId);
    return disciplina?.nome || 'N/A';
  };

  const getProfessorNome = (professorId: number): string => {
    const professor = professores.find(p => p.id === professorId);
    return professor?.nome || 'N/A';
  };

  const getTurmaNome = (turmaId: number): string => {
    const turma = turmas.find(t => t.id === turmaId);
    return turma?.nome || 'N/A';
  };

  const getDisciplinaCor = (disciplinaId: number): string => {
    const disciplina = disciplinas.find(d => d.id === disciplinaId);
    return disciplina?.cor || '#3B82F6';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">{horario?.nome}</h1>
            <p className="text-gray-600">
              Ano Letivo: {horario?.ano_letivo} - {horario?.semestre}º Semestre
            </p>
          </div>
          <button className="flex items-center space-x-2 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition">
            <FaDownload />
            <span>Exportar PDF</span>
          </button>
        </div>

        {/* Estatísticas */}
        <div className="grid grid-cols-3 gap-4 mt-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Total de Aulas</p>
            <p className="text-2xl font-bold text-blue-600">{horario?.total_aulas}</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Aulas Alocadas</p>
            <p className="text-2xl font-bold text-green-600">{horario?.aulas_alocadas}</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Qualidade</p>
            <p className="text-2xl font-bold text-purple-600">{horario?.qualidade_score}%</p>
          </div>
        </div>
      </div>

      {/* Controles de Visualização */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex space-x-4 items-center">
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setVisualizacao('turma');
                if (turmas.length > 0) setSelecionado(turmas[0].id);
              }}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition ${
                visualizacao === 'turma'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              <FaCalendarAlt />
              <span>Por Turma</span>
            </button>
            <button
              onClick={() => {
                setVisualizacao('professor');
                if (professores.length > 0) setSelecionado(professores[0].id);
              }}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition ${
                visualizacao === 'professor'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              <FaChalkboardTeacher />
              <span>Por Professor</span>
            </button>
          </div>

          <select
            value={selecionado || ''}
            onChange={(e) => setSelecionado(Number(e.target.value))}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {visualizacao === 'turma'
              ? turmas.map((turma) => (
                  <option key={turma.id} value={turma.id}>
                    {turma.nome} - {turma.ano_serie}
                  </option>
                ))
              : professores.map((professor) => (
                  <option key={professor.id} value={professor.id}>
                    {professor.nome}
                  </option>
                ))}
          </select>
        </div>
      </div>

      {/* Grade de Horários */}
      <div className="bg-white rounded-lg shadow-md p-6 overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-4 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Horário
              </th>
              {diasSemana.map((dia) => (
                <th key={dia} className="px-4 py-3 bg-gray-50 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {dia}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {horarios.map((horario, idx) => (
              <tr key={idx}>
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                  {horario}
                </td>
                {diasSemana.map((dia) => {
                  const aula = getAula(dia, idx);
                  return (
                    <td key={dia} className="px-4 py-3 text-center">
                      {aula ? (
                        <div 
                          className="border rounded p-2 text-xs shadow-sm"
                          style={{ 
                            backgroundColor: `${getDisciplinaCor(aula.disciplina_id)}20`,
                            borderColor: getDisciplinaCor(aula.disciplina_id)
                          }}
                        >
                          <p className="font-semibold text-gray-900">
                            {getDisciplinaNome(aula.disciplina_id)}
                          </p>
                          <p className="text-gray-700 mt-1">
                            {visualizacao === 'turma' 
                              ? getProfessorNome(aula.professor_id)
                              : getTurmaNome(aula.turma_id)
                            }
                          </p>
                          <p className="text-gray-500 text-xs mt-1">
                            {aula.horario_inicio} - {aula.horario_fim}
                          </p>
                        </div>
                      ) : (
                        <div className="text-gray-400 text-xs">-</div>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
