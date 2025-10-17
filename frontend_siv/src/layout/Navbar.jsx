import { Link } from "react-router-dom";

export default function Navbar() {
  // Simulamos roles del usuario
  const userRole = "supervisor"; // puede ser "supervisor", "operador" o null si no está logueado

  return (
    <nav className="navbar">
      {/* Logo o nombre de la app */}
      <Link className="navbar-brand" to="/">SIV App</Link>

      {/* Links principales */}
      <ul className="nav-links">
        {/* Links visibles siempre */}
        <li>
          <Link className="nav-link" to="/login">Login</Link>
        </li>
        <li>
          <Link className="nav-link" to="/register">Registrar</Link>
        </li>

        {/* Links según rol */}
        {userRole === "supervisor" && (
          <>
            <li>
              <Link className="nav-link" to="/dashboard">Dashboard Supervisor</Link>
            </li>
            <li>
              <Link className="nav-link" to="/reports">Reportes</Link>
            </li>
          </>
        )}

        {userRole === "operador" && (
          <li>
            <Link className="nav-link" to="/tasks">Tareas</Link>
          </li>
        )}

        {/* Logout si hay usuario */}
        {userRole && (
          <li>
            <Link className="nav-link logout" to="/logout">Cerrar Sesión</Link>
          </li>
        )}
      </ul>
    </nav>
  );
}
