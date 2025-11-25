@echo off
REM Script de teste rápido do sistema (Windows)

echo 🧪 TESTE RÁPIDO DO SISTEMA DE PREVISÃO DE ENERGIA
echo ==================================================
echo.

REM Teste 1: Básico com dados simulados
echo 📋 Teste 1: Pipeline básico (dados simulados)
echo ---------------------------------------------
python run_pipeline.py --horizon 7 --no-gui
if %errorlevel% equ 0 (
    echo ✅ Teste 1: PASSOU
) else (
    echo ❌ Teste 1: FALHOU
)
echo.

REM Teste 2: Com PVGIS
echo 📋 Teste 2: Com PVGIS (API real - São Paulo)
echo ---------------------------------------------
python run_pipeline.py --use-real-data --lat -23.5505 --lon -46.6333 --horizon 7 --no-gui
if %errorlevel% equ 0 (
    echo ✅ Teste 2: PASSOU
) else (
    echo ❌ Teste 2: FALHOU
)
echo.

REM Teste 3: Verificar arquivos
echo 📋 Teste 3: Verificando arquivos gerados
echo ---------------------------------------------
if exist "results\forecast_results.csv" (
    echo ✅ CSV encontrado
) else (
    echo ❌ CSV não encontrado
)

if exist "results\forecast_comparison.png" (
    echo ✅ Gráfico 1 encontrado
) else (
    echo ❌ Gráfico 1 não encontrado
)

if exist "results\surplus_deficit.png" (
    echo ✅ Gráfico 2 encontrado
) else (
    echo ❌ Gráfico 2 não encontrado
)
echo.

echo ==================================================
echo ✅ Testes concluídos!
echo Verifique os resultados em: results\
pause

