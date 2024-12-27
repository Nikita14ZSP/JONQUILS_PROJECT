import React, { useState, useEffect } from "react";
import axios from "axios";
import "./AdminPageCars.css";

const AdminPageCars = () => {
  const [cars, setCars] = useState([]);
  const [selectedCar, setSelectedCar] = useState(null);
  const [message, setMessage] = useState("");
  const [carIdInput, setCarIdInput] = useState("");
  const [newCar, setNewCar] = useState({
    car_number: "",
    is_rented: false,
    model: "",
    car_type: "",
    fuel_type: "",
    car_rating: 0,
    year_to_start: 0,
    year_to_work: 0,
    rides: 0
  });
  const [updatedCar, setUpdatedCar] = useState({
    car_number: "",
    is_rented: false,
    model: "",
    car_type: "",
    fuel_type: "",
    car_rating: 0,
    year_to_start: 0,
    year_to_work: 0,
    rides: 0
  });

  const baseURL = "http://127.0.0.1:8000";

  // Загрузка всех машин
  const fetchAllCars = async () => {
    try {
      const response = await axios.get(`${baseURL}/cars/get_all`, { timeout: 5000 });
      setCars(response.data);
      setMessage("Список машин успешно загружен.");
    } catch (error) {
      setMessage("Ошибка загрузки машин.");
    }
  };

    // Загрузка данных машины по ID
    const fetchCarById = async (carId) => {
      try {
        const response = await axios.get(`${baseURL}/cars/get_by_id/${carId}`,  { timeout: 5000 });
        setSelectedCar(response.data);
        setMessage(`Машина с ID ${carId} успешно загружена.`);
      } catch (error) {
        setMessage("Ошибка загрузки машины.");
      }
    };
  
    // Обработчик нажатия на кнопку загрузки машины по ID
    const handleFetchCarById = () => {
      if (carIdInput.trim() === "") {
        setMessage("Введите корректный ID машины.");
        return;
      }
      fetchCarById(carIdInput);
    };

  // Добавление новой машины
  const addCar = async () => {
    try {
      await axios.post(`${baseURL}/cars/add`, newCar, {
        headers: {
          "Content-Type": "application/json"
        }
      },  { timeout: 5000 });
      setMessage("Машина успешно добавлена.");
      fetchAllCars(); // Обновить список машин
    } catch (error) {
      setMessage("Ошибка добавления машины.");
    }
  };

  // Обновление данных машины
  const updateCar = async (carId) => {
    try {
      await axios.put(`${baseURL}/cars/update/${carId}`, updatedCar, {
        headers: {
          "Content-Type": "application/json"
        }, 
      },  { timeout: 5000 });
      setMessage(`Машина с ID ${carId} успешно обновлена.`);
      fetchAllCars(); // Обновить список машин
    } catch (error) {
      setMessage("Ошибка обновления данных машины.");
    }
  };

  // Удаление машины
  const deleteCar = async (carId) => {
    try {
      await axios.delete(`${baseURL}/cars/delete/${carId}`, { timeout: 5000 });
      setMessage(`Машина с ID ${carId} успешно удалена.`);
      fetchAllCars(); // Обновить список машин
    } catch (error) {
      setMessage("Ошибка удаления машины.");
    }
  };

  useEffect(() => {
    fetchAllCars(); // Загружаем все машины при первом рендере
  }, []);

  const handleNewCarChange = (event) => {
    const { name, value } = event.target;
    setNewCar((prev) => ({ ...prev, [name]: value }));
  };

  const handleUpdatedCarChange = (event) => {
    const { name, value } = event.target;
    setUpdatedCar((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="admin-page">
      <header>
        <h1>Административная панель - Управление машинами</h1>
        <p>Здесь вы можете добавлять, обновлять, просматривать и удалять машины.</p>
      </header>

      <div className="actions">
        <button onClick={fetchAllCars} className="btn btn-primary">
          Загрузить все машины
        </button>

        {/* Новая кнопка для загрузки машины по ID */}
        <input
          type="text"
          placeholder="Введите ID машины"
          value={carIdInput}
          onChange={(e) => setCarIdInput(e.target.value)}
          className="input-id"
        />
        <button onClick={handleFetchCarById} className="btn btn-secondary">
          Загрузить машину по ID
        </button>
      </div>

      {message && <p className="message">{message}</p>}
      <div className="new-car-form">
        <h2>Добавить новую машину</h2>
        <div>
          <label>Номер машины</label>
          <input
            type="text"
            name="car_number"
            placeholder="Введите номер машины"
            value={newCar.car_number}
            onChange={handleNewCarChange}
          />
        </div>
        <div>
          <label>Модель</label>
          <input
            type="text"
            name="model"
            placeholder="Введите модель машины"
            value={newCar.model}
            onChange={handleNewCarChange}
          />
        </div>
        <div>
          <label>Тип машины</label>
          <input
            type="text"
            name="car_type"
            placeholder="Введите тип машины"
            value={newCar.car_type}
            onChange={handleNewCarChange}
          />
        </div>
        <div>
          <label>Тип топлива</label>
          <input
            type="text"
            name="fuel_type"
            placeholder="Введите тип топлива"
            value={newCar.fuel_type}
            onChange={handleNewCarChange}
          />
        </div>
        <div>
          <label>Рейтинг машины</label>
          <input
            type="number"
            name="car_rating"
            placeholder="Введите рейтинг машины"
            value={newCar.car_rating}
            onChange={handleNewCarChange}
          />
        </div>
        <div>
          <label>Год начала эксплуатации</label>
          <input
            type="number"
            name="year_to_start"
            placeholder="Введите год начала эксплуатации"
            value={newCar.year_to_start}
            onChange={handleNewCarChange}
          />
        </div>
        <div>
          <label>Год окончания эксплуатации</label>
          <input
            type="number"
            name="year_to_work"
            placeholder="Введите год окончания эксплуатации"
            value={newCar.year_to_work}
            onChange={handleNewCarChange}
          />
        </div>
        <div>
          <label>Количество поездок</label>
          <input
            type="number"
            name="rides"
            placeholder="Введите количество поездок"
            value={newCar.rides}
            onChange={handleNewCarChange}
          />
        </div>
        <button onClick={addCar} className="btn btn-success">
          Добавить машину
        </button>
      </div>

      <div className="cars-list">
        <h2>Список машин</h2>
        <ul>
          {cars.map((car) => (
            <li key={car.car_id}>
              <strong>{car.model} ({car.car_number})</strong> - Рейтинг: {car.car_rating}
              <button onClick={() => fetchCarById(car.car_id)}>Посмотреть</button>
              <button onClick={() => deleteCar(car.car_id)}>Удалить</button>
            </li>
          ))}
        </ul>
      </div>

      {selectedCar && (
        <div className="car-details">
          <h2>Детали машины</h2>
          <p><strong>ID:</strong> {selectedCar.car_id}</p>
          <p><strong>Номер машины:</strong> {selectedCar.car_number}</p>
          <p><strong>Модель:</strong> {selectedCar.model}</p>
          <p><strong>Тип машины:</strong> {selectedCar.car_type}</p>
          <p><strong>Тип топлива:</strong> {selectedCar.fuel_type}</p>
          <p><strong>Рейтинг:</strong> {selectedCar.car_rating}</p>
          <p><strong>Год начала эксплуатации:</strong> {selectedCar.year_to_start}</p>
          <p><strong>Год окончания эксплуатации:</strong> {selectedCar.year_to_work}</p>
          <p><strong>Количество поездок:</strong> {selectedCar.rides}</p>

          <h3>Обновить данные машины</h3>
          <div>
            <label>Номер машины</label>
            <input
              type="text"
              name="car_number"
              placeholder="Введите номер машины"
              value={updatedCar.car_number}
              onChange={handleUpdatedCarChange}
            />
          </div>
          <div>
            <label>Модель</label>
            <input
              type="text"
              name="model"
              placeholder="Введите модель машины"
              value={updatedCar.model}
              onChange={handleUpdatedCarChange}
            />
          </div>
          <div>
            <label>Тип машины</label>
            <input
              type="text"
              name="car_type"
              placeholder="Введите тип машины"
              value={updatedCar.car_type}
              onChange={handleUpdatedCarChange}
            />
          </div>
          <div>
            <label>Тип топлива</label>
            <input
              type="text"
              name="fuel_type"
              placeholder="Введите тип топлива"
              value={updatedCar.fuel_type}
              onChange={handleUpdatedCarChange}
            />
          </div>
          <div>
            <label>Рейтинг машины</label>
            <input
              type="number"
              name="car_rating"
              placeholder="Введите рейтинг машины"
              value={updatedCar.car_rating}
              onChange={handleUpdatedCarChange}
            />
          </div>
          <div>
            <label>Год начала эксплуатации</label>
            <input
              type="number"
              name="year_to_start"
              placeholder="Введите год начала эксплуатации"
              value={updatedCar.year_to_start}
              onChange={handleUpdatedCarChange}
            />
          </div>
          <div>
            <label>Год окончания эксплуатации</label>
            <input
              type="number"
              name="year_to_work"
              placeholder="Введите год окончания эксплуатации"
              value={updatedCar.year_to_work}
              onChange={handleUpdatedCarChange}
            />
          </div>
          <div>
            <label>Количество поездок</label>
            <input
              type="number"
              name="rides"
              placeholder="Введите количество поездок"
              value={updatedCar.rides}
              onChange={handleUpdatedCarChange}
            />
          </div>
          <button onClick={() => updateCar(selectedCar.car_id)} className="btn btn-warning">
            Обновить машину
          </button>
        </div>
      )}
    </div>
  );
};

export default AdminPageCars;