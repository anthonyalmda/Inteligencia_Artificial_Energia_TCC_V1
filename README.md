# Sistema de Previsão de Energia - TCC

Sistema completo de previsão de consumo e produção de energia com análise financeira e interface gráfica, desenvolvido para Trabalho de Conclusão de Curso sobre Inteligência Artificial aplicada à Geração Distribuída e Mercado Livre de Energia no Brasil.

## 🎯 Objetivo

Antecipar consumo e produção de energia sustentável (solar, eólica, etc.) para apoiar decisões de comercialização, maximizando lucros ao vender excedentes e minimizando custos ao comprar energia quando há déficit.

## 📋 Funcionalidades

- **Previsão de Consumo e Produção**: Modelos Prophet, SARIMAX e XGBoost
- **Integração com Dados Reais**: Conectores para INMET, ONS, CCEE, ANEEL e PVGIS
- **Análise Financeira**: Cálculo de lucro considerando PLD (Preço de Liquidação das Diferenças)
- **Motor de Decisão**: Regras simples e econômicas para compra/venda
- **Interface Gráfica**: Visualização interativa com filtros e gráficos
- **Engenharia de Features**: Lags, janelas móveis, features de calendário e climáticas

## 🏗️ Estrutura do Projeto

```
Inteligencia_Artificial_Energia_TCC_V1/
├── src/
│   ├── data/          # Conectores de dados (INMET, ONS, CCEE, ANEEL, PVGIS)
│   ├── features/      # Engenharia de atributos
│   ├── models/        # Modelos de previsão (consumo, produção, avaliação)
│   ├── finance/       # Análise financeira e cálculo de lucro
│   ├── rules/         # Motor de decisão
│   ├── viz/           # Visualizações e interface gráfica
│   └── config/        # Schemas Pydantic e configurações
├── config/
│   └── default.yaml   # Configurações padrão
├── tests/             # Testes pytest
├── results/           # Resultados gerados (CSV, Parquet, gráficos)
├── requirements_minimal.txt
└── run_pipeline.py    # Pipeline principal
```

## 🚀 Instalação

### 1. Instalar dependências

```bash
pip install -r requirements_minimal.txt
```

**Dependências principais:**
- pandas, numpy
- matplotlib
- scikit-learn, statsmodels
- prophet (Meta Prophet)
- xgboost
- pydantic
- requests, pyyaml

### 2. Configurar

Edite `config/default.yaml` conforme necessário:

```yaml
data:
  region: "SE"
  submercado: "SE"
  inmet_station: "A701"
  cache_dir: "data/raw"

model:
  horizon_days: 14
  algo_consumption: "prophet"
  algo_production: "xgboost"

finance:
  use_pld: true
  sell_price_brl_per_kwh: 0.75
  buy_price_brl_per_kwh: 0.90
  cost_rate: 0.10

decisions:
  buffer_kwh: 1.0
  pld_premium_threshold_brl_mwh: 50
```

## 💻 Uso

### Pipeline completo

```bash
python run_pipeline.py --horizon 14 --region SE --submercado SE
```

### Opções disponíveis

```bash
python run_pipeline.py --help
```

**Principais argumentos:**
- `--horizon`: Horizonte de previsão em dias (padrão: 14)
- `--region`: Região (SE, S, NE, N, CO)
- `--submercado`: Submercado (SE, S, NE, N)
- `--train-start`: Data inicial de treino (YYYY-MM-DD)
- `--train-end`: Data final de treino (YYYY-MM-DD)
- `--use-real-data`: Tentar usar dados reais (fallback para simulado)
- `--cache`: Usar cache de dados
- `--no-gui`: Não abrir interface gráfica
- `--output-dir`: Diretório para salvar resultados

### Exemplos

**Execução básica:**
```bash
python run_pipeline.py --horizon 7
```

**Com dados reais:**
```bash
python run_pipeline.py --horizon 14 --use-real-data --cache
```

**Período específico:**
```bash
python run_pipeline.py --train-start 2024-01-01 --train-end 2024-03-31 --horizon 14
```

**Com coordenadas para PVGIS:**
```bash
python run_pipeline.py --lat -23.5505 --lon -46.6333 --use-real-data
```

## 📊 Saídas

O pipeline gera:

1. **forecast_results.csv/parquet**: Tabela com previsões e análise financeira
   - Consumo, produção, excedente, déficit
   - Receitas, custos, lucro líquido
   - Decisões (Vender/Comprar/Neutro)

2. **Gráficos PNG**:
   - `forecast_comparison.png`: Consumo vs Produção
   - `surplus_deficit.png`: Excedente vs Déficit
   - `cumulative_profit.png`: Lucro acumulado
   - `pld_timeseries.png`: Evolução do PLD

3. **Interface Gráfica**: Abas com tabela, gráficos e resumo estatístico

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/

# Teste específico
pytest tests/test_profit.py -v
pytest tests/test_models.py -v
```

## 📡 Conectores de Dados

### Dados Reais (com fallback para simulado)

**APIs Implementadas e Funcionando:**
- ✅ **PVGIS**: Irradiação solar (API real funcionando)
- ✅ **OpenWeatherMap**: Clima completo (API real funcionando, requer chave gratuita)

**Estrutura Pronta (usando simulado):**
- ⚠️ **ONS**: Carga e geração de energia por região
- ⚠️ **CCEE**: PLD (Preço de Liquidação das Diferenças) diário/horário
- ✅ **ANEEL**: Dados de geração distribuída (funcionando)

**Nota**: PVGIS funciona automaticamente. Para OpenWeatherMap, adicione a chave em `config/default.yaml`. Para implementação completa de outras APIs, consulte `IMPLEMENTAR_APIS.md` e:

- INMET: https://portal.inmet.gov.br/
- ONS: https://dados.ons.org.br/
- CCEE: https://dadosabertos.ccee.org.br/
- PVGIS: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/

## 🔧 Desenvolvimento

### Estrutura Modular

- **data/**: Conectores isolados, fácil adicionar novas fontes
- **models/**: Modelos independentes, fácil trocar algoritmos
- **finance/**: Lógica financeira separada
- **rules/**: Motor de decisão configurável
- **viz/**: Visualizações reutilizáveis

### Adicionar Novo Modelo

1. Criar classe em `src/models/` com métodos `fit()` e `predict()`
2. Adicionar opção em `config/default.yaml`
3. Atualizar `run_pipeline.py` se necessário

### Adicionar Nova Fonte de Dados

1. Criar função em `src/data/` seguindo padrão dos conectores existentes
2. Adicionar fallback para dados simulados
3. Integrar em `src/data/loader.py`

## 📝 Licença

Trabalho de Conclusão de Curso - Uso acadêmico.

## 👤 Autor

Desenvolvido para TCC sobre Inteligência Artificial e Energia Sustentável.

## 🔗 Referências

- Portal INMET: https://portal.inmet.gov.br/
- Dados Abertos ONS: https://dados.ons.org.br/
- Dados Abertos CCEE: https://dadosabertos.ccee.org.br/
- PVGIS API: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/
