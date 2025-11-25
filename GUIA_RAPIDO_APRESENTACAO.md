# GUIA RÁPIDO PARA APRESENTAÇÃO DO TCC
## Cheat Sheet - Estudo e Apresentação

---

## 🎯 RESUMO EXECUTIVO (30 segundos)

**O que é?** Sistema de IA que prevê consumo e produção de energia para unidades de Geração Distribuída, calcula lucros e decide automaticamente quando vender/comprar energia.

**Resultado principal:** Lucro de R$ 64,17 em 30 dias, ROI de 294%, com previsões de qualidade (MAE < 11 kWh, MAPE < 10%).

---

## 📊 NÚMEROS PRINCIPAIS (Memorizar)

### Melhor Cenário (04_horizon_30)
- **Lucro Total**: R$ 64,17
- **ROI**: 294,10%
- **Lucro Médio**: R$ 2,14/dia
- **Excedente**: 274,25 kWh
- **Decisões**: 76,7% vender, 23,3% comprar

### Qualidade das Previsões
- **MAE Consumo**: 10,88 kWh ✅ (Bom: < 10)
- **MAPE Consumo**: 9,89% ✅ (Bom: < 10%)
- **MAE Produção**: 11,46 kWh ✅ (Aceitável: 10-20)
- **MAPE Produção**: 8,97% ✅ (Bom: < 10%)

### Comparação de Cenários
- **Horizonte 7 dias**: R$ 28,64 (lucro médio maior: R$ 4,09)
- **Horizonte 14 dias**: R$ 50,07 (baseline)
- **Horizonte 30 dias**: R$ 64,17 ⭐ (melhor lucro total)

---

## 🏗️ ARQUITETURA (3 Componentes Principais)

1. **PREVISÃO** → Modelos (Baseline, Prophet, XGBoost)
2. **ANÁLISE FINANCEIRA** → Cálculo de lucros com PLD
3. **DECISÃO AUTOMATIZADA** → Vender/Comprar/Neutro

**Fluxo**: Dados → Modelos → Previsões → Análise Financeira → Decisão → Visualização

---

## 🔧 TECNOLOGIAS (Stack)

**Core:**
- Python 3.x
- Pandas, NumPy
- Scikit-learn (métricas)
- Prophet (previsão)
- Matplotlib (gráficos)

**APIs:**
- PVGIS (irradiação solar)
- CCEE (PLD)
- ONS (carga/geração)
- ANEEL (GD)
- OpenWeatherMap (clima)

---

## 📈 RESULTADOS POR CENÁRIO (Top 3)

| Cenário | Lucro Total | ROI | Excedente | Destaque |
|---------|-------------|-----|-----------|----------|
| **04_horizon_30** | R$ 64,17 | 294% | 274 kWh | ⭐ Melhor resultado |
| **01_baseline** | R$ 50,07 | 5.952% | 159 kWh | Baseline sólido |
| **03_horizon_7** | R$ 28,64 | - | 89 kWh | Lucro médio maior |

---

## ✅ PONTOS FORTES (Argumentos)

1. **Robustez**: Validação automática de dados, fallback inteligente
2. **Metodologia**: Validação temporal, múltiplas métricas (MAE, RMSE, MAPE, R²)
3. **Integração**: APIs reais (PVGIS, CCEE, ONS, ANEEL)
4. **Viabilidade**: ROI positivo demonstrado, lucros consistentes
5. **Modularidade**: Estrutura extensível, fácil manutenção

---

## ⚠️ LIMITAÇÕES (Ser Transparente)

1. **Modelos Baseline**: R² baixo, necessitam otimização
2. **APIs PVGIS**: Problemas de escala detectados (valores anômalos)
3. **Validação**: Apenas dados históricos, não futuros reais
4. **Análise Financeira**: Simplificada, pode ser expandida

**Trabalhos Futuros**: Otimizar Prophet/XGBoost, validar em dados reais, expandir análise financeira

---

## 🎤 ROTEIRO DE APRESENTAÇÃO (12 minutos)

### 1. INTRODUÇÃO (2 min)
- Problema: GD precisa otimizar compra/venda
- Solução: Sistema integrado de IA
- Objetivo: Maximizar lucros

### 2. METODOLOGIA (3 min)
- Arquitetura: 3 componentes (Previsão → Análise → Decisão)
- Modelos: Baseline, Prophet, XGBoost
- Validação: MAE, RMSE, MAPE, R²
- Integração: APIs reais

### 3. RESULTADOS (4 min)
- **Melhor cenário**: R$ 64,17, ROI 294%
- **Qualidade**: MAE < 11 kWh, MAPE < 10%
- **9 cenários testados**: Comparação completa
- **Gráficos**: Mostrar visualizações

### 4. CONCLUSÕES (2 min)
- Viabilidade demonstrada
- Potencial comercial
- Trabalhos futuros

