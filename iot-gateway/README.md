# Install 
pip install flask azure-iot-device


# Umgebungsvariabel mit dem Connectionstring setzen
echo 'export IOT_HUB_CONNECTION_STRING="HostName=<YourIoTHubName>.azure-devices.net;DeviceId=<YourDeviceId>;SharedAccessKey=<YourDeviceKey>"' >> ~/.bashrc
source ~/.bashrc
