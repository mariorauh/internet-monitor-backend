@echo off
setlocal

echo ================================
echo   Internet Monitor Release
echo ================================
echo.

set /p VERSION=Bitte Versionsnummer eingeben (z.B. 0.2.0): 

if "%VERSION%"=="" (
    echo.
    echo Fehler: Keine Versionsnummer angegeben.
    pause
    exit /b 1
)

echo.
echo Folgende Version wird veröffentlicht:
echo.
echo    %VERSION%
echo.

set /p CONFIRM=Fortfahren? (y/n): 

if /I not "%CONFIRM%"=="y" (
    echo.
    echo Abgebrochen.
    pause
    exit /b 0
)

git add .

git commit -m "Release %VERSION%"

git tag v%VERSION%

git push origin main
git push origin v%VERSION%

echo.
echo ================================
echo Release %VERSION% abgeschlossen.
echo ================================

pause