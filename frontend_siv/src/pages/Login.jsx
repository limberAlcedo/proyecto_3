import React, { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

const Login = ({ switchView }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error de login");
      setMessage(data.message);
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div className="card p-4 mx-auto shadow rounded" style={{ maxWidth: "400px", backgroundColor: "#f8f9fa" }}>
      <h3 className="text-center mb-3">Login</h3>
      {message && <div className="alert alert-info">{message}</div>}
      <form onSubmit={handleLogin}>
        <div className="mb-3">
          <label>Email</label>
          <input type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="mb-3">
          <label>Contraseña</label>
          <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button className="btn btn-primary w-100" type="submit">Ingresar</button>
      </form>
      <p className="text-center mt-3">
        ¿No tienes cuenta? <button className="btn btn-link p-0" onClick={switchView}>Regístrate</button>
      </p>
    </div>
  );
};

export default Login;
