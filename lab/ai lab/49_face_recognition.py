"""
Program 9 : Face Recognition using a pre-trained model (CO5)
Aim   : Recognise people in photos with the pre-trained deep-learning model of the
        "face_recognition" library (a ResNet network trained on millions of faces).
How it works :
   1. Detect faces in the image                      (HOG face detector)
   2. Convert every face into a 128-number encoding  (pre-trained ResNet "embedding")
   3. Compare encodings : distance < 0.6  ->  same person, otherwise "Unknown"
Run   : python 09_face_recognition.py                  (downloads 4 sample photos, then recognises)
        python 09_face_recognition.py --known known_faces --test photo.jpg
              (known_faces folder contains one photo per person, file name = person name)
        python 09_face_recognition.py --webcam          (live camera, press q to quit)
Install (Windows / Linux / Mac, no C++ compiler needed) :
        pip install dlib-bin
        pip install face_recognition_models Click Pillow numpy matplotlib opencv-python
        pip install face_recognition --no-deps
        (if you get "No module named pkg_resources":  pip install "setuptools<81")
"""
import os
import sys
import glob
import argparse
import urllib.request
import numpy as np
import face_recognition
from PIL import Image, ImageDraw
import matplotlib
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DIR = os.path.join(BASE, "faces")
RAW = "https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/"
SAMPLES = ["obama.jpg", "biden.jpg", "obama2.jpg", "two_people.jpg"]
TOLERANCE = 0.60            # smaller = stricter


def download_samples():
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    for name in SAMPLES:
        path = os.path.join(SAMPLE_DIR, name)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            print("Downloading", name, "...")
            urllib.request.urlretrieve(RAW + name, path)


def load_known(paths):
    """Return (names, encodings) - one encoding per known person."""
    names, encodings = [], []
    for path in paths:
        image = face_recognition.load_image_file(path)
        found = face_recognition.face_encodings(image)
        if not found:
            print(f"  warning: no face found in {os.path.basename(path)} - skipped")
            continue
        names.append(os.path.splitext(os.path.basename(path))[0].capitalize())
        encodings.append(found[0])
        print(f"  learned face of {names[-1]:<10} from {os.path.basename(path)}")
    return names, encodings


def recognise(image, known_names, known_encodings):
    """Return the image (PIL) with boxes + names, and a list of results."""
    locations = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image, locations)
    pil = Image.fromarray(image)
    draw = ImageDraw.Draw(pil)
    results = []
    for (top, right, bottom, left), enc in zip(locations, encodings):
        distances = face_recognition.face_distance(known_encodings, enc)
        best = int(np.argmin(distances))
        name = known_names[best] if distances[best] <= TOLERANCE else "Unknown"
        color = (0, 200, 0) if name != "Unknown" else (220, 0, 0)
        draw.rectangle(((left, top), (right, bottom)), outline=color, width=4)
        label = f"{name} ({distances[best]:.2f})"
        draw.rectangle(((left, bottom), (right, bottom + 22)), fill=color)
        draw.text((left + 4, bottom + 5), label, fill=(255, 255, 255))
        results.append((name, float(distances[best]), (top, right, bottom, left)))
    return pil, results


def run_images(known_paths, test_paths):
    print("\nLearning known faces:")
    known_names, known_encodings = load_known(known_paths)
    if not known_names:
        sys.exit("No known faces could be learned.")
    panels = []
    for path in test_paths:
        image = face_recognition.load_image_file(path)
        pil, results = recognise(image, known_names, known_encodings)
        print(f"\nImage {os.path.basename(path)} : {len(results)} face(s) found")
        for i, (name, dist, box) in enumerate(results, 1):
            print(f"   Face {i}: {name:<8} distance = {dist:.3f}  (match if <= {TOLERANCE})   box = {box}")
        panels.append((os.path.basename(path), pil))
    fig, axes = plt.subplots(1, len(panels), figsize=(5.5 * len(panels), 5), squeeze=False)
    for ax, (title, pil) in zip(axes[0], panels):
        ax.imshow(pil)
        ax.set_title(title)
        ax.axis("off")
    plt.tight_layout()
    out = os.path.join(BASE, "face_recognition_result.png")
    plt.savefig(out, dpi=110)
    print("\nResult image saved as", out)
    if matplotlib.get_backend().lower() != "agg":
        plt.show()


def run_webcam(known_paths):
    import cv2
    names, encodings = load_known(known_paths)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit("Camera not found.")
    print("Press q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        for (top, right, bottom, left), enc in zip(face_recognition.face_locations(rgb),
                                                   face_recognition.face_encodings(rgb)):
            d = face_recognition.face_distance(encodings, enc)
            name = names[int(np.argmin(d))] if d.min() <= TOLERANCE else "Unknown"
            top, right, bottom, left = top * 2, right * 2, bottom * 2, left * 2
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 200, 0), 2)
            cv2.putText(frame, name, (left, bottom + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)
        cv2.imshow("Face recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--known", help="folder with one photo per known person")
    ap.add_argument("--test", nargs="+", help="photo(s) to recognise")
    ap.add_argument("--webcam", action="store_true")
    args = ap.parse_args()
    print("FACE RECOGNITION WITH A PRE-TRAINED MODEL")

    if args.known:
        known = sorted(glob.glob(os.path.join(args.known, "*.jp*g")) + glob.glob(os.path.join(args.known, "*.png")))
        tests = args.test or []
    else:
        download_samples()
        known = [os.path.join(SAMPLE_DIR, "obama.jpg"), os.path.join(SAMPLE_DIR, "biden.jpg")]
        tests = [os.path.join(SAMPLE_DIR, "obama2.jpg"), os.path.join(SAMPLE_DIR, "two_people.jpg")]

    if args.webcam:
        run_webcam(known)
    elif tests:
        run_images(known, tests)
    else:
        sys.exit("Give photos with --test, or run without options for the sample demo.")
