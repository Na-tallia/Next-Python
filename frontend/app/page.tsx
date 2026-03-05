"use client"; // Это директива Next.js: говорим, что код выполняется в браузере (нужно для кнопок и запросов)

import { useEffect, useState } from "react";

export default function Home() {
  // 1. Создаем "состояние" (хранилище) для сообщения от бэкенда
  const [message, setMessage] = useState<string>("Загрузка данных...");
  const [error, setError] = useState<string | null>(null);

  // 2. useEffect — это хук, который срабатывает СРАЗУ, как только страница открылась
  useEffect(() => {
    // Делаем запрос (fetch) к нашему Django серверу
    fetch("http://127.0.0.1:8000/api/hello/")
      .then((res) => {
        if (!res.ok) throw new Error("Сервер ответил с ошибкой");
        return res.json(); // Превращаем ответ из JSON-строки в объект JavaScript
      })
      .then((data) => {
        // Записываем текст из поля "message" в наше состояние
        setMessage(data.message);
      })
      .catch((err) => {
        console.error(err);
        setError("Не удалось соединиться с Django. Проверь, запущен ли сервер!");
      });
  }, []); // Пустые скобки [] значат: выполнить 1 раз при старте

  // 3. Верстка (интерфейс)
  return (
    <main style={{ 
      display: "flex", 
      flexDirection: "column", 
      alignItems: "center", 
      justifyContent: "center", 
      minHeight: "100vh",
      fontFamily: "Arial, sans-serif" 
    }}>
      <h1 style={{ color: "#0070f3" }}>Fullstack: Next.js + Django</h1>
      
      <div style={{
        padding: "20px",
        borderRadius: "12px",
        border: "1px solid #eaeaea",
        boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
        backgroundColor: error ? "#fff5f5" : "#f9f9f9"
      }}>
        <p style={{ fontSize: "1.2rem" }}>
          {error ? (
            <span style={{ color: "red" }}>{error}</span>
          ) : (
            <span><strong>Статус API:</strong> {message}</span>
          )}
        </p>
      </div>

      <button 
        onClick={() => window.location.reload()}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          backgroundColor: "#0070f3",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer"
        }}
      >
        Обновить данные
      </button>
    </main>
  );
}