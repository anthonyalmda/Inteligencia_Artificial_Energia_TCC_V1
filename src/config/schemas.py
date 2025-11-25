"""Schemas Pydantic para validação de dados."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EnergySample(BaseModel):
    """Schema para amostra de energia."""
    timestamp: datetime
    region: str = Field(..., description="Região (SE, S, NE, N, CO)")
    consumption_kwh: float = Field(..., ge=0, description="Consumo em kWh")
    production_kwh: float = Field(..., ge=0, description="Produção em kWh")
    temp_c: Optional[float] = Field(None, description="Temperatura em Celsius")
    wind_ms: Optional[float] = Field(None, ge=0, description="Velocidade do vento em m/s")
    ghi_wm2: Optional[float] = Field(None, ge=0, description="Irradiação solar global horizontal em W/m²")
    pld_brl_mwh: Optional[float] = Field(None, ge=0, description="PLD em R$/MWh")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class FinanceParams(BaseModel):
    """Parâmetros financeiros para cálculo de lucro."""
    sell_price_brl_per_kwh: float = Field(0.75, ge=0, description="Preço de venda em R$/kWh")
    buy_price_brl_per_kwh: float = Field(0.90, ge=0, description="Preço de compra em R$/kWh")
    cost_rate: float = Field(0.10, ge=0, le=1, description="Taxa de custo fixo (0-1)")
    submercado: str = Field("SE", description="Submercado")
    use_pld: bool = Field(True, description="Usar PLD quando disponível")

