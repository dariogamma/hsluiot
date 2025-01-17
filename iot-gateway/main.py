from flask import Flask, request, jsonify
from azure.iot.device import IoTHubDeviceClient, Message
import requests
import os

# Flask-App initialisieren
app = Flask(__name__)

# IoT Hub Verbindungseinstellungen
IOT_HUB_CONNECTION_STRING = os.getenv("IOT_HUB_CONNECTION_STRING")
THRESHOLD_TEMPERATURE = os.getenv("THRESHOLD_TEMPERATURE")
THRESHOLD_HUMIDITY = os.getenv("THRESHOLD_HUMIDITY")
NOTIFICATION_SERVICE_URL = 'http://localhost:5000/notify'

# IoT-Client initialisieren
iot_client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONNECTION_STRING)

@app.route('/data', methods=['POST'])
def send_data_to_iot_hub():
    try:
        # JSON-Daten aus der Anfrage lesen
        data = request.json
        
        # Erwartete Felder prüfen
        if not all(k in data for k in ("temperature", "id", "humidity")):
            print(data)
            return jsonify({"error": "Missing one or more required fields: 'temperature', 'id', 'humidity'"}), 400
        
        # Daten auslesen
        temperature = data['temperature']
        device_id = data['id']
        humidity = data['humidity']
        
        if float(temperature) >= float(THRESHOLD_TEMPERATURE) or float(humidity) >= float(THRESHOLD_HUMIDITY):
            print(f'Send alert: temp. {temperature} / humi. {humidity}')
            try:
                # POST-Request senden
                headers = { "Content-Type": "application/json" }
                response = requests.post(NOTIFICATION_SERVICE_URL, json=data, headers=headers)

                # Antwort prüfen
                if response.status_code == 200:
                    print("User notified successfully:", response.json())
                else:
                    print("Error sending notification:", response.status_code, response.json())
            except requests.exceptions.RequestException as e:
                print("Error sending notification:", e)
        
        # IoT-Hub Nachricht vorbereiten
        iot_message = {
            "deviceId": device_id,
            "temperature": temperature,
            "humidity": int(humidity)
        }
        
        # Nachricht senden
        message = Message(str(iot_message))
        iot_client.send_message(message)
        
        return jsonify({"status": "success", "message": "Data sent to IoT Hub"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

# Flask-Server starten
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)