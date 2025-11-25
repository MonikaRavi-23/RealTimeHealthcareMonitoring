import csv
import os
from datetime import datetime

def check_alert(vitals, patient_id="1"):
    alerts = []
    severity = "Normal"

    
    if vitals["Heart_Rate"] < 50 or vitals["Heart_Rate"] > 120:
        alerts.append(f"Heart Rate abnormal ({vitals['Heart_Rate']} bpm)")
        severity = "Critical"

   
    if vitals["Systolic_BP"] < 90 or vitals["Systolic_BP"] > 140:
        alerts.append(f"Systolic BP abnormal ({vitals['Systolic_BP']} mmHg)")
        severity = "Critical"

    if vitals["Diastolic_BP"] < 60 or vitals["Diastolic_BP"] > 90:
        alerts.append(f"Diastolic BP abnormal ({vitals['Diastolic_BP']} mmHg)")
        if severity != "Critical":
            severity = "Warning"

   
    if vitals.get("SpO2", 100) < 92:
        alerts.append(f"Low SpO₂ ({vitals['SpO2']}%)")
        severity = "Critical"

    
    if vitals.get("Temperature", 37) < 35 or vitals.get("Temperature", 37) > 38:
        alerts.append(f"Temperature abnormal ({vitals['Temperature']} °C)")
        if severity != "Critical":
            severity = "Warning"

    
    if not alerts:
        summary = f" Patient {patient_id}: All vitals normal"
        severity = "Normal"
    else:
        summary = f" Patient {patient_id}: " + " | ".join(alerts)

   
    file_exists = os.path.isfile('alert_history.csv')
    with open('alert_history.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Patient_ID", "Severity", "Message"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), patient_id, severity, " | ".join(alerts) if alerts else "Normal"])

    return summary, severity
