'use client';

import { useState, useEffect } from 'react';
import { FaPlus, FaEdit, FaTrash, FaSave, FaTimes } from 'react-icons/fa';
import { disciplinaService, Disciplina } from '@/lib/api';

export default function DisciplinasPage() {
  const [disciplinas, setDisciplinas] = useState<Disciplina[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    nome: '',
    codigo: '',
    carga_horaria_semanal: 4,
    duracao_aula: 50,
    cor: '#3B82F6',
    ativa: true,
  });

  useEffect(() => {
    carregarDisciplinas();
  }, []);

  const carregarDisciplinas = async () => {
    try {
      const response = await disciplinaService.getAll();
      setDisciplinas(response.data);
    } catch (error) {
      console.error('Erro ao carregar disciplinas:', error);
      alert('Erro ao carregar disciplinas');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        await disciplinaService.update(editingId, formData);
      } else {
        await disciplinaService.create(formData);
      }
      await carregarDisciplinas();
      handleCloseModal();
      alert(editingId ? 'Disciplina atualizada com sucesso!' : 'Disciplina criada com sucesso!');
    } catch (error) {
      console.error('Erro ao salvar disciplina:', error);
      alert('Erro ao salvar disciplina');
    }
  };

  const handleEdit = (disciplina: Disciplina) => {
    setEditingId(disciplina.id);
    setFormData({
      nome: disciplina.nome,
      codigo: disciplina.codigo,
      carga_horaria_semanal: disciplina.carga_horaria_semanal,
      duracao_aula: disciplina.duracao_aula,
      cor: disciplina.cor,
      ativa: disciplina.ativa,
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Deseja realmente excluir esta disciplina?')) return;
    
    try {
      await disciplinaService.delete(id);
      await carregarDisciplinas();
      alert('Disciplina excluída com sucesso!');
    } catch (error) {
      console.error('Erro ao excluir disciplina:', error);
      alert('Erro ao excluir disciplina');
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingId(null);
    setFormData({
      nome: '',
      codigo: '',
      carga_horaria_semanal: 4,
      duracao_aula: 50,
      cor: '#3B82F6',
      ativa: true,
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Disciplinas</h1>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition"
        >
          <FaPlus />
          <span>Nova Disciplina</span>
        </button>
      </div>

      {/* Tabela */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Código
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Nome
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Carga Horária
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Duração (min)
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Cor
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ações
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {disciplinas.map((disciplina) => (
              <tr key={disciplina.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {disciplina.codigo}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {disciplina.nome}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {disciplina.carga_horaria_semanal} aulas/semana
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {disciplina.duracao_aula} min
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div className="flex items-center space-x-2">
                    <div
                      className="w-6 h-6 rounded"
                      style={{ backgroundColor: disciplina.cor }}
                    ></div>
                    <span>{disciplina.cor}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      disciplina.ativa
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {disciplina.ativa ? 'Ativa' : 'Inativa'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button
                    onClick={() => handleEdit(disciplina)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    <FaEdit />
                  </button>
                  <button
                    onClick={() => handleDelete(disciplina.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <FaTrash />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">
              {editingId ? 'Editar Disciplina' : 'Nova Disciplina'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Código
                </label>
                <input
                  type="text"
                  required
                  value={formData.codigo}
                  onChange={(e) => setFormData({ ...formData, codigo: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
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
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Carga Horária Semanal (aulas)
                </label>
                <input
                  type="number"
                  required
                  min="1"
                  value={formData.carga_horaria_semanal}
                  onChange={(e) =>
                    setFormData({ ...formData, carga_horaria_semanal: Number(e.target.value) })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Duração da Aula (minutos)
                </label>
                <input
                  type="number"
                  required
                  min="1"
                  value={formData.duracao_aula}
                  onChange={(e) =>
                    setFormData({ ...formData, duracao_aula: Number(e.target.value) })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cor
                </label>
                <input
                  type="color"
                  value={formData.cor}
                  onChange={(e) => setFormData({ ...formData, cor: e.target.value })}
                  className="w-full h-10 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="ativa"
                  checked={formData.ativa}
                  onChange={(e) => setFormData({ ...formData, ativa: e.target.checked })}
                  className="mr-2"
                />
                <label htmlFor="ativa" className="text-sm font-medium text-gray-700">
                  Disciplina Ativa
                </label>
              </div>
              <div className="flex space-x-2 pt-4">
                <button
                  type="submit"
                  className="flex-1 flex items-center justify-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition"
                >
                  <FaSave />
                  <span>Salvar</span>
                </button>
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="flex-1 flex items-center justify-center space-x-2 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-lg transition"
                >
                  <FaTimes />
                  <span>Cancelar</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
