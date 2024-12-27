import axios from "axios";

// Создаем экземпляр Axios
const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // Замените на адрес вашего бэкенда
  headers: {
    "Content-Type": "application/json",
  },
});

// Добавляем перехватчик для логирования запросов
api.interceptors.request.use(
  (config) => {
    console.log("Request:", config); // Логируем запрос
    return config;
  },
  (error) => {
    console.error("Request Error:", error); // Логируем ошибки запроса
    return Promise.reject(error);
  }
);

// Добавляем перехватчик для логирования ответов
api.interceptors.response.use(
  (response) => {
    console.log("Response:", response); // Логируем ответ
    return response;
  },
  (error) => {
    console.error("Response Error:", error.response || error); // Логируем ошибки ответа
    return Promise.reject(error);
  }
);

export default api;
