"""
Program 4 : Image Segmentation using Computer Vision (CO3)
Aim   : Divide an image into meaningful regions (objects and background).
Methods used (OpenCV):
   1. Grayscale + Gaussian blur         - remove noise
   2. Otsu thresholding (saturation)    - automatic threshold -> object mask
   3. K-Means colour clustering         - group pixels by colour into K segments
   4. Contour detection                 - find each object, count it, name its shape
   5. Canny edge detection              - object boundaries
Run   : python 04_image_segmentation.py              (uses a generated sample image)
        python 04_image_segmentation.py my_photo.jpg (use your own image)
Install : pip install opencv-python numpy matplotlib
"""
import os
import sys
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def make_sample_image():
    """Light background with three coloured shapes + noise."""
    img = np.full((400, 500, 3), 235, np.uint8)
    cv2.circle(img, (120, 130), 70, (40, 40, 220), -1)                          # red circle (BGR)
    cv2.rectangle(img, (260, 60), (440, 190), (200, 90, 30), -1)               # blue rectangle
    cv2.fillPoly(img, [np.array([[120, 360], [220, 220], [320, 360]])], (60, 170, 60))  # green triangle
    cv2.circle(img, (400, 300), 45, (30, 190, 230), -1)                         # yellow circle
    noise = np.random.default_rng(0).normal(0, 8, img.shape)
    return np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def shape_name(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.03 * peri, True)
    corners = len(approx)
    if corners == 3:
        return "triangle"
    if corners == 4:
        return "rectangle"
    area = cv2.contourArea(contour)
    circularity = 4 * np.pi * area / (peri * peri + 1e-9)
    return "circle" if circularity > 0.8 else f"polygon({corners})"


def segment(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 1. Otsu threshold on the SATURATION channel (grey background = low saturation,
    #    coloured objects = high saturation), so bright objects are not missed either
    sat = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:, :, 1], (5, 5), 0)
    t, mask = cv2.threshold(sat, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))   # remove specks
    print(f"Otsu threshold value chosen automatically : {t:.0f}")

    # 2. K-Means colour segmentation
    K = 5
    data = img.reshape(-1, 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
    kmeans_img = centers.astype(np.uint8)[labels.flatten()].reshape(img.shape)
    print(f"K-Means colour segmentation with K = {K} done")

    # 3. Contours on the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = [c for c in contours if cv2.contourArea(c) > 500]
    annotated = img.copy()
    print(f"\nObjects found : {len(objects)}")
    for i, c in enumerate(sorted(objects, key=lambda c: cv2.boundingRect(c)[0]), 1):
        x, y, w, h = cv2.boundingRect(c)
        name = shape_name(c)
        print(f"  Object {i}: {name:<10} area = {cv2.contourArea(c):8.0f} px   box = ({x},{y},{w},{h})")
        cv2.drawContours(annotated, [c], -1, (0, 0, 0), 2)
        cv2.putText(annotated, f"{i}:{name}", (x, max(y - 6, 12)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # 4. Edges
    edges = cv2.Canny(blur, 50, 150)
    # segmented foreground (mask applied on the original)
    foreground = cv2.bitwise_and(img, img, mask=mask)
    return gray, mask, kmeans_img, annotated, edges, foreground


if __name__ == "__main__":
    if len(sys.argv) > 1:
        img = cv2.imread(sys.argv[1])
        if img is None:
            sys.exit(f"Cannot read image: {sys.argv[1]}")
        img = cv2.resize(img, (500, int(500 * img.shape[0] / img.shape[1])))
    else:
        img = make_sample_image()
        cv2.imwrite(os.path.join(OUT_DIR, "sample_input.png"), img)
    print("IMAGE SEGMENTATION\n")
    gray, mask, kmeans_img, annotated, edges, fg = segment(img)

    rgb = lambda a: cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
    panels = [("Original", rgb(img), None), ("Grayscale", gray, "gray"),
              ("Otsu mask (objects = white)", mask, "gray"),
              ("K-Means colour segments", rgb(kmeans_img), None),
              ("Contours and shapes", rgb(annotated), None), ("Canny edges", edges, "gray")]
    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for ax, (title, im, cmap) in zip(axes.ravel(), panels):
        ax.imshow(im, cmap=cmap)
        ax.set_title(title)
        ax.axis("off")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "segmentation_result.png")
    plt.savefig(out, dpi=110)
    print("\nResult image saved as", out)
    if matplotlib.get_backend().lower() != "agg":
        plt.show()
