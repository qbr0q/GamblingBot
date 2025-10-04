# 🎰 GamblingBot
**GamblingBot** — Telegram-бот для азартной мини-игры.  
Делай ставки, крути рулетку и проверяй удачу!  

Проект написан на **Python** с использованием библиотеки [`pyTelegramBotAPI`](https://github.com/eternnoir/pyTelegramBotAPI).  
Реализованы фоновая обработка, кэширование и хранение данных в базе.

## ⚙️ Стек технологий

- Python 3.10+
- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
- SQLModel (ORM)
- dotenv (для конфигов)
- threading (фоновый процесс рулетки)

## 🚀 Установка и запуск

1. Клонируй репозиторий:

   ```
   git clone https://github.com/qbr0q/GamblingBot.git
   cd GamblingBot
   
2. Создай виртуальное окружение:

    ```
    python -m venv venv
    source venv/bin/activate       # macOS / Linux
    venv\Scripts\activate          # Windows
   
3. Установи зависимости:

    ```    
    pip install -r requirements.txt
    ```
    Создай config.env со своим токеном и settings.py со своими настройками


4. Запусти бота:

    ```
    python main.py
   