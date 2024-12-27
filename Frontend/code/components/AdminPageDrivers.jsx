import React, { useState } from "react";
import axios from "axios";
import "./AdminPage.css";

const AdminPageDrivers = () => {
  const [drivers, setDrivers] = useState([]);
  const [selectedDriver, setSelectedDriver] = useState(null);
  const [rides, setRides] = useState([]);
  const [message, setMessage] = useState("");
  const [updatedData, setUpdatedData] = useState({
    user_data: {
      firstname: "",
      lastname: "",
      email: "",
    },
    driver_data: {
      age: 0,
      driver_rating: 0,
      driver_rides: 0,
      driver_time_accidents: 0,
      first_ride_date: "",
    },
  });
  const [driverIdInput, setDriverIdInput] = useState(""); // For the driver ID input field

  const baseURL = "http://127.0.0.1:8000";

  // 1. Загрузить водителей
  const fetchAllDrivers = async () => {
    try {
      const response = await axios.get(`${baseURL}/drivers/get_all`, { timeout: 10000 });
      setDrivers(response.data);
      setMessage("Список водителей успешно загружен.");
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось загрузить список водителей."}`);
    }
  };
  
  const fetchDriverById = async (driverId) => {
    try {
      const response = await axios.get(`${baseURL}/drivers/get_by_id/${driverId}`, { timeout: 5000 });
      setSelectedDriver(response.data);
      setMessage(`Данные водителя с ID ${driverId} успешно загружены.`);
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось загрузить данные водителя."}`);
    }
  };
  
  const fetchDriverRides = async (driverId) => {
    try {
      const response = await axios.get(`${baseURL}/drivers/get_rides/${driverId}`, { timeout: 5000 });
      setRides(response.data);
      setMessage(`Список поездок водителя с ID ${driverId} успешно загружен.`);
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось загрузить поездки водителя."}`);
    }
  };
  
  const deleteDriver = async (driverId) => {
    try {
      await axios.delete(`${baseURL}/drivers/delete_by_id/${driverId}`, { timeout: 5000 });
      setMessage(`Водитель с ID ${driverId} успешно удалён.`);
      fetchAllDrivers();
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось удалить водителя."}`);
    }
  };
  

  // 5. Обновить данные водителя
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setUpdatedData((prevData) => {
      if (name.startsWith("user_data")) {
        return {
          ...prevData,
          user_data: {
            ...prevData.user_data,
            [name.split(".")[1]]: value,
          },
        };
      }
      return {
        ...prevData,
        driver_data: {
          ...prevData.driver_data,
          [name.split(".")[1]]: value,
        },
      };
    });
  };

  const validateData = () => {
    const { firstname, lastname, email } = updatedData.user_data;
    const { age, driver_rating, driver_rides, driver_time_accidents } = updatedData.driver_data;
    if (!firstname || !lastname || !email || age <= 0 || driver_rating < 0 || driver_rides < 0 || driver_time_accidents < 0) {
      setMessage("Пожалуйста, заполните все поля корректно.");
      return false;
    }
    return true;
  };

  const updateDriver = async (driverId) => {
    if (!validateData()) return;
  
    const requestData = {
      user_data: updatedData.user_data,
      driver_data: updatedData.driver_data,
    };
  
    try {
      await axios.put(
        `${baseURL}/drivers/update_by_id/${driverId}`,
        JSON.stringify(requestData),
        {
          headers: {
            "Content-Type": "application/json",
          },
          timeout: 5000,
        }
      );
      setMessage(`Данные водителя с ID ${driverId} успешно обновлены.`);
      fetchAllDrivers();
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось обновить данные водителя."}`);
    }
  };

  const handleDriverIdChange = (event) => {
    setDriverIdInput(event.target.value);
  };

  const handleFetchDriverById = () => {
    if (driverIdInput) {
      fetchDriverById(driverIdInput);
    } else {
      setMessage("Пожалуйста, введите ID водителя.");
    }
  };

  return (
    <div className="admin-page">
      <header>
        <h1>Административная панель</h1>
        <p>Управление водителями</p>
      </header>

      <div className="actions">
        <button onClick={fetchAllDrivers} className="btn btn-primary">Загрузить всех водителей</button>

        {/* Container for the "Получить водителя по ID" button and input */}
        <div className="fetch-driver">
          <input
            type="number"
            placeholder="Введите ID водителя"
            value={driverIdInput}
            onChange={handleDriverIdChange}
          />
          <button onClick={handleFetchDriverById} className="btn btn-secondary">Получить водителя по ID</button>
        </div>
      </div>

      {message && <p className="message">{message}</p>}

      {drivers.length > 0 && (
        <div className="drivers-list">
          <h2>Список водителей</h2>
          <ul>
            {drivers.map((driver) => (
              <li key={driver.driver_id}>
                <strong>{driver.firstname} {driver.lastname}</strong> (ID: {driver.driver_id})
                <button onClick={() => fetchDriverById(driver.driver_id)}>Посмотреть детали</button>
                <button onClick={() => fetchDriverRides(driver.driver_id)}>Посмотреть поездки</button>
                <button onClick={() => deleteDriver(driver.driver_id)}>Удалить</button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {selectedDriver && (
        <div className="driver-details">
          <h2>Детали водителя</h2>
          <div className="details-card">
            <p><strong>ID:</strong> {selectedDriver.driver_id}</p>
            <p><strong>Имя:</strong> {selectedDriver.firstname}</p>
            <p><strong>Фамилия:</strong> {selectedDriver.lastname}</p>
            <p><strong>Email:</strong> {selectedDriver.email}</p>
            <p><strong>Возраст:</strong> {selectedDriver.age}</p>
            <p><strong>Пол:</strong> {selectedDriver.sex}</p>
            <p><strong>Рейтинг:</strong> {selectedDriver.driver_rating}</p>
            <p><strong>Всего поездок:</strong> {selectedDriver.driver_rides}</p>
            <p><strong>Всего аварий:</strong> {selectedDriver.driver_time_accidents}</p>
            <p><strong>Дата первой поездки:</strong> {selectedDriver.first_ride_date}</p>
          </div>

          <h3>Обновить данные водителя</h3>
          <form>
            <label>
              Имя:
              <input
                type="text"
                name="user_data.firstname"
                value={updatedData.user_data.firstname}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Фамилия:
              <input
                type="text"
                name="user_data.lastname"
                value={updatedData.user_data.lastname}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Email:
              <input
                type="email"
                name="user_data.email"
                value={updatedData.user_data.email}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Возраст:
              <input
                type="number"
                name="driver_data.age"
                value={updatedData.driver_data.age}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Рейтинг:
              <input
                type="number"
                name="driver_data.driver_rating"
                value={updatedData.driver_data.driver_rating}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Всего поездок:
              <input
                type="number"
                name="driver_data.driver_rides"
                value={updatedData.driver_data.driver_rides}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Всего аварий:
              <input
                type="number"
                name="driver_data.driver_time_accidents"
                value={updatedData.driver_data.driver_time_accidents}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Дата первой поездки:
              <input
                type="date"
                name="driver_data.first_ride_date"
                value={updatedData.driver_data.first_ride_date}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <button type="button" onClick={() => updateDriver(selectedDriver.driver_id)}>Обновить</button>
          </form>
        </div>
      )}

      {rides.length > 0 && (
        <div className="driver-rides">
          <h2>Список поездок водителя</h2>
          <ul>
            {rides.map((ride, index) => (
              <li key={index}>
                <p><strong>Дата поездки:</strong> {ride.ride_date}</p>
                <p><strong>Стоимость:</strong> {ride.ride_cost}</p>
                <p><strong>Средняя скорость:</strong> {ride.speed_avg} км/ч</p>
                <p><strong>Максимальная скорость:</strong> {ride.speed_max} км/ч</p>
                <p><strong>Количество остановок:</strong> {ride.stop_times}</p>
                <p><strong>Расстояние:</strong> {ride.distance} км</p>
                <p><strong>Заправки:</strong> {ride.refueling}</p>
                <p><strong>Качество поездки:</strong> {ride.user_ride_quality}</p>
                <p><strong>Отклонение от нормы:</strong> {ride.deviation_normal}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default AdminPageDrivers;