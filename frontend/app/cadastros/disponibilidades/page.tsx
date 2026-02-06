'use client';

import { useState, useEffect } from 'react';
import axios from '@/lib/api';

interface Professor {
  id: number;
  nome: string;
}

interface Disponibilidade {
  id: number;
  professor_id: number;
  dia_semana: string;
  horario_inicio: string;
  horario_fim: string;
  disponivel: boolean;
}

const DIAS_SEMANA = ['SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO'];
const DIAS_LABEL = {
  SEGUNDA: 'Segunda-feira',
  TERCA: 'Terça-feira',
  QUARTA: 'Quarta-feira',
  QUINTA: 'Quinta-feira',
  SEXTA: 'Sexta-feira',
  SABADO: 'Sábado'
};

const HORARIOS = [
  '07:00', '07:55', '08:50', '09:45', '10:40', '11:35',
  '12:30', '13:25', '14:20', '15:15', '16:10', '17:05',
  '18:00', '18:55', '19:50', '20:45', '21:40'
];

export default function DisponibilidadesPage() {
  const [professores, setProfessores] = useState<Professor[]>([]);
  const [professorSelecionado, setProfessorSelecionado] = useState<number | null>(null);
  const [disponibilidades, setDisponibilidades] = useState<Disponibilidade[]>([]);
  const [loading, setLoading] = useState(true);
  const [salvando, setSalvando] = useState(false);

  useEffect(() => {
    carregarProfessores();
  }, []);

  useEffect(() => {
    if (professorSelecionado) {
      carregarDisponibilidades();
    }
  }, [professorSelecionado]);

  const carregarProfessores = async () => {
    try {
      const response = await axios.get('/professores');
      setProfessores(response.data);
      if (response.data.length > 0) {
        setProfessorSelecionado(response.data[0].id);
      }
    } catch (error) {
      console.error('Erro ao carregar professores:', error);
      alert('Erro ao carregar professores');
    }
  };

  const carregarDisponibilidades = async () => {
    if (!professorSelecionado) return;
    
    try {
      setLoading(true);
      const response = await axios.get(`/disponibilidades/professor/${professorSelecionado}`);
      setDisponibilidades(response.data);
    } catch (error) {
      console.error('Erro ao carregar disponibilidades:', error);
      setDisponibilidades([]);
    } finally {
      setLoading(false);
    }
  };

  const toggleDisponibilidade = async (dia: string, horario: string) => {
    if (!professorSelecionado) return;

    const existente = disponibilidades.find(
      d => d.dia_semana === dia && d.horario_inicio === horario
    );

    setSalvando(true);
    try {
      if (existente) {
        // Atualizar disponibilidade existente
        await axios.put(`/disponibilidades/${existente.id}`, {
          ...existente,
          disponivel: !existente.disponivel
        });
      } else {
        // Criar nova disponibilidade (indisponível)
        await axios.post('/disponibilidades', {
          professor_id: professorSelecionado,
          dia_semana: dia,
          horario_inicio: horario,
          horario_fim: calcularHorarioFim(horario),
          disponivel: false
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
    const idx = HORARIOS.indexOf(inicio);
    if (idx >= 0 && idx < HORARIOS.length - 1) {
      return HORARIOS[idx + 1];
    }
    // Adicionar 50 minutos para o último horário
    const [h, m] = inicio.split(':').map(Number);
    const novoMinuto = m + 50;
    const novaHora = h + Math.floor(novoMinuto / 60);
    return `${String(novaHora).padStart(2, '0')}:${String(novoMinuto % 60).padStart(2, '0')}`;
  };

  const isIndisponivel = (dia: string, horario: string): boolean => {
    const disp = disponibilidades.find(
      d => d.dia_semana === dia && d.horario_inicio === horario
    );
    return disp ? !disp.disponivel : false;
  };

  const limparTodasDisponibilidades = async () => {
    if (!professorSelecionado) return;
    
    if (!confirm('Deseja remover todas as indisponibilidades deste professor?')) {
      return;
    }

    setSalvando(true);
    try {
      for (const disp of disponibilidades) {
        await axios.delete(`/disponibilidades/${disp.id}`);
      }
      await carregarDisponibilidades();
      alert('Todas as indisponibilidades foram removidas!');
    } catch (error) {
      console.error('Erro ao limpar disponibilidades:', error);
      alert('Erro ao limpar disponibilidades');
    } finally {
      setSalvando(false);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          Disponibilidades
        </h1>
        <p className="text-gray-600">
          Marque os horários em que o professor NÃO está disponível (clique para alternar)
        </p>
      </div>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-gray-700">
            Professor:
          </label>
          <select
            value={professorSelecionado || ''}
            onChange={(e) => setProfessorSelecionado(Number(e.target.value))}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            disabled={salvando}
          >
            {professores.map(prof => (
              <option key={prof.id} value={prof.id}>
                {prof.nome}
              </option>
            ))}
          </select>
          <button
            onClick={limparTodasDisponibilidades}
            disabled={salvando || disponibilidades.length === 0}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Limpar Todas
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="text-gray-500">Carregando disponibilidades...</div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
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
              </thead>
              <tbody>
                {HORARIOS.map((horario, idx) => (
                  <tr key={horario} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-4 py-2 text-sm font-medium text-gray-700 border-b border-r whitespace-nowrap">
                      {horario}
                    </td>
                    {DIAS_SEMANA.map(dia => {
                      const indisponivel = isIndisponivel(dia, horario);
                      return (
                        <td key={`${dia}-${horario}`} className="border-b border-r p-0">
                          <button
                            onClick={() => toggleDisponibilidade(dia, horario)}
                            disabled={salvando}
                            className={`w-full h-12 transition-colors ${
                              indisponivel
                                ? 'bg-red-100 hover:bg-red-200'
                                : 'bg-green-50 hover:bg-green-100'
                            } disabled:opacity-50 disabled:cursor-not-allowed`}
                            title={indisponivel ? 'Indisponível (clique para marcar como disponível)' : 'Disponível (clique para marcar como indisponível)'}
                          >
                            {indisponivel && (
                              <span className="text-red-600 font-bold">✕</span>
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

      <div className="mt-4 p-4 bg-blue-50 rounded-lg">
        <div className="text-sm text-gray-700">
          <strong>Legenda:</strong>
          <div className="flex items-center gap-6 mt-2">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-green-50 border border-gray-300 rounded"></div>
              <span>Disponível</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-red-100 border border-gray-300 rounded flex items-center justify-center">
                <span className="text-red-600 font-bold">✕</span>
              </div>
              <span>Indisponível</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
