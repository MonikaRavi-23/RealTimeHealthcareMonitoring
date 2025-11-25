🏥 Real-Time Healthcare Monitoring System

A lightweight Python project that monitors patient vitals in real time using CSV files and raises alerts whenever abnormal values occur.

This system is perfect for:

Healthcare automation
Real-time anomaly detection
Patient monitoring dashboards
Academic or research projects

📘 README.md
# 🏥 Real-Time Healthcare Monitoring System  

A smart Python-based system that reads patient vitals, analyzes them, generates alerts, and logs data for future analysis. Simple, effective, and ready for expansion into a full dashboard or IoT-connected healthcare system.


## 📂 Files
- `app.py` → main program  
- `alerts.py` → alert detection logic  
- `alert_history.csv` → auto-created log file  
- `Patient_1_vitals.csv` etc. → patient data

## 🚀 Features

- 📊 Real-time vitals monitoring from CSV  
- 🚨 Automatic alert generation  
- 📝 Patient historical data logging  
- 👩‍⚕️ Multi-patient support  
- 💾 Lightweight CSV-based data pipeline  
- 🧠 Expandable for machine learning / AI  


## 📂 Project Structure



RealTimeHealthcareMonitoring/
│── app.py → Main runner script
│── alerts.py → Alert detection logic
│── requirements.txt → Project dependencies
│── alert_history.csv → System-level alert logs
│── Patient_*_vitals.csv → Multiple patient vitals
│── *_vitals_log.csv → Auto-generated log files
│── README.md → Documentation


## 🛠️ Installation

Install dependencies:
pip install -r requirements.txt

## ▶️ How to Run
python app.py

## 🧠 Logic Overview

1. System loads CSV containing vitals  
2. Checks vitals for abnormalities  
3. Logs warnings & critical alerts  
4. Updates history logs  

** Future Enhancements**

🤖 Machine-learning anomaly detection
📡 Live sensor integration
🖥️ Interactive dashboard
📈 Real-time charts
