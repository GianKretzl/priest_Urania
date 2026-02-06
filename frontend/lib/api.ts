import axios from 'axios';

// Usar proxy interno do Next.js para evitar problemas de CORS e portas
const getApiUrl = () => {
  // Se estiver no browser, usa o proxy do Next.js
  if (typeof window !== 'undefined') {
    return '/api/proxy';
  }
  // Server-side: acessa o backend diretamente via rede Docker
  return 'http://backend:8000/api/v1';
};

const API_URL = getApiUrl();

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default api;

// Tipos
export interface Disciplina {
  id: number;
  nome: string;
  codigo: string;
  carga_horaria_semanal: number;
  duracao_aula: number;
  cor: string;
  ativa: boolean;
}

export interface Turma {
  id: number;
  nome: string;
  ano_serie: string;
  turno: 'MATUTINO' | 'VESPERTINO' | 'NOTURNO' | 'INTEGRAL';
  numero_alunos: number;
  ativa: boolean;
}

export interface Professor {
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
}

export interface Sede {
  id: number;
  nome: string;
  endereco?: string;
  cidade?: string;
  estado?: string;
  cep?: string;
  ativa: boolean;
}

export interface Ambiente {
  id: number;
  nome: string;
  codigo: string;
  tipo: 'SALA_AULA' | 'LABORATORIO' | 'QUADRA' | 'AUDITORIO' | 'BIBLIOTECA' | 'SALA_INFORMATICA';
  capacidade: number;
  sede_id: number;
  ativo: boolean;
}

export interface GradeCurricular {
  id: number;
  turma_id: number;
  disciplina_id: number;
  professor_id: number;
  aulas_por_semana: number;
  ativa: boolean;
}

export interface Disponibilidade {
  id: number;
  professor_id: number;
  dia_semana: 'SEGUNDA' | 'TERCA' | 'QUARTA' | 'QUINTA' | 'SEXTA' | 'SABADO';
  horario_inicio: string;
  horario_fim: string;
  disponivel: boolean;
}

export interface Horario {
  id: number;
  nome: string;
  ano_letivo: number;
  semestre: number;
  status: 'RASCUNHO' | 'EM_PROGRESSO' | 'FINALIZADO' | 'APROVADO';
  data_criacao: string;
  data_atualizacao: string;
  total_aulas: number;
  aulas_alocadas: number;
  pendencias: any[];
  qualidade_score: number;
}

export interface HorarioAula {
  id: number;
  horario_id: number;
  turma_id: number;
  disciplina_id: number;
  professor_id: number;
  ambiente_id: number;
  dia_semana: 'SEGUNDA' | 'TERCA' | 'QUARTA' | 'QUINTA' | 'SEXTA' | 'SABADO';
  horario_inicio: string;
  horario_fim: string;
  ordem: number;
}

// Serviços de API
export const disciplinaService = {
  getAll: () => api.get<Disciplina[]>('/disciplinas'),
  getById: (id: number) => api.get<Disciplina>(`/disciplinas/${id}`),
  create: (data: Omit<Disciplina, 'id'>) => api.post<Disciplina>('/disciplinas', data),
  update: (id: number, data: Partial<Disciplina>) => api.put<Disciplina>(`/disciplinas/${id}`, data),
  delete: (id: number) => api.delete(`/disciplinas/${id}`),
};

export const turmaService = {
  getAll: () => api.get<Turma[]>('/turmas'),
  getById: (id: number) => api.get<Turma>(`/turmas/${id}`),
  create: (data: Omit<Turma, 'id'>) => api.post<Turma>('/turmas', data),
  update: (id: number, data: Partial<Turma>) => api.put<Turma>(`/turmas/${id}`, data),
  delete: (id: number) => api.delete(`/turmas/${id}`),
};

export const professorService = {
  getAll: () => api.get<Professor[]>('/professores'),
  getById: (id: number) => api.get<Professor>(`/professores/${id}`),
  create: (data: Omit<Professor, 'id'>) => api.post<Professor>('/professores', data),
  update: (id: number, data: Partial<Professor>) => api.put<Professor>(`/professores/${id}`, data),
  delete: (id: number) => api.delete(`/professores/${id}`),
};

