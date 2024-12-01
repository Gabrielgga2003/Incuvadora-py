from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Inicializar la cámara
camera = cv2.VideoCapture(2)  # Cambia el índice según la cámara externa


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


@app.route('/video_feed_filtered')
def video_feed_filtered():
    """Ruta para el video filtrado."""
    return Response(generate_frames(filtered=True),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
