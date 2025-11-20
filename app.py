from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_temp_db():
    conn = sqlite3.connect('iot_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_intrusion_db():
    conn = sqlite3.connect('security_intrusions.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/line-chart')
def line_chart():
    return render_template('line_chart.html')

@app.route('/bar-chart')
def bar_chart():
    return render_template('bar_chart.html')

@app.route('/pie-chart')
def pie_chart():
    return render_template('pie_chart.html')

@app.route('/api/pie-data')
def pie_data():
    data = {
        'labels': ['Active', 'Inactive', 'Maintenance', 'Offline'],
        'datasets': [{
            'label': 'Device Status',
            'data': [12, 3, 2, 1],
            'backgroundColor': [
                'rgba(75, 192, 192, 0.7)',
                'rgba(255, 99, 132, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(153, 102, 255, 0.7)'
            ],
            'borderColor': [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(153, 102, 255, 1)'
            ],
            'borderWidth': 1
        }]
    }
    return jsonify(data)

@app.route('/api/line-data')
def line_data():
    conn = get_temp_db()

    try:
        rows = conn.execute("""
            SELECT timestamp, temperature
            FROM temperature_readings
            ORDER BY timestamp
        """).fetchall()
    except Exception as e:
        print("ERROR in line chart SQL:", e)
        rows = []

    conn.close()

    data = {
        'labels': [row['timestamp'] for row in rows],
        'datasets': [{
            'label': 'Temperature (°C)',
            'data': [row['temperature'] for row in rows],
            'borderColor': 'rgb(75, 192, 192)',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'tension': 0.4,
            'fill': True
        }]
    }
    return jsonify(data)

@app.route('/api/bar-data')
def bar_data():
    conn = get_intrusion_db()

    try:
        rows = conn.execute("""
            SELECT intrusion_type, COUNT(*) AS total
            FROM intrusions
            GROUP BY intrusion_type
        """).fetchall()
    except Exception as e:
        print("ERROR in bar chart SQL:", e)
        rows = []

    conn.close()

    data = {
        'labels': [row['intrusion_type'] for row in rows],
        'datasets': [{
            'label': 'Security Intrusion Count',
            'data': [row['total'] for row in rows],
            'backgroundColor': 'rgba(54, 162, 235, 0.7)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1
        }]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
