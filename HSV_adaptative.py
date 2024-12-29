import cv2
import numpy as np


# Inicializa la cámara (0 para la cámara por defecto)
camera_index = 0  # Cambia este índice para usar otra cámara conectada
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Error: No se puede acceder a la cámara.")
    exit()

umbral_d=0
umbral_u=0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede capturar el frame.")
        break

    # Quitar el efecto espejo (volteo horizontal)
    frame_no_mirror = cv2.flip(frame, 1)

    #Calculo de luminosidad normalizada
    gray = cv2.cvtColor(frame_no_mirror, cv2.COLOR_BGR2GRAY)
    # Calcular la luminosidad total de la imagen
    luminosidad_total = np.mean(gray)
    # Normalizar la luminosidad al rango 0-100
    luminosidad_normalizada = (luminosidad_total / 255) * 100
    #print(luminosidad_normalizada)
    
    if luminosidad_normalizada>40 and luminosidad_normalizada<70: #luz intermedia
        umbral_d=120
        umbral_u=200
    elif luminosidad_normalizada>70: #Mucha luz
        umbral_d=200
        umbral_u=255
    else: #poca luz
        umbral_d=40
        umbral_u=120

    # Convertir el frame a espacio de color HSV si el switch está activado
    hsv = cv2.cvtColor(frame_no_mirror, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([25, 100, umbral_d])  # Rango mínimo de amarillo ajustado
    upper_yellow = np.array([35, 255, umbral_u])  # Rango máximo de amarillo ajustado
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Aplicar la máscara al frame original
    yellow_banda = cv2.bitwise_and(frame_no_mirror, frame_no_mirror, mask=mask)

    # Mostrar el resultado
    cv2.imshow('Banda Amarilla Detectada', yellow_banda)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
