'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { FaPlus, FaEye, FaPlay, FaTrash, FaClock, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import { horarioService, Horario, HorarioCreate } from '@/lib/api';

export default function HorariosPage() {
  const [horarios, setHorarios] = useState<Horario[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [showGerarModal, setShowGerarModal] = useState(false);
  const [showProgressModal, setShowProgressModal] = useState(false);
  const [progressTime, setProgressTime] = useState(0);
  const [horarioToGenerate, setHorarioToGenerate] = useState<number | null>(null);
  const [turnoGerar, setTurnoGerar] = useState<'MATUTINO' | 'VESPERTINO' | 'NOTURNO' | ''>('');
  const [formData, setFormData] = useState<HorarioCreate>({
    nome: '',
    ano_letivo: new Date().getFullYear(),
    semestre: 1,
  });

  useEffect(() => {
    carregarHorarios();
  }, []);

  const carregarHorarios = async () => {
    try {
      const response = await horarioService.getAll();
      setHorarios(response.data);
    } catch (error) {
      console.error('Erro ao carregar horários:', error);
      alert('Erro ao carregar horários');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await horarioService.create(formData);
      await carregarHorarios();
      setShowModal(false);
      setFormData({
        nome: '',
        ano_letivo: new Date().getFullYear(),
        semestre: 1,
      });
      alert('Horário criado com sucesso!');
    } catch (error) {
      console.error('Erro ao criar horário:', error);
      alert('Erro ao criar horário');
    }
  };

  const handleGerar = async (id: number) => {
    setHorarioToGenerate(id);
    setShowGerarModal(true);
  };

  const handleConfirmGerar = async () => {
    if (!horarioToGenerate) return;

    setShowGerarModal(false);
    setShowProgressModal(true);
    setProgressTime(0);

    // Iniciar timer
    const timer = setInterval(() => {
      setProgressTime(prev => prev + 1);
    }, 1000);

    try {
      // Iniciar geração em background
      await horarioService.gerar(horarioToGenerate, {
        horario_id: horarioToGenerate,
        turno: turnoGerar || null,
        limitar_janelas: true,
        respeitar_deslocamento: true,
        distribuir_uniformemente: true,
        tempo_maximo_geracao: 300,
      });

      // Polling para verificar status com contador de tentativas
      let pollAttempts = 0;
      const maxPollAttempts = 150; // 5 minutos = 150 tentativas de 2 segundos

      const pollStatus = async () => {
        pollAttempts++;
        
        // Verificar se excedeu o número máximo de tentativas
        if (pollAttempts > maxPollAttempts) {
          clearInterval(timer);
          alert('Timeout: A geração do horário demorou mais que o esperado. Verifique o status manualmente.');
          setShowProgressModal(false);
          setHorarioToGenerate(null);
          setTurnoGerar('');
          setProgressTime(0);
          await carregarHorarios();
          return;
        }

        try {
          const response = await horarioService.getById(horarioToGenerate);
          const horario = response.data;

          if (horario.status === 'FINALIZADO' || horario.status === 'APROVADO') {
            clearInterval(timer);
            alert(`Horário gerado com sucesso!\n\nAulas alocadas: ${horario.aulas_alocadas}/${horario.total_aulas}\nQualidade: ${horario.qualidade_score}%\nConflitos: ${horario.tem_conflitos ? 'Sim' : 'Não'}`);
            await carregarHorarios();
            setShowProgressModal(false);
            setHorarioToGenerate(null);
            setTurnoGerar('');
            setProgressTime(0);
          } else if (horario.status === 'RASCUNHO') {
            // Erro na geração
            clearInterval(timer);
            alert('Erro ao gerar horário');
            setShowProgressModal(false);
            setHorarioToGenerate(null);
            setTurnoGerar('');
            setProgressTime(0);
          } else {
            // Ainda em progresso, continuar polling
            setTimeout(pollStatus, 2000);
          }
        } catch (error: any) {
          // Em caso de erro, continuar tentando até o limite
          console.warn(`Tentativa ${pollAttempts} falhou, continuando...`, error);
          if (pollAttempts < maxPollAttempts) {
            setTimeout(pollStatus, 2000);
          } else {
            clearInterval(timer);
            console.error('Erro ao verificar status após múltiplas tentativas:', error);
            alert('Erro ao verificar status da geração após múltiplas tentativas');
            setShowProgressModal(false);
            setHorarioToGenerate(null);
            setTurnoGerar('');
            setProgressTime(0);
          }
        }
      };

      // Iniciar polling após 2 segundos
      setTimeout(pollStatus, 2000);

    } catch (error: any) {
      clearInterval(timer);
      console.error('Erro ao iniciar geração:', error);
      alert(`Erro ao iniciar geração: ${error.response?.data?.detail || error.message}`);
      setShowProgressModal(false);
      setHorarioToGenerate(null);
      setTurnoGerar('');
      setProgressTime(0);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Deseja realmente excluir este horário?')) return;

    try {
      await horarioService.delete(id);
      await carregarHorarios();
      alert('Horário excluído com sucesso!');
    } catch (error) {
      console.error('Erro ao excluir horário:', error);
      alert('Erro ao excluir horário');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'RASCUNHO':
        return 'bg-gray-100 text-gray-800';
      case 'EM_PROGRESSO':
        return 'bg-yellow-100 text-yellow-800';
      case 'FINALIZADO':
        return 'bg-green-100 text-green-800';
      case 'APROVADO':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Horários</h1>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition"
        >
          <FaPlus />
          <span>Novo Horário</span>
        </button>
      </div>

      {/* Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {horarios.map((horario) => (
          <div key={horario.id} className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-gray-800">{horario.nome}</h3>
              <span
                className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(
                  horario.status
                )}`}
              >
                {horario.status}
              </span>
            </div>

            <div className="space-y-2 text-sm text-gray-600 mb-4">
              <p>
                <strong>Ano Letivo:</strong> {horario.ano_letivo}
              </p>
              <p>
                <strong>Semestre:</strong> {horario.semestre}º
              </p>
              <p>
                <strong>Aulas Alocadas:</strong> {horario.aulas_alocadas}/{horario.total_aulas}
              </p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full"
                  style={{
                    width: horario.total_aulas > 0
                      ? `${(horario.aulas_alocadas / horario.total_aulas) * 100}%`
                      : '0%',
                  }}
                ></div>
              </div>
              <p>
                <strong>Qualidade:</strong> {horario.qualidade_score}%
              </p>
              {horario.tem_conflitos && (
                <div className="flex items-center space-x-2 text-red-600">
                  <FaExclamationTriangle />
                  <span className="text-sm font-medium">Conflitos detectados</span>
                </div>
              )}
            </div>

            <div className="flex space-x-2">
              <Link
                href={`/horarios/${horario.id}`}
                className="flex-1 flex items-center justify-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded-lg text-sm transition"
              >
                <FaEye />
                <span>Visualizar</span>
              </Link>
              
              {horario.status === 'RASCUNHO' && (
                <button
                  onClick={() => handleGerar(horario.id)}
                  className="flex-1 flex items-center justify-center space-x-2 bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded-lg text-sm transition"
                >
                  <FaPlay />
                  <span>Gerar</span>
                </button>
              )}

              <button
                onClick={() => handleDelete(horario.id)}
                className="flex items-center justify-center bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded-lg text-sm transition"
              >
                <FaTrash />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Novo Horário</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome
                </label>
                <input
                  type="text"
                  required
                  value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ex: Horário 1º Semestre 2024"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Ano Letivo
                </label>
                <input
                  type="number"
                  required
                  value={formData.ano_letivo}
                  onChange={(e) =>
                    setFormData({ ...formData, ano_letivo: Number(e.target.value) })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Semestre
                </label>
                <select
                  value={formData.semestre}
                  onChange={(e) =>
                    setFormData({ ...formData, semestre: Number(e.target.value) })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value={1}>1º Semestre</option>
                  <option value={2}>2º Semestre</option>
                </select>
              </div>
              <div className="flex space-x-2 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition"
                >
                  Criar
                </button>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-lg transition"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      {/* Modal de Progresso */}
      {showProgressModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Gerando Horário
              </h3>
              <p className="text-gray-600 mb-4">
                Por favor, aguarde enquanto o horário está sendo otimizado...
              </p>
              
              <div className="space-y-2 text-sm text-gray-700">
                <div className="flex justify-between">
                  <span>Tempo percorrido:</span>
                  <span className="font-mono">{Math.floor(progressTime / 60)}:{(progressTime % 60).toString().padStart(2, '0')}</span>
                </div>
                <div className="flex justify-between">
                  <span>Tempo estimado:</span>
                  <span className="font-mono">até 5:00</span>
                </div>
              </div>
              
              <div className="mt-4">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full transition-all duration-1000"
                    style={{
                      width: `${Math.min((progressTime / 300) * 100, 100)}%`,
                    }}
                  ></div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {Math.min(Math.round((progressTime / 300) * 100), 100)}% do tempo estimado
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
      {/* Modal Configuração Geração */}
      {showGerarModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Gerar Horário</h2>
            <div className="space-y-4">
              <p className="text-gray-600">
                Selecione o turno para gerar o horário. Se nenhum turno for selecionado, todos os turnos serão gerados.
              </p>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Turno
                </label>
                <select
                  value={turnoGerar}
                  onChange={(e) => setTurnoGerar(e.target.value as any)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Todos os Turnos</option>
                  <option value="MATUTINO">Manhã (07:00 - 12:15)</option>
                  <option value="VESPERTINO">Tarde (13:00 - 18:15)</option>
                  <option value="NOTURNO">Noite (18:00 - 21:40)</option>
                </select>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <p className="text-sm text-blue-800">
                  <strong>Importante:</strong> As aulas regentes serão priorizadas no turno principal. 
                  As horas-atividade serão alocadas preferencialmente em contra-turno quando possível.
                </p>
              </div>

              <div className="flex space-x-2 pt-4">
                <button
                  type="button"
                  onClick={handleConfirmGerar}
                  className="flex-1 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition"
                >
                  Gerar
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowGerarModal(false);
                    setHorarioToGenerate(null);
                    setTurnoGerar('');
                  }}
                  className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-lg transition"
                >
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
