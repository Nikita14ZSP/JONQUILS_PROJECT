import React, { useState, useEffect } from "react";
import axios from "axios";
import "./AdminPageCars.css";

const AdminPageFixes = () => {
  const [fixes, setFixes] = useState([]);
  const [selectedFix, setSelectedFix] = useState(null);
  const [message, setMessage] = useState("");
  const [newFix, setNewFix] = useState({
    car_id: 0,
    mechanic_id: 0,
    fix_date: new Date().toISOString().slice(0, 16),
    work_type: "",
    destroy_degree: 0,
    work_duration: 0,
  });
  const [updatedFix, setUpdatedFix] = useState({
    fix_date: new Date().toISOString().slice(0, 16),
    work_type: "",
    destroy_degree: 0,
    work_duration: 0,
  });
  const baseURL = "http://127.0.0.1:8000";

   // Fetch all fixes
   const fetchAllFixes = async () => {
    try {
      const response = await axios.get(`${baseURL}/fixes/get_all`, { timeout: 5000 });
      setFixes(response.data);
      setMessage("Список ремонтов успешно загружен.");
    } catch (error) {
      setMessage("Ошибка загрузки списка ремонтов.");
    }
  };

  // Fetch fix by ID
  const fetchFixById = async (fixId) => {
    try {
      const response = await axios.get(`${baseURL}/fixes/get_by_id/${fixId}`, { timeout: 5000 });
      setSelectedFix(response.data);
      setMessage(`Ремонт с ID ${fixId} успешно загружен.`);
    } catch (error) {
      setMessage("Ошибка загрузки ремонта.");
    }
  };

  // Add new fix
  const addFix = async () => {
    try {
      await axios.post(`${baseURL}/fixes/add`, newFix, {
        headers: { "Content-Type": "application/json" },
        timeout: 5000,
      });
      setMessage("Новый ремонт успешно добавлен.");
      fetchAllFixes();
    } catch (error) {
      setMessage("Ошибка добавления ремонта.");
    }
  };

  // Update fix
  const updateFix = async (fixId) => {
    try {
      await axios.put(`${baseURL}/fixes/update/${fixId}`, updatedFix, {
        headers: { "Content-Type": "application/json" },
        timeout: 5000,
      });
      setMessage(`Ремонт с ID ${fixId} успешно обновлен.`);
      fetchAllFixes();
    } catch (error) {
      setMessage("Ошибка обновления ремонта.");
    }
  };

  // Delete fix
  const deleteFix = async (fixId) => {
    try {
      await axios.delete(`${baseURL}/fixes/delete/${fixId}`, { timeout: 5000 });
      setMessage(`Ремонт с ID ${fixId} успешно удален.`);
      fetchAllFixes();
    } catch (error) {
      setMessage("Ошибка удаления ремонта.");
    }
  };

  useEffect(() => {
    fetchAllFixes();
  }, []);

  const handleNewFixChange = (event) => {
    const { name, value } = event.target;
    setNewFix((prev) => ({ ...prev, [name]: value }));
  };

  const handleUpdatedFixChange = (event) => {
    const { name, value } = event.target;
    setUpdatedFix((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="admin-page-fixes">
      <header className="header">
        <h1>Административная панель - Управление ремонтами</h1>
        <p>Добавляйте, обновляйте, просматривайте и удаляйте ремонты.</p>
      </header>

      {message && <p className="message">{message}</p>}

      <section className="fetch-fix-by-id">
        <h2>Получить ремонт по ID</h2>
        <div className="form-inline">
          <label>ID ремонта:</label>
          <input
            type="number"
            placeholder="Введите ID"
            onChange={(e) => setSelectedFix({ fix_info_id: e.target.value })}
          />
          <button
            onClick={() => fetchFixById(selectedFix?.fix_info_id)}
            className="btn btn-primary"
          >
            Получить
          </button>
        </div>
      </section>

      <section className="new-fix-section">
        <h2>Добавить новый ремонт</h2>
        <div className="form-grid">
          <div>
            <label>ID машины</label>
            <input
              type="number"
              name="car_id"
              value={newFix.car_id}
              onChange={handleNewFixChange}
            />
          </div>
          <div>
            <label>ID механика</label>
            <input
              type="number"
              name="mechanic_id"
              value={newFix.mechanic_id}
              onChange={handleNewFixChange}
            />
          </div>
          <div>
            <label>Дата ремонта</label>
            <input
              type="datetime-local"
              name="fix_date"
              value={newFix.fix_date}
              onChange={handleNewFixChange}
            />
          </div>
          <div>
            <label>Тип работы</label>
            <input
              type="text"
              name="work_type"
              value={newFix.work_type}
              onChange={handleNewFixChange}
            />
          </div>
          <div>
            <label>Степень разрушения</label>
            <input
              type="number"
              name="destroy_degree"
              value={newFix.destroy_degree}
              onChange={handleNewFixChange}
            />
          </div>
          <div>
            <label>Длительность работы (минут)</label>
            <input
              type="number"
              name="work_duration"
              value={newFix.work_duration}
              onChange={handleNewFixChange}
            />
          </div>
        </div>
        <button onClick={addFix} className="btn btn-success">
          Добавить ремонт
        </button>
      </section>

      <section className="fixes-list-section">
        <h2>Список ремонтов</h2>
        <ul className="fixes-list">
          {fixes.map((fix) => (
            <li key={fix.fix_info_id} className="fix-card">
              <h3>Ремонт ID: {fix.fix_info_id}</h3>
              <p><strong>Тип работы:</strong> {fix.work_type}</p>
              <p><strong>Степень разрушения:</strong> {fix.destroy_degree}</p>
              <button
                onClick={() => fetchFixById(fix.fix_info_id)}
                className="btn btn-primary"
              >
                Просмотреть
              </button>
              <button
                onClick={() => deleteFix(fix.fix_info_id)}
                className="btn btn-danger"
              >
                Удалить
              </button>
            </li>
          ))}
        </ul>
      </section>

      {selectedFix && (
        <section className="selected-fix-details">
          <h2>Детали ремонта ID {selectedFix.fix_info_id}</h2>
          <ul>
            <li><strong>ID машины:</strong> {selectedFix.car_id}</li>
            <li><strong>ID механика:</strong> {selectedFix.mechanic_id}</li>
            <li><strong>Дата ремонта:</strong> {new Date(selectedFix.fix_date).toLocaleString()}</li>
            <li><strong>Тип работы:</strong> {selectedFix.work_type}</li>
            <li><strong>Степень разрушения:</strong> {selectedFix.destroy_degree}</li>
            <li><strong>Длительность работы:</strong> {selectedFix.work_duration} минут</li>
          </ul>
        </section>
      )}
    </div>
  );
};

export default AdminPageFixes;