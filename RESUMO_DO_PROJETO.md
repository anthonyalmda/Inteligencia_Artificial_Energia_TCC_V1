# RESUMO DO PROJETO - Inteligência Artificial e Energia Sustentável (TCC)

## VISÃO GERAL
Sistema de previsão de consumo e produção de energia com análise financeira e interface gráfica. O projeto permite antecipar a demanda e oferta de energia, calcular lucros/despesas decorrentes de excedentes (venda) e déficits (compra), e visualizar os resultados através de gráficos e uma interface desktop.

---

## OBJETIVO PRINCIPAL
Antecipar o consumo e produção de energia sustentável (solar, eólica, etc.) para apoiar decisões de comercialização, maximizando lucros ao vender excedentes e minimizando custos ao comprar energia quando há déficit.

---

## ESTRUTURA E FUNCIONALIDADES DO CÓDIGO

### 1. **CARREGAMENTO E GERAÇÃO DE DADOS** (`data_loader.py`)
- **Função**: Carrega dados históricos de consumo e produção de energia
- **Estratégias de carregamento** (em ordem de prioridade):
  1. Busca arquivos CSV em `src/data/raw/` (dados reais)
  2. Busca em `src/data/simulation/` (dados simulados pré-gerados)
  3. Gera dados simulados em memória se não encontrar arquivos
- **Dados simulados**: Usam funções seno/cosseno com ruído aleatório para simular padrões sazonais
- **Formato esperado**: CSVs com colunas `date` e `consumption`/`production` (em kWh)

### 2. **PRÉ-PROCESSAMENTO** (`preprocessing.py`)
- **Função**: Limpeza básica dos dados
- **Método**: Forward fill (preenche valores faltantes com o último valor válido)
- **Saída**: DataFrame limpo e sem valores nulos

### 3. **MODELOS DE PREVISÃO** (`model.py`)
- **ProductionForecaster**: Modelo simplificado para prever produção futura
  - Treino: Calcula a média dos últimos 10 valores de produção
  - Previsão: Retorna valores constantes iguais à tendência calculada
  - Nota: O modelo de consumo (`ConsumptionForecaster`) está referenciado mas não implementado no código atual

### 4. **MOTOR DE DECISÃO** (`engine.py`)
- **Função**: Define estratégias baseadas em médias de consumo e produção
- **Estratégias disponíveis**:
  - `"lucro"`: Recomenda "Vender excedente" se produção > consumo, senão "Comprar energia"
  - `"eficiencia"`: Recomenda balancear produção e consumo
  - Outras: Mantém estratégia atual
- **Nota**: Este módulo não está integrado no pipeline principal atualmente

### 5. **ANÁLISE FINANCEIRA** (`profit.py`)
- **Classe**: `ProfitCalculator`
- **Função**: Calcula lucro líquido considerando venda de excedentes e compra de energia
- **Parâmetros configuráveis**:
  - `sell_price`: Preço de venda do kWh excedente (padrão: R$ 0,75)
  - `buy_price`: Preço de compra quando há déficit (padrão: R$ 0,90)
  - `cost_rate`: Percentual de custo fixo sobre receita (padrão: 10%)
- **Lógica de cálculo**:
  - **Excedente (Produção > Consumo)**:
    - Excedente = Produção - Consumo
    - Receita = Excedente × preço_venda
    - Custo Fixo = Receita × taxa_custo
    - Lucro Líquido = Receita - Custo Fixo
    - Decisão: "Vender"
  - **Déficit (Consumo > Produção)**:
    - Déficit = Consumo - Produção
    - Custo Compra = Déficit × preço_compra
    - Custo Fixo = Custo Compra × taxa_custo
    - Lucro Líquido = -(Custo Compra + Custo Fixo) [negativo]
    - Decisão: "Comprar"
- **Saída**: DataFrame com colunas: Consumo, Produção, Excedente, Déficit, Receita Venda, Custo Compra, Lucro Líquido, Decisão

### 6. **MÉTRICAS DE AVALIAÇÃO** (`metrics.py`)
- **Função**: Calcula métricas para avaliar qualidade das previsões
- **Métrica disponível**: RMSE (Root Mean Squared Error) usando scikit-learn

### 7. **PIPELINE PRINCIPAL** (`run_pipeline.py`)
- **Função**: Orquestra todo o fluxo do sistema
- **Passos executados**:
  1. Cria pasta `results/` para armazenar saídas
  2. Define horizonte de previsão (padrão: 10 dias)
  3. Instancia modelos de consumo e produção
  4. Gera previsões para os próximos dias
  5. Calcula análise financeira usando `ProfitCalculator`
  6. Salva resultados em CSV (`results/forecast_results.csv`)
  7. Gera gráficos:
     - **Gráfico 1**: Linha temporal comparando Consumo vs Produção previstos
     - **Gráfico 2**: Barras mostrando Excedente (verde) vs Déficit (vermelho) por período
  8. Abre interface gráfica para visualização dos resultados
