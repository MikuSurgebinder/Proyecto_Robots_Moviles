import cv2
import numpy as np

# Inicializa la cámara (0 para la cámara por defecto)
camera_index = 0  # Cambia este índice para usar otra cámara conectada
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Error: No se puede acceder a la cámara.")
    exit()

print("""
Seleccione una opción:
  'h' - Modo HSV
  'l' - Modo HSL
  'g' - Modo escala de grises
  'c' - Modo BGR (por defecto)
  'q' - Salir
""")

# Función para cambiar el espacio de color
def cambiar_espacio_color(frame, tipo_espacio):
    if tipo_espacio == 'hsv':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    elif tipo_espacio == 'hsl':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    elif tipo_espacio == 'grey':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:  # 'color' (modo BGR)
        return frame

# Switch para elegir el espacio de color
tipe = 'no especificado'  # Inicialmente no especificado

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede capturar el frame.")
        break

    # Quitar el efecto espejo (volteo horizontal)
    frame_no_mirror = cv2.flip(frame, 1)

    # Cambiar el espacio de color según el modo seleccionado
    frame_transformado = cambiar_espacio_color(frame_no_mirror, tipe)

    # Si estamos en modo HSV, HSL o gris, realizamos la detección de color
    if tipe == 'hsv':
        hsv = frame_transformado
        lower_yellow = np.array([25, 100, 150])  # Rango mínimo de amarillo ajustado
        upper_yellow = np.array([35, 255, 255])  # Rango máximo de amarillo ajustado
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    elif tipe == 'hsl':
        hsl = frame_transformado
        lower_yellow_hsl = np.array([27, 70, 100])  # Rango mínimo de amarillo ajustado en HSL
        upper_yellow_hsl = np.array([32, 160, 255])  # Rango máximo de amarillo ajustado en HSL
        mask = cv2.inRange(hsl, lower_yellow_hsl, upper_yellow_hsl)
    elif tipe == 'grey':
        gray = frame_transformado
        # Rango de luminosidad ajustado para detectar la banda amarilla reflectante
        lower_brightness = 190  # Ajuste para la luminosidad mínima (banda amarilla brillante)
        upper_brightness = 200  # Luminosidad máxima (el rango para un blanco brillante)
        mask = cv2.inRange(gray, lower_brightness, upper_brightness)
    else:  # 'color' (modo BGR)
        lower_yellow_bgr = np.array([0, 140, 140])  # Rango mínimo de amarillo en BGR
        upper_yellow_bgr = np.array([80, 255, 255])  # Rango máximo de amarillo en BGR
        mask = cv2.inRange(frame_transformado, lower_yellow_bgr, upper_yellow_bgr)

    # Aplicar la máscara al frame original
    yellow_banda = cv2.bitwise_and(frame_no_mirror, frame_no_mirror, mask=mask)

    # Mostrar el resultado
    cv2.imshow('Banda Amarilla Detectada', yellow_banda)

    # Cambiar el modo entre BGR, HSV, HSL, gris con la tecla correspondiente
    key = cv2.waitKey(1) & 0xFF
    if key == ord('h'):
        tipe = 'hsv'  # Cambiar a HSV
        print("Modo HSV activado.")
    elif key == ord('l'):
        tipe = 'hsl'  # Cambiar a HSL
        print("Modo HSL activado.")
    elif key == ord('g'):
        tipe = 'grey'  # Cambiar a escala de grises
        print("Modo escala de grises activado.")
    elif key == ord('c'):
        tipe = 'color'  # Cambiar a BGR
        print("Modo BGR activado.")
    elif key == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
