import cv2
import numpy as np

# Inicializa la cámara (0 para la cámara por defecto)
camera_index = 0  # Cambia este índice para usar otra cámara conectada
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Error: No se puede acceder a la cámara.")
    exit()

umbral_d = 0
umbral_u = 0
AREA_MAXIMA=15000
AREA_MINIMA=500

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede capturar el frame.")
        break

    # Quitar el efecto espejo (volteo horizontal)
    frame_no_mirror = cv2.flip(frame, 1)

    # Calculo de luminosidad normalizada
    gray = cv2.cvtColor(frame_no_mirror, cv2.COLOR_BGR2GRAY)
    # Calcular la luminosidad total de la imagen
    luminosidad_total = np.mean(gray)
    # Normalizar la luminosidad al rango 0-100
    luminosidad_normalizada = (luminosidad_total / 255) * 100
    #print(luminosidad_normalizada)
    
    if luminosidad_normalizada > 40 and luminosidad_normalizada < 70:  # luz intermedia
        umbral_d = 120
        umbral_u = 200
    elif luminosidad_normalizada > 70:  # Mucha luz
        umbral_d = 200
        umbral_u = 255
    else:  # poca luz
        umbral_d = 40
        umbral_u = 120

    # Convertir el frame a espacio de color HSV
    hsv = cv2.cvtColor(frame_no_mirror, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([25, 100, umbral_d])  # Rango mínimo de amarillo ajustado
    upper_yellow = np.array([35, 255, umbral_u])  # Rango máximo de amarillo ajustado
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    yellow_banda = cv2.bitwise_and(frame_no_mirror, frame_no_mirror, mask=mask)
    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Inicializar el área máxima y el contorno correspondiente
    max_area = 0
    largest_contour = None
    # Iterar sobre los contornos encontrados
    for contour in contours:
        # Calcular el área del contorno
        area = cv2.contourArea(contour)
        #print(area)
        if area>AREA_MINIMA and area<AREA_MAXIMA: #Area dentro de umbrales
            # Si el área es mayor que el área máxima actual, actualizamos
            if area > max_area:
                max_area = area
                largest_contour = contour
    # Si encontramos el contorno más grande
    if largest_contour is not None:
        # Obtener el rectángulo delimitador del contorno más grande
        x, y, w, h = cv2.boundingRect(largest_contour)
        # Dibujar el rectángulo en la imagen
        cv2.rectangle(yellow_banda, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.drawContours(yellow_banda, largest_contour, -1, (0, 0, 255), 2)
        # Calcular el punto medio del rectángulo
        center_x = x + w // 2
        center_y = y + h // 2
        # Dibujar el punto medio en la imagen
        cv2.circle(yellow_banda, (center_x, center_y), 5, (0, 0, 255), -1)
        print('Area: ',area, 'x: ',x,'y: ',y)

    # Mostrar el resultado
    cv2.imshow('Banda Amarilla Detectada', yellow_banda)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