- **Problema conhecido**: Os imports referenciam estrutura de pastas `src/models/...` que não existe no projeto atual

### 8. **INTERFACE GRÁFICA** (`interface.py`)
- **Tecnologia**: Tkinter (GUI desktop nativa Python)
- **Função**: Exibe resultados de forma visual e interativa
- **Componentes**:
  - **Tabela (Treeview)**: Mostra todos os dados do DataFrame de resultados em formato tabular
  - **Gráfico integrado**: Exibe o gráfico de previsão (forecast_graph.png) diretamente na interface
- **Tamanho da janela**: 1600x800 pixels

### 9. **GERAÇÃO DE DADOS SIMULADOS** (`generate_simulated_data.py`)
- **Função**: Script standalone para gerar CSVs de exemplo
- **Uso**: `python generate_sim policed_data.py --out raw --days Ł20`
- **Parâmetros**:
  - `--out`: Onde salvar (`raw` ou `simulation`)
  - `--days`: Quantidade de dias a simular
  - `--seed`: Semente para reprodutibilidade
  - `--start`: Data inicial (formato YYYY-MM-DD)
- **Saída**: Dois CSVs (`consumption.csv` e `production.csv`) com dados simulados

### 10. **NOTEBOOKS JUPYTER**
- **data_exploration.ipynb**: Exploração e visualização dos dados históricos
- **model_training.ipynb**: Experimentos de treinamento e teste dos modelos (nota: também referencia estrutura `src/...` que não existe)

---

## FLUXO COMPLETO DO SISTEMA

```
1. DADOS
   └─> Carregamento (CSV real/simulado/geração in-memory)
   
2. PRÉ-PROCESSAMENTO
   └─> Limpeza e tratamento de valores faltantes
   
3. PREVISÃO
   ├─> Modelo de Consumo → Lista de valores previstos
   └─> Modelo de Produção → Lista de valores previstos
   
4. ANÁLISE FINANCEIRA
   └─> ProfitCalculator → DataFrame com excedente, déficit, receitas, custos, lucro
   
5. VISUALIZAÇÃO
   ├─> Gráficos salvos (PNG) em results/
   └─> Interface gráfica (Tkinter) exibindo tabela e gráficos
```

---

## TECNOLOGIAS UTILIZADAS

- **Python 3.x**
- **Pandas**: Manipulação de dados tabulares
- **NumPy**: Operações matemáticas e arrays
- **Matplotlib**: Geração de gráficos estáticos
- **Scikit-learn**: Métricas de avaliação (RMSE)
- **Tkinter**: Interface gráfica desktop (biblioteca padrão Python)

---

## DEPENDÊNCIAS NO REQUIREMENTS.TXT

O arquivo `requirements.txt` contém muitas dependências não utilizadas no código atual (TensorFlow, PyQt5, Flask, Eel, SpeechRecognition, etc.). As dependências essenciais são:
- pandas
- numpy
- matplotlib
- scikit-learn
- tkinter (geralmente já incluído no Python)

---

## PROBLEMAS CONHECIDOS / LIMITAÇÕES

1. **Estrutura de pastas inconsistente**: O código referencia `src/models/...` mas os arquivos estão na raiz do projeto
2. **Modelo de consumo ausente**: `ConsumptionForecaster` é importado mas não existe
3. **Inconsistência de nomes**: O `ProfitCalculator` usa nomes diferentes (maiúsculas vs minúsculas) nas colunas dependendo do cenário
4. **Modelos muito simplificados**: Os modelos de previsão atuais retornam valores constantes (média simples)
5. **DecisionEngine não integrado**: O módulo de decisão não é chamado no pipeline principal

---

## CASOS DE USO

1. **Operadores de energia solar/eólica**: Prever produção e decidir quando vender excedentes
2. **Gestores de microgeração**: Antecipar déficits para comprar energia antes de ocorrer
3. **Análise financeira**: Calcular ROI e lucro líquido esperado em diferentes cenários
4. **Planejamento**: Visualizar tendências e tomar decisões estratégicas baseadas em previsões

---

## ENTRADAS E SAÍDAS

### ENTRADAS:
- CSVs com dados históricos: `consumption.csv` e `production.csv` (colunas: `date`, `consumption`/`production`)
- Parâmetros financeiros: preços de venda/compra, taxa de custo

### SAÍDAS:
- `results/forecast_results.csv`: Tabela com previsões e análise financeira
- `results/forecast_graph.png`: Gráfico de linha (Consumo vs Produção)
- `results/excedente_deficit.png`: Gráfico de barras (Excedente vs Déficit)
- Interface gráfica interativa com tabela e visualizações

---

## PRÓXIMOS PASSOS SUGERIDOS

1. Implementar modelos de ML mais sofisticados (ARIMA, LSTM, Prophet)
2. Integrar o DecisionEngine no pipeline
3. Adicionar análise de ROI e payback
4. Implementar conexão com APIs de dados reais
5. Melhorar tratamento de sazonalidade e tendências
6. Adicionar validação cruzada e métricas de qualidade de previsão

