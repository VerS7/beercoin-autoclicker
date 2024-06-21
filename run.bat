@echo off

where python >nul
if %errorlevel% == 0 (
    echo --- Python found.
) else (
    echo --- Python is not installed.
    goto :EOF
)

pip list | findstr selenium >nul
if %errorlevel% == 0 (
    echo --- Selenium found.
    goto :run
) else (
    echo --- Selenium is not installed.
)

set /P choice= "--- Would you like to install selenium right now [y/n] "
if /I "%choice%" EQU "y" (
    pip install -r requirements.txt
    goto :run
) else if /I "%choice%" EQU "n" (
    goto :EOF
)

:run
python src\main.py