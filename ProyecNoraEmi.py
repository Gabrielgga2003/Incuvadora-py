import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(3)

# Crear la ventana principal
root = tk.Tk()
root.title("Detección de grietas en huevos")

# Configurar el tamaño de la ventana
root.geometry("1200x600")

# Crear dos etiquetas para las imágenes
frame_label_original = Label(root, text="Imagen original", font=("Arial", 14))
frame_label_original.grid(row=0, column=0, padx=10, pady=10)

frame_label_filtrada = Label(root, text="Imagen filtrada", font=("Arial", 14))
frame_label_filtrada.grid(row=0, column=1, padx=10, pady=10)

canvas_original = tk.Canvas(root, width=640, height=480)
canvas_original.grid(row=1, column=0, padx=10, pady=10)

canvas_filtrada = tk.Canvas(root, width=640, height=480)
canvas_filtrada.grid(row=1, column=1, padx=10, pady=10)


def actualizar_imagenes():
    # Leer el cuadro actual de la cámara
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar la imagen de la cámara.")
        return

    # Convertir la imagen original para Tkinter
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imagen_original = Image.fromarray(frame_rgb)
    imagen_tk_original = ImageTk.PhotoImage(image=imagen_original)

    # Convertir la imagen filtrada para Tkinter
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(blurred, 10, 100)
    imagen_filtrada = Image.fromarray(edged)
    imagen_tk_filtrada = ImageTk.PhotoImage(image=imagen_filtrada)

    # Actualizar las imágenes en los canvas
    canvas_original.create_image(0, 0, anchor=tk.NW, image=imagen_tk_original)
    canvas_filtrada.create_image(0, 0, anchor=tk.NW, image=imagen_tk_filtrada)

    # Mantener referencias para evitar que se borren
    canvas_original.image = imagen_tk_original
    canvas_filtrada.image = imagen_tk_filtrada

    # Actualizar el bucle
    root.after(10, actualizar_imagenes)


# Iniciar el bucle de actualización
actualizar_imagenes()

# Ejecutar la ventana
root.mainloop()

# Liberar la cámara al cerrar la ventana
cap.release()
