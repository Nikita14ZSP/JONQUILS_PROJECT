import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Стили в формате CSS-in-JS
const styles = {
  container: {
    padding: '30px',
    fontFamily: 'Arial, sans-serif',
    background: 'linear-gradient(to bottom, #FFA500, #FF6347)', // оранжевый градиент для фона
    minHeight: '100vh',
  },
  header: {
    textAlign: 'center',
    color: '#2d2d2d',
    marginBottom: '30px',
  },
  button: {
    padding: '12px 20px',
    margin: '10px 0',
    fontSize: '16px',
    cursor: 'pointer',
    backgroundColor: '#FF8C00', // персиковый цвет
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    transition: 'background-color 0.3s ease',
  },
  buttonHover: {
    backgroundColor: '#32CD32', // зеленый цвет при наведении
  },
  input: {
    padding: '12px 15px',
    margin: '10px 0',
    fontSize: '16px',
    width: '100%',
    maxWidth: '500px', // ограничиваем максимальную ширину
    border: '1px solid #ccc',
    borderRadius: '5px',
    backgroundColor: '#fff',
    boxSizing: 'border-box', // учитываем padding при расчете ширины
    marginLeft: 'auto', // отцентрировать по горизонтали
    marginRight: 'auto', // отцентрировать по горизонтали
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    maxWidth: '600px',
    margin: '0 auto',
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 0 15px rgba(0, 0, 0, 0.1)',
  },
  error: {
    color: 'red',
    fontSize: '14px',
    textAlign: 'center',
    marginTop: '10px',
  },
  rideDetails: {
    padding: '20px',
    marginTop: '20px',
    border: '1px solid #ddd',
    borderRadius: '5px',
    backgroundColor: '#fff',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  },
  rideItem: {
    padding: '15px',
    borderBottom: '1px solid #ddd',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: '5px',
    marginBottom: '10px',
    boxShadow: '0 0 5px rgba(0, 0, 0, 0.1)',
  },
  rideList: {
    listStyleType: 'none',
    padding: '0',
  },
  rideKey: {
    fontWeight: 'bold',
    minWidth: '150px',
    color: '#333',
  },
  rideValue: {
    flex: 1,
    color: '#555',
  },
  rideRow: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '5px 0',
  },
  inputContainer: {
    marginBottom: '20px',
  },
  formActions: {
    display: 'flex',
    justifyContent: 'center',
    marginTop: '20px',
  },
};

