@echo off
set OUTPUT_DIR=build_output

echo Limpiando builds anteriores...
rmdir /s /q %OUTPUT_DIR% 2>nul
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul

echo Compilando...
pyinstaller main.py --onefile --windowed --clean --add-data "ui;ui" --distpath %OUTPUT_DIR%\dist --workpath %OUTPUT_DIR%\build --specpath %OUTPUT_DIR%

echo.
echo Listo. Ejecutable en %OUTPUT_DIR%\dist\
pause