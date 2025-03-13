import cv2
import numpy as np
import os
from YoloV8.model import encode_image
import pickle

def contorno(img_path, result_file_path):
    cv2.setUseOptimized(False)

    with open(result_file_path, 'rb') as f:
        result_data = pickle.load(f)

    img_layer = cv2.imread(img_path)

    # Capa del borde del segmento
    border_layer = np.zeros_like(img_layer)
    segment = result_data['segments']
    if len(segment) > 1:
        for segments in segment:
            segment_np = np.array(segments).astype(np.int32)
            cv2.polylines(border_layer, [segment_np], isClosed=True, color=(0, 0, 255), thickness=2)
    else:
        segment_np = np.array(segment[0]).astype(np.int32)
        cv2.polylines(border_layer, [segment_np], isClosed=True, color=(0, 0, 255), thickness=2)

    # Capa de relleno del contorno
    fill_layer = np.zeros_like(img_layer)
    if len(segment) > 1:
        for segments in segment:
            segment_np = np.array(segments).astype(np.int32)
            cv2.fillPoly(fill_layer, [segment_np], color=(0, 0, 255))
    else:
        segment_np = np.array(segment[0]).astype(np.int32)
        cv2.fillPoly(fill_layer, [segment_np], color=(0, 0, 255))

    # Combinar las capas
    combined = cv2.addWeighted(img_layer, 1, border_layer, 1, 0)
    combined = cv2.addWeighted(combined, 1, fill_layer, 0.2, 0)

    img_name = os.path.basename(img_path)
    save_img_path = os.path.join("./YoloV8/", f"annotated_contour_{img_name}")
    cv2.imwrite(save_img_path, combined)

    # Codificar la imagen
    encoded_img = encode_image(save_img_path)
    #return encoded_img
    return encoded_img