'use client';

export default function RelatoriosPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Relatórios e Exportações</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Tipos de Relatórios Disponíveis</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-lg mb-2">📊 Horário por Turma</h3>
            <p className="text-gray-600 text-sm mb-4">
              Grade horária completa para cada turma com todas as aulas da semana
            </p>
            <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition w-full">
              Gerar Relatório
            </button>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-lg mb-2">👨‍🏫 Horário por Professor</h3>
            <p className="text-gray-600 text-sm mb-4">
              Visualização individualizada dos horários de cada professor
            </p>
            <button className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition w-full">
              Gerar Relatório
            </button>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-lg mb-2">🏫 Ocupação de Ambientes</h3>
            <p className="text-gray-600 text-sm mb-4">
              Mapa de utilização das salas e espaços físicos
            </p>
            <button className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg transition w-full">
              Gerar Relatório
            </button>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-lg mb-2">📈 Estatísticas Gerais</h3>
            <p className="text-gray-600 text-sm mb-4">
              Análise completa com métricas e indicadores do horário
            </p>
            <button className="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded-lg transition w-full">
              Gerar Relatório
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Formatos de Exportação</h2>
        <div className="flex space-x-4">
          <div className="flex-1 text-center p-4 border border-gray-200 rounded-lg">
            <div className="text-3xl mb-2">📄</div>
            <p className="font-semibold">PDF</p>
            <p className="text-xs text-gray-600">Impressão e compartilhamento</p>
          </div>
          <div className="flex-1 text-center p-4 border border-gray-200 rounded-lg">
            <div className="text-3xl mb-2">🌐</div>
            <p className="font-semibold">HTML</p>
            <p className="text-xs text-gray-600">Publicação web</p>
          </div>
          <div className="flex-1 text-center p-4 border border-gray-200 rounded-lg">
            <div className="text-3xl mb-2">📊</div>
            <p className="font-semibold">Excel</p>
            <p className="text-xs text-gray-600">Análise de dados</p>
          </div>
        </div>
      </div>
    </div>
  );
}
