import cv2
import numpy as np

# Inicializa la cámara (0 para la cámara por defecto)
camera_index = 0  # Cambia este índice para usar otra cámara conectada
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Error: No se puede acceder a la cámara.")
    exit()

# Crear la ventana antes de configurar el callback
cv2.namedWindow('Cinta Amarilla')

# Variable para almacenar el valor de color bajo el cursor
selected_color = {'x': 0, 'y': 0, 'bgr': (0, 0, 0), 'hsv': (0, 0, 0), 'hsl': (0, 0, 0), 'gray': 0}

# Función para manejar los eventos del ratón
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  # Detectar movimiento del ratón
        selected_color['x'] = x
        selected_color['y'] = y

# Registrar el callback del ratón
cv2.setMouseCallback('Cinta Amarilla', mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede capturar el frame.")
        break

    # Quitar el efecto espejo (volteo horizontal)
    frame_no_mirror = cv2.flip(frame, 1)

    # Obtener las coordenadas actuales del ratón
    x, y = selected_color['x'], selected_color['y']

    # Verificar si las coordenadas son válidas
    if 0 <= x < frame_no_mirror.shape[1] and 0 <= y < frame_no_mirror.shape[0]:
        bgr = frame_no_mirror[y, x]  # Obtiene el color en formato BGR
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]  # Convierte a HSV
        hsl = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HLS)[0][0]  # Convierte a HSL
        gray = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2GRAY)[0][0]  # Convierte a escala de grises

        selected_color['bgr'] = tuple(bgr)
        selected_color['hsv'] = tuple(hsv)
        selected_color['hsl'] = tuple(hsl)
        selected_color['gray'] = int(gray)

    # Mostrar los valores en pantalla
    info = f"Pos: ({x}, {y}) | BGR: {selected_color['bgr']} | HSV: {selected_color['hsv']}"
    cv2.putText(frame_no_mirror, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    info2 = f"Pos: ({x}, {y}) | HSL: {selected_color['hsl']} | Gray: {selected_color['gray']}"
    cv2.putText(frame_no_mirror, info2, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    # Mostrar el frame procesado
    cv2.imshow('Cinta Amarilla', frame_no_mirror)

    # Salir con la tecla 'q'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
