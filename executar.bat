@echo off
chcp 65001 >nul
echo ========================================================
echo Iniciando o Paint App - Computacao Grafica
echo ========================================================
echo.

:: Verificar se o Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] O Python não foi encontrado no sistema ou não está no PATH!
    echo.
    echo Por favor, instale o Python 3.x (versões recomendadas: 3.8 a 3.12).
    echo Lembre-se de marcar a caixa "Add Python to PATH" durante a instalação.
    echo.
    pause
    exit /b
)

:: Mostrar a versão do Python (conforme requisito)
echo Versão do Python detectada no sistema:
python --version
echo.

:: Instalar dependências necessárias
echo Instalando/Verificando dependências necessárias (customtkinter)...
pip install customtkinter
if %errorlevel% neq 0 (
    echo.
    echo [AVISO] Houve um problema ao tentar instalar as dependências.
    echo O programa tentará iniciar mesmo assim, mas poderá falhar.
    echo.
) else (
    echo Dependências verificadas com sucesso!
    echo.
)

:: Executar a aplicação
echo Abrindo o aplicativo...
echo.
python main.py

echo.
pause
