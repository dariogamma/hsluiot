from flask import Flask, request, jsonify
from azure.iot.device import IoTHubDeviceClient, Message
import os

# Flask-App initialisieren
app = Flask(__name__)

# IoT Hub Verbindungseinstellungen
IOT_HUB_CONNECTION_STRING = os.getenv("IOT_HUB_CONNECTION_STRING")

# IoT-Client initialisieren
iot_client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONNECTION_STRING)

@app.route('/send-data', methods=['POST'])
def send_data_to_iot_hub():
    try:
        # JSON-Daten aus der Anfrage lesen
        data = request.json
        
        # Erwartete Felder prüfen
        if not all(k in data for k in ("temperature", "id", "humidity")):
            return jsonify({"error": "Missing one or more required fields: 'temperature', 'id', 'humidity'"}), 400
        
        # Daten auslesen
        temperature = data['temperature']
        device_id = data['id']
        humidity = data['humidity']
        
        # IoT-Hub Nachricht vorbereiten
        iot_message = {
            "deviceId": device_id,
            "temperature": temperature,
            "humidity": humidity
        }
        
        # Nachricht senden
        message = Message(str(iot_message))
        iot_client.send_message(message)
        
        return jsonify({"status": "success", "message": "Data sent to IoT Hub"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask-Server starten
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)