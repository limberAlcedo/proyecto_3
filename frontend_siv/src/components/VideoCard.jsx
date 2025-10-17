import React from "react";

const VideoCard = ({ title, thumbnail, link }) => {
  return (
    <div className="card video-card">
      <a href={link} target="_blank" rel="noopener noreferrer">
        <img src={thumbnail} alt={title} className="video-thumb" />
      </a>
      <h3>{title}</h3>
    </div>
  );
};

export default VideoCard;
