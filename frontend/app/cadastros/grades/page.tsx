'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { FaEdit, FaTrash, FaPlus, FaFilter, FaCopy, FaTimes } from 'react-icons/fa';

interface Professor {
  id: number;
  nome: string;
  ativo: boolean;
}

interface Disciplina {
  id: number;
  nome: string;
  ativa: boolean;
}

interface Turma {
  id: number;
  nome: string;
  ano_serie: string;
  turno: string;
  ativa: boolean;
}

interface GradeCurricular {
  id: number;
  turma_id: number;
  disciplina_id: number;
  professor_id: number;
  professor_id_2: number | null;
  aulas_por_semana: number;
  ativa: boolean;
  turma?: Turma;
  disciplina?: Disciplina;
  professor?: Professor;
  professor_2?: Professor;
}

const TURNO_LABELS: { [key: string]: string } = {
  MATUTINO: 'Manhã',
  VESPERTINO: 'Tarde',
  NOTURNO: 'Noite'
};

export default function GradesCurricularesPage() {
  const [grades, setGrades] = useState<GradeCurricular[]>([]);
  const [professores, setProfessores] = useState<Professor[]>([]);
  const [disciplinas, setDisciplinas] = useState<Disciplina[]>([]);
  const [turmas, setTurmas] = useState<Turma[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [showCopiarModal, setShowCopiarModal] = useState(false);
  const [editando, setEditando] = useState<GradeCurricular | null>(null);
  
  // Filtros
  const [filtroTurma, setFiltroTurma] = useState<string>('');
  const [filtroDisciplina, setFiltroDisciplina] = useState<string>('');
  const [filtroProfessor, setFiltroProfessor] = useState<string>('');
  const [mostrarInativas, setMostrarInativas] = useState(false);
  
  // Dados do formulário de copiar
  const [copiarData, setCopiarData] = useState({
    turma_origem_id: 0,
    turma_destino_id: 0,
    sobrescrever: true,
  });
  
  const [formData, setFormData] = useState({
    turma_id: 0,
    disciplina_id: 0,
    professor_id: 0,
    professor_id_2: null as number | null,
    aulas_por_semana: 2,
    ativa: true,
  });

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      const [gradesRes, professorRes, disciplinasRes, turmasRes] = await Promise.all([
        api.get('/grades-curriculares'),
        api.get('/professores'),
        api.get('/disciplinas'),
        api.get('/turmas'),
      ]);
      
      setGrades(gradesRes.data);
      setProfessores(professorRes.data.filter((p: Professor) => p.ativo));
      setDisciplinas(disciplinasRes.data.filter((d: Disciplina) => d.ativa));
      setTurmas(turmasRes.data.filter((t: Turma) => t.ativa));
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      alert('Erro ao carregar dados');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.turma_id || !formData.disciplina_id || !formData.professor_id) {
      alert('Preencha todos os campos obrigatórios');
      return;
    }
    
    try {
      if (editando) {
        await api.put(`/grades-curriculares/${editando.id}`, formData);
        alert('Grade curricular atualizada com sucesso!');
      } else {
        await api.post('/grades-curriculares', formData);
        alert('Grade curricular cadastrada com sucesso!');
      }
      
      setShowForm(false);
      setEditando(null);
      resetForm();
      carregarDados();
    } catch (error: any) {
      console.error('Erro ao salvar grade curricular:', error);
      const mensagem = error.response?.data?.detail || 'Erro ao salvar grade curricular';
      alert(mensagem);
    }
  };

  const handleEdit = (grade: GradeCurricular) => {
    setEditando(grade);
    setFormData({
      turma_id: grade.turma_id,
      disciplina_id: grade.disciplina_id,
      professor_id: grade.professor_id,
      professor_id_2: grade.professor_id_2,
      aulas_por_semana: grade.aulas_por_semana,
      ativa: grade.ativa,
    });
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Deseja realmente excluir esta grade curricular?')) return;
    
    try {
      await api.delete(`/grades-curriculares/${id}`);
      alert('Grade curricular excluída com sucesso!');
      carregarDados();
    } catch (error) {
      console.error('Erro ao excluir grade curricular:', error);
      alert('Erro ao excluir grade curricular');
    }
  };

  const toggleAtiva = async (grade: GradeCurricular) => {
    try {
      await api.put(`/grades-curriculares/${grade.id}`, {
        ...grade,
        ativa: !grade.ativa,
      });
      carregarDados();
    } catch (error) {
      console.error('Erro ao atualizar status:', error);
      alert('Erro ao atualizar status');
    }
  };

  const resetForm = () => {
    setFormData({
      turma_id: 0,
      disciplina_id: 0,
      professor_id: 0,
      professor_id_2: null,
      aulas_por_semana: 2,
      ativa: true,
    });
  };

  const copiarGrades = async () => {
    if (!copiarData.turma_origem_id || !copiarData.turma_destino_id) {
      alert('Selecione as turmas de origem e destino');
      return;
    }

    if (copiarData.turma_origem_id === copiarData.turma_destino_id) {
      alert('As turmas de origem e destino devem ser diferentes');
      return;
    }

    try {
      const response = await api.post('/grades-curriculares/copiar', copiarData);
      alert(response.data.message);
      setShowCopiarModal(false);
      setCopiarData({ turma_origem_id: 0, turma_destino_id: 0, sobrescrever: true });
      carregarDados();
    } catch (error: any) {
      console.error('Erro ao copiar grades:', error);
      const mensagem = error.response?.data?.detail || 'Erro ao copiar grades';
      alert(mensagem);
    }
  };

  // Filtrar grades
  const gradesFiltradas = grades.filter(grade => {
    if (!mostrarInativas && !grade.ativa) return false;
    
    if (filtroTurma && grade.turma_id !== parseInt(filtroTurma)) return false;
    if (filtroDisciplina && grade.disciplina_id !== parseInt(filtroDisciplina)) return false;
    if (filtroProfessor && grade.professor_id !== parseInt(filtroProfessor) && 
        grade.professor_id_2 !== parseInt(filtroProfessor)) return false;
    
    return true;
  });

  if (loading) {
    return <div className="text-center py-8">Carregando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Grade Curricular</h1>
        <div className="flex gap-2">
          <button
            onClick={() => setShowCopiarModal(true)}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center gap-2"
          >
            <FaCopy /> Copiar Grade
          </button>
          <button
            onClick={() => {
              setEditando(null);
              resetForm();
              setShowForm(true);
            }}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <FaPlus /> Nova Grade
          </button>
        </div>
      </div>

      {/* Filtros */}
      <div className="bg-white p-4 rounded-lg shadow space-y-4">
        <div className="flex items-center gap-2 text-gray-700 font-medium">
          <FaFilter /> Filtros
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Turma
            </label>
            <select
              value={filtroTurma}
              onChange={(e) => setFiltroTurma(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">Todas</option>
              {turmas.map(turma => (
                <option key={turma.id} value={turma.id}>
                  {turma.nome} - {TURNO_LABELS[turma.turno] || turma.turno}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Disciplina
            </label>
            <select
              value={filtroDisciplina}
              onChange={(e) => setFiltroDisciplina(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">Todas</option>
              {disciplinas.map(disciplina => (
                <option key={disciplina.id} value={disciplina.id}>
                  {disciplina.nome}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Professor
            </label>
            <select
              value={filtroProfessor}
              onChange={(e) => setFiltroProfessor(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">Todos</option>
              {professores.map(professor => (
                <option key={professor.id} value={professor.id}>
                  {professor.nome}
                </option>
              ))}
            </select>
          </div>
          
          <div className="flex items-end">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={mostrarInativas}
                onChange={(e) => setMostrarInativas(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-gray-700">Mostrar inativas</span>
            </label>
          </div>
        </div>
      </div>

      {/* Modal de Formulário */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
              <h2 className="text-xl font-semibold">
                {editando ? 'Editar Grade Curricular' : 'Nova Grade Curricular'}
              </h2>
              <button
                onClick={() => {
                  setShowForm(false);
                  setEditando(null);
                  resetForm();
                }}
                className="text-gray-500 hover:text-gray-700"
              >
                <FaTimes size={24} />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Turma *
                </label>
                <select
                  required
                  value={formData.turma_id}
                  onChange={(e) => setFormData({...formData, turma_id: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value={0}>Selecione...</option>
                  {turmas.map(turma => (
                    <option key={turma.id} value={turma.id}>
                      {turma.nome} - {TURNO_LABELS[turma.turno] || turma.turno} ({turma.ano_serie})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Disciplina *
                </label>
                <select
                  required
                  value={formData.disciplina_id}
                  onChange={(e) => setFormData({...formData, disciplina_id: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value={0}>Selecione...</option>
                  {disciplinas.map(disciplina => (
                    <option key={disciplina.id} value={disciplina.id}>
                      {disciplina.nome}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Professor Principal *
                </label>
                <select
                  required
                  value={formData.professor_id}
                  onChange={(e) => setFormData({...formData, professor_id: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value={0}>Selecione...</option>
                  {professores.map(professor => (
                    <option key={professor.id} value={professor.id}>
                      {professor.nome}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Professor Auxiliar (opcional)
                </label>
                <select
                  value={formData.professor_id_2 || ''}
                  onChange={(e) => setFormData({
                    ...formData, 
                    professor_id_2: e.target.value ? parseInt(e.target.value) : null
                  })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value="">Nenhum</option>
                  {professores.filter(p => p.id !== formData.professor_id).map(professor => (
                    <option key={professor.id} value={professor.id}>
                      {professor.nome}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Aulas por Semana *
                </label>
                <input
                  type="number"
                  required
                  min={1}
                  max={20}
                  value={formData.aulas_por_semana}
                  onChange={(e) => setFormData({...formData, aulas_por_semana: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                />
              </div>

              <div className="flex items-center">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.ativa}
                    onChange={(e) => setFormData({...formData, ativa: e.target.checked})}
                    className="w-4 h-4"
                  />
                  <span className="text-sm text-gray-700">Ativa</span>
                </label>
              </div>
            </div>

            <div className="flex gap-2 justify-end">
              <button
                type="button"
                onClick={() => {
                  setShowForm(false);
                  setEditando(null);
                  resetForm();
                }}
                className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
              >
                {editando ? 'Atualizar' : 'Cadastrar'}
              </button>
            </div>
          </form>
          </div>
        </div>
      )}

      {/* Modal de Copiar Grade */}
      {showCopiarModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="bg-white border-b px-6 py-4 flex justify-between items-center rounded-t-lg">
              <h2 className="text-xl font-semibold">Copiar Grade Curricular</h2>
              <button
                onClick={() => {
                  setShowCopiarModal(false);
                  setCopiarData({ turma_origem_id: 0, turma_destino_id: 0, sobrescrever: true });
                }}
                className="text-gray-500 hover:text-gray-700"
              >
                <FaTimes size={24} />
              </button>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Turma de Origem (copiar de) *
                </label>
                <select
                  value={copiarData.turma_origem_id}
                  onChange={(e) => setCopiarData({...copiarData, turma_origem_id: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value={0}>Selecione...</option>
                  {turmas.map(turma => (
                    <option key={turma.id} value={turma.id}>
                      {turma.nome} - {TURNO_LABELS[turma.turno] || turma.turno} ({turma.ano_serie})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Turma de Destino (copiar para) *
                </label>
                <select
                  value={copiarData.turma_destino_id}
                  onChange={(e) => setCopiarData({...copiarData, turma_destino_id: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value={0}>Selecione...</option>
                  {turmas.map(turma => (
                    <option 
                      key={turma.id} 
                      value={turma.id}
                      disabled={turma.id === copiarData.turma_origem_id}
                    >
                      {turma.nome} - {TURNO_LABELS[turma.turno] || turma.turno} ({turma.ano_serie})
                    </option>
                  ))}
                </select>
              </div>

              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <label className="flex items-start gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={copiarData.sobrescrever}
                    onChange={(e) => setCopiarData({...copiarData, sobrescrever: e.target.checked})}
                    className="w-4 h-4 mt-1"
                  />
                  <div className="text-sm">
                    <span className="font-medium text-gray-700">Sobrescrever grades existentes</span>
                    <p className="text-gray-600 text-xs mt-1">
                      Se marcado, remove todas as grades da turma de destino antes de copiar
                    </p>
                  </div>
                </label>
              </div>

              <div className="flex gap-2 justify-end pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowCopiarModal(false);
                    setCopiarData({ turma_origem_id: 0, turma_destino_id: 0, sobrescrever: true });
                  }}
                  className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
                >
                  Cancelar
                </button>
                <button
                  onClick={copiarGrades}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center gap-2"
                >
                  <FaCopy /> Copiar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Listagem */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Turma
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Disciplina
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Professor(es)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Aulas/Semana
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
              {gradesFiltradas.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                    Nenhuma grade curricular encontrada
                  </td>
                </tr>
              ) : (
                gradesFiltradas.map((grade) => (
                  <tr key={grade.id} className={!grade.ativa ? 'bg-gray-50 opacity-60' : ''}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {grade.turma?.nome}
                      </div>
                      <div className="text-sm text-gray-500">
                        {grade.turma?.ano_serie}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {grade.disciplina?.nome}
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900">
                        {grade.professor?.nome}
                      </div>
                      {grade.professor_2 && (
                        <div className="text-sm text-gray-500">
                          + {grade.professor_2.nome}
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
                      {grade.aulas_por_semana}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => toggleAtiva(grade)}
                        className={`px-2 py-1 text-xs rounded-full ${
                          grade.ativa
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {grade.ativa ? 'Ativa' : 'Inativa'}
                      </button>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleEdit(grade)}
                          className="text-blue-600 hover:text-blue-900"
                          title="Editar"
                        >
                          <FaEdit />
                        </button>
                        <button
                          onClick={() => handleDelete(grade.id)}
                          className="text-red-600 hover:text-red-900"
                          title="Excluir"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Resumo */}
      <div className="bg-blue-50 p-4 rounded-lg">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p className="text-xs text-gray-600 mb-1">Total de Grades</p>
            <p className="text-2xl font-bold text-blue-700">
              {gradesFiltradas.length}
            </p>
            {(filtroTurma || filtroDisciplina || filtroProfessor) && (
              <p className="text-xs text-gray-500 mt-1">(filtrado)</p>
            )}
          </div>
          
          <div>
            <p className="text-xs text-gray-600 mb-1">Total de Aulas/Semana</p>
            <p className="text-2xl font-bold text-green-700">
              {gradesFiltradas.reduce((sum, grade) => sum + grade.aulas_por_semana, 0)}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              soma de todas as aulas
            </p>
          </div>
          
          <div>
            <p className="text-xs text-gray-600 mb-1">Disciplinas Diferentes</p>
            <p className="text-2xl font-bold text-purple-700">
              {new Set(gradesFiltradas.map(g => g.disciplina_id)).size}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              disciplinas únicas
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
