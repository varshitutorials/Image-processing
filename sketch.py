import cv2
import numpy as np
import qrcode
import os
import webbrowser
from imagekitio import ImageKit

# Initialize ImageKit SDK
imagekit = ImageKit(
    private_key="private_rTEOmcoD6R3Wa5ieM8+Gvokhosc=",
    public_key="public_liXKSQwl4RW9YbGkHFgUWhZd9C4=",
    url_endpoint="https://ik.imagekit.io/4tnm6bk5n/"  # Corrected URL
)

# Set the working directory where images will be stored
working_directory = r"C:\Users\varsh\OneDrive\Desktop\ML\Image Processing"

# Ensure directory exists
if not os.path.exists(working_directory):
    os.makedirs(working_directory)

# Define file paths for captured image, sketch, and QR code
captured_image_path = os.path.join(working_directory, "captured.jpg")
sketch_path = os.path.join(working_directory, "sketch.jpg")
qr_code_path = os.path.join(working_directory, "qrcode.png")

# Open camera
cap = cv2.VideoCapture(0)
cv2.namedWindow("Press SPACE to Capture", cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    cv2.imshow("Press SPACE to Capture", frame)
    key = cv2.waitKey(1)

    if key == 32:  # SPACE key to capture
        cv2.imwrite(captured_image_path, frame)
        print(f"Image saved at {captured_image_path}")
        break

cap.release()
cv2.destroyAllWindows()

# Convert to Sketch
def to_sketch(img_path, save_path):
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    cv2.imwrite(save_path, sketch)
    return save_path

# Generate sketch from captured image
to_sketch(captured_image_path, sketch_path)
print(f"Sketch saved at {sketch_path}")

# Upload Sketch to ImageKit
if os.path.exists(sketch_path):
    upload_response = imagekit.upload(
        file=open(sketch_path, "rb"),
        file_name="sketch.jpg"
    )
    sketch_url = upload_response.url
    print(f"Sketch uploaded! Access it here: {sketch_url}")
else:
    print("Error: Sketch file not found. Upload skipped.")
    exit()

# Generate QR Code for the uploaded image
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(sketch_url)
qr.make(fit=True)
qr_img = qr.make_image(fill="black", back_color="white")
qr_img.save(qr_code_path)
print(f"QR Code saved at {qr_code_path}")

# Display Sketch & QR Code
sketch_img = cv2.imread(sketch_path)
qr_display = cv2.imread(qr_code_path)

cv2.imshow("Sketch", sketch_img)
cv2.imshow("QR Code - Scan to View Image", qr_display)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Open the uploaded sketch URL in the browser
webbrowser.open(sketch_url)
