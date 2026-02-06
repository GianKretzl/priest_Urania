'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface Professor {
  id: number;
  nome: string;
}

interface Disciplina {
  id: number;
  nome: string;
  cor: string;
}

interface Turma {
  id: number;
  nome: string;
  ano_serie: string;
}

interface GradeCurricular {
  id: number;
  turma_id: number;
  disciplina_id: number;
  professor_id: number;
  aulas_por_semana: number;
  turma: Turma;
  disciplina: Disciplina;
  professor: Professor;
}

export default function GradesPage() {
  const [grades, setGrades] = useState<GradeCurricular[]>([]);
  const [turmas, setTurmas] = useState<Turma[]>([]);
  const [disciplinas, setDisciplinas] = useState<Disciplina[]>([]);
  const [professores, setProfessores] = useState<Professor[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editando, setEditando] = useState<GradeCurricular | null>(null);
  const [turmaSelecionada, setTurmaSelecionada] = useState<number | null>(null);
  
  const [formData, setFormData] = useState({
    turma_id: 0,
    disciplina_id: 0,
    professor_id: 0,
    aulas_por_semana: 2,
    ativa: true,
  });

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      const [gradesRes, turmasRes, disciplinasRes, professoresRes] = await Promise.all([
        api.get('/grades-curriculares'),
        api.get('/turmas'),
        api.get('/disciplinas'),
        api.get('/professores'),
      ]);
      
      setGrades(gradesRes.data);
      setTurmas(turmasRes.data);
      setDisciplinas(disciplinasRes.data);
      setProfessores(professoresRes.data);
      
      if (turmasRes.data.length > 0) {
        setTurmaSelecionada(turmasRes.data[0].id);
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      alert('Erro ao carregar dados');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (editando) {
        await api.put(`/grades-curriculares/${editando.id}`, formData);
        alert('Grade atualizada com sucesso!');
      } else {
        await api.post('/grades-curriculares', formData);
        alert('Grade cadastrada com sucesso!');
      }
      
      setShowForm(false);
      setEditando(null);
      resetForm();
      carregarDados();
    } catch (error) {
      console.error('Erro ao salvar grade:', error);
      alert('Erro ao salvar grade');
    }
  };

  const handleEdit = (grade: GradeCurricular) => {
    setEditando(grade);
    setFormData({
      turma_id: grade.turma_id,
      disciplina_id: grade.disciplina_id,
      professor_id: grade.professor_id,
      aulas_por_semana: grade.aulas_por_semana,
      ativa: true,
    });
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Deseja realmente excluir esta grade curricular?')) return;
    
    try {
      await api.delete(`/grades-curriculares/${id}`);
      alert('Grade excluída com sucesso!');
      carregarDados();
    } catch (error) {
      console.error('Erro ao excluir grade:', error);
      alert('Erro ao excluir grade');
    }
  };

  const resetForm = () => {
    setFormData({
      turma_id: turmaSelecionada || 0,
      disciplina_id: 0,
      professor_id: 0,
      aulas_por_semana: 2,
      ativa: true,
    });
  };

  const gradesFiltradas = turmaSelecionada
    ? grades.filter(g => g.turma_id === turmaSelecionada && g.disciplina && g.professor && g.turma)
    : grades.filter(g => g.disciplina && g.professor && g.turma);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-500">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          Grade Curricular
        </h1>
        <p className="text-gray-600">
          Gerencie a atribuição de disciplinas, professores e turmas
        </p>
      </div>

      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 flex-1">
            <label className="text-sm font-medium text-gray-700">
              Filtrar por Turma:
            </label>
            <select
              value={turmaSelecionada || ''}
              onChange={(e) => setTurmaSelecionada(Number(e.target.value))}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              {turmas.map(turma => (
                <option key={turma.id} value={turma.id}>
                  {turma.nome} - {turma.ano_serie}
                </option>
              ))}
            </select>
          </div>
          <button
            onClick={() => {
              resetForm();
              setShowForm(true);
            }}
            className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            + Nova Grade
          </button>
        </div>
      </div>

      {/* Formulário Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">
              {editando ? 'Editar Grade' : 'Nova Grade'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Turma
                </label>
                <select
                  required
                  value={formData.turma_id}
                  onChange={(e) => setFormData({ ...formData, turma_id: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value={0}>Selecione uma turma</option>
                  {turmas.map(turma => (
                    <option key={turma.id} value={turma.id}>
                      {turma.nome} - {turma.ano_serie}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Disciplina
                </label>
                <select
                  required
                  value={formData.disciplina_id}
                  onChange={(e) => setFormData({ ...formData, disciplina_id: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value={0}>Selecione uma disciplina</option>
                  {disciplinas.map(disc => (
                    <option key={disc.id} value={disc.id}>
                      {disc.nome}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Professor
                </label>
                <select
                  required
                  value={formData.professor_id}
                  onChange={(e) => setFormData({ ...formData, professor_id: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value={0}>Selecione um professor</option>
                  {professores.map(prof => (
                    <option key={prof.id} value={prof.id}>
                      {prof.nome}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Aulas por Semana
                </label>
                <input
                  type="number"
                  required
                  min="1"
                  max="20"
                  value={formData.aulas_por_semana}
                  onChange={(e) => setFormData({ ...formData, aulas_por_semana: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
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

      {/* Tabela */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Disciplina
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Professor
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Aulas/Semana
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ações
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {gradesFiltradas.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-6 py-8 text-center text-gray-500">
                  Nenhuma grade curricular cadastrada para esta turma
                </td>
              </tr>
            ) : (
              gradesFiltradas.map((grade) => (
                <tr key={grade.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-2">
                      <div
                        className="w-4 h-4 rounded"
                        style={{ backgroundColor: grade.disciplina?.cor || '#9CA3AF' }}
                      ></div>
                      <span className="text-sm font-medium text-gray-900">
                        {grade.disciplina?.nome || 'N/A'}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {grade.professor?.nome || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {grade.aulas_por_semana} aulas
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      onClick={() => handleEdit(grade)}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDelete(grade.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Excluir
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Resumo */}
      {turmaSelecionada && (
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">Resumo da Turma</h3>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-blue-700">Total de Disciplinas:</span>
              <span className="ml-2 font-semibold text-blue-900">{gradesFiltradas.length}</span>
            </div>
            <div>
              <span className="text-blue-700">Total de Aulas/Semana:</span>
              <span className="ml-2 font-semibold text-blue-900">
                {gradesFiltradas.reduce((sum, g) => sum + g.aulas_por_semana, 0)}
              </span>
            </div>
            <div>
              <span className="text-blue-700">Professores Diferentes:</span>
              <span className="ml-2 font-semibold text-blue-900">
                {new Set(gradesFiltradas.map(g => g.professor_id)).size}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
