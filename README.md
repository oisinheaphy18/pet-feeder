# Smart Pet Feeder with Monitoring and Alerts

#### Student Name: *Oisin Heaphy*     Student ID: *20107294*

A smart IoT-based automatic pet feeder system that dispenses food for a pet dog at scheduled times or when the pet is detected nearby. The system also monitors whether the food is consumed and notifies the owner in real-time. The project uses sensors to detect motion and measure food levels, a Raspberry Pi for processing and control, and Azure IoT services for data transmission and visualization. The application provides feeding history and alerts through a dashboard.

## Tools, Technologies and Equipment

- **Hardware**:
  - Raspberry Pi 4
  - HC-SR04 Ultrasonic Sensor (to detect pet proximity)
  - Load Cell + HX711 (to measure food weight)
  - Servo Motor (for dispensing food)
  - Pi Camera (optional for pet monitoring)

- **Software/Technologies**:
  - Python (for scripting and sensor logic)
  - MQTT Protocol (for sending telemetry to Azure)
  - Azure IoT Hub (data transmission and cloud communication)
  - Azure Time Series Insights / Power BI (dashboard and data trends)
  - Visual Studio Code
