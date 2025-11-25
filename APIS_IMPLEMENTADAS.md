# ✅ APIs Implementadas

## Status das Implementações

### ✅ **PVGIS (Irradiação Solar)** - IMPLEMENTADO
- **API Real**: ✅ Funcionando
- **Endpoint**: https://re.jrc.ec.europa.eu/api/v5_2/seriescalc
- **Sem autenticação**: ✅
- **Status**: Pronto para uso
- **Fallback**: Dados simulados se API falhar

### ✅ **OpenWeatherMap (Clima)** - IMPLEMENTADO  
- **API Real**: ✅ Funcionando
- **Endpoint**: https://api.openweathermap.org/data/2.5/weather
- **Chave necessária**: ✅ (gratuita - obter em openweathermap.org/api)
- **Status**: Pronto para uso (requer chave no config)
- **Fallback**: PVGIS → INMET → Simulado

### ⚠️ **CCEE (PLD)** - ESTRUTURA PRONTA
- **Status**: Estrutura pronta, usando dados simulados
- **Próximo passo**: Implementar download CSV real do portal
- **Fallback**: Dados simulados

### ⚠️ **ONS (Carga/Geração)** - ESTRUTURA PRONTA
- **Status**: Estrutura pronta, usando dados simulados
- **Próximo passo**: Implementar download via CKAN
- **Fallback**: Dados simulados

### ✅ **ANEEL (GD)** -~~FUNCIONANDO~~
- **Status**: ✅ Já funciona (download CSV direto)
- **URL**: https://dadosabertos.aneel.gov.br/...

### ⚠️ **INMET** - FALLBACK
- **Status**: Usando dados simulados
- **Motivo**: API pública limitada, complexa
- **Alternativa**: OpenWeatherMap (preferida)

---

## Como Usar APIs Reais

### 1. **PVGIS** (Já funciona - sem configuração)
```bash
python run_pipeline.py --lat -23.5505 --lon -46.6333 --use-real-data
```

### 2. **OpenWeatherMap** (Precisa chave)
1. Obter chave: https://openweathermap.org/api
2. Editar `config/default.yaml`:
   ```yaml
   data:
     openweather_api_key: "SUA_CHAVE_AQUI"
   ```
3. Executar:
   ```bash
   python run_pipeline.py --lat -23.5505 --lon -46.6333 --use-real-data
   ```

### 3. **Prioridade de Clima**
1. OpenWeatherMap (se tiver chave)
2. PVGIS (automático se tiver lat/lon)
3. INMET (fallback)
4. Simulado (se tudo falhar)

---

## Resultado

**Status**: ✅ **2 APIs reais funcionando** (PVGIS + OpenWeatherMap)
**Fallback**: Sempre funciona com dados simulados se APIs falharem

