@echo off
cd /d "%~dp0.."
echo [Avrasya2] lib klasoru yazma izni tanimlaniyor ve sitecustomize.pyc kuruluyor...
icacls "C:\Program Files (x86)\Avrasya2\lib" /grant "%USERNAME%:(OI)(CI)M" >nul 2>&1
python "%~dp0bagla.py" kur
echo.
pause
