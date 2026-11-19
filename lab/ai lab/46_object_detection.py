"""
Program 6 : Object Detection using a pre-trained model (CO3)
Aim   : Detect and label objects in an image with a pre-trained YOLOv4-tiny
        network (trained on the COCO data set - 80 object classes such as
        person, car, dog, bicycle, chair ...). The model is run with OpenCV's
        DNN module, so no deep-learning framework needs to be installed.
First run : the model files (about 24 MB) and a sample photo are downloaded
            automatically into the folder "models" (internet needed once).
Run   : python 06_object_detection.py                 (sample image)
        python 06_object_detection.py my_photo.jpg    (your own image)
        python 06_object_detection.py --webcam        (live camera, press q to quit)
Install : pip install "opencv-python<5" numpy matplotlib
"""
import os
import sys
import urllib.request
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE, "models")
FILES = {
    "yolov4-tiny.weights": "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights",
    "yolov4-tiny.cfg": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg",
    "coco.names": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names",
}
SAMPLE_URL = "https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/dog.jpg"
CONF_THRESHOLD, NMS_THRESHOLD = 0.40, 0.40


def download(url, path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        print("Downloading", os.path.basename(path), "...")
        urllib.request.urlretrieve(url, path)


def load_model():
    os.makedirs(MODEL_DIR, exist_ok=True)
    for name, url in FILES.items():
        download(url, os.path.join(MODEL_DIR, name))
    with open(os.path.join(MODEL_DIR, "coco.names")) as f:
        names = [line.strip() for line in f if line.strip()]
    if not hasattr(cv2.dnn, "readNetFromDarknet"):
        sys.exit("This OpenCV version has no Darknet loader. Install OpenCV 4:  pip install \"opencv-python<5\"")
    net = cv2.dnn.readNetFromDarknet(os.path.join(MODEL_DIR, "yolov4-tiny.cfg"),
                                     os.path.join(MODEL_DIR, "yolov4-tiny.weights"))
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1 / 255.0, swapRB=True)
    return model, names


def detect(model, names, img):
    class_ids, scores, boxes = model.detect(img, CONF_THRESHOLD, NMS_THRESHOLD)
    results = []
    rng = np.random.default_rng(1)
    colors = rng.integers(60, 255, size=(len(names), 3)).tolist()
    for cid, score, box in zip(np.array(class_ids).flatten(), np.array(scores).flatten(), boxes):
        x, y, w, h = [int(v) for v in box]
        label = f"{names[cid]} {score:.0%}"
        color = tuple(int(c) for c in colors[cid])
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img, (x, y - th - 8), (x + tw + 4, y), color, -1)
        cv2.putText(img, label, (x + 2, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        results.append((names[cid], float(score), (x, y, w, h)))
    return img, results


def run_image(path):
    model, names = load_model()
    img = cv2.imread(path)
    if img is None:
        sys.exit(f"Cannot read image: {path}")
    out, results = detect(model, names, img.copy())
    print(f"\nObjects detected in {os.path.basename(path)} : {len(results)}")
    for name, score, (x, y, w, h) in results:
        print(f"  {name:<14} confidence {score:5.1%}   box (x={x}, y={y}, w={w}, h={h})")
    save = os.path.join(BASE, "detected_output.jpg")
    cv2.imwrite(save, out)
    print("\nAnnotated image saved as", save)
    plt.figure(figsize=(9, 7))
    plt.imshow(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title("Object detection - YOLOv4-tiny (COCO)")
    if matplotlib.get_backend().lower() != "agg":
        plt.show()


def run_webcam():
    model, names = load_model()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit("Camera not found.")
    print("Press q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame, _ = detect(model, names, frame)
        cv2.imshow("YOLOv4-tiny object detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("OBJECT DETECTION WITH A PRE-TRAINED MODEL (YOLOv4-tiny, COCO classes)")
    if "--webcam" in sys.argv:
        run_webcam()
    else:
        if len(sys.argv) > 1:
            image_path = sys.argv[1]
        else:
            os.makedirs(os.path.join(BASE, "sample_images"), exist_ok=True)
            image_path = os.path.join(BASE, "sample_images", "dog.jpg")
            download(SAMPLE_URL, image_path)
        run_image(image_path)
