# 🚀 Predictive Maintenance API for Industrial Equipment  

**An AI-powered solution to monitor, analyze, and predict failures in industrial equipment.**  
Integrating IoT sensors and ERP systems, this API processes real-time data to detect anomalies and prevent failures before they occur—reducing costs and downtime.  

---

## ✨ Key Features  

✅ **Real-Time Monitoring** – Collect and analyze sensor data, including temperature, vibration, and energy consumption.  
✅ **AI-Powered Failure Prediction** – Machine learning algorithms identify patterns and anticipate mechanical failures.  
✅ **Detailed Reports** – Generate insights and statistics for each piece of equipment.  
✅ **Custom Configuration** – Adjust thresholds and limits based on your operational needs.  
✅ **Seamless Integration** – Designed to work with ERP systems and industrial platforms.  
✅ **Secure Authentication** – API key-based access for enhanced security.  

---

## 🔧 Installation  

To run this API locally, follow these steps:  

### 1️⃣ Clone this repository  

```bash
git clone https://github.com/MicaelSoares7/predictive-maintenance-api.git
cd predictive-maintenance-api
```

### 2️⃣ Create a virtual environment (optional but recommended)  

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3️⃣ Install dependencies  

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the API  

```bash
uvicorn api-diagnostico-preventivo:app --reload
```

The API will be available at: `predictive-maintenance-api.up.railway.app`  

---

## 📌 API Endpoints  

### 🟢 Add Equipment Data  

```http
POST /equipamento/{equip_id}/dados
```

#### 🔹 Request Example  

```json
{
  "temperatura": 75.5,
  "vibracao": 4.2,
  "energia": 450.0
}
```

#### 🔹 Response Example  

```json
{
  "message": "Data received successfully",
  "status": "OK"
}
```

---

### 📊 Get Equipment Report  

```http
GET /equipamento/{equip_id}/relatorio
```

#### 🔹 Response Example  

```json
{
  "equipamento_id": "123",
  "historico": [
    {"temperatura": 75.5, "vibracao": 4.2, "energia": 450.0, "timestamp": "2025-02-19T12:00:00"}
  ],
  "status": "Normal",
  "previsao_falha": false
}
```

---

### ⚙️ Configure Equipment Limits  

```http
POST /equipamento/{equip_id}/configurar_limites
```

#### 🔹 Request Example  

```json
{
  "temperatura_max": 100,
  "vibracao_max": 5.0,
  "energia_max": 500
}
```

#### 🔹 Response Example  

```json
{
  "message": "Thresholds updated successfully",
  "status": "OK"
}
```

---

## 🔐 Authentication  

To use this API, include an **API Key** in the request headers:  

```json
{
  "x-api-key": "your-api-key-here"
}
```

---

## 🚀 Business Benefits  

🔹 **Lower maintenance costs** – Reduce unplanned downtime and avoid costly repairs.  
🔹 **Increased equipment availability** – Minimize operational disruptions.  
🔹 **Optimized production efficiency** – Enhance performance and reduce waste.  
🔹 **Scalable and flexible** – Easily integrates with existing industrial platforms.  

💡 **Available as a REST API for seamless integration.**  

---

## 📩 Get in Touch  

Have questions or need support? Feel free to reach out!  

---
