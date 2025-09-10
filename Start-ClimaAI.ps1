# Script PowerShell para inicialização automática do Clima.AI
# Execute este script para iniciar a aplicação automaticamente

param(
    [switch]$SkipDeps,
    [switch]$ForceReinstall,
    [string]$Port = "8501"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   INICIANDO CLIMA.AI - Sistema de IA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurações
$PythonPath = "C:\Users\matheus.rezende\AppData\Local\Programs\Python\Python312\python.exe"
$VenvPath = "venv"
$AppFile = "app.py"
$RequirementsFile = "requirements.txt"

# Verificar se o Python existe
if (-not (Test-Path $PythonPath)) {
    Write-Host "[ERRO] Python não encontrado em: $PythonPath" -ForegroundColor Red
    Write-Host "Por favor, ajuste o caminho no script ou instale o Python." -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Criar ambiente virtual se não existir
if (-not (Test-Path $VenvPath)) {
    Write-Host "[INFO] Criando ambiente virtual..." -ForegroundColor Green
    & $PythonPath -m venv $VenvPath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[INFO] Ambiente virtual criado com sucesso!" -ForegroundColor Green
    } else {
        Write-Host "[ERRO] Falha ao criar ambiente virtual" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
    Write-Host ""
}

# Ativar ambiente virtual
Write-Host "[INFO] Ativando ambiente virtual..." -ForegroundColor Green
& "$VenvPath\Scripts\Activate.ps1"

# Instalar dependências
if (-not $SkipDeps) {
    Write-Host "[INFO] Verificando dependências..." -ForegroundColor Green
    
    if ($ForceReinstall) {
        Write-Host "[INFO] Reinstalando dependências..." -ForegroundColor Yellow
        & pip install -r $RequirementsFile --force-reinstall
    } else {
        & pip install -r $RequirementsFile --quiet
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[INFO] Dependências verificadas!" -ForegroundColor Green
    } else {
        Write-Host "[AVISO] Algumas dependências podem não ter sido instaladas corretamente" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Verificar se o arquivo da aplicação existe
if (-not (Test-Path $AppFile)) {
    Write-Host "[ERRO] Arquivo da aplicação não encontrado: $AppFile" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Executar aplicação
Write-Host "[INFO] Iniciando aplicação Clima.AI..." -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Aplicação disponível em:" -ForegroundColor White
Write-Host "  http://localhost:$Port" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pressione Ctrl+C para parar a aplicação" -ForegroundColor Gray
Write-Host ""

# Tentar abrir o navegador automaticamente
try {
    Start-Process "http://localhost:$Port"
    Write-Host "[INFO] Navegador aberto automaticamente" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Abra manualmente: http://localhost:$Port" -ForegroundColor Yellow
}

# Executar Streamlit
& streamlit run $AppFile --server.port $Port
