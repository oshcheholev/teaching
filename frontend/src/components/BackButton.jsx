import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/BackButton.css';

function BackButton({ className = '', style = {} }) {
  const navigate = useNavigate();

  const handleGoBack = () => {
    navigate(-1);
  };

  return (
    <button 
      onClick={handleGoBack} 
      className={`back-button ${className}`}
      style={style}
    >
      ← Back
    </button>
  );
}

export default BackButton;
