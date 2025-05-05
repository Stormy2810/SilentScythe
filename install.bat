@echo off
cls
title SilentScythe Modules Installer

:: Try to use 'python' if available
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=python
    goto setup
)

:: Try to use 'py' if 'python' not found
where py >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=py
    goto setup
)

:: Neither found
echo Python is not installed or not added to PATH.
pause
exit /b

:setup
%PYTHON% -m pip install --upgrade pip

echo.
echo Uninstalling discord.py...
%PYTHON% -m pip uninstall -y discord.py >nul 2>&1

echo Installing discord.py-self...
%PYTHON% -m pip install -U discord.py-self

echo Installing other requirements...
%PYTHON% -m pip install -r requirements.txt

echo.
echo ✅ Finished installing everything!
pause
