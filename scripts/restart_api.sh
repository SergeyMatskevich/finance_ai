#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Порт для API
PORT=8001

echo -e "${GREEN}Проверяю состояние порта $PORT...${NC}"

# Проверяем, занят ли порт
PID=$(lsof -ti tcp:$PORT)

if [ ! -z "$PID" ]; then
    echo -e "${RED}Порт $PORT занят процессом $PID${NC}"
    echo -e "${GREEN}Останавливаю процесс...${NC}"
    kill -9 $PID
    sleep 2
    echo -e "${GREEN}Процесс остановлен${NC}"
else
    echo -e "${GREEN}Порт $PORT свободен${NC}"
fi

# Проверяем, запущены ли контейнеры
echo -e "${GREEN}Проверяю состояние контейнеров...${NC}"
if ! docker ps | grep -q "finance_ai-db-1"; then
    echo -e "${RED}База данных не запущена${NC}"
    echo -e "${GREEN}Запускаю контейнеры...${NC}"
    docker-compose up -d
    sleep 5
fi

# Запускаем API
echo -e "${GREEN}Запускаю FastAPI сервер...${NC}"
uvicorn app.main:app --reload --port $PORT 