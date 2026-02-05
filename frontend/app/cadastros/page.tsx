'use client';

export default function CadastrosPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Central de Cadastros</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          { nome: 'Disciplinas', desc: 'Gerenciar matérias e cargas horárias', link: '/cadastros/disciplinas' },
          { nome: 'Turmas', desc: 'Gerenciar turmas e séries', link: '/cadastros/turmas' },
          { nome: 'Professores', desc: 'Gerenciar corpo docente', link: '/cadastros/professores' },
          { nome: 'Sedes', desc: 'Gerenciar unidades escolares', link: '/cadastros/sedes' },
          { nome: 'Ambientes', desc: 'Gerenciar salas e espaços', link: '/cadastros/ambientes' },
          { nome: 'Grade Curricular', desc: 'Associar disciplinas e professores', link: '/cadastros/grades' },
          { nome: 'Disponibilidade', desc: 'Configurar horários dos professores', link: '/cadastros/disponibilidades' },
        ].map((item) => (
          <a
            key={item.nome}
            href={item.link}
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
          >
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{item.nome}</h3>
            <p className="text-gray-600 text-sm">{item.desc}</p>
          </a>
        ))}
      </div>
    </div>
  );
}
