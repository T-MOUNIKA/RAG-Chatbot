@echo off
echo Testing API endpoints...

echo.
echo Testing health endpoint:
curl -X GET http://localhost:8000/health

echo.
echo.
echo Testing chat with Docker question:
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"question\": \"What is Docker?\"}"

echo.
echo.
echo Testing chat with weather question (should be restricted):
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"question\": \"What is the weather today?\"}"

echo.
echo Done!