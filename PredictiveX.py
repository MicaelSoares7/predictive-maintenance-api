from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import sqlite3
import requests
import uuid
import logging
from contextlib import closing
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Configuração de logging
logging.basicConfig(filename="api_logs.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Configuração do banco de dados
def init_db():
    with closing(sqlite3.connect("equipments.db")) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS equipment (
                          id TEXT PRIMARY KEY, 
                          temperatura REAL, 
                          vibracao REAL, 
                          energia REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS thresholds (
                          equip_id TEXT PRIMARY KEY,
                          temperatura REAL, 
                          vibracao REAL, 
                          energia REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS erp_config (
                          equip_id TEXT PRIMARY KEY,
                          webhook_url TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS api_keys (
                          key TEXT PRIMARY KEY)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS equipment_history (
                          id TEXT,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                          temperatura REAL, 
                          vibracao REAL, 
                          energia REAL)''')
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_equipment_id ON equipment (id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_thresholds_id ON thresholds (equip_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_erp_id ON erp_config (equip_id)")

init_db()

class EquipmentData(BaseModel):
    temperatura: float
    vibracao: float
    energia: float

class ThresholdConfig(BaseModel):
    temperatura: float
    vibracao: float
    energia: float

class ERPConfig(BaseModel):
    webhook_url: str

def verify_api_key(x_api_key: str = Header(...)):
    with closing(sqlite3.connect("equipments.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key FROM api_keys WHERE key = ?", (x_api_key,))
        if not cursor.fetchone():
            logging.warning(f"Tentativa de acesso com chave de API inválida: {x_api_key}")
            raise HTTPException(status_code=403, detail="Chave de API inválida")

def generate_api_key():
    return str(uuid.uuid4())

@app.post("/api_keys/generate")
def create_api_key():
    new_key = generate_api_key()
    with closing(sqlite3.connect("equipments.db")) as conn, conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO api_keys (key) VALUES (?)", (new_key,))
    logging.info("Nova chave de API gerada")
    return {"api_key": new_key}

@app.get("/api_keys/list")
def list_api_keys():
    with closing(sqlite3.connect("equipments.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key FROM api_keys")
        keys = [row[0] for row in cursor.fetchall()]
    return {"api_keys": keys}

@app.delete("/api_keys/delete/{key}")
def delete_api_key(key: str):
    with closing(sqlite3.connect("equipments.db")) as conn, conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM api_keys WHERE key = ?", (key,))
    logging.info(f"Chave de API removida: {key}")
    return {"message": "API Key removida"}

def get_thresholds(equip_id):
    with closing(sqlite3.connect("equipments.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT temperatura, vibracao, energia FROM thresholds WHERE equip_id = ?", (equip_id,))
        row = cursor.fetchone()
    
    return {"temperatura": row[0], "vibracao": row[1], "energia": row[2]} if row else {"temperatura": 100, "vibracao": 10, "energia": 500}

def get_erp_webhook(equip_id):
    with closing(sqlite3.connect("equipments.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT webhook_url FROM erp_config WHERE equip_id = ?", (equip_id,))
        row = cursor.fetchone()
    return row[0] if row else None

def detect_anomaly(data, thresholds):
    return {param: value for param, value in data.dict().items() if value > thresholds[param]}

def send_notification(equip_id, anomalies):
    webhook_url = get_erp_webhook(equip_id)
    if webhook_url:
        payload = {"equip_id": equip_id, "anomalias": anomalies}
        try:
            requests.post(webhook_url, json=payload)
            logging.info(f"Notificação enviada para {equip_id}: {anomalies}")
        except Exception as e:
            logging.error(f"Erro ao enviar notificação: {e}")

@app.get("/")
def read_root():
    return {"message": "API de Diagnóstico Preventivo Ativa"}

@app.post("/equipamento/{equip_id}/treinar_modelo")
def treinar_modelo():
    with closing(sqlite3.connect("equipments.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT temperatura, vibracao, energia FROM equipment_history")
        dados = cursor.fetchall()
    
    if not dados:
        raise HTTPException(status_code=400, detail="Dados insuficientes para treinamento")
    
    X = np.array(dados)
    y = (X[:, 0] > 80).astype(int)
    modelo = RandomForestClassifier()
    modelo.fit(X, y)
    joblib.dump(modelo, "modelo_ia.pkl")
    return {"message": "Modelo treinado com sucesso"}

@app.post("/equipamento/{equip_id}/prever_falha")
def prever_falha(equip_id: str, dados: EquipmentData):
    try:
        modelo = joblib.load("modelo_ia.pkl")
        X_novo = np.array([[dados.temperatura, dados.vibracao, dados.energia]])
        previsao = modelo.predict(X_novo)
        return {"equip_id": equip_id, "falha_prevista": bool(previsao[0])}
    except Exception as e:
        logging.error(f"Erro ao prever falha: {e}")
        raise HTTPException(status_code=500, detail="Erro ao prever falha")
