'use client';

import { FaBell, FaUser } from 'react-icons/fa';

export default function Header() {
  return (
    <header className="bg-white shadow-md">
      <div className="flex items-center justify-between h-16 px-6">
        <div className="flex items-center">
          <h2 className="text-xl font-semibold text-gray-800">
            Sistema de Geração de Horários
          </h2>
        </div>

        <div className="flex items-center space-x-4">
          {/* Notificações */}
          <button className="relative p-2 text-gray-600 hover:bg-gray-100 rounded-full transition">
            <FaBell className="text-xl" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          {/* Perfil */}
          <button className="flex items-center space-x-2 p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition">
            <FaUser className="text-xl" />
            <span className="text-sm font-medium">Administrador</span>
          </button>
        </div>
      </div>
    </header>
  );
}