export const sedeService = {
  getAll: () => api.get<Sede[]>('/sedes'),
  getById: (id: number) => api.get<Sede>(`/sedes/${id}`),
  create: (data: Omit<Sede, 'id'>) => api.post<Sede>('/sedes', data),
  update: (id: number, data: Partial<Sede>) => api.put<Sede>(`/sedes/${id}`, data),
  delete: (id: number) => api.delete(`/sedes/${id}`),
};

export const ambienteService = {
  getAll: () => api.get<Ambiente[]>('/ambientes'),
  getBySede: (sedeId: number) => api.get<Ambiente[]>(`/ambientes/sede/${sedeId}`),
  getById: (id: number) => api.get<Ambiente>(`/ambientes/${id}`),
  create: (data: Omit<Ambiente, 'id'>) => api.post<Ambiente>('/ambientes', data),
  update: (id: number, data: Partial<Ambiente>) => api.put<Ambiente>(`/ambientes/${id}`, data),
  delete: (id: number) => api.delete(`/ambientes/${id}`),
};

export const gradeCurricularService = {
  getAll: () => api.get<GradeCurricular[]>('/grades-curriculares'),
  getByTurma: (turmaId: number) => api.get<GradeCurricular[]>(`/grades-curriculares/turma/${turmaId}`),
  getByProfessor: (professorId: number) => api.get<GradeCurricular[]>(`/grades-curriculares/professor/${professorId}`),
  getById: (id: number) => api.get<GradeCurricular>(`/grades-curriculares/${id}`),
  create: (data: Omit<GradeCurricular, 'id'>) => api.post<GradeCurricular>('/grades-curriculares', data),
  update: (id: number, data: Partial<GradeCurricular>) => api.put<GradeCurricular>(`/grades-curriculares/${id}`, data),
  delete: (id: number) => api.delete(`/grades-curriculares/${id}`),
};

export const disponibilidadeService = {
  getAll: () => api.get<Disponibilidade[]>('/disponibilidades'),
  getByProfessor: (professorId: number) => api.get<Disponibilidade[]>(`/disponibilidades/professor/${professorId}`),
  getById: (id: number) => api.get<Disponibilidade>(`/disponibilidades/${id}`),
  create: (data: Omit<Disponibilidade, 'id'>) => api.post<Disponibilidade>('/disponibilidades', data),
  update: (id: number, data: Partial<Disponibilidade>) => api.put<Disponibilidade>(`/disponibilidades/${id}`, data),
  delete: (id: number) => api.delete(`/disponibilidades/${id}`),
};

// Tipo para criação de horário (status é opcional)
export interface HorarioCreate {
  nome: string;
  ano_letivo: number;
  semestre: number;
  status?: 'RASCUNHO' | 'EM_PROGRESSO' | 'FINALIZADO' | 'APROVADO';
}

export const horarioService = {
  getAll: () => api.get<Horario[]>('/horarios'),
  getById: (id: number) => api.get<Horario>(`/horarios/${id}`),
  getAulas: (id: number) => api.get<HorarioAula[]>(`/horarios/${id}/aulas`),
  getAulasByTurma: (horarioId: number, turmaId: number) => 
    api.get<HorarioAula[]>(`/horarios/${horarioId}/turma/${turmaId}`),
  getAulasByProfessor: (horarioId: number, professorId: number) => 
    api.get<HorarioAula[]>(`/horarios/${horarioId}/professor/${professorId}`),
  create: (data: HorarioCreate) => 
    api.post<Horario>('/horarios', data),
  update: (id: number, data: Partial<Horario>) => api.put<Horario>(`/horarios/${id}`, data),
  delete: (id: number) => api.delete(`/horarios/${id}`),
  gerar: (id: number, params: any) => api.post(`/horarios/${id}/gerar`, params),
};
