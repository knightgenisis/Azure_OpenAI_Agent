@echo off
echo  Setting up OpenAI Agents with Opik Tracing...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo 📋 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your Azure OpenAI credentials
    echo    Required: AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_DEPLOYMENT_NAME
)

REM Build and start services
echo 🏗️  Building and starting services...
docker-compose up --build -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Check service status
echo 🔍 Checking service status...
docker-compose ps

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Access your application:
echo    App:   http://localhost:8501
echo    Opik:  http://localhost:5173
echo.
echo 📋 Next steps:
echo    1. Edit .env file with your Azure OpenAI credentials
echo    2. Restart services: docker-compose restart openai-agents-app
echo    3. Open http://localhost:8501 in your browser
echo.
echo 🛑 To stop: docker-compose down
