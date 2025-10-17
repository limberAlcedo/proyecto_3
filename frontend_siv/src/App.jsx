import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./layout/Navbar";
import Footer from "./layout/Footer";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { useState } from "react";
import "./styles/App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      <div className={`app-container ${!isLoggedIn ? "blurred" : ""}`}>
        <Navbar />
        <div className="content">
          <Routes>
            <Route path="/register" element={<Register />} />
          </Routes>
        </div>
        <Footer />
      </div>

      {!isLoggedIn && (
        <div className="overlay">
          <Login onLogin={() => setIsLoggedIn(true)} />
        </div>
      )}
    </Router>
  );
}

export default App;
