# pet_feeder_server.py — listens to telemetry and sends feed command via MQTT

import json
import time
import paho.mqtt.client as mqtt

id = 'oisin123'
telemetry_topic = id + '/telemetry'
command_topic = id + '/commands'
client_name = id + '_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org', 1883)
mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        motion = payload.get("motion", False)
        distance = payload.get("distance_cm", 999)

        print("Received:", payload)

        if motion and distance < 40:
            command = {"feed_now": True}
            mqtt_client.publish(command_topic, json.dumps(command))
            print("Sent command:", command)

    except Exception as e:
        print("Telemetry error:", e)

mqtt_client.subscribe(telemetry_topic)
mqtt_client.on_message = handle_telemetry

print("Server listening for telemetry...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Server stopped.")
