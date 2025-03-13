import cv2
import numpy as np
import os
import pickle

from YoloV8.model import encode_image

def box(img_path, result_file_path):
    cv2.setUseOptimized(False)

    with open(result_file_path, 'rb') as f:
        result_data = pickle.load(f)

    img_layer = cv2.imread(img_path)

    # Extraer las coordenadas de la caja
    boxes = result_data['boxes']
    for box in boxes:
        x1, y1, x2, y2 = box  # Tomar las coordenadas de la caja

        # Convertir a enteros
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Dibujar el rectángulo en la imagen
        cv2.rectangle(
            img_layer,
            (x1, y1),
            (x2, y2),
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

    # Guardar la imagen resultante
    annotated_img_path = "./YoloV8/annotated_boxes_" + os.path.basename(img_path)
    cv2.imwrite(annotated_img_path, img_layer)

    encoded_img = encode_image(annotated_img_path)

    return encoded_img