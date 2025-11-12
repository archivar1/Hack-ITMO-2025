**Human API** - это платформа, которая предоставляет единый API для доступа к данным о здоровье пользователей из различных источников:
- **Apple HealthKit** (iOS)
- **Google Fit / Health Connect** (Android)
- **Fitbit**
- **Garmin**
- И другие

### Процесс авторизации

1. **Пользователь инициирует подключение** через бота
2. **Бот перенаправляет** пользователя на Human API для авторизации
3. **Пользователь выбирает источники данных** (HealthKit, Google Fit и т.д.)
4. **Human API возвращает authorization code**
5. **Бот обменивает code на session token**
6. **С session token бот может запрашивать данные** о здоровье

### Типы данных, которые можно получить

- **Шаги** (steps) - количество шагов за день/период
- **Калории** (calories) - сожженные калории
- **Активность** (activities) - тренировки, бег, велосипед и т.д.
- **Сон** (sleep) - данные о сне
- **Вес** (weight) - вес пользователя
- **Сердцебиение** (heart rate) - пульс


```python
# Получить шаги пользователя за сегодня
steps = human_api_service.get_steps(user_session_token, date="today")

# Получить сожженные калории
calories = human_api_service.get_calories(user_session_token, date="today")

# Получить активность
activities = human_api_service.get_activities(user_session_token, date="today")
```

### Получить URL для авторизации:
```
GET /auth/human/connect?user_id=12345
Возвращает URL для перенаправления пользователя
```

### Callback после авторизации:
```
GET /auth/human/callback?code=AUTHORIZATION_CODE&user_id=12345
Сохраняет session token для пользователя
```

### Получить шаги:
```
GET /api/human/steps?user_id=12345&date=2025-01-15
Возвращает количество шагов за указанную дату
```

### Получить калории:
```
GET /api/human/calories?user_id=12345&date=2025-01-15
Возвращает сожженные калории за указанную дату
```
