# 🌐 APIs Disponíveis para Dados Reais

## 📊 Fontes Brasileiras (Gratuitas)

### 1. **CCEE - Dados Abertos** ⭐ MELHOR OPÇÃO
- **Site**: https://dadosabertos.ccee.org.br/
- **PLD Diário**: https://dadosabertos.ccee.org.br/dataset/pld_diario
- **PLD Horário**: https://dadosabertos.ccee.org.br/dataset/pld_horario
- **API**: CKAN (download direto de CSV/JSON)
- **Sem autenticação necessária**
- **Implementação**: Baixar CSV ou usar API CKAN

### 2. **ONS - Dados Abertos** ⭐ BOA OPÇÃO
- **Site**: https://dados.ons.org.br/
- **Catálogo**: https://dados.ons.org.br/dataset/
- **Carga**: https://dados.ons.org.br/dataset/carga-energia
- **API**: CKAN (download direto)
- **Sem autenticação necessária**
- **Implementação**: Baixar CSV ou usar API CKAN

### 3. **ANEEL - Dados Abertos** ✅ JÁ FUNCIONA
- **Site**: https://dadosabertos.aneel.gov.br/
- **GD**: CSV direto já implementado
- **URL**: https://dadosabertos.aneel.gov.br/dataset/.../download/empreendimento-geracao-distribuida.csv
- **Status**: ✅ Já funciona no código!

### 4. **INMET** ⚠️ COMPLEXO
- **Site**: https://portal.inmet.gov.br/
- **API Tempo**: https://tempo.inmet.gov.br/ (limitada)
- **Problema**: API pública é limitada, dados históricos requerem cadastro
- **Alternativa**: Usar OpenWeatherMap (gratuita, 1000 calls/dia)

### 5. **PVGIS** ✅ BOM PARA GHI
- **Site**: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/
- **API**: https://re.jrc.ec.europa.eu/api/v5_2/
- **Sem autenticação**
- **Implementação**: POST requests com lat/lon

---

## 🚀 Implementação Rápida - 3 Opções

### **Opção 1: CCEE + ONS (Mais Fácil)** ⭐ RECOMENDADO
```python
# Ambos usam CKAN, download direto de CSV
# Não precisa autenticação
# Dados atualizados diariamente
```

### **Opção 2: OpenWeatherMap (Para Clima)** 
- **API Key gratuita**: https://openweathermap.org/api
- **1000 calls/dia grátis**
- **Dados de GHI, temperatura, vento**
- **Fácil integração**

### **Opção 3: Solcast (Para GHI)**
- **API gratuita**: https://solcast.com/
- **Dados de irradiação solar**
- **API Toolkit gratuito**

---

## 💡 Recomendação Prática

**Para seu TCC, use:**
1. ✅ **CCEE** (PLD) - Implementar download CSV
2. ✅ **ONS** (Carga) - Implementar download CSV  
3. ✅ **OpenWeatherMap** (Clima) - API simples, chave gratuita
4. ✅ **PVGIS** (GHI) - API já preparada no código

**Tempo estimado**: 2-3 horas para implementar as 4 fontes.

---

## 📝 Como Implementar

Veja arquivo `IMPLEMENTAR_APIS.md` para código pronto.

