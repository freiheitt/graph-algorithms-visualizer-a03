@echo off
chcp 65001 > nul
if not exist .venv\Scripts\python.exe (
    echo Сначала запустите START_ПРОГРАММЫ.bat или создайте окружение.
    py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
pytest
pause
