import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import random
from collections import deque
from alerts import check_alert
import csv
import os


PATIENTS = ["Patient_1", "Patient_2", "Patient_3"]
data_dict = {p: deque(maxlen=50) for p in PATIENTS}  
alert_history = deque(maxlen=50)  

app = dash.Dash(__name__)
app.title = "Multi-Patient Real-Time Healthcare Monitoring"

app.layout = html.Div([
    html.H1("Multi-Patient Real-Time Healthcare Monitoring", style={'textAlign': 'center'}),
    
    # Patient selection tabs
    dcc.Tabs(id='patient-tabs', value=PATIENTS[0],
             children=[dcc.Tab(label=p, value=p) for p in PATIENTS]),
    
    html.Div(id='patient-content'),

    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)  # update every second
])


def generate_vitals():
    data = {
        "Heart_Rate": random.randint(60, 100),
        "Systolic_BP": random.randint(90, 140),
        "Diastolic_BP": random.randint(60, 90),
        "SpO2": random.randint(95, 100),
        "Temperature": round(random.uniform(36.0, 37.5), 1),
        "Timestamp": pd.Timestamp.now()
    }
    # Occasionally introduce abnormal values
    if random.random() < 0.05:
        data["Heart_Rate"] = random.randint(40, 50)
    if random.random() < 0.05:
        data["SpO2"] = random.randint(85, 91)
    if random.random() < 0.05:
        data["Temperature"] = round(random.uniform(38.5, 39.5), 1)
    return data


@app.callback(
    Output('patient-content', 'children'),
    [Input('patient-tabs', 'value'),
     Input('interval-component', 'n_intervals')]
)
def render_patient_tab(selected_patient, _):
    vitals = generate_vitals()
    data_dict[selected_patient].append(vitals)
    df = pd.DataFrame(data_dict[selected_patient])

    # Ensure Timestamp is datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # --- Log vitals ---
    file_name = f"{selected_patient}_vitals.csv"
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=vitals.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(vitals)

    # --- Check alerts ---
    alert_text, severity = check_alert(vitals, patient_id=selected_patient)
    alert_history.appendleft({
        "Timestamp": vitals["Timestamp"].strftime("%H:%M:%S"),
        "Patient_ID": selected_patient,
        "Severity": severity,
        "Message": alert_text
    })

    # --- Graphs ---
    hr_fig = {
        'data': [{'x': df['Timestamp'], 'y': df['Heart_Rate'], 'type': 'line', 'mode': 'lines+markers', 'name': 'Heart Rate'}],
        'layout': {'title': f'{selected_patient} - Heart Rate (bpm)', 'xaxis': {'title': 'Time'}, 'yaxis': {'title': 'BPM'}}
    }

    bp_fig = {
        'data': [
            {'x': df['Timestamp'], 'y': df['Systolic_BP'], 'type': 'line', 'mode': 'lines+markers', 'name': 'Systolic BP'},
            {'x': df['Timestamp'], 'y': df['Diastolic_BP'], 'type': 'line', 'mode': 'lines+markers', 'name': 'Diastolic BP'}
        ],
        'layout': {'title': f'{selected_patient} - Blood Pressure (mmHg)', 'xaxis': {'title': 'Time'}, 'yaxis': {'title': 'mmHg'}}
    }

    spo2_fig = {
        'data': [{'x': df['Timestamp'], 'y': df['SpO2'], 'type': 'line', 'mode': 'lines+markers', 'name': 'SpO₂'}],
        'layout': {'title': f'{selected_patient} - Oxygen Saturation (%)', 'xaxis': {'title': 'Time'}, 'yaxis': {'title': '%'}}
    }

    temp_fig = {
        'data': [{'x': df['Timestamp'], 'y': df['Temperature'], 'type': 'line', 'mode': 'lines+markers', 'name': 'Temperature'}],
        'layout': {'title': f'{selected_patient} - Body Temperature (°C)', 'xaxis': {'title': 'Time'}, 'yaxis': {'title': '°C'}}
    }

 
    if severity == "Critical":
        summary_text = "🚨 CRITICAL: Immediate medical attention required!"
    elif severity == "Warning":
        summary_text = "⚠️ WARNING: Some vitals out of safe range."
    else:
        summary_text = "✅ All vitals stable and normal."

    return html.Div([
        html.Div(summary_text, style={'backgroundColor': '#f2f2f2',
                                      'padding': '10px', 'textAlign': 'center',
                                      'fontWeight': 'bold', 'fontSize': 18,
                                      'marginBottom': '10px'}),
        dcc.Graph(figure=hr_fig),
        dcc.Graph(figure=bp_fig),
        dcc.Graph(figure=spo2_fig),
        dcc.Graph(figure=temp_fig),
        html.Div(alert_text, style={'color': 'red', 'fontWeight': 'bold', 'fontSize': 18, 'textAlign': 'center'}),
        html.H3(" Recent Alert History", style={'textAlign': 'center', 'marginTop': '30px'}),
        dash_table.DataTable(
            columns=[
                {'name': 'Timestamp', 'id': 'Timestamp'},
                {'name': 'Patient_ID', 'id': 'Patient_ID'},
                {'name': 'Severity', 'id': 'Severity'},
                {'name': 'Message', 'id': 'Message'}
            ],
            data=list(alert_history),
            style_table={'margin': 'auto', 'width': '90%'},
            style_header={'fontWeight': 'bold', 'backgroundColor': '#dcdcdc'},
            style_cell={'textAlign': 'center'},
            page_size=10
        )
    ])


if __name__ == '__main__':
    app.run(debug=True)
