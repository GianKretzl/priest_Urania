'use client';

import { useState, useEffect } from 'react';
import axios from '@/lib/api';

interface Professor {
  id: number;
  nome: string;
  horas_atividade: number;
  horas_regencia: number;
  carga_horaria_total: number;
}

interface Disponibilidade {
  id: number;
  professor_id: number;
  dia_semana: string;
  turno: string | null;
  horario_inicio: string;
  horario_fim: string;
  disponivel: boolean;
  dia_nao_trabalha: boolean;
}

const DIAS_SEMANA = ['SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO'];
const DIAS_LABEL = {
  SEGUNDA: 'Segunda',
  TERCA: 'Terça',
  QUARTA: 'Quarta',
  QUINTA: 'Quinta',
  SEXTA: 'Sexta',
  SABADO: 'Sábado'
};

const TURNOS = {
  MATUTINO: { 
    label: 'Manhã', 
    horarios: ['07:00', '07:50', '08:45', '09:45', '10:35', '11:25'],
    intervalo: '09:30 às 09:45'
  },
  VESPERTINO: { 
    label: 'Tarde', 
    horarios: ['13:00', '13:50', '14:40', '15:45', '16:35', '17:25'],
    intervalo: '15:30 às 15:45'
  },
  NOTURNO: { 
    label: 'Noite', 
    horarios: ['18:00', '18:55', '19:50', '20:45', '21:40'],
    intervalo: null
  }
};

