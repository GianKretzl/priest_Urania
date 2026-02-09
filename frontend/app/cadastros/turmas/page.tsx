'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { FaEdit, FaTrash } from 'react-icons/fa';

interface Turma {
  id: number;
  nome: string;
  ano_serie: string;
  turno: string;
  numero_alunos: number;
  ativa: boolean;
}

export default function TurmasPage() {
  const [turmas, setTurmas] = useState<Turma[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editando, setEditando] = useState<Turma | null>(null);
  
  const [formData, setFormData] = useState({
    nome: '',
    ano_serie: '',
    turno: 'MATUTINO',
    numero_alunos: 0,
    ativa: true,
  });

  useEffect(() => {
    carregarTurmas();
  }, []);

  const carregarTurmas = async () => {
    try {
      const response = await api.get('/turmas');
      // Ordenar alfabeticamente por nome
      const turmasOrdenadas = response.data.sort((a: Turma, b: Turma) => 
        a.nome.localeCompare(b.nome)
      );
      setTurmas(turmasOrdenadas);
    } catch (error) {
      console.error('Erro ao carregar turmas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (editando) {
        await api.put(`/turmas/${editando.id}`, formData);
        alert('Turma atualizada com sucesso!');
      } else {
        await api.post('/turmas', formData);
        alert('Turma cadastrada com sucesso!');
      }
      
      setShowForm(false);
      setEditando(null);
      resetForm();
      carregarTurmas();
    } catch (error) {
      console.error('Erro ao salvar turma:', error);
      alert('Erro ao salvar turma');
    }
  };

  const handleEdit = (turma: Turma) => {
    setEditando(turma);
    setFormData({
      nome: turma.nome,
      ano_serie: turma.ano_serie,
      turno: turma.turno,
      numero_alunos: turma.numero_alunos,
      ativa: turma.ativa,
    });
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Deseja realmente excluir esta turma?')) return;
    
    try {
      await api.delete(`/turmas/${id}`);
      alert('Turma excluída com sucesso!');
      carregarTurmas();
    } catch (error) {
      console.error('Erro ao excluir turma:', error);
      alert('Erro ao excluir turma');
    }
  };

  const resetForm = () => {
    setFormData({
      nome: '',
      ano_serie: '',
      turno: 'MATUTINO',
      numero_alunos: 0,
      ativa: true,
    });
  };

  if (loading) {
    return <div className="text-center py-8">Carregando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Turmas</h1>
        <button
          onClick={() => {
            setEditando(null);
            resetForm();
            setShowForm(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          + Nova Turma
        </button>
      </div>

      {/* Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">
              {editando ? 'Editar Turma' : 'Nova Turma'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nome *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.nome}
                    onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Ex: 1A, 2B"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Ano/Série *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.ano_serie}
                    onChange={(e) => setFormData({ ...formData, ano_serie: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Ex: 1º Ano - ADM"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Turno *
                  </label>
                  <select
                    required
                    value={formData.turno}
                    onChange={(e) => setFormData({ ...formData, turno: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="MATUTINO">Manhã</option>
                    <option value="VESPERTINO">Tarde</option>
                    <option value="NOTURNO">Noite</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Número de Alunos
                  </label>
                  <input
                    type="number"
                    value={formData.numero_alunos}
                    onChange={(e) => setFormData({ ...formData, numero_alunos: parseInt(e.target.value) || 0 })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={formData.ativa}
                      onChange={(e) => setFormData({ ...formData, ativa: e.target.checked })}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700">Ativa</span>
                  </label>
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditando(null);
                    resetForm();
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {editando ? 'Atualizar' : 'Cadastrar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Nome
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ano/Série
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Turno
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Alunos
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
            {turmas.map((turma) => (
              <tr key={turma.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {turma.nome}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {turma.ano_serie}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {turma.turno === 'MATUTINO' ? 'Manhã' : turma.turno === 'VESPERTINO' ? 'Tarde' : turma.turno === 'NOTURNO' ? 'Noite' : turma.turno}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {turma.numero_alunos}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      turma.ativa
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {turma.ativa ? 'Ativa' : 'Inativa'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleEdit(turma)}
                      className="flex items-center gap-1 px-3 py-1.5 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors"
                      title="Editar turma"
                    >
                      <FaEdit className="text-sm" />
                      <span>Editar</span>
                    </button>
                    <button
                      onClick={() => handleDelete(turma.id)}
                      className="flex items-center gap-1 px-3 py-1.5 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors"
                      title="Excluir turma"
                    >
                      <FaTrash className="text-sm" />
                      <span>Excluir</span>
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {turmas.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            Nenhuma turma cadastrada
          </div>
        )}
      </div>
    </div>
  );
}