const AdminPageRides = () => {
  const [rides, setRides] = useState([]);
  const [rideId, setRideId] = useState('');
  const [rideData, setRideData] = useState({
    driver_id: '',
    car_id: '',
    rating: '',
    ride_date: '',
    ride_duration: '',
    ride_cost: '',
    speed_avg: '',
    speed_max: '',
    stop_times: '',
    distance: '',
    refueling: '',
    user_ride_quality: '',
    deviation_normal: '',
  });
  const [error, setError] = useState('');
  const [rideInfo, setRideInfo] = useState(null);

  useEffect(() => {
    fetchRides();
  }, []);

  const fetchRides = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/rides/get_all');
      setRides(response.data);
    } catch (err) {
      setError();
    }
  };

  const addRide = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/rides/add', {
        ride_data: {
          driver_id: rideData.driver_id,
          car_id: rideData.car_id,
          rating: rideData.rating,
        },
        ride_info_data: {
          ride_date: rideData.ride_date,
          ride_duration: rideData.ride_duration,
          ride_cost: rideData.ride_cost,
          speed_avg: rideData.speed_avg,
          speed_max: rideData.speed_max,
          stop_times: rideData.stop_times,
          distance: rideData.distance,
          refueling: rideData.refueling,
          user_ride_quality: rideData.user_ride_quality,
          deviation_normal: rideData.deviation_normal,
        },
      });
      setError('');
      fetchRides(); // Обновить список поездок
    } catch (err) {
      setError('Ошибка при добавлении поездки');
    }
  };

  const fetchRideById = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/rides/get_by_id/${rideId}`);
      setRideInfo(response.data);
      setError('');
    } catch (err) {
      setError('Ошибка при получении поездки по ID');
      setRideInfo(null);
    }
  };

  const deleteRide = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/rides/delete/${id}`);
      fetchRides(); // Обновить список поездок после удаления
      setError('');
    } catch (err) {
      setError('Ошибка при удалении поездки');
    }
  };

  const updateRide = async (id) => {
    try {
      await axios.put(`http://127.0.0.1:8000/rides/update/${id}`, {
        ride_data: {
          rating: rideData.rating,
        },
        ride_info_data: {
          ride_date: rideData.ride_date,
          ride_duration: rideData.ride_duration,
          ride_cost: rideData.ride_cost,
          speed_avg: rideData.speed_avg,
          speed_max: rideData.speed_max,
          stop_times: rideData.stop_times,
          distance: rideData.distance,
          refueling: rideData.refueling,
          user_ride_quality: rideData.user_ride_quality,
          deviation_normal: rideData.deviation_normal,
        },
      });
      fetchRides(); // Обновить список поездок после обновления
      setError('');
    } catch (err) {
      setError('Ошибка при обновлении поездки');
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Админ панель для управления поездками</h1>

      {/* Кнопка для получения всех поездок */}
      <div style={styles.formActions}>
        <button
          style={styles.button}
          onClick={fetchRides}
          onMouseOver={(e) => e.target.style.backgroundColor = styles.buttonHover.backgroundColor}
          onMouseOut={(e) => e.target.style.backgroundColor = styles.button.backgroundColor}
        >
          Получить все поездки
        </button>
      </div>

      {/* Форма для добавления новой поездки */}
      <div style={styles.form}>
        <h3>Добавить новую поездку</h3>
        <div style={styles.inputContainer}>
          <input
            style={styles.input}
            type="number"
            placeholder="ID водителя"
            value={rideData.driver_id}
            onChange={(e) => setRideData({ ...rideData, driver_id: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="ID автомобиля"
            value={rideData.car_id}
            onChange={(e) => setRideData({ ...rideData, car_id: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Рейтинг"
            value={rideData.rating}
            onChange={(e) => setRideData({ ...rideData, rating: e.target.value })}
          />
          <input
            style={styles.input}
            type="text"
            placeholder="Дата поездки"
            value={rideData.ride_date}
            onChange={(e) => setRideData({ ...rideData, ride_date: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Длительность поездки"
            value={rideData.ride_duration}
            onChange={(e) => setRideData({ ...rideData, ride_duration: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Стоимость поездки"
            value={rideData.ride_cost}
            onChange={(e) => setRideData({ ...rideData, ride_cost: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Средняя скорость"
            value={rideData.speed_avg}
            onChange={(e) => setRideData({ ...rideData, speed_avg: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Максимальная скорость"
            value={rideData.speed_max}
            onChange={(e) => setRideData({ ...rideData, speed_max: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Количество остановок"
            value={rideData.stop_times}
            onChange={(e) => setRideData({ ...rideData, stop_times: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Дистанция"
            value={rideData.distance}
            onChange={(e) => setRideData({ ...rideData, distance: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Количество заправок"
            value={rideData.refueling}
            onChange={(e) => setRideData({ ...rideData, refueling: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Качество поездки"
            value={rideData.user_ride_quality}
            onChange={(e) => setRideData({ ...rideData, user_ride_quality: e.target.value })}
          />
          <input
            style={styles.input}
            type="number"
            placeholder="Отклонение от нормы"
            value={rideData.deviation_normal}
            onChange={(e) => setRideData({ ...rideData, deviation_normal: e.target.value })}
          />
          <button
            style={styles.button}
            onClick={addRide}
            onMouseOver={(e) => e.target.style.backgroundColor = styles.buttonHover.backgroundColor}
            onMouseOut={(e) => e.target.style.backgroundColor = styles.button.backgroundColor}
          >
            Добавить поездку
          </button>
        </div>
      </div>

      {/* Ошибки */}
      {error && <div style={styles.error}>{error}</div>}

      {/* Список всех поездок */}
      <div style={styles.rideList}>
        {rides.map((ride) => (
          <div key={ride.ride_id} style={styles.rideItem}>
            <div>
              <p style={styles.rideKey}>ID Поездки:</p>
              <p style={styles.rideValue}>{ride.ride_id}</p>
            </div>
            <div>
              <p style={styles.rideKey}>ID Водителя:</p>
              <p style={styles.rideValue}>{ride.driver_id}</p>
            </div>
            <div>
              <p style={styles.rideKey}>ID Автомобиля:</p>
              <p style={styles.rideValue}>{ride.car_id}</p>
            </div>
            <div style={styles.formActions}>
              <button
                style={styles.button}
                onClick={() => fetchRideById(ride.ride_id)}
                onMouseOver={(e) => e.target.style.backgroundColor = styles.buttonHover.backgroundColor}
                onMouseOut={(e) => e.target.style.backgroundColor = styles.button.backgroundColor}
              >
                Просмотреть детали
              </button>
              <button
                style={styles.button}
                onClick={() => deleteRide(ride.ride_id)}
                onMouseOver={(e) => e.target.style.backgroundColor = styles.buttonHover.backgroundColor}
                onMouseOut={(e) => e.target.style.backgroundColor = styles.button.backgroundColor}
              >
                Удалить поездку
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Детали выбранной поездки */}
      {rideInfo && (
        <div style={styles.rideDetails}>
          <h3>Детали поездки</h3>
          <p><strong>ID Поездки:</strong> {rideInfo.ride_id}</p>
          <p><strong>ID Водителя:</strong> {rideInfo.driver_id}</p>
          <p><strong>ID Автомобиля:</strong> {rideInfo.car_id}</p>
          <p><strong>Дата поездки:</strong> {rideInfo.ride_date}</p>
          <p><strong>Длительность поездки:</strong> {rideInfo.ride_duration}</p>
          <p><strong>Стоимость поездки:</strong> {rideInfo.ride_cost}</p>
          <p><strong>Средняя скорость:</strong> {rideInfo.speed_avg}</p>
          <p><strong>Максимальная скорость:</strong> {rideInfo.speed_max}</p>
          <p><strong>Количество остановок:</strong> {rideInfo.stop_times}</p>
          <p><strong>Дистанция:</strong> {rideInfo.distance}</p>
          <p><strong>Количество заправок:</strong> {rideInfo.refueling}</p>
          <p><strong>Качество поездки:</strong> {rideInfo.user_ride_quality}</p>
          <p><strong>Отклонение от нормы:</strong> {rideInfo.deviation_normal}</p>
        </div>
      )}
    </div>
  );
};

export default AdminPageRides;

