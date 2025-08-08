# Task Flow

![In Development](https://img.shields.io/badge/Status-В%20разработке-yellow?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

Доска для управления задачами с синхронизацией между пользователями.

## 🚀 Текущий статус проекта

### ✅ Реализовано
- **Django 4.2.7** проект с базовой настройкой
- **Структура приложений**:
  - `accounts` - управление пользователями
  - `boards` - управление досками
  - `tasks` - управление задачами
- **Модели данных**:
  - `Board` - доски проектов
  - `BoardMember` - участники досок с ролями
  - `Task` - задачи с 4 статусами (Задачи, В процессе, На проверке, Выполнено)
- **Админ-панель** Django с удобным интерфейсом
- **Безопасность**: SECRET_KEY в .env файле
- **Локализация** на русском языке

### 🏗️ В планах разработки
- **Аутентификация**: страницы логина и регистрации
- **Главная страница**: список досок пользователя
- **Интерфейс доски**: канбан с колонками статусов
- **Drag & Drop**: перемещение задач между колонками
- **Управление участниками**: добавление пользователей к доске по email
- **CRUD операции**: создание и удаление досок и задач

## 🛠️ Технологии

- **Backend**: Django 4.2.7, SQLite
- **Frontend**: HTML, CSS, Bootstrap
- **Авторизация**: Django Auth
- **Стиль**: Bootstrap без сложных фреймворков

## 📁 Структура проекта

```
Task-Flow/
├── taskflow/           # Настройки Django
├── accounts/           # Пользователи и авторизация (Еще не реализовано)
├── boards/             # Управление досками
├── tasks/              # Управление задачами
├── templates/          # HTML шаблоны (Пока их нет)
├── static/            # CSS, JS файлы (Пока их нет)
├── requirements.txt   # Зависимости
└── .env              # Секретные настройки
```

## 🚀 Установка и запуск

1. **Клонировать репозиторий**:
```bash
git clone https://github.com/QSnock/Task-Flow.git
cd Task-Flow
```

2. **Создать виртуальное окружение**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. **Установить зависимости**:
```bash
pip install -r requirements.txt
```

4. **Создать .env файл**:
```bash
SECRET_KEY=your-secret-key-here
```

5. **Выполнить миграции**:
```bash
python manage.py migrate
```

6. **Создать суперпользователя**:
```bash
python manage.py createsuperuser
```

7. **Запустить сервер**:
```bash
python manage.py runserver
```

## 📋 Модели данных

### Board (Доска)
- Название и описание
- Владелец доски
- Даты создания и обновления

### BoardMember (Участник доски)
- Связь пользователь-доска
- Роль (Владелец/Участник)
- Дата добавления

### Task (Задача)
- Название и описание
- Принадлежность к доске
- Статус (todo/in_progress/review/done)
- Исполнитель и создатель
- Позиция для drag & drop

## 🎯 Особенности

- **Простота**: минимум зависимостей, чистый Django
- **Локализация**: полностью на русском языке
- **Безопасность**: секретные данные в .env