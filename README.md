🐾 Smart IoT Pet Feeder with Proximity-Based Dispensing and Azure Integration
Student Name: Oisin Heaphy        Student ID: 20107294
🔧 Project Summary
A smart IoT-based automatic pet feeder system built using a Raspberry Pi 4, sensors, and servo control logic. The system detects pet presence using motion and ultrasonic sensors, activates a servo-controlled hatch to release food, and provides visual (LED) and audio (buzzer melody) feedback. The system is being upgraded to transmit telemetry data to Azure IoT Hub using MQTT for real-time monitoring and data visualization via Azure Time Series Insights.

This enables tracking of pet feeding behavior, distance monitoring, and actuator status, with potential for future enhancements like camera-based detection or remote cloud-triggered feeding.

🧰 Tools, Technologies and Equipment
✅ Hardware
Raspberry Pi 4 (main controller)

Grove PIR Motion Sensor (detects pet presence)

Grove Ultrasonic Sensor (measures distance for close-range confirmation)

Servo Motor (opens feeding hatch at 180° rotation)

Grove Buzzer (plays short melody/jingle)

Grove Red LED (status indicator during feeding)

Relay (optional) (controls auxiliary devices like fan or safety override)

Small fan (for future integration with relay for heat/presence detection)

✅ Software / Cloud
Python (all sensor and actuator logic)

Visual Studio Code (development environment)

Azure IoT Hub (telemetry communication)

MQTT Protocol (for lightweight message transmission)

Azure Time Series Insights (real-time dashboard for sensor trends)
