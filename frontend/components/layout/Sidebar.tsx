'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  FaHome, 
  FaCalendarAlt, 
  FaBook, 
  FaUsers, 
  FaChalkboardTeacher,
  FaBuilding,
  FaDoorOpen,
  FaClipboardList,
  FaClock,
  FaChartBar
} from 'react-icons/fa';

const menuItems = [
  { 
    name: 'Início', 
    path: '/', 
    icon: FaHome 
  },
  { 
    name: 'Horários', 
    path: '/horarios', 
    icon: FaCalendarAlt 
  },
  {
    name: 'Cadastros',
    icon: FaClipboardList,
    submenu: [
      { name: 'Disciplinas', path: '/cadastros/disciplinas', icon: FaBook },
      { name: 'Turmas', path: '/cadastros/turmas', icon: FaUsers },
      { name: 'Professores', path: '/cadastros/professores', icon: FaChalkboardTeacher },
      { name: 'Sedes', path: '/cadastros/sedes', icon: FaBuilding },
      { name: 'Ambientes', path: '/cadastros/ambientes', icon: FaDoorOpen },
      { name: 'Grade Curricular', path: '/cadastros/grades', icon: FaClipboardList },
      { name: 'Disponibilidade', path: '/cadastros/disponibilidades', icon: FaClock },
    ]
  },
  { 
    name: 'Relatórios', 
    path: '/relatorios', 
    icon: FaChartBar 
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="bg-gray-900 text-white w-64 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition duration-200 ease-in-out">
      {/* Logo */}
      <div className="flex items-center space-x-2 px-4">
        <FaCalendarAlt className="text-3xl text-blue-500" />
        <span className="text-2xl font-extrabold">No Cry Baby</span>
      </div>

      {/* Navigation */}
      <nav>
        {menuItems.map((item) => (
          <div key={item.name}>
            {item.submenu ? (
              <div>
                <div className="flex items-center space-x-2 py-3 px-4 text-gray-300">
                  <item.icon className="text-lg" />
                  <span className="font-semibold">{item.name}</span>
                </div>
                <div className="ml-4">
                  {item.submenu.map((subitem) => (
                    <Link
                      key={subitem.path}
                      href={subitem.path}
                      className={`flex items-center space-x-2 py-2 px-4 rounded transition duration-200 ${
                        pathname === subitem.path
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                      }`}
                    >
                      <subitem.icon className="text-sm" />
                      <span className="text-sm">{subitem.name}</span>
                    </Link>
                  ))}
                </div>
              </div>
            ) : (
              <Link
                href={item.path!}
                className={`flex items-center space-x-2 py-3 px-4 rounded transition duration-200 ${
                  pathname === item.path
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <item.icon className="text-lg" />
                <span className="font-semibold">{item.name}</span>
              </Link>
            )}
          </div>
        ))}
      </nav>
    </div>
  );
}
