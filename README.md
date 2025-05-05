🐾 Smart IoT Pet Feeder with Proximity-Based Dispensing and MQTT Integration
Student Name: Oisin Heaphy        Student ID: 20107294

🔧 Project Summary
A smart IoT-based automatic pet feeder system developed using a Raspberry Pi 4 and Grove sensors. The system detects a pet's presence using a PIR motion sensor and ultrasonic distance measurement, then activates a servo motor to open a flap and dispense food.

The feeding action is accompanied by visual (LED) and auditory (buzzer melody) feedback, and system messages are displayed in real-time on a 16x2 LCD screen.

The feeder sends JSON-formatted telemetry data (motion, distance, timestamp) to the public MQTT broker test.mosquitto.org, where it can be monitored live using MQTT Explorer. A companion Python script running on a PC simulates a cloud service by listening to telemetry and sending remote feed commands back via MQTT.

In parallel, the system integrates with the Blynk mobile app, allowing remote users to:

Turn the feeder ON/OFF (V0)

View live motion detection (V1)

View the measured distance to the pet (V2)

This system demonstrates real-time sensing, cloud-style actuation, and mobile control. It lays a strong foundation for future upgrades like camera-based pet recognition or automatic scheduling based on telemetry trends.

🧰 Tools, Technologies and Equipment
✅ Hardware
Raspberry Pi 4 (main controller)

Grove PIR Motion Sensor – detects pet movement

Grove Ultrasonic Sensor – confirms proximity

Servo Motor – rotates to open food flap

Grove Buzzer – plays jingle or audio alert during feeding

Grove Red LED – indicates feeding in progress

Grove LCD Display (JHD1802) – displays messages like "Feeding in progress"

Fan – powered directly via 5V/GND (used for airflow during operation)

✅ Software / Networking
Python – main programming language for logic and sensor control

Visual Studio Code – development and testing environment

MQTT Protocol (via paho-mqtt) – lightweight messaging between Pi and remote listener

test.mosquitto.org – public MQTT broker for telemetry and command exchange

MQTT Explorer – live monitoring of JSON telemetry messages

Blynk App – mobile dashboard for remote enable/disable and live sensor readings
