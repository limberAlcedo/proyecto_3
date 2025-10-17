import Navbar from "../layout/Navbar";
import Footer from "../layout/Footer";

const Dashboard = () => {
  return (
    <div className="app-container">
      <Navbar />
      <div className="content dashboard">
        <p>Dashboard sin datos dinámicos por ahora.</p>
        <div className="cards-container">
          {/* Aquí puedes poner tus componentes de gráficos o videos estáticos */}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Dashboard;
