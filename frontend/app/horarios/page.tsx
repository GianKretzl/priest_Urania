'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { FaPlus, FaEye, FaPlay, FaTrash, FaClock, FaCheckCircle } from 'react-icons/fa';
import { horarioService, Horario } from '@/lib/api';

export default function HorariosPage() {
  const [horarios, setHorarios] = useState<Horario[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
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
    if (!confirm('Deseja iniciar a geração automática do horário? Este processo pode levar alguns minutos.')) {
      return;
    }

    try {
      const response = await horarioService.gerar(id, {
        horario_id: id,
        limitar_janelas: true,
        respeitar_deslocamento: true,
        distribuir_uniformemente: true,
        tempo_maximo_geracao: 300,
      });

      const data = response.data;
      if (data.success) {
        alert(`Horário gerado com sucesso!\n\nAulas alocadas: ${data.aulas_alocadas}/${data.total_aulas}\nQualidade: ${data.qualidade_score}%\nTempo: ${data.tempo_geracao.toFixed(2)}s`);
        await carregarHorarios();
      } else {
        alert(`Erro ao gerar horário: ${data.message}`);
      }
    } catch (error: any) {
      console.error('Erro ao gerar horário:', error);
      alert(`Erro ao gerar horário: ${error.response?.data?.detail || error.message}`);
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
    </div>
  );
}
