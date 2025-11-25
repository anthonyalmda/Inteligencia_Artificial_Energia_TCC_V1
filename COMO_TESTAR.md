# 🧪 Como Testar o Sistema

## ⚡ Teste Rápido - COMANDO MAIS SIMPLES

```bash
# Abra o terminal na pasta do projeto e execute:
python run_pipeline.py --horizon 7 --no-gui
```

Isso já testa tudo! ✅

---

## 📋 Testes Detalhados (5 minutos)

### 1. Teste Básico com Dados Simulados
```bash
python run_pipeline.py --horizon 7 --no-gui
```

**Resultado esperado:**
- ✅ Pipeline executa sem erros
- ✅ Arquivos gerados em `results/`
- ✅ CSV e gráficos PNG criados

---

### 2. Teste com PVGIS (API Real - Sem Configuração)

```bash
python run_pipeline.py \
  --use-real-data \
  --lat -23.5505 \
  --lon -46.6333 \
  --horizon 14 \
  --no-gui
```

**Coordenadas de exemplo:**
- São Paulo: `--lat -23.5505 --lon -46.6333`
- Rio de Janeiro: `--lat -22.9068 --lon -43.1729`
- Brasília: `--lat -15.7942 --lon -47.8822`

**Resultado esperado:**
- ✅ Mensagem: "✓ Dados PVGIS obtidos via API real"
- ✅ Dados reais de irradiação solar
- ✅ CSV e gráficos gerados

---

### 3. Teste com OpenWeatherMap (Requer Chave)

**Passo 1: Obter chावave**
1. Acesse: https://openweathermap.org/api
2. Cadastre-se (grátis)
3. Copie sua chave API

**Passo 2: Configurar**
Edite `config/default.yaml`:
```yaml
data:
  openweather_api_key: "COLE_SUA_CHAVE_AQUI"
```

**Passo 3: Testar**
```bash
python run_pipeline.py \
  --use-real-data \
  --lat -23.5505 \
  --lon -46.6333 \
  --horizon 14 \
  --no-gui
```

**Resultado esperado:**
- ✅ Mensagem: "✓ Dados climáticos obtidos via OpenWeatherMap"
- ✅ Dados reais de temperatura, vento, etc.

---

### 4. Teste Completo com Interface Gráfica

```bash
python run_pipeline.py --horizon 7
```

**Resultado esperado:**
- ✅ Pipeline executa
- ✅ Interface gráfica abre
- ✅ Abas: Dados, Gráficos, Resumo
- ✅ Filtros funcionando
- ✅ Exportação CSV funcionando

---

## 📋 Verificar Resultados

Após executar, verifique:

### Arquivos Gerados (`results/`):
```bash
ls results/
# Deve ter:
# - forecast_results.csv
# - forecast_results.parquet
# - forecast_comparison.png
# - surplus_deficit.png
# - cumulative_profit.png
```

### Conteúdo do CSV:
```bash
python -c "import pandas as pd; df = pd.read_csv('results/forecast_results.csv'); print(df.head()); print(f'\nTotal: {len(df)} registros')"
```

### Verificar se APIs funcionaram:
```bash
# Procurar mensagens no output:
grep "✓ Dados" output.log  # ou ver no terminal
```

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements_minimal.txt
```

### Erro: "Prophet não disponível"
```bash
pip install prophet
```
(O sistema funciona com baseline se Prophet não estiver instalado)

### Erro: API não funciona
**Normal!** O sistema usa fallback automático. Verifique:
1. Internet conectada?
2. Para OpenWeatherMap: chave configurada?
3. Para PVGIS: coordenadas válidas?

### Interface não abre
```bash
# Use --no-gui para executar sem interface
python run_pipeline.py --no-gui
```

---

## 🧪 Testes Automatizados

```bash
# Executar testes pytest
pytest tests/ -v

# Teste específico
pytest tests/test_profit.py -v
pytest tests/test_models.py -v
```

---

## 📊 Exemplos de Saída Esperada

### Saída do Pipeline:
```
📊 Pipeline de Previsão de Energia
============================================================
Região: SE
Submercado: SE
Período de treino: 2024-01-01 a 2024-04-01
Horizonte de previsão: 14 dias
============================================================

[1/7] Carregando dados...
✓ Dados PVGIS obtidos via API real
✓ Dados carregados: 90 registros

[2/7] Preparando dados...
✓ Dados preparados: 90 registros, 15 colunas

[3/7] Treinando modelos...
✓ Modelo de consumo treinado (baseline)
✓ Modelo de produção treinado (baseline)

[4/7] Gerando previsões...
✓ Previsões geradas: 14 períodos

[5/7] Preparando PLD para análise financeira...

[6/7] Calculando análise financeira...
✓ Análise financeira concluída
✓ Decisões geradas: {'Vender': 8, 'Comprar': 6}

[7/7] Salvando resultados...
✓ CSV salvo: results/forecast_results.csv
✓ Parquet salvo: results/forecast_results.parquet
✓ Gráficos salvos em results

============================================================
📈 RESUMO DOS RESULTADOS
============================================================
Lucro líquido total: R$ 125.50
Excedente total: 45.20 kWh
Déficit total: 28.30 kWh
Decisões: {'Vender': 8, 'Comprar': 6}
============================================================

✅ Pipeline concluído com sucesso!
```

---

## ✅ Checklist de Testes

- [ ] Pipeline básico executa
- [ ] Arquivos gerados em `results/`
- [ ] CSV tem dados corretos
- [ ] Gráficos PNG criados
- [ ] PVGIS funciona (se usar --lat --lon)
- [ ] OpenWeatherMap funciona (se tiver chave)
- [ ] Interface gráfica abre
- [ ] Testes pytest passam
- [ ] Fallback funciona (sem internet/APIs)

---

## 🚀 Próximos Passos

Após testar:
1. Analisar resultados em `results/forecast_results.csv`
2. Visualizar gráficos gerados
3. Explorar interface gráfica
4. Testar diferentes regiões/coordenadas
5. Ajustar configurações em `config/default.yaml`

---

## 💡 Dicas

- Use `--no-gui` para testes rápidos
- Use `--cache` para acelerar testes repetidos
- PVGIS funciona melhor com coordenadas reais
- OpenWeatherMap tem limite de 1000 calls/dia (gratuito)

