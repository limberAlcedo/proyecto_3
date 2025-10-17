
// src/pages/Dashboard.jsx
import React, { useEffect, useState } from "react";
import VideoCard from "../components/VideoCard";

const Dashboard = () => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    // Aquí llamas a tu API que devuelve los videos generados por YOLO
    // Ejemplo:
    fetch("http://localhost:8021/api/videos")
      .then((res) => res.json())
      .then((data) => setVideos(data))
      .catch((err) => console.error("Error cargando videos:", err));
  }, []);

  return (
    <div className="dashboard">
      <h2>Dashboard de Videos</h2>
      <div className="cards-container">
        {videos.length === 0 && <p>No hay videos aún. Entrena YOLO para generar contenido.</p>}
        {videos.map((video, index) => (
          <VideoCard
            key={index}
            title={video.title}
            thumbnail={video.thumbnail}
            link={video.link}
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
