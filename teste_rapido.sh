#!/bin/bash
# Script de teste rápido do sistema

echo "🧪 TESTE RÁPIDO DO SISTEMA DE PREVISÃO DE ENERGIA"
echo "=================================================="
echo ""

# Teste 1: Básico com dados simulados
echo "📋 Teste 1: Pipeline básico (dados simulados)"
echo "---------------------------------------------"
python run_pipeline.py --horizon 7 --no-gui
if [ $? -eq 0 ]; then
    echo "✅ Teste 1: PASSOU"
else
    echo "❌ Teste 1: FALHOU"
fi
echo ""

# Teste 2: Com PVGIS (API real)
echo "📋 Teste 2: Com PVGIS (API real - São Paulo)"
echo "---------------------------------------------"
python run_pipeline.py \
  --use-real-data \
  --lat -23.5505 \
  --lon -46.6333 \
  --horizon 7 \
  --no-gui
if [ $? -eq 0 ]; then
    echo "✅ Teste 2: PASSOU"
else
    echo "❌ Teste 2: FALHOU"
fi
echo ""

# Teste 3: Verificar arquivos gerados
echo "📋 Teste 3: Verificando arquivos gerados"
echo "---------------------------------------------"
if [ -f "results/forecast_results.csv" ]; then
    echo "✅ CSV encontrado"
    echo "   Linhas: $(wc -l < results/forecast_results.csv)"
else
    echo "❌ CSV não encontrado"
fi

if [ -f "results/forecast_comparison.png" ]; then
    echo "✅ Gráfico 1 encontrado"
else
    echo "❌ Gráfico 1 não encontrado"
fi

if [ -f "results/surplus_deficit.png" ]; then
    echo "✅ Gráfico 2 encontrado"
else
    echo "❌ Gráfico 2 não encontrado"
fi
echo ""

# Teste 4: Testes pytest
echo "📋 Teste 4: Executando testes pytest"
echo "---------------------------------------------"
if command -v pytest &> /dev/null; then
    pytest tests/ -v
else
    echo "⚠️  pytest não instalado. Pule este teste ou instale: pip install pytest"
fi
echo ""

echo "=================================================="
echo "✅ Testes concluídos!"
echo "Verifique os resultados em: results/"

