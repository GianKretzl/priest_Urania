'use client';

import Link from 'next/link';
import Image from 'next/image';
import { FaCalendarAlt, FaChartLine, FaClock } from 'react-icons/fa';

export default function Home() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="flex-shrink-0">
            <Image
              src="/logo.png"
              alt="No Cry Baby Logo"
              width={200}
              height={200}
              priority
              className="w-48 h-auto"
              onError={(e) => {
                e.currentTarget.src = '/logo.svg';
              }}
            />
          </div>
          <div className="flex-1 text-center md:text-left">
            <h1 className="text-4xl font-bold text-gray-800 mb-3">
              No Cry Baby
            </h1>
            <p className="text-xl text-gray-600 mb-2">
              Sistema de Geração Automática de Horários Escolares
            </p>
            <p className="text-gray-500">
              Com otimização inteligente e respeito a todas as restrições
            </p>
          </div>
        </div>
      </div>

      {/* Cards de Acesso Rápido */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link href="/horarios" className="block">
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  Horários
                </h3>
                <p className="text-gray-600 text-sm">
                  Criar e gerenciar horários escolares
                </p>
              </div>
              <FaCalendarAlt className="text-4xl text-blue-500" />
            </div>
          </div>
        </Link>

        <Link href="/cadastros" className="block">
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  Cadastros
                </h3>
                <p className="text-gray-600 text-sm">
                  Gerenciar disciplinas, turmas e professores
                </p>
              </div>
              <FaClock className="text-4xl text-green-500" />
            </div>
          </div>
        </Link>

        <Link href="/relatorios" className="block">
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  Relatórios
                </h3>
                <p className="text-gray-600 text-sm">
                  Visualizar e exportar relatórios
                </p>
              </div>
              <FaChartLine className="text-4xl text-purple-500" />
            </div>
          </div>
        </Link>
      </div>

      {/* Recursos do Sistema */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          Recursos Principais
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-start space-x-3">
            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
            <div>
              <h4 className="font-semibold text-gray-800">Geração Automática</h4>
              <p className="text-gray-600 text-sm">
                Algoritmo inteligente que distribui aulas respeitando todas as restrições
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
            <div>
              <h4 className="font-semibold text-gray-800">Gestão de Disponibilidade</h4>
              <p className="text-gray-600 text-sm">
                Controle completo dos horários disponíveis de cada professor
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
            <div>
              <h4 className="font-semibold text-gray-800">Otimização de Janelas</h4>
              <p className="text-gray-600 text-sm">
                Minimiza horários vagos entre as aulas dos professores
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
            <div>
              <h4 className="font-semibold text-gray-800">Relatórios Completos</h4>
              <p className="text-gray-600 text-sm">
                Exportação em PDF, HTML e planilhas para alunos, professores e direção
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
