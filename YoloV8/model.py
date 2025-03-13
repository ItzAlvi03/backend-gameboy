from ultralytics import YOLO
import cv2
import os
import base64

def encode_image(img_path):
    img = cv2.imread(img_path)

    if img is None or img.size == 0:
        raise ValueError(f'Error al cargar la imagen en {img_path}')

    _, img_encoded = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(img_encoded)
    return img_base64.decode('utf-8')

def predict(img_path, conf):
    cv2.setUseOptimized(False)

    model = YOLO("./YoloV8/best.pt")
    resultado = model.predict(img_path, imgsz=640, conf=conf)

    segments_list = []
    boxes_list = []
    person_list = []
    list_conf = []
    total_confianza = 0
    total_personas = 0

    for r in resultado:
        #Obtener total personas y % de predicciones
        total_personas += len(r.boxes)
    if len(r.boxes) > 0:
        for box_conf in r.boxes.conf:
            confianza = box_conf.item()
            list_conf.append(confianza)
            total_confianza += confianza

        #Obtener las coordenadas del rectangulo de las personas detectadas
        if r.boxes is not None:
            boxes = r.boxes.xyxy
            for box in boxes:
                boxes_list.append(box.tolist())

        #Obtener la máscara de segmentación de las personas detectadas
        if r.masks is not None:
            segments = r.masks.xy
            for segment in segments:
                mask_list = []
                # Obteniendo todas las posiciones de los puntos de la mascara de 1 persona
                for position in segment.tolist():
                    mask = {'x': position[0], 'y': position[1]}
                    mask_list.append(mask)
                # Añadiendo toda la mascara de puntos de 1 persona
                segments_list.append(mask_list)

    person = []
    # Hacer un json para recogerlo como un objeto persona
    for num in range(total_personas):
        person = {
            'segments': segments_list[num],
            'boxes': boxes_list[num],
            'conf': list_conf[num] * 100
        }
        person_list.append(person)

    media_confianza = total_confianza / total_personas if total_personas > 0 else 0
    media = round(media_confianza * 100, 2)

    result = {
        'total_detections': total_personas,
        'porcentaje_promedio': media,
        'person': person_list
    }

    return result