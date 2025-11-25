# 🔧 Como Implementar APIs Reais

## Implementação Prática - Passo a Passo

### 1. **CCEE - PLD (Mais Importante)** ⭐

**A API CKAN permite download direto:**

```python
# src/data/ccee.py - Implementação real
import requests
import pandas as pd

def fetch_pld_real(submercado, start, end, granularity="diario"):
    """Busca PLD real do CCEE."""
    base_url = "https://dadosabertos.ccee.org.br/api/3/action/datastore_search"
    
    # IDs dos datasets
    resource_ids = {
        "diario": {
            "SE": "b7638051-6d65-4e05-a7e6-2b8e1e5c8f5a",
            "S": "...",  # Buscar no catálogo
            "NE": "...",
            "N": "..."
        }
    }
    
    resource_id = resource_ids[granularity].get(submercado)
    if not resource_id:
        raise ValueError(f"Submercado {submercado} não encontrado")
    
    # Buscar dados
    params = {
        "resource_id": resource_id,
        "filters": json.dumps({
            "data": [f"{start}:{end}"]
        }),
        "limit": 10000
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()["result"]["records"]
    
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["data"])
    df["pld_brl_mwh"] = df["valor"].astype(float)
    
    return df[["timestamp", "pld_brl_mwh", "submercado"]]
```

**OU mais simples - Download CSV direto:**
```python
def fetch_pld_csv(submercado, start, end):
    """Download CSV direto do portal CCEE."""
    url = f"https://www.ccee.org.br/dados-e-analises/dados-pld"
    # Baixar CSV e processar
    # Implementação similar ao ANEEL que já funciona
```

---

### 2. **ONS - Carga/Geração**

```python
# src/data/ons.py - Implementação real
def fetch_ons_load_real(region, start, end):
    """Busca carga real do ONS via CKAN."""
    base_url = "https://dados.ons.org.br/api/3/action/datastore_search"
    
    # Buscar resource_id no catálogo ONS
    # https://dados.ons.org.br/dataset/carga-energia
    
    params = {
        "resource_id": "ons-carga-energia-id",  # Buscar no site
        "filters": json.dumps({"data": [f"{start}:{end}"]}),
        "limit": 10000
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()["result"]["records"]
    
    return pd.DataFrame(data)
```

---

### 3. **OpenWeatherMap (Clima)** ⭐ FÁCIL

**Passos:**
1. Cadastre-se: https://openweathermap.org/api
2. Obtenha API key grátis (1000 calls/dia)
3. Use:

```python
# src/data/openweather.py (novo arquivo)
import requests

def fetch_weather_owm(lat, lon, start, end, api_key):
    """Busca clima via OpenWeatherMap."""
    # Para histórico, usar One Call API 3.0
    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    
    dates = pd.date_range(start, end, freq='D')
    all_data = []
    
    for date in dates:
        params = {
            "lat": lat,
            "lon": lon,
            "dt": int(date.timestamp()),
            "appid": api_key
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        all_data.append({
            "timestamp": date,
            "temp_c": data["current"]["temp"] - 273.15,  # Kelvin para Celsius
            "ghi_wm2": data["current"].get("solar_irradiance", 0),
            "wind_ms": data["current"]["wind_speed"]
        })
    
    return pd.DataFrame(all_data)
```

**No código:**
```python
# config/default.yaml
openweather:
  api_key: "SUA_CHAVE_AQUI"  # Obter em openweathermap.org/api

# src/data/loader.py
from .openweather import fetch_weather_owm
# Usar se INMET falhar
```

---

### 4. **PVGIS (Já Preparado)**

O código já tem estrutura. Só implementar a requisição:

```python
# src/data/pvgis.py - Atualizar
def fetch_pvgis_ghi_real(lat, lon, start, end):
    """API real do PVGIS."""
    url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
    
    params = {
        "lat": lat,
        "lon": lon,
        "startyear": start.year,
        "endyear": end.year,
        "pvcalculation": 0,  # Só GHI, não PV
        "outputformat": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()["outputs"]["daily_profile"]
    
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["time"])
    df["ghi_wm2"] = df["G(i)"]
    
    return df[["timestamp", "ghi_wm2"]]
```

---

## ✅ Status Atual

**JÁ IMPLEMENTADO:**
- ✅ **PVGIS** - API real funcionando
- ✅ **OpenWeatherMap** - API real funcionando (requer chave)

**Para testar:**
```bash
# PVGIS (já funciona):
python run_pipeline.py --use-real-data --lat -23.5505 --lon -46.6333

# OpenWeatherMap (adicionar chave no config/default.yaml primeiro):
python run_pipeline.py --use-real-data --lat -23.5505 --lon -46.6333
```

**Próximos (opcional):**
- ⚠️ **CCEE PLD** - CSV direto (30 min) 
- ⚠️ **ONS** - Via CKAN (opcional)

---

## 📚 Links Úteis

- **CCEE CKAN API**: https://dadosabertos.ccee.org.br/api/3/action/help_show?name=datastore_search
- **ONS Datasets**: https://dados.ons.org.br/dataset/
- **OpenWeatherMap Docs**: https://openweathermap.org/api
- **PVGIS API**: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/api-non-interactive-service_en

---

## ⚠️ Nota

Para **uso acadêmico/TCC**, os dados simulados já são suficientes. 
Implemente APIs reais apenas se necessário para demonstração.

