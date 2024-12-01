from flask import Flask, json, render_template, Response, jsonify
import threading
import paho.mqtt.client as mqtt
import cv2

app = Flask(__name__)

# Inicializar la cámara
camera = cv2.VideoCapture(2)  # Cambia el índice según la cámara externa

data = {"temperature": 0.0, "humidity": 0.0}


# MQTT Configuration
MQTT_BROKER = "18.205.126.177" # Cambia esto a tu servidor MQTT
MQTT_PORT = 1883
MQTT_TOPIC = "incubator/sensor-data"

def on_message(client, userdata, msg):
    global data
    print(f"Mensaje recibido: {msg.payload}")  # Para verificar qué llega exactamente
    try:
        payload = msg.payload.decode()  # Decodificar el mensaje
        message = json.loads(payload)  # Parsear JSON
        # Usa las claves en inglés según lo que envía el ESP32
        data["temperature"] = message.get("temperature", data["temperature"])
        data["humidity"] = message.get("humidity", data["humidity"])
        print(f"Datos recibidos: {data}")
    except Exception as e:
        print(f"Error procesando el mensaje MQTT: {e}")


# Hilo para el cliente MQTT
def mqtt_thread():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)
    print(f"Conectado al broker MQTT en {MQTT_BROKER}:{MQTT_PORT}, suscrito al tópico {MQTT_TOPIC}")
    client.loop_forever()



def generate_frames(filtered=False):
    """Generador de cuadros de video en tiempo real."""
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            if filtered:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (3, 3), 0)
                frame = cv2.Canny(blurred, 10, 100)

            # Codificar el cuadro como JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Crear el flujo de datos para el navegador
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html')


@app.route('/video_feed_original')
def video_feed_original():
    """Ruta para el video original."""
    return Response(generate_frames(filtered=False),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/api/data")
def get_data():
    return jsonify(data)

@app.route('/video_feed_filtered')
def video_feed_filtered():
    """Ruta para el video filtrado."""
    return Response(generate_frames(filtered=True),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    threading.Thread(target=mqtt_thread, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
