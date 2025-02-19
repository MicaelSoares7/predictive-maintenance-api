import numpy as np

def calculate_anomaly_score(temperatura, vibracao, energia):
    """Calcula um score de anomalia baseado nos parâmetros do equipamento."""
    return np.mean([temperatura, vibracao, energia]) * 0.1