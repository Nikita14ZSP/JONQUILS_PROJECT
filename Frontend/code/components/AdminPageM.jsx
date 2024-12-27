import React, { useState, useEffect } from "react";
import axios from "axios";
import "./AdminPage.css";

const AdminPage = () => {
  const [mechanics, setMechanics] = useState([]);
  const [selectedMechanic, setSelectedMechanic] = useState(null);
  const [fixes, setFixes] = useState([]);
  const [message, setMessage] = useState("");
  const [mechanicIdInput, setMechanicIdInput] = useState("");
  const [updatedData, setUpdatedData] = useState({
    user_data: {
      firstname: "",
      lastname: "",
      email: "",
    },
    mechanic_data: {
      age: 0,
      mechanic_rating: 0,
      car_times_repaired: 0,
    },
  });

  const baseURL = "http://127.0.0.1:8000"; // Убедитесь, что этот адрес верный
  const timeout = 10000; 

  const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: timeout,
  });

  const fetchMechanicByIdFromInput = async () => {
    if (!mechanicIdInput) {
      setMessage("Пожалуйста, введите ID механика.");
      return;
    }
    try {
      const response = await axios.get(`${baseURL}/mechanics/get_by_id/${mechanicIdInput}`);
      setSelectedMechanic(response.data);
      setMessage(`Механик с ID ${mechanicIdInput} успешно загружен.`);
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось загрузить данные механика."}`);
    }
  };

  // 1. Получить всех механиков
  const fetchAllMechanics = async () => {
    try {
      const response = await axios.get(`${baseURL}/mechanics/get_all`);
      setMechanics(response.data);
      setMessage("Список механиков успешно загружен.");
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось загрузить список механиков."}`);
    }
  };

  // 2. Получить механика по ID
  const fetchMechanicById = async (mechanicId) => {
    try {
      const response = await axios.get(`${baseURL}/mechanics/get_by_id/${mechanicId}`);
      setSelectedMechanic(response.data);
      setMessage(`Механик с ID ${mechanicId} успешно загружен.`);
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось загрузить данные механика."}`);
    }
  };

  // 3. Получить работы механика
  const fetchMechanicFixes = async (mechanicId) => {
    try {
      const response = await axios.get(`${baseURL}/mechanics/get_fixes/${mechanicId}`);
      setFixes(response.data);
      setMessage(`Работы механика с ID ${mechanicId} успешно загружены.`);
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось загрузить работы механика."}`);
    }
  };

  // 4. Удалить механика
  const deleteMechanic = async (mechanicId) => {
    try {
      await axios.delete(`${baseURL}/mechanics/delete_by_id/${mechanicId}`);
      setMessage(`Механик с ID ${mechanicId} успешно удален.`);
      fetchAllMechanics(); // Обновить список механиков
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось удалить механика."}`);
    }
  };

  // 5. Обновить механика
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
        mechanic_data: {
          ...prevData.mechanic_data,
          [name.split(".")[1]]: value,
        },
      };
    });
  };

  const validateData = () => {
    const { firstname, lastname, email } = updatedData.user_data;
    const { age, mechanic_rating, car_times_repaired } = updatedData.mechanic_data;
    if (!firstname || !lastname || !email || age <= 0 || mechanic_rating < 0 || car_times_repaired < 0) {
      setMessage("Пожалуйста, заполните все поля корректно.");
      return false;
    }
    return true;
  };

  const updateMechanic = async (mechanicId) => {
    if (!validateData()) return; // Validate before updating

    // Формирование правильных данных для отправки
    const requestData = {
      user_data: updatedData.user_data,
      mechanic_data: updatedData.mechanic_data,
    };

    try {
      // Обновляем механика
      const response = await axios.put(
        `${baseURL}/mechanics/update_by_id/${mechanicId}`, 
        JSON.stringify(requestData), // Сериализуем данные в JSON
        {
          headers: {
            'Content-Type': 'application/json', // Устанавливаем правильный заголовок
          },
        }
      );
      
      setMessage(`Механик с ID ${mechanicId} успешно обновлен.`);
      fetchAllMechanics(); // Обновить список механиков
    } catch (error) {
      setMessage(`Ошибка: ${error.response?.data?.detail || "Не удалось обновить данные механика."}`);
      console.error("Error response:", error.response?.data); // Log the full error response
    }
};


return (
  <div className="admin-page">
    <header>
      <h1>Админ-панель</h1>
      <p>Управление механиками</p>
    </header>

    <div className="actions">
      <button onClick={fetchAllMechanics} className="btn btn-primary">Получить всех механиков</button>

      <div>
        <label>
          Введите ID механика:
          <input
            type="number"
            value={mechanicIdInput}
            onChange={(e) => setMechanicIdInput(e.target.value)}
            placeholder="ID механика"
          />
        </label>
        <button onClick={fetchMechanicByIdFromInput} className="btn btn-primary">Получить механика по ID</button>
      </div>
    </div>

    {message && <p className="message">{message}</p>}

    {mechanics.length > 0 && (
      <div className="mechanics-list">
        <h2>Список механиков</h2>
        <ul>
          {mechanics.map((mechanic) => (
            <li key={mechanic.mechanic_id}>
              <strong>{mechanic.firstname} {mechanic.lastname}</strong> (ID: {mechanic.mechanic_id})
              <button onClick={() => fetchMechanicById(mechanic.mechanic_id)}>Посмотреть</button>
              <button onClick={() => fetchMechanicFixes(mechanic.mechanic_id)}>Работы</button>
              <button onClick={() => deleteMechanic(mechanic.mechanic_id)}>Удалить</button>
            </li>
          ))}
        </ul>
      </div>
    )}

    {selectedMechanic && (
      <div className="mechanic-details">
        <h2>Детали механика</h2>
        <p><strong>ID:</strong> {selectedMechanic.mechanic_id}</p>
        <p><strong>Имя:</strong> {selectedMechanic.firstname}</p>
        <p><strong>Фамилия:</strong> {selectedMechanic.lastname}</p>
        <p><strong>Email:</strong> {selectedMechanic.email}</p>
        <p><strong>Возраст:</strong> {selectedMechanic.age}</p>
        <p><strong>Рейтинг механика:</strong> {selectedMechanic.mechanic_rating}</p>
        <p><strong>Количество отремонтированных машин:</strong> {selectedMechanic.car_times_repaired}</p>
      </div>
    )}

    {fixes.length > 0 && (
      <div className="mechanic-fixes">
        <h2>Работы механика</h2>
        <table className="fixes-table">
          <thead>
            <tr>
              <th>Дата работы</th>
              <th>Тип работы</th>
              <th>Степень повреждения</th>
              <th>Продолжительность работы (сек)</th>
              <th>Номер машины</th>
              <th>Модель</th>
              <th>Тип топлива</th>
              <th>Год начала эксплуатации</th>
              <th>Год работы</th>
              <th>Пробег</th>
            </tr>
          </thead>
          <tbody>
            {fixes.map((fix, index) => (
              <tr key={index}>
                <td>{new Date(fix.fix_date).toLocaleString()}</td>
                <td>{fix.work_type}</td>
                <td>{fix.destroy_degree}</td>
                <td>{fix.work_duration}</td>
                <td>{fix.car_number}</td>
                <td>{fix.model}</td>
                <td>{fix.fuel_type}</td>
                <td>{fix.year_to_start}</td>
                <td>{fix.year_to_work}</td>
                <td>{fix.rides}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )}
  </div>
);


};

export default AdminPage;