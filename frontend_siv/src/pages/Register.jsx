import React, { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

const Register = ({ switchView }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const res = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error al registrar");
      setMessage("Usuario registrado con éxito!");
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div className="card p-4 mx-auto shadow rounded" style={{ maxWidth: "400px", backgroundColor: "#f8f9fa" }}>
      <h3 className="text-center mb-3">Registro</h3>
      {message && <div className="alert alert-info">{message}</div>}
      <form onSubmit={handleRegister}>
        <div className="mb-3">
          <label>Nombre de usuario</label>
          <input type="text" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>
        <div className="mb-3">
          <label>Email</label>
          <input type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="mb-3">
          <label>Contraseña</label>
          <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button className="btn btn-success w-100" type="submit">Registrarse</button>
      </form>
      <p className="text-center mt-3">
        ¿Ya tienes cuenta? <button className="btn btn-link p-0" onClick={switchView}>Inicia sesión</button>
      </p>
    </div>
  );
};

export default Register;
