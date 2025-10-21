import React, { useState } from 'react';
import {
  Home,
  TrendingUp,
  Bell,
  Users,
  Settings,
  HelpCircle,
  ChevronDown,
  Trash2,
  Archive,
  Shield
} from 'lucide-react';
import 'bootstrap/dist/css/bootstrap.min.css';

// ============================================
// OPCIONES DE NAVEGACIÓN
// ============================================
const navigationItems = [
  {
    id: 'inicio',
    label: 'Inicio',
    icon: Home,
    path: '/',
    badge: null
  },
  {
    id: 'rendimiento',
    label: 'Rendimiento',
    icon: TrendingUp,
    path: '/rendimiento',
    badge: null
  },
  {
    id: 'notificaciones',
    label: 'Notificaciones',
    icon: Bell,
    path: '/notificaciones',
    badge: '5'
  },
  {
    id: 'usuarios',
    label: 'Administración de Usuarios',
    icon: Users,
    path: '/usuarios',
    badge: null
  }
];

// ============================================
// COMPONENTE SIDEBAR
// ============================================
function Sidebar({ activeRoute = 'inicio' }) {
  const [expanded, setExpanded] = useState(false);
  const [activeNav, setActiveNav] = useState(activeRoute);
  const [hoveredNav, setHoveredNav] = useState(null);
  const [showUserMenu, setShowUserMenu] = useState(false);

  /**
   * Maneja la navegación
   */
  const handleNavigation = (item) => {
    setActiveNav(item.id);
    console.log('Navegando a:', item.path);
    // Para React Router: 
    // const navigate = useNavigate();
    // navigate(item.path);
  };

  return (
    <div 
      className="d-flex flex-column bg-dark text-white"
      onMouseEnter={() => setExpanded(true)}
      onMouseLeave={() => {
        setExpanded(false);
        setShowUserMenu(false);
      }}
      style={{
        width: expanded ? '280px' : '70px',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        alignItems: 'center',
        transition: 'width 0.3s cubic-bezier(0.5, 0, 0.5, 1)',
        overflow: 'hidden',
        borderRight: '1px solid rgba(255,255,255,0.1)',
        zIndex: 1050,
        boxShadow: expanded ? '4px 0 20px rgba(0,0,0,0.3)' : 'none'
      }}
    >
      {/* ========== HEADER - LOGO AVANSER ========== */}
      <div 
        className="p-3 border-bottom d-flex align-items-center justify-content-center" 
        style={{ 
          borderColor: 'rgba(255,255,255,0.1)',
          minHeight: '70px'
        }}
      >
        {expanded ? (
          <div className="d-flex align-items-center w-100 px-2">
            <div 
              className="rounded-circle d-flex align-items-center justify-content-center me-3 flex-shrink-0"
              style={{ 
                width: '40px', 
                height: '40px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
              }}
            >
              <Shield size={22} className="text-white" />
            </div>
            <div>
              <h4 className="mb-0 fw-bold" style={{ fontSize: '22px', letterSpacing: '-0.5px' }}>
                Avanser
              </h4>
              <p className="mb-0 small" style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px' }}>
                Sistema de Gestión
              </p>
            </div>
          </div>
        ) : (
          <div 
            className="rounded-circle d-flex align-items-center justify-content-center"
            style={{ 
              width: '40px', 
              height: '40px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            }}
          >
            <Shield size={22} className="text-white" />
          </div>
        )}
      </div>

      {/* ========== NAVEGACIÓN PRINCIPAL ========== */}
      <div 
        className="flex-grow-1 overflow-auto py-3"
        style={{
          scrollbarWidth: 'thin',
          scrollbarColor: 'rgba(255,255,255,0.2) transparent'
        }}
      >
        <div className={expanded ? 'px-2' : 'px-1'}>
          {/* Etiqueta de sección (solo cuando está expandido) */}
          {expanded && (
            <div 
              className="px-3 py-2 text-uppercase small fw-semibold"
              style={{ 
                color: 'rgba(255,255,255,0.4)',
                fontSize: '11px',
                letterSpacing: '0.5px'
              }}
            >
              Navegación
            </div>
          )}

          {/* Items de navegación */}
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeNav === item.id;
            const isHovered = hoveredNav === item.id;

            return (
              <div
                key={item.id}
                className="position-relative"
                onMouseEnter={() => setHoveredNav(item.id)}
                onMouseLeave={() => setHoveredNav(null)}
              >
                <button
                  onClick={() => handleNavigation(item)}
                  className={`btn w-100 border-0 mb-1 ${
                    isActive ? 'bg-light bg-opacity-10' : ''
                  }`}
                  style={{
                    padding: expanded ? '12px 16px' : '12px 0',
                    borderRadius: '8px',
                    transition: 'all 0.2s',
                    backgroundColor: isActive 
                      ? 'rgba(255,255,255,0.1)' 
                      : isHovered 
                        ? 'rgba(255,255,255,0.05)' 
                        : 'transparent',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: expanded ? 'space-between' : 'center'
                  }}
                >
                  <div className="d-flex align-items-center flex-grow-1 overflow-hidden">
                    <Icon 
                      size={22} 
                      className={expanded ? 'me-3 flex-shrink-0' : ''}
                      style={{ 
                        color: isActive ? '#ffffff' : 'rgba(255,255,255,0.7)'
                      }}
                    />
                    {expanded && (
                      <span 
                        className="text-truncate text-start"
                        style={{ 
                          fontSize: '14px',
                          color: isActive ? '#ffffff' : 'rgba(255,255,255,0.8)',
                          fontWeight: isActive ? '600' : '400'
                        }}
                      >
                        {item.label}
                      </span>
                    )}
                  </div>

                  {/* Badge de notificaciones */}
                  {expanded && item.badge && (
                    <span 
                      className="badge rounded-pill flex-shrink-0"
                      style={{
                        backgroundColor: '#dc3545',
                        fontSize: '11px',
                        padding: '4px 8px',
                        fontWeight: '600'
                      }}
                    >
                      {item.badge}
                    </span>
                  )}

                  {/* Badge como punto cuando está colapsado */}
                  {!expanded && item.badge && (
                    <span 
                      className="position-absolute rounded-circle"
                      style={{
                        width: '8px',
                        height: '8px',
                        backgroundColor: '#dc3545',
                        top: '8px',
                        right: '16px',
                        border: '2px solid #212529'
                      }}
                    />
                  )}
                </button>

                {/* Tooltip cuando está colapsado */}
                {!expanded && isHovered && (
                  <div
                    className="position-fixed bg-dark text-white px-3 py-2 rounded shadow-lg"
                    style={{
                      left: '80px',
                      zIndex: 1100,
                      fontSize: '13px',
                      whiteSpace: 'nowrap',
                      border: '1px solid rgba(255,255,255,0.1)',
                      pointerEvents: 'none'
                    }}
                  >
                    {item.label}
                    {item.badge && (
                      <span 
                        className="badge bg-danger rounded-pill ms-2"
                        style={{ fontSize: '11px' }}
                      >
                        {item.badge}
                      </span>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Separador */}
        <div 
          className="my-3"
          style={{ 
            height: '1px',
            backgroundColor: 'rgba(255,255,255,0.1)',
            marginLeft: expanded ? '16px' : '12px',
            marginRight: expanded ? '16px' : '12px'
          }}
        />

        {/* Sección Sistema */}
        <div className={expanded ? 'px-2' : 'px-1'}>
          {expanded && (
            <div 
              className="px-3 py-2 text-uppercase small fw-semibold"
              style={{ 
                color: 'rgba(255,255,255,0.4)',
                fontSize: '11px',
                letterSpacing: '0.5px'
              }}
            >
              Sistema
            </div>
          )}
          
          {/* Botón Configuración */}
          <button
            className="btn w-100 border-0 mb-1"
            style={{
              padding: expanded ? '12px 16px' : '12px 0',
              borderRadius: '8px',
              transition: 'background-color 0.2s',
              display: 'flex',
              alignItems: 'center',
              justifyContent: expanded ? 'flex-start' : 'center'
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = 'rgba(255,255,255,0.05)'}
            onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
          >
            <Settings 
              size={22} 
              className={expanded ? 'me-3' : ''}
              style={{ color: 'rgba(255,255,255,0.7)' }}
            />
            {expanded && (
              <span style={{ fontSize: '14px', color: 'rgba(255,255,255,0.8)' }}>
                Configuración
              </span>
            )}
          </button>

          {/* Botón Ayuda */}
          <button
            className="btn w-100 border-0 mb-1"
            style={{
              padding: expanded ? '12px 16px' : '12px 0',
              borderRadius: '8px',
              transition: 'background-color 0.2s',
              display: 'flex',
              alignItems: 'center',
              justifyContent: expanded ? 'flex-start' : 'center'
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = 'rgba(255,255,255,0.05)'}
            onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
          >
            <HelpCircle 
              size={22} 
              className={expanded ? 'me-3' : ''}
              style={{ color: 'rgba(255,255,255,0.7)' }}
            />
            {expanded && (
              <span style={{ fontSize: '14px', color: 'rgba(255,255,255,0.8)' }}>
                Ayuda y Soporte
              </span>
            )}
          </button>
        </div>
      </div>

      {/* ========== FOOTER - MENÚ DE USUARIO ========== */}
      <div 
        className="border-top p-2"
        style={{ borderColor: 'rgba(255,255,255,0.1)' }}
      >
        {/* Menú desplegable del usuario */}
        {expanded && showUserMenu && (
          <div 
            className="mb-2 rounded"
            style={{ 
              backgroundColor: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              padding: '4px'
            }}
          >
            <button 
              className="btn btn-sm w-100 text-white text-start d-flex align-items-center border-0 py-2 px-3"
              style={{ 
                fontSize: '13px',
                borderRadius: '6px',
                transition: 'background-color 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.backgroundColor = 'rgba(255,255,255,0.05)'}
              onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
            >
              <Settings size={16} className="me-2" style={{ color: 'rgba(255,255,255,0.6)' }} />
              Mi Perfil
            </button>
            <button 
              className="btn btn-sm w-100 text-white text-start d-flex align-items-center border-0 py-2 px-3"
              style={{ 
                fontSize: '13px',
                borderRadius: '6px',
                transition: 'background-color 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.backgroundColor = 'rgba(255,255,255,0.05)'}
              onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
            >
              <Archive size={16} className="me-2" style={{ color: 'rgba(255,255,255,0.6)' }} />
              Preferencias
            </button>
            <div 
              className="my-1"
              style={{ 
                height: '1px',
                backgroundColor: 'rgba(255,255,255,0.1)',
                margin: '4px 8px'
              }}
            />
            <button 
              className="btn btn-sm w-100 text-danger text-start d-flex align-items-center border-0 py-2 px-3"
              style={{ 
                fontSize: '13px',
                borderRadius: '6px',
                transition: 'background-color 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.backgroundColor = 'rgba(220,53,69,0.1)'}
              onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
            >
              <Trash2 size={16} className="me-2" />
              Cerrar Sesión
            </button>
          </div>
        )}

        {/* Botón de perfil de usuario */}
        <button
          onClick={() => expanded && setShowUserMenu(!showUserMenu)}
          className="btn w-100 border-0 p-2"
          style={{
            backgroundColor: showUserMenu ? 'rgba(255,255,255,0.05)' : 'transparent',
            borderRadius: '8px',
            transition: 'background-color 0.2s',
            display: 'flex',
            alignItems: 'center',
            justifyContent: expanded ? 'space-between' : 'center'
          }}
          onMouseEnter={(e) => !showUserMenu && (e.target.style.backgroundColor = 'rgba(255,255,255,0.03)')}
          onMouseLeave={(e) => !showUserMenu && (e.target.style.backgroundColor = 'transparent')}
        >
          <div className="d-flex align-items-center overflow-hidden">
            <div 
              className="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
              style={{ 
                width: '36px', 
                height: '36px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                marginRight: expanded ? '12px' : '0'
              }}
            >
              <span className="text-white fw-semibold" style={{ fontSize: '14px' }}>AD</span>
            </div>
            {expanded && (
              <div className="overflow-hidden text-start">
                <div 
                  className="text-white small fw-medium text-truncate"
                  style={{ fontSize: '14px' }}
                >
                  Administrador
                </div>
                <div 
                  className="text-truncate"
                  style={{ 
                    fontSize: '12px',
                    color: 'rgba(255,255,255,0.5)'
                  }}
                >
                  admin@avanser.com
                </div>
              </div>
            )}
          </div>
          {expanded && (
            <ChevronDown 
              size={18} 
              style={{ 
                color: 'rgba(255,255,255,0.6)',
                transform: showUserMenu ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.2s',
                flexShrink: 0
              }}
            />
          )}
        </button>
      </div>
    </div>
  );
}

export default Sidebar;