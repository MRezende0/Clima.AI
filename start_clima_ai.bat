@echo off
echo ========================================
echo    INICIANDO CLIMA.AI - Sistema de IA
echo ========================================
echo.

REM Verificar se o ambiente virtual existe
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    "C:\Users\matheus.rezende\AppData\Local\Programs\Python\Python312\python.exe" -m venv venv
    echo [INFO] Ambiente virtual criado!
    echo.
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências se necessário
echo [INFO] Verificando dependências...
pip install -r requirements.txt --quiet

REM Executar aplicação
echo [INFO] Iniciando aplicação Clima.AI...
echo.
echo ========================================
echo   Aplicação disponível em:
echo   http://localhost:8501
echo ========================================
echo.
echo Pressione Ctrl+C para parar a aplicação
echo.

streamlit run app.py

pause

