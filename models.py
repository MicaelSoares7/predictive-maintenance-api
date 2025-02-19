from pydantic import BaseModel

class EquipmentData(BaseModel):
    temperatura: float
    vibracao: float
    energia: float

class EquipmentReport(BaseModel):
    equipamento_id: int
    status: str
    previsao_falha: float
    recomendacoes: str