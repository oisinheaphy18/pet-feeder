# pet_feeder.py — MQTT + Blynk hybrid with feed trigger improvements

import time
import json
import RPi.GPIO as GPIO
import BlynkLib
import paho.mqtt.client as mqtt
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.display.jhd1802 import JHD1802

# === MQTT SETUP ===
id = 'oisin123'
client_name = id + '_petfeeder_device'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org', 1883)
mqtt_client.loop_start()
telemetry_topic = id + '/telemetry'
command_topic = id + '/commands'

# === BLYNK SETUP (direct IP fallback) ===
BLYNK_AUTH = 'yzuG540HzA7jBZsl45vCK4wOBTFRzy5g'
blynk = BlynkLib.Blynk(BLYNK_AUTH, server="46.101.217.214", port=80)
feeder_enabled = False

def handle_v0_write(value):
    global feeder_enabled
    feeder_enabled = (value[0] == "1")
    print(f"[Blynk] Feeder enabled: {feeder_enabled}")
blynk.on("V0", handle_v0_write)

# === FEEDER CONFIGURATION ===
BIG_FEED_DURATION = 0.3
SMALL_FEED_DURATION = 0.2
DISTANCE_THRESHOLD_CM = 40
COOLDOWN_PERIOD = 60
FLAP_OPEN = 7.5
FLAP_CLOSE = 2.0

# === GPIO SETUP ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
MOTION_PIN = 16
BUZZER_PIN = 22
LED_PIN = 5
SERVO_PIN = 24
ULTRASONIC_GPIO = 18

GPIO.setup(MOTION_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# === INIT DEVICES ===
try:
    servo = GPIO.PWM(SERVO_PIN, 50)
    print("✅ Servo PWM created")
    servo.start(0)
    print("✅ Servo started")

    ultrasonic = GroveUltrasonicRanger(ULTRASONIC_GPIO)
    print("✅ Ultrasonic sensor initialized")

    lcd = JHD1802()
    print("✅ LCD initialized")

except Exception as e:
    print(f"❌ ERROR during hardware setup: {e}")
    exit()

# === BEEPING INTRO JINGLE ===
def morse_jingle():
    dot = 0.1
    dash = 0.3
    gap = 0.2
    sequence = [dot, dash, dot, dot, gap, dot, gap, dash, gap*2,
                dot, dot, gap, dot, gap, dot, gap, dash, dot,
                dot, gap, dot, dash, gap, dot, dash, dot]
    for dur in sequence:
        if dur in [gap, gap * 2]:
            time.sleep(dur)
        else:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(dur)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(dot)

def big_feed():
    print("🍖 BIG FEED triggered")
    lcd.setCursor(0, 0)
    lcd.write("Feeding in prog...")
    lcd.setCursor(1, 0)
    lcd.write("Dispensing food...")
    morse_jingle()
    GPIO.output(LED_PIN, GPIO.HIGH)
    servo.ChangeDutyCycle(FLAP_OPEN)
    time.sleep(BIG_FEED_DURATION)
    GPIO.output(LED_PIN, GPIO.LOW)
    servo.ChangeDutyCycle(FLAP_CLOSE)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)
    lcd.setCursor(0, 0)
    lcd.write("Feeding done!   ")
    lcd.setCursor(1, 0)
    lcd.write("System reset... ")

def small_feed():
    print("🍗 SMALL FEED triggered")
    lcd.setCursor(0, 0)
    lcd.write("Dog still hungry")
    lcd.setCursor(1, 0)
    lcd.write("Dispensing more.")
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_PIN, GPIO.HIGH)
    servo.ChangeDutyCycle(FLAP_OPEN)
    time.sleep(SMALL_FEED_DURATION)
    GPIO.output(LED_PIN, GPIO.LOW)
    servo.ChangeDutyCycle(FLAP_CLOSE)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)
    lcd.setCursor(0, 0)
    lcd.write("Feeding done!   ")
    lcd.setCursor(1, 0)
    lcd.write("System reset... ")

# === HANDLE MQTT COMMANDS (if used later) ===
def handle_command(client, userdata, message):
    global last_feed_time, first_feed_done
    try:
        payload = json.loads(message.payload.decode())
        if payload.get("feed_now"):
            now = time.time()
            if not first_feed_done:
                big_feed()
                first_feed_done = True
                last_feed_time = now
            elif now - last_feed_time > COOLDOWN_PERIOD:
                small_feed()
                last_feed_time = now
    except Exception as e:
        print(f"❌ Error in command handler: {e}")

mqtt_client.subscribe(command_topic)
mqtt_client.on_message = handle_command

# === MAIN LOOP ===
print("🚀 MQTT Pet Feeder ready.")
lcd.setCursor(0, 0)
lcd.write("Feeder Ready")

last_feed_time = None
first_feed_done = False
consecutive_in_range = 0

try:
    while True:
        blynk.run()

        if not feeder_enabled:
            lcd.setCursor(0, 0)
            lcd.write("Feeder DISABLED ")
            time.sleep(0.3)
            continue

        motion = GPIO.input(MOTION_PIN)
        distance = ultrasonic.get_distance()

        # Skip sensor noise
        if distance > 500:
            continue

        telemetry = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "motion": bool(motion),
            "distance_cm": round(distance, 2)
        }
        mqtt_client.publish(telemetry_topic, json.dumps(telemetry))
        print("📡 Sent telemetry:", telemetry)

        # Show to Blynk + LCD
        blynk.virtual_write(2, int(motion))
        blynk.virtual_write(3, round(distance, 2))
        lcd.setCursor(1, 0)
        lcd.write(f"D:{distance:>5.1f}cm     ")

        # Feed trigger logic
        if motion and distance < DISTANCE_THRESHOLD_CM:
            consecutive_in_range += 1
        else:
            consecutive_in_range = 0

        if consecutive_in_range >= 2:
            now = time.time()
            if not first_feed_done:
                big_feed()
                first_feed_done = True
                last_feed_time = now
            elif now - last_feed_time > COOLDOWN_PERIOD:
                small_feed()
                last_feed_time = now
            consecutive_in_range = 0

        time.sleep(0.3)  # 🔄 Faster refresh

except KeyboardInterrupt:
    print("🛑 Shutting down...")
    lcd.clear()
    servo.stop()
    GPIO.cleanup()
