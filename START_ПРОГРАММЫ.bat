@echo off
chcp 65001 > nul
if not exist .venv\Scripts\python.exe (
    echo Создаю виртуальное окружение...
    py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python app.py
pause
