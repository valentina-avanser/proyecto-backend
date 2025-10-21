import React, { useState } from 'react';
import { UserCheck, UserX, Search, Shield, User } from 'lucide-react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './estilos/UserList.css';
import Navbar from './Components/Navbar';


const initialUsers = [
  { id: 1, name: 'Juan Pérez', role: 'Administrador', active: true },
  { id: 2, name: 'Ana López', role: 'Usuario', active: true },
  { id: 3, name: 'Carlos Díaz', role: 'Usuario', active: false },
];

function UserList() {
  // Estados
  const [users, setUsers] = useState(initialUsers);
  const [showConfirm, setShowConfirm] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');


  const handleToggleClick = (user) => {
    if (user.active) {
      setSelectedUser(user);
      setShowConfirm(true);
    } else {
      toggleUserStatus(user.id);
    }
  };

  
  const toggleUserStatus = (userId) => {
    setUsers((prevUsers) =>
      prevUsers.map((user) =>
        user.id === userId ? { ...user, active: !user.active } : user
      )
    );
    setShowConfirm(false);
  };

  // Filtra usuarios según el término de búsqueda
  const filteredUsers = users.filter((user) =>
    user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.role.toLowerCase().includes(searchTerm.toLowerCase())
  );

 
  const totalUsers = users.length;
  const activeUsers = users.filter((u) => u.active).length;
  const inactiveUsers = users.filter((u) => !u.active).length;


  return (
    
    <div className="min-vh-100 bg-dark px-5" style={{ marginLeft: '20px' }}>

      <Navbar />
      
      {/* ========== HEADER ========== */}
      <div className="bg-gradient-primary py-4 " style={{marginLeft:'20px',}}>
        <div className="container">
          <h1 className="display-4 fw-bold text-white mb-2">Gestión de Usuarios</h1>
          <p className="text-white-50 mb-0">Administra y controla el acceso de tu equipo</p>
      
        </div>

        {/* ========== BARRA DE BÚSQUEDA ========== */}
        <div className="container mt-4 px-5">
          <div className="position-relative">
            <Search 
              className="position-absolute text-secondary" 
              style={{ left: '15px', top: '50%', transform: 'translateY(-50%)', width: '20px', height: '20px' }}
            />
            <input
              type="text"
              placeholder="Buscar por nombre o rol..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="form-control form-control-lg ps-5 bg-dark text-white border-secondary"
              style={{ borderRadius: '12px' }}
            />
          </div>
        </div>
      </div>

      {/* ========== CONTENEDOR PRINCIPAL ========== */}
      <div className="container py-4 px-5">
        
        {/* ========== TARJETAS DE ESTADÍSTICAS ========== */}
        <div className="row g-4 mb-4">
          
          {/* Tarjeta: Total Usuarios */}
          <div className="col-12 col-md-4">
            <div className="card bg-primary text-white shadow-lg border-0" style={{ borderRadius: '12px' }}>
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <p className="text-white-50 small mb-1">Total Usuarios</p>
                    <h2 className="display-5 fw-bold mb-0">{totalUsers}</h2>
                  </div>
                  <User size={48} className="text-white opacity-75" />
                </div>
              </div>
            </div>
          </div>

          {/* Tarjeta: Usuarios Activos */}
          <div className="col-12 col-md-4">
            <div className="card bg-success text-white shadow-lg border-0" style={{ borderRadius: '12px' }}>
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <p className="text-white-50 small mb-1">Usuarios Activos</p>
                    <h2 className="display-5 fw-bold mb-0">{activeUsers}</h2>
                  </div>
                  <UserCheck size={48} className="text-white opacity-75" />
                </div>
              </div>
            </div>
          </div>

          {/* Tarjeta: Usuarios Inactivos */}
          <div className="col-12 col-md-4">
            <div className="card bg-danger text-white shadow-lg border-0" style={{ borderRadius: '12px' }}>
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <p className="text-white-50 small mb-1">Usuarios Inactivos</p>
                    <h2 className="display-5 fw-bold mb-0">{inactiveUsers}</h2>
                  </div>
                  <UserX size={48} className="text-white opacity-75" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* ========== TABLA DE USUARIOS ========== */}
        {filteredUsers.length === 0 ? (
          
          // Estado vacío
          <div className="card bg-dark border-0 shadow-lg text-center " style={{ borderRadius: '12px' }}>
            <div className="card-body">
              <User size={64} className="text-secondary mb-3 mx-auto" />
              <p className="text-secondary fs-5 mb-0">
                {searchTerm ? 'No se encontraron usuarios' : 'No hay usuarios registrados'}
              </p>
            </div>
          </div>
        ) : (
          
          // Tabla con usuarios
          <div className="card bg-dark border-0 shadow-lg " style={{ borderRadius: '12px' }}>
            <div className="table-responsive">
              <table className="table table-dark table-hover mb-0">
                
                {/* Encabezado de la tabla */}
                <thead className="table-secondary">
                  <tr>
                    <th className="py-3 px-4 text-uppercase small fw-semibold">Nombre</th>
                    <th className="py-3 px-4 text-uppercase small fw-semibold">Rol</th>
                    <th className="py-3 px-4 text-uppercase small fw-semibold">Estado</th>
                    <th className="py-3 px-4 text-uppercase small fw-semibold text-end">Acción</th>
                  </tr>
                </thead>

                {/* Cuerpo de la tabla */}
                <tbody>
                  {filteredUsers.map((user) => (
                    <tr key={user.id} style={{ transition: 'background-color 0.2s' }}>
                      
                      {/* Columna: Nombre */}
                      <td className="py-3 px-4 align-middle">
                        <div className="d-flex align-items-center">
                          <div 
                            className="rounded-circle bg-gradient-primary d-flex align-items-center justify-content-center me-3 text-white fw-semibold"
                            style={{ width: '40px', height: '40px' }}
                          >
                            {user.name.charAt(0)}
                          </div>
                          <span className="text-white fw-medium">{user.name}</span>
                        </div>
                      </td>

                      {/* Columna: Rol */}
                      <td className="py-3 px-4 align-middle">
                        <div className="d-flex align-items-center">
                          {user.role === 'Administrador' ? (
                            <Shield size={16} className="text-warning me-2" />
                          ) : (
                            <User size={16} className="text-info me-2" />
                          )}
                          <span className="text-white-50">{user.role}</span>
                        </div>
                      </td>

                      {/* Columna: Estado */}
                      <td className="py-3 px-4 align-middle">
                        <span
                          className={`badge ${user.active ? 'bg-success' : 'bg-danger'} d-inline-flex align-items-center`}
                          style={{ padding: '6px 12px' }}
                        >
                          {user.active ? (
                            <UserCheck size={14} className="me-1" />
                          ) : (
                            <UserX size={14} className="me-1" />
                          )}
                          {user.active ? 'Activo' : 'Inactivo'}
                        </span>
                      </td>

                      {/* Columna: Acción */}
                      <td className="py-3 px-4 align-middle text-end">
                        <button
                          onClick={() => handleToggleClick(user)}
                          className={`btn ${user.active ? 'btn-danger' : 'btn-success'} btn-sm fw-semibold px-4`}
                          style={{ 
                            borderRadius: '8px',
                            transition: 'all 0.2s',
                            boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
                          }}
                        >
                          {user.active ? 'Desactivar' : 'Activar'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* ========== MODAL DE CONFIRMACIÓN ========== */}
      {showConfirm && (
        <>
          {/* Backdrop */}
          <div 
            className="modal-backdrop fade show" 
            style={{ backgroundColor: 'rgba(0,0,0,0.75)' }}
            onClick={() => setShowConfirm(false)}
          />
          
          {/* Modal */}
          <div className="modal fade show d-block" tabIndex="-1">
            <div className="modal-dialog modal-dialog-centered">
              <div className="modal-content bg-dark border-0 shadow-lg" style={{ borderRadius: '16px' }}>
                
                {/* Header del modal */}
                <div className="modal-header bg-danger border-0">
                  <h5 className="modal-title text-white fw-bold">Confirmar desactivación</h5>
                </div>

                {/* Contenido del modal */}
                <div className="modal-body p-4">
                  <div className="d-flex align-items-start mb-3">
                    <div 
                      className="rounded-circle bg-danger bg-opacity-25 d-flex align-items-center justify-content-center me-3 flex-shrink-0"
                      style={{ width: '48px', height: '48px' }}
                    >
                      <UserX size={24} className="text-danger" />
                    </div>
                    <div>
                      <p className="text-white-50 small mb-1">
                        ¿Estás seguro que deseas desactivar a:
                      </p>
                      <p className="text-white fw-bold fs-5 mb-0">{selectedUser?.name}</p>
                    </div>
                  </div>
                  <p className="text-secondary small mb-0">
                    El usuario perderá acceso al sistema hasta que sea reactivado.
                  </p>
                </div>

                {/* Footer del modal con botones */}
                <div className="modal-footer bg-dark bg-opacity-50 border-0">
                  <button
                    onClick={() => setShowConfirm(false)}
                    className="btn btn-secondary px-4"
                    style={{ borderRadius: '8px' }}
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={() => toggleUserStatus(selectedUser.id)}
                    className="btn btn-danger px-4 fw-semibold"
                    style={{ 
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px rgba(220,53,69,0.3)'
                    }}
                  >
                    Confirmar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default UserList;