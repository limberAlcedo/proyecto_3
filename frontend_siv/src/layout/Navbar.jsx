import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="nav-logo">SIV</Link>
        <div className="nav-links">
          <Link className="nav-link" to="/">Login</Link>
          <Link className="nav-link" to="/register">Registro</Link>
          <Link className="nav-link" to="/dashboard">Dashboard</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
