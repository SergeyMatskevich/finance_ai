# Family Finance AI

An intelligent family finance management system that helps track expenses, manage budgets, and achieve financial goals through natural conversation.

## Key Features

- **Conversational Interface**
  - Natural language interaction for expense tracking
  - Voice input support
  - AI-powered financial insights and recommendations

- **Family Finance Management**
  - Multi-user support for family members
  - Shared access to financial data
  - Real-time synchronization across devices
  - Mobile-first design

- **Expense Tracking**
  - Manual expense entry through conversation
  - Google Sheets integration for bulk data import
  - Categorization of expenses
  - Historical expense analysis

- **Budget Management**
  - Set and track family budgets
  - Real-time budget monitoring
  - Smart notifications for budget alerts
  - Budget vs. actual expense comparisons

- **Financial Goals**
  - Set and track family financial goals
  - Progress monitoring
  - AI-powered recommendations for goal achievement

## Technical Stack

- **Backend**
  - Python
  - FastAPI for REST API
  - PostgreSQL for data storage
  - Redis for real-time features

- **AI/ML**
  - Natural Language Processing for conversation
  - Machine Learning for expense categorization
  - Predictive analytics for budget forecasting

- **Frontend**
  - React Native for mobile app
  - Progressive Web App support
  - Real-time updates

- **Integrations**
  - Google Sheets API
  - Push notifications
  - Cloud storage

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/finance_ai.git

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

## Development Setup

1. Set up the database
2. Configure Google Sheets API credentials
3. Set up push notification service
4. Run the development server

## Usage

[Detailed usage instructions will be added as features are implemented]

## License

MIT

## Деплой на Render.com

### Шаги для деплоя:

1. Создайте аккаунт на [Render.com](https://render.com)

2. Подключите ваш GitHub репозиторий к Render

3. В Render Dashboard:
   - Нажмите "New +"
   - Выберите "Blueprint"
   - Выберите ваш репозиторий
   - Нажмите "Apply"

4. Render автоматически:
   - Создаст базу данных PostgreSQL
   - Развернёт ваше приложение
   - Настроит все переменные окружения
   - Предоставит URL для доступа

### Доступ к приложению

После успешного деплоя, ваше приложение будет доступно по адресу:
```
https://finance-ai-api.onrender.com
```

API документация будет доступна по адресу:
```
https://finance-ai-api.onrender.com/docs
```

### Мониторинг

- В Render Dashboard вы можете:
  - Видеть логи приложения
  - Мониторить использование ресурсов
  - Настраивать автоматические деплои
  - Управлять переменными окружения

### Важные замечания

1. Бесплатный тариф Render имеет ограничения:
   - Приложение "засыпает" после 15 минут неактивности
   - Первый запрос после "сна" может занять до 30 секунд
   - Ограниченное количество часов работы в месяц

2. Для продакшена рекомендуется:
   - Использовать платный тариф
   - Настроить мониторинг
   - Настроить бэкапы базы данных 