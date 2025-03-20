import joblib
import json
import numpy as np
import base64
import cv2
import pywt  # ✅ Ensure PyWavelets is used

# Global Variables
__class_name_to_number = {}
__class_number_to_name = {}
__model = None

def w2d(img, mode='db1', level=1):
    """Apply Wavelet Transform."""
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coeffs2 = pywt.wavedec2(img_gray, mode, level=level)
    coeffs2[0] *= 0  # Remove approximation coefficients
    img_har = pywt.waverec2(coeffs2, mode)
    return img_har

def classify_image(image_base64_data, file_path=None):
    """Classify image after preprocessing."""
    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)
    if imgs is None or len(imgs) == 0:
        return ["No face with two eyes detected"]
    
    result = []
    for img in imgs:
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))

        combined_img = np.vstack((
            scalled_raw_img.reshape(32*32*3, 1),
            scalled_img_har.reshape(32*32, 1)
        ))

        len_image_array = 32 * 32 * 3 + 32 * 32  # ✅ Corrected

        final = combined_img.reshape(1, len_image_array).astype(float)

        prediction = __model.predict(final)[0]
        result.append({
            'class': class_number_to_name(__model.predict(final)[0]),
            'class_probability': np.around(__model.predict_proba(final)*100,2).tolist()[0],
            'class_dictionary': __class_name_to_number
        })
    return result

def class_number_to_name(class_num):
    return __class_number_to_name[class_num]

def load_saved_artifacts():
    """Load the model and class dictionary."""
    print("Loading saved artifacts...")

    global __class_name_to_number
    global __class_number_to_name
    global __model

    with open(r'C:\Users\user\Desktop\Davischoice\portfolio_project\sports_celebrity_classification\server\artifacts\class_dictionary.json', "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v: k for k, v in __class_name_to_number.items()}

    if __model is None:
        with open(r'C:\Users\user\Desktop\Davischoice\portfolio_project\sports_celebrity_classification\server\artifacts\saved_model.pkl', 'rb') as f:
            __model = joblib.load(f)
    
    print("Loading saved artifacts...done")

def get_cv2_image_from_base64_string(b64str):
    """Convert base64 string to OpenCV image."""
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    """Detect faces and return cropped images if two eyes are detected."""
    face_cascade = cv2.CascadeClassifier(r'C:\Users\user\Desktop\Davischoice\portfolio_project\sports_celebrity_classification\server\opencv\haarcascades\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(r'C:\Users\user\Desktop\Davischoice\portfolio_project\sports_celebrity_classification\server\opencv\haarcascades\haarcascade_eye.xml')

    img = cv2.imread(image_path) if image_path else get_cv2_image_from_base64_string(image_base64_data)

    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) >= 2:
            cropped_faces.append(roi_color)

    return cropped_faces if cropped_faces else None

def get_b64_test_image_for_antoine():
    """Load base64 test image from file."""
    with open(r"C:\Users\user\Desktop\Davischoice\portfolio_project\sports_celebrity_classification\server\64.txt.txt") as f:
        return f.read()

if __name__ == '__main__':
    load_saved_artifacts()
    print(classify_image(get_b64_test_image_for_antoine(), None))
