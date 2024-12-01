import cv2

# Inicializar la captura de video desde la camara
cap = cv2.VideoCapture(3)

while True:
    # Leer cada cuadro de la camara
    ret, frame = cap.read()
    
    # Verificar si la captura fue exitosa
    if not ret:
        print("No se pudo capturar la imagen de la camara.")
        break

    # Mostrar el cuadro en una ventana
    #video=cv2.imshow("En vivo", frame)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(blurred, 10, 100)

    #imagen deteccion de bordes
    #cv2.imshow("En vivo", frame)
    cv2.imshow("Bordes", edged)

# Liberar la captura de video y cerrar ventanas
cap.release()
cv2.destroyAllWindows()