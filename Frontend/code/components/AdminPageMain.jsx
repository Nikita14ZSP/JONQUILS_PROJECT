import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const AdminPageMain = () => {
  const navigate = useNavigate();
  const [predictionResponse, setPredictionResponse] = useState(null);
  const [hoveredButton, setHoveredButton] = useState(null); // Состояние для отслеживания наведения на конкретную кнопку

  const handleMechanicsClick = () => {
    navigate("/admin-page-mechanics");
  };

  const handleDriversClick = () => {
    navigate("/admin-page-drivers");
  };

  const handleCarsClick = () => {
    navigate("/admin-page-cars");
  };

  const handleFixesClick = () => {
    navigate("/admin-page-fixes");
  };

  const handleRidesClick = () => {
    navigate("/admin-page-rides");
  };

  const handlePredictionClick = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8002/ml/predict", {
        method: "GET",
        timeout: 30000,
        headers: {
          Accept: "application/json",
        },
      });

      setPredictionResponse(response.status);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      setPredictionResponse("Error");
    }
  };

  // Функция для обработки наведения на кнопку
  const handleMouseEnter = (buttonId) => {
    setHoveredButton(buttonId);
  };

  const handleMouseLeave = () => {
    setHoveredButton(null);
  };

  // Стиль для кнопки с учетом состояния наведения
  const buttonStyle = (buttonId) => ({
    padding: "12px 25px",
    fontSize: "16px",
    backgroundColor: hoveredButton === buttonId ? "#28A745" : "#FF7F50", // Зеленый при наведении на конкретную кнопку
    color: "white",
    border: "2px solid #FF7F50", // Персиковая рамка
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background-color 0.3s, transform 0.2s, border-color 0.3s",
  });

  return (
    <div style={styles.container}>
      <div style={styles.buttonsWrapper}>
        <h1 style={styles.header}>Добро пожаловать!</h1>
        <div style={styles.buttonsContainer}>
          <button
            onClick={handleMechanicsClick}
            style={buttonStyle("mechanics")}
            onMouseEnter={() => handleMouseEnter("mechanics")}
            onMouseLeave={handleMouseLeave}
          >
            Перейти на страницу управления механиками
          </button>
          <button
            onClick={handleDriversClick}
            style={buttonStyle("drivers")}
            onMouseEnter={() => handleMouseEnter("drivers")}
            onMouseLeave={handleMouseLeave}
          >
            Перейти на страницу управления водителями
          </button>
          <button
            onClick={handleCarsClick}
            style={buttonStyle("cars")}
            onMouseEnter={() => handleMouseEnter("cars")}
            onMouseLeave={handleMouseLeave}
          >
            Перейти на страницу управления машинами
          </button>
          <button
            onClick={handleFixesClick}
            style={buttonStyle("fixes")}
            onMouseEnter={() => handleMouseEnter("fixes")}
            onMouseLeave={handleMouseLeave}
          >
            Перейти на страницу управления починками
          </button>
          <button
            onClick={handleRidesClick}
            style={buttonStyle("rides")}
            onMouseEnter={() => handleMouseEnter("rides")}
            onMouseLeave={handleMouseLeave}
          >
            Перейти на страницу управления поездками
          </button>
        </div>
      </div>
      <button
        onClick={handlePredictionClick}
        style={styles.buttonGray}
      >
        Выполнить запрос к /ml/predict
      </button>
      {predictionResponse && (
        <div style={styles.predictionResponse}>
          Результат запроса: {predictionResponse}
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    background: "linear-gradient(135deg, #FFA500, #FF7F50)", // Оранжевый градиент
    fontFamily: "'Roboto', sans-serif",
  },
  buttonsWrapper: {
    backgroundColor: "#F5DEB3", // Бежевое полотно для кнопок
    padding: "30px", // Добавим отступы внутри полотна
    borderRadius: "10px", // Закругленные углы для полотна
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "20px",
  },
  header: {
    fontSize: "2.5rem",
    color: "#333",
    marginBottom: "30px",
  },
  buttonsContainer: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  buttonGray: {
    padding: "12px 25px",
    fontSize: "16px",
    backgroundColor: "#6C757D",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background-color 0.3s, transform 0.2s",
  },
  predictionResponse: {
    marginTop: "20px",
    fontSize: "18px",
    color: "#555",
    fontWeight: "bold",
  },
};

export default AdminPageMain;





