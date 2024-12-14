from flask import Flask, request, jsonify
from gmailAltert import GmailAlert
import os

# Flask-App initialisieren
app = Flask(__name__)

# Set up Gmail credentials and server details
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = 587
EMAIL = os.getenv("EMAIL")  # Replace with your Gmail address
PASSWORD = os.getenv("SMTP_PASSWORD")  # Replace with your Gmail app password

alert = GmailAlert(SMTP_SERVER, SMTP_PORT, EMAIL, PASSWORD)

@app.route('/notify', methods=['POST'])
def send_notification():
    try:
        # JSON-Daten aus der Anfrage lesen
        data = request.json
        
        # Erwartete Felder prüfen
        if not all(k in data for k in ("temperature", "id", "humidity")):
            print(data)
            return jsonify({"error": "Missing one or more required fields: 'temperature', 'id', 'humidity'"}), 400
        
        
        result = alert.send_email(
            recipient_email="vxw18543@msssg.com",
            subject="WATER ALERT",
            body= f'Sensor {data['id']} detected temperature of {data['temperature']} and humidity of {data['humidity']}'
        )

        print(result)
            
        return jsonify({"status": "success", "message": "Notification send"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Flask-Server starten
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)