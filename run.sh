#!/bin/sh

export APP_MODULE=${APP_MODULE-app.main:app}
export HOST=${HOST:-62.84.120.87}
export PORT=${PORT:-8001}

exec uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"