export default function DisponibilidadesPage() {
  const [professores, setProfessores] = useState<Professor[]>([]);
  const [professorSelecionado, setProfessorSelecionado] = useState<number | null>(null);
  const [professor, setProfessor] = useState<Professor | null>(null);
  const [disponibilidades, setDisponibilidades] = useState<Disponibilidade[]>([]);
  const [diasTurnosNaoTrabalha, setDiasTurnosNaoTrabalha] = useState<Set<string>>(new Set()); // Formato: "DIA_TURNO"
  const [turnoSelecionado, setTurnoSelecionado] = useState<string>('MATUTINO');
  const [loading, setLoading] = useState(true);
  const [salvando, setSalvando] = useState(false);

  useEffect(() => {
    carregarProfessores();
  }, []);

  useEffect(() => {
    if (professorSelecionado) {
      carregarDisponibilidades();
      carregarProfessorDetalhes();
    }
  }, [professorSelecionado]);

  const carregarProfessores = async () => {
    try {
      const response = await axios.get('/professores');
      const professoresOrdenados = response.data.sort((a: Professor, b: Professor) => 
        a.nome.localeCompare(b.nome)
      );
      setProfessores(professoresOrdenados);
      if (professoresOrdenados.length > 0) {
        setProfessorSelecionado(professoresOrdenados[0].id);
      }
    } catch (error) {
      console.error('Erro ao carregar professores:', error);
      alert('Erro ao carregar professores');
    }
  };

  const carregarProfessorDetalhes = async () => {
    if (!professorSelecionado) return;
    
    try {
      const response = await axios.get(`/professores/${professorSelecionado}`);
      setProfessor(response.data);
    } catch (error) {
      console.error('Erro ao carregar detalhes do professor:', error);
    }
  };

  const carregarDisponibilidades = async () => {
    if (!professorSelecionado) return;
    
    try {
      setLoading(true);
      const response = await axios.get(`/disponibilidades/professor/${professorSelecionado}`);
      setDisponibilidades(response.data);
      
      // Identificar dias/turnos que não trabalha
      const diasTurnosNT = new Set<string>();
      response.data.forEach((d: Disponibilidade) => {
        if (d.dia_nao_trabalha && d.turno) {
          diasTurnosNT.add(`${d.dia_semana}_${d.turno}`);
        }
      });
      setDiasTurnosNaoTrabalha(diasTurnosNT);
    } catch (error) {
      console.error('Erro ao carregar disponibilidades:', error);
      setDisponibilidades([]);
      setDiasTurnosNaoTrabalha(new Set());
    } finally {
      setLoading(false);
    }
  };

  const toggleDiaTurnoNaoTrabalha = async (dia: string, turno: string) => {
    if (!professorSelecionado) return;

    const key = `${dia}_${turno}`;
    setSalvando(true);
    try {
      if (diasTurnosNaoTrabalha.has(key)) {
        // Desmarcar turno como não trabalhado
        await axios.delete(`/disponibilidades/desmarcar-dia-nao-trabalha/${professorSelecionado}/${dia}/${turno}`);
      } else {
        // Marcar turno como não trabalhado
        await axios.post(`/disponibilidades/marcar-dia-nao-trabalha/${professorSelecionado}/${dia}/${turno}`);
      }
      await carregarDisponibilidades();
    } catch (error) {
      console.error('Erro ao alterar turno não trabalhado:', error);
      alert('Erro ao alterar disponibilidade do turno');
    } finally {
      setSalvando(false);
    }
  };

  const toggleDisponibilidade = async (dia: string, horario: string) => {
    const key = `${dia}_${turnoSelecionado}`;
    if (!professorSelecionado || diasTurnosNaoTrabalha.has(key)) return;

    const existente = disponibilidades.find(
      d => d.dia_semana === dia && d.horario_inicio === horario && !d.dia_nao_trabalha
    );

    setSalvando(true);
    try {
      if (existente) {
        await axios.put(`/disponibilidades/${existente.id}`, {
          ...existente,
          disponivel: !existente.disponivel
        });
      } else {
        await axios.post('/disponibilidades', {
          professor_id: professorSelecionado,
          dia_semana: dia,
          turno: turnoSelecionado,
          horario_inicio: horario,
          horario_fim: calcularHorarioFim(horario),
          disponivel: false,
          dia_nao_trabalha: false
        });
      }
      await carregarDisponibilidades();
    } catch (error) {
      console.error('Erro ao salvar disponibilidade:', error);
      alert('Erro ao salvar disponibilidade');
    } finally {
      setSalvando(false);
    }
  };

  const calcularHorarioFim = (inicio: string): string => {
    const todosHorarios = Object.values(TURNOS).flatMap(t => t.horarios);
    const idx = todosHorarios.indexOf(inicio);
    if (idx >= 0 && idx < todosHorarios.length - 1) {
      return todosHorarios[idx + 1];
    }
    const [h, m] = inicio.split(':').map(Number);
    const novoMinuto = m + 50;
    const novaHora = h + Math.floor(novoMinuto / 60);
    return `${String(novaHora).padStart(2, '0')}:${String(novoMinuto % 60).padStart(2, '0')}`;
  };

  const isIndisponivel = (dia: string, horario: string): boolean => {
    const key = `${dia}_${turnoSelecionado}`;
    if (diasTurnosNaoTrabalha.has(key)) return true;
    const disp = disponibilidades.find(
      d => d.dia_semana === dia && d.horario_inicio === horario && 
           d.turno === turnoSelecionado && !d.dia_nao_trabalha
    );
    return disp ? !disp.disponivel : false;
  };

  const limparDisponibilidadesTurno = async () => {
    if (!professorSelecionado || !confirm(`Deseja remover todas as indisponibilidades do turno ${TURNOS[turnoSelecionado as keyof typeof TURNOS].label}?`)) {
      return;
    }

    setSalvando(true);
    try {
      const dispTurno = disponibilidades.filter(d => 
        d.turno === turnoSelecionado && !d.dia_nao_trabalha && d.disponivel === false
      );
      for (const disp of dispTurno) {
        await axios.delete(`/disponibilidades/${disp.id}`);
      }
      await carregarDisponibilidades();
      alert('Indisponibilidades do turno removidas!');
    } catch (error) {
      console.error('Erro ao limpar disponibilidades:', error);
      alert('Erro ao limpar disponibilidades');
    } finally {
      setSalvando(false);
    }
  };

  const calcularHorasDisponiveis = () => {
    if (!professor) return 0;
    // As horas disponíveis para aulas são as horas de regência
    return professor.horas_regencia;
  };

  const calcularHorasPorTurno = (turno: string) => {
    const horariosTurno = TURNOS[turno as keyof typeof TURNOS].horarios;
    let horasDisponiveis = 0;
    
    DIAS_SEMANA.forEach(dia => {
      const key = `${dia}_${turno}`;
      if (!diasTurnosNaoTrabalha.has(key)) {
        horariosTurno.forEach(horario => {
          const indisponivel = disponibilidades.some(
            d => d.dia_semana === dia && d.horario_inicio === horario && 
                 d.turno === turno && d.disponivel === false && !d.dia_nao_trabalha
          );
          if (!indisponivel) {
            horasDisponiveis += 0.833; // ~50min = 0.833h
          }
        });
      }
    });
    
    return horasDisponiveis.toFixed(1);
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          Disponibilidades dos Professores
        </h1>
        <p className="text-gray-600">
          Gerencie os horários e dias que os professores estão indisponíveis
        </p>
      </div>

      {/* Seleção de Professor */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Professor:
            </label>
            <select
              value={professorSelecionado || ''}
              onChange={(e) => setProfessorSelecionado(Number(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              disabled={salvando}
            >
              {professores.map(prof => (
                <option key={prof.id} value={prof.id}>
                  {prof.nome}
                </option>
              ))}
            </select>
          </div>

          {professor && (
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Informações do Professor</h3>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Carga Horária Total:</span>
                  <span className="font-semibold text-blue-700">{professor.carga_horaria_total}h/semana</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Horas de Regência:</span>
                  <span className="font-semibold text-green-600">{professor.horas_regencia}h/semana</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Horas Atividade:</span>
                  <span className="font-semibold text-orange-600">{professor.horas_atividade}h/semana</span>
                </div>
                <div className="text-xs text-gray-500 mt-2 pt-2 border-t">
                  💡 Regra 15/5: 3h regência → 1h atividade
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Seleção de Turno */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700">Turno:</label>
            <div className="flex gap-2">
              {Object.entries(TURNOS).map(([key, value]) => (
                <button
                  key={key}
                  onClick={() => setTurnoSelecionado(key)}
                  className={`px-6 py-2 rounded-lg font-medium transition-all ${
                    turnoSelecionado === key
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {value.label}
                </button>
              ))}
            </div>
          </div>
          <button
            onClick={limparDisponibilidadesTurno}
            disabled={salvando}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Limpar Turno
          </button>
        </div>

        {/* Estatísticas por turno */}
        <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t">
          {Object.entries(TURNOS).map(([key, value]) => (
            <div key={key} className="bg-gray-50 p-3 rounded-lg">
              <div className="text-xs text-gray-600">{value.label}</div>
              <div className="text-lg font-bold text-blue-600">{calcularHorasPorTurno(key)}h</div>
              <div className="text-xs text-gray-500">disponíveis</div>
            </div>
          ))}
        </div>
      </div>

      {/* Grade de Horários */}
      {loading ? (
        <div className="text-center py-12">
          <div className="text-gray-500">Carregando disponibilidades...</div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-4 bg-gray-50 border-b">
            <h3 className="font-semibold text-gray-800">
              Horários do Turno: {TURNOS[turnoSelecionado as keyof typeof TURNOS].label}
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              Clique nos horários para marcar como indisponível (vermelho) ou disponível (verde)
            </p>
            {TURNOS[turnoSelecionado as keyof typeof TURNOS].intervalo && (
              <p className="text-xs text-orange-600 mt-1 font-medium">
                ⏰ Intervalo: {TURNOS[turnoSelecionado as keyof typeof TURNOS].intervalo}
              </p>
            )}
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-r">
                    Horário
                  </th>
                  {DIAS_SEMANA.map(dia => (
                    <th key={dia} className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-r">
                      {DIAS_LABEL[dia as keyof typeof DIAS_LABEL]}
                    </th>
                  ))}
                </tr>
                {/* Linha de controle de dias não trabalha */}
                <tr className="bg-gray-100 border-b-2">
                  <td className="px-4 py-2 text-xs font-semibold text-gray-700 border-r">
                    Não trabalha neste turno:
                  </td>
                  {DIAS_SEMANA.map(dia => {
                    const key = `${dia}_${turnoSelecionado}`;
                    const naoTrabalha = diasTurnosNaoTrabalha.has(key);
                    return (
                      <td key={dia} className="px-2 py-2 text-center border-r">
                        <button
                          onClick={() => toggleDiaTurnoNaoTrabalha(dia, turnoSelecionado)}
                          disabled={salvando}
                          className={`w-full px-2 py-1 rounded text-xs font-medium transition-all ${
                            naoTrabalha
                              ? 'bg-red-500 text-white hover:bg-red-600'
                              : 'bg-white text-gray-600 hover:bg-gray-200 border border-gray-300'
                          } disabled:opacity-50 disabled:cursor-not-allowed`}
                          title={naoTrabalha ? 'Clique para desmarcar' : 'Clique para marcar como não trabalhado'}
                        >
                          {naoTrabalha ? '✕ Não' : 'Sim'}
                        </button>
                      </td>
                    );
                  })}
                </tr>
              </thead>
              <tbody>
                {TURNOS[turnoSelecionado as keyof typeof TURNOS].horarios.map((horario, idx) => (
                  <tr key={horario} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-4 py-2 text-sm font-medium text-gray-700 border-b border-r whitespace-nowrap">
                      {horario}
                    </td>
                    {DIAS_SEMANA.map(dia => {
                      const key = `${dia}_${turnoSelecionado}`;
                      const indisponivel = isIndisponivel(dia, horario);
                      const diaNaoTrabalha = diasTurnosNaoTrabalha.has(key);
                      
                      return (
                        <td key={`${dia}-${horario}`} className="border-b border-r p-0">
                          <button
                            onClick={() => !diaNaoTrabalha && toggleDisponibilidade(dia, horario)}
                            disabled={salvando || diaNaoTrabalha}
                            className={`w-full h-14 transition-colors ${
                              diaNaoTrabalha
                                ? 'bg-gray-300 cursor-not-allowed'
                                : indisponivel
                                ? 'bg-red-100 hover:bg-red-200'
                                : 'bg-green-50 hover:bg-green-100'
                            } disabled:opacity-50`}
                            title={
                              diaNaoTrabalha 
                                ? 'Professor não trabalha neste turno'
                                : indisponivel 
                                ? 'Indisponível (clique para marcar como disponível)' 
                                : 'Disponível (clique para marcar como indisponível)'
                            }
                          >
                            {indisponivel && !diaNaoTrabalha && (
                              <span className="text-red-600 font-bold text-xl">✕</span>
                            )}
                            {diaNaoTrabalha && (
                              <span className="text-gray-500 text-xs">---</span>
                            )}
                          </button>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Legenda */}
      <div className="mt-4 p-4 bg-blue-50 rounded-lg">
        <div className="text-sm text-gray-700">
          <strong>Legenda:</strong>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-2">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-green-50 border border-gray-300 rounded"></div>
              <span>Disponível</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-red-100 border border-gray-300 rounded flex items-center justify-center">
                <span className="text-red-600 font-bold">✕</span>
              </div>
              <span>Indisponível</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gray-300 border border-gray-300 rounded flex items-center justify-center">
                <span className="text-gray-500 text-xs">---</span>
              </div>
              <span>Não trabalha</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
