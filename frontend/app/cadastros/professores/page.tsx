'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface Disciplina {
  id: number;
  nome: string;
}

interface Professor {
  id: number;
  nome: string;
  email: string;
  telefone?: string;
  cpf?: string;
  carga_horaria_maxima: number;
  horas_atividade: number;
  max_aulas_seguidas: number;
  max_aulas_dia: number;
  tempo_deslocamento: number;
  ativo: boolean;
  disciplinas?: Disciplina[];
}

export default function ProfessoresPage() {
  const [professores, setProfessores] = useState<Professor[]>([]);
  const [disciplinas, setDisciplinas] = useState<Disciplina[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editando, setEditando] = useState<Professor | null>(null);
  
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    telefone: '',
    cpf: '',
    carga_horaria_maxima: 40,
    horas_atividade: 8,
    max_aulas_seguidas: 4,
    max_aulas_dia: 8,
    tempo_deslocamento: 0,
    ativo: true,
    disciplinas_ids: [] as number[],
  });

  useEffect(() => {
    carregarProfessores();
    carregarDisciplinas();
  }, []);

  const carregarDisciplinas = async () => {
    try {
      const response = await api.get('/disciplinas');
      setDisciplinas(response.data);
    } catch (error) {
      console.error('Erro ao carregar disciplinas:', error);
    }
  };

  const carregarProfessores = async () => {
    try {
      const response = await api.get('/professores');
      setProfessores(response.data);
    } catch (error) {
      console.error('Erro ao carregar professores:', error);
      alert('Erro ao carregar professores');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (editando) {
        await api.put(`/professores/${editando.id}`, formData);
        alert('Professor atualizado com sucesso!');
      } else {
        await api.post('/professores', formData);
        alert('Professor cadastrado com sucesso!');
      }
      
      setShowForm(false);
      setEditando(null);
      resetForm();
      carregarProfessores();
    } catch (error) {
      console.error('Erro ao salvar professor:', error);
      alert('Erro ao salvar professor');
    }
  };

  const handleEdit = (professor: Professor) => {
    setEditando(professor);
    setFormData({
      nome: professor.nome,
      email: professor.email,
      telefone: professor.telefone || '',
      cpf: professor.cpf || '',
      carga_horaria_maxima: professor.carga_horaria_maxima,
      horas_atividade: professor.horas_atividade,
      max_aulas_seguidas: professor.max_aulas_seguidas,
      max_aulas_dia: professor.max_aulas_dia,
      tempo_deslocamento: professor.tempo_deslocamento,
      ativo: professor.ativo,
      disciplinas_ids: professor.disciplinas?.map(d => d.id) || [],
    });
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Deseja realmente excluir este professor?')) return;
    
    try {
      await api.delete(`/professores/${id}`);
      alert('Professor excluído com sucesso!');
      carregarProfessores();
    } catch (error) {
      console.error('Erro ao excluir professor:', error);
      alert('Erro ao excluir professor');
    }
  };

  const resetForm = () => {
    setFormData({
      nome: '',
      email: '',
      telefone: '',
      cpf: '',
      carga_horaria_maxima: 40,
      horas_atividade: 8,
      max_aulas_seguidas: 4,
      max_aulas_dia: 8,
      tempo_deslocamento: 0,
      ativo: true,
      disciplinas_ids: [],
    });
  };

  if (loading) {
    return <div className="text-center py-8">Carregando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Professores</h1>
        <button
          onClick={() => {
            setShowForm(!showForm);
            setEditando(null);
            resetForm();
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          {showForm ? 'Cancelar' : '+ Novo Professor'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">
            {editando ? 'Editar Professor' : 'Novo Professor'}
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
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email *
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Telefone
                </label>
                <input
                  type="text"
                  value={formData.telefone}
                  onChange={(e) => setFormData({ ...formData, telefone: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  CPF
                </label>
                <input
                  type="text"
                  value={formData.cpf}
                  onChange={(e) => setFormData({ ...formData, cpf: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Carga Horária Máxima (aulas/semana)
                </label>
                <input
                  type="number"
                  value={formData.carga_horaria_maxima}
                  onChange={(e) => setFormData({ ...formData, carga_horaria_maxima: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Horas-Atividade (h/semana)
                </label>
                <input
                  type="number"
                  value={formData.horas_atividade}
                  onChange={(e) => setFormData({ ...formData, horas_atividade: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Máx. Aulas Seguidas
                </label>
                <input
                  type="number"
                  value={formData.max_aulas_seguidas}
                  onChange={(e) => setFormData({ ...formData, max_aulas_seguidas: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Máx. Aulas por Dia
                </label>
                <input
                  type="number"
                  value={formData.max_aulas_dia}
                  onChange={(e) => setFormData({ ...formData, max_aulas_dia: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tempo Deslocamento (minutos)
                </label>
                <input
                  type="number"
                  value={formData.tempo_deslocamento}
                  onChange={(e) => setFormData({ ...formData, tempo_deslocamento: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Disciplinas que leciona
                </label>
                <div className="border border-gray-300 rounded-lg p-3 max-h-64 overflow-y-auto bg-gray-50">
                  {disciplinas.length === 0 ? (
                    <p className="text-sm text-gray-500">Nenhuma disciplina cadastrada</p>
                  ) : (
                    <div className="space-y-2">
                      {disciplinas.map((disciplina) => (
                        <label key={disciplina.id} className="flex items-center space-x-2 hover:bg-gray-100 p-2 rounded cursor-pointer">
                          <input
                            type="checkbox"
                            checked={formData.disciplinas_ids.includes(disciplina.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setFormData({
                                  ...formData,
                                  disciplinas_ids: [...formData.disciplinas_ids, disciplina.id]
                                });
                              } else {
                                setFormData({
                                  ...formData,
                                  disciplinas_ids: formData.disciplinas_ids.filter(id => id !== disciplina.id)
                                });
                              }
                            }}
                            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700">
                            {disciplina.nome} <span className="text-gray-500">({disciplina.codigo})</span>
                          </span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              <div>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.ativo}
                    onChange={(e) => setFormData({ ...formData, ativo: e.target.checked })}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-sm font-medium text-gray-700">Ativo</span>
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
      )}

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Nome
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Disciplinas
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Carga Horária
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
            {professores.map((professor) => (
              <tr key={professor.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {professor.nome}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {professor.email}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {professor.disciplinas && professor.disciplinas.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {professor.disciplinas.map((disc) => (
                        <span
                          key={disc.id}
                          className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs"
                        >
                          {disc.nome}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span className="text-gray-400 italic">Nenhuma</span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {professor.carga_horaria_maxima}h
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      professor.ativo
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {professor.ativo ? 'Ativo' : 'Inativo'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button
                    onClick={() => handleEdit(professor)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    Editar
                  </button>
                  <button
                    onClick={() => handleDelete(professor.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    Excluir
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {professores.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            Nenhum professor cadastrado
          </div>
        )}
      </div>
    </div>
  );
}