### 5. DEMONSTRAÇÃO (1 min)
- Executar pipeline
- Mostrar resultados

---

## 💡 FRASES-CHAVE (Memorizar)

**Abertura:**
> "Desenvolvi um sistema integrado de Inteligência Artificial que prevê consumo e produção de energia para unidades de Geração Distribuída, calcula lucros considerando o PLD e decide automaticamente quando vender ou comprar energia."

**Resultado Principal:**
> "O melhor cenário alcançou lucro de R$ 64,17 em 30 dias, com ROI de 294%, e previsões de qualidade com erro médio absoluto inferior a 11 kWh."

**Qualidade:**
> "As previsões apresentaram MAE de 10,88 kWh e MAPE de 9,89%, ambos dentro das faixas consideradas aceitáveis para aplicação prática."

**Viabilidade:**
> "O sistema demonstrou viabilidade técnica e financeira, com ROI positivo em múltiplos cenários e estrutura modular que permite extensão para diferentes contextos operacionais."

---

## 📁 ARQUIVOS IMPORTANTES

**Para Apresentação:**
- `results/tcc_coleta_completa/04_horizon_30/forecast_comparison.png`
- `results/tcc_coleta_completa/04_horizon_30/cumulative_profit.png`
- `results/tcc_coleta_completa/metricas_comparativas.xlsx`

**Para Estudo:**
- `RESUMO_TECNICO_TCC.md` (este arquivo completo)
- `results/tcc_coleta_completa/ANALISE_METRICAS.md`
- `CONSIDERACOES_FINAIS.md`

**Código:**
- `run_pipeline.py` (pipeline principal)
- `src/` (estrutura modular)

---

## 🎯 PERGUNTAS PROVÁVEIS E RESPOSTAS

**Q: Por que alguns cenários têm lucro negativo?**
R: Cenários com dados PVGIS apresentaram problemas de escala (valores anômalos detectados automaticamente). Cenários com treino muito curto ou muito longo também tiveram performance ruim, indicando necessidade de ajuste de hiperparâmetros.

**Q: Os modelos são adequados para produção?**
R: Modelos baseline são adequados para demonstração metodológica. Para produção comercial, é necessário otimizar Prophet e XGBoost com validação cruzada temporal.

**Q: Como o sistema lida com falhas de API?**
R: Sistema tem fallback automático para dados simulados. Validação automática detecta valores anômalos e emite avisos, mas continua processando.

**Q: Qual a precisão das previsões?**
R: MAE médio de ~11 kWh e MAPE de ~10%, dentro de faixas aceitáveis. R² baixo indica necessidade de modelos mais sofisticados para variabilidade complexa.

**Q: O sistema considera variações horárias do PLD?**
R: Atualmente considera PLD diário. Expansão para PLD horário é trabalho futuro, permitindo análise mais granular.

---

## 🚀 COMANDOS PARA DEMONSTRAÇÃO

```bash
# Executar melhor cenário
python run_pipeline.py --horizon 30 --region SE

# Ver resultados
cd results/tcc_coleta_completa/04_horizon_30
# Abrir gráficos PNG e forecast_results.csv
```

---

## 📊 MÉTRICAS PARA CITAR

**Financeiras:**
- Lucro Total: R$ 64,17
- ROI: 294,10%
- Lucro Médio: R$ 2,14/dia
- Excedente: 274,25 kWh

**Qualidade:**
- MAE: 10,88 kWh (consumo), 11,46 kWh (produção)
- MAPE: 9,89% (consumo), 8,97% (produção)
- RMSE: 14,32 kWh (consumo), 14,12 kWh (produção)

**Decisões:**
- 76,7% vendas, 23,3% compras
- 0% neutro (sistema sempre decide)

---

## 🎓 CONCEITOS TÉCNICOS (Definições Rápidas)

**MAE (Mean Absolute Error)**: Erro médio absoluto em kWh. Quanto menor, melhor. < 10 kWh é bom.

**MAPE (Mean Absolute Percentage Error)**: Erro percentual. Independente da escala. < 10% é bom.

**R² (Coeficiente de Determinação)**: Qualidade do ajuste. 1.0 = perfeito, > 0.7 = bom, < 0 = ruim.

**PLD (Preço de Liquidação das Diferenças)**: Preço de referência para compra/venda de energia no mercado livre.

**ROI (Return on Investment)**: Retorno sobre investimento. Percentual de lucro sobre custo.

---

## ✅ CHECKLIST PRÉ-APRESENTAÇÃO

- [ ] Ler `RESUMO_TECNICO_TCC.md` completo
- [ ] Memorizar números principais
- [ ] Preparar gráficos para slides
- [ ] Testar execução do pipeline
- [ ] Preparar respostas para perguntas frequentes
- [ ] Revisar estrutura de arquivos
- [ ] Preparar demonstração ao vivo (opcional)

---

**BOA SORTE NA APRESENTAÇÃO! 🚀**




