# 🚀 Guia de Início Rápido

## Instalação Rápida

```bash
# 1. Instalar dependências
pip install -r requirements_minimal.txt

# 2. Executar exemplo básico
python example_usage.py

# 3. Executar pipeline completo
python run_pipeline.py --horizon 7
```

## Exemplos Rápidos

### 1. Previsão Simples (7 dias)

```bash
python run_pipeline.py --horizon 7 --no-gui
```

### 2. Com Interface Gráfica

```bash
python run_pipeline.py --horizon 14
```

### 3. Período Específico

```bash
python run_pipeline.py \
  --train-start 2024-01-01 \
  --train-end 2024-03-31 \
  --horizon 14
```

### 4. Tentar Dados Reais (com fallback)

```bash
python run_pipeline.py --use-real-data --cache --horizon 14
```

### 5. Região Diferente

```bash
python run_pipeline.py --region NE --submercado NE --horizon 14
```

## Estrutura de Resultados

Após executar, você encontrará em `results/`:

- `forecast_results.csv` - Tabela completa com previsões
- `forecast_results.parquet` - Versão Parquet (mais eficiente)
- `forecast_comparison.png` - Gráfico de consumo vs produção
- `surplus_deficit.png` - Gráfico de excedente vs déficit
- `cumulative_profit.png` - Lucro acumulado
- `pld_timeseries.png` - Evolução do PLD

## Próximos Passos

1. **Personalizar configuração**: Edite `config/default.yaml`
2. **Adicionar dados reais**: Implemente conectores em `src/data/`
3. **Melhorar modelos**: Ajuste hiperparâmetros em `src/models/`
4. **Expandir features**: Adicione engenh livreia de features em `src/features/`

## Troubleshooting

### Erro: "Prophet não disponível"
```bash
pip install prophet
```

### Erro: "XGBoost não disponível"
```bash
pip install xgboost
```

### Erro ao carregar dados reais
O sistema automaticamente usa dados simulados como fallback. Isso é normal se as APIs não estiverem disponíveis.

### Interface gráfica não abre
Use `--no-gui` para executar apenas o pipeline sem interface.

## Comandos Úteis

```bash
# Executar testes
pytest tests/ -v

# Ver ajuda completa
python run_pipeline.py --help

# Executar exemplo de uso
python example_usage.py
```

## Suporte

Consulte o `README.md` completo para mais detalhes.

