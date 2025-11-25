# 🔑 Como Obter Chaves de API

## OpenWeatherMap (Recomendado para Clima) ⭐

**Por quê?**: Mais fácil que INMET, API bem documentada, 1000 calls/dia grátis.

### Passos:
1. Acesse: https://openweathermap.org/api
2. Clique em "Sign Up" (canto superior direito)
3. Crie conta gratuita
4. Confirme email
5. Vá em "API keys" no dashboard
6. Copie a chave (começa com algo como `abc123def456...`)
7. Adicione no `config/default.yaml`:

```yaml
openweather:
  api_key: "SUA_CHAVE_AQUI"
```

**Pronto!** ✅ Sem custos no plano gratuito.

---

## Outras APIs (Não Precisam Chave)

### CCEE - PLD
- **Não precisa chave** ✅
- Download direto de CSV do portal
- Link: https://www.ccee.org.br/dados-e-analises/dados-pld

### ONS - Carga
- **Não precisa chave** ✅
- Dados abertos CKAN
- Link: https://dados.ons.org.br/

### PVGIS - GHI
- **Não precisa chave** ✅
- API pública
- Já implementado no código

### ANEEL - GD
- **Não precisa chave** ✅
- CSV direto (já funciona!)

---

## ⚡ Resumo Rápido

**APIs já funcionando:**
1. ✅ **PVGIS** - Funciona sem configuração (irradiação solar)
2. ✅ **OpenWeatherMap** - Precisa chave gratuita (clima completo)

**Para usar dados reais:**
- **PVGIS**: Já funciona! Use `--lat` e `--lon`
- **OpenWeatherMap**: Adicione chave no `config/default.yaml` (2 min para obter)

**Teste rápido:**
```bash
# PVGIS (já funciona):
python run_pipeline.py --use-real-data --lat -23.5505 --lon -46.6333

# Com OpenWeatherMap (após adicionar chave):
python run_pipeline.py --use-real-data --lat -23.5505 --lon -46.6333
```

**Tempo total**: 2 minutos para OpenWeatherMap (opcional)

**Status**: ✅ 2 APIs reais funcionando! Dados simulados sempre como fallback.

