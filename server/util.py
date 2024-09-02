#Sending a image into a base64 encoded string. 
# This is to send the image that is uploaded into our website to the server to do image classification.
import cv2 as cv
import numpy as np
import base64
import pywt
import joblib
import json
import matplotlib.pyplot as plt

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name

    with open(r"D:\Study\Projects\ImageClassification\PremierLeaguePlayersClassifier\server\artifacts\players_dictionary.json","r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {value:key for key,value in __class_name_to_number.items()}
    
    global model
    model = None
    if model is None:
        with open(r'D:\Study\Projects\ImageClassification\PremierLeaguePlayersClassifier\server\artifacts\saved_model.pkl', 'rb') as f:
            model = joblib.load(f)
    print("loading saved artifacts...done")

def get_image_from_base64_string(b64str):
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    return img

def get_face_image(image):
    #Using the face as the feature can be improved to find eyes and using eyes also as an feature
    face_cascade = cv.CascadeClassifier("D:\Study\Projects\ImageClassification\haarcascades\haarcascade_frontalface_default.xml") 
    face_image = face_cascade.detectMultiScale(image,1.3,3)
    #Unable to find the face
    if(len(face_image) == 0):
        face_image = face_cascade.detectMultiScale(image,1.05,1)
        if(len(face_image) == 0):
            face_image = face_cascade.detectMultiScale(image,1.1,2)
    cropped_faces = []
    print(len(face_image))
    for (x,y,w,h) in face_image:
        region_of_interest = image[y:y+h,x:x+w]
        cropped_faces.append(region_of_interest)
    return cropped_faces

def wavelet_transform(image,mode="haar",level =1):
    img = np.float32(image)
    img/=255

    coefficients = pywt.wavedec2(image,mode,level=level)
    haar_coefficients = list(coefficients)
    haar_coefficients[0]*=0

    wavelet_image = pywt.waverec2(haar_coefficients,mode)
    wavelet_image*=255
    wavelet_image = np.uint8(wavelet_image)

    return wavelet_image

def class_number_to_name(class_num):
    return __class_number_to_name[class_num]


def classify_image(base64_image):
    image = get_image_from_base64_string(base64_image)
    #image = base64_image
    gray_image = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    faces = get_face_image(gray_image)
    result = []
    for face in faces:
        scaled_raw_image = cv.resize(image,(32,32))
        haar_wavelet_image = wavelet_transform(gray_image,'db1',5) 
        scaled_wavelet_image = cv.resize(haar_wavelet_image,(32,32))
        #print(scaled_wavelet_image1.shape)
        #scaled_wavelet_image = cv.cvtColor(scaled_wavelet_image1,cv.COLOR_BGR2GRAY)
        combined_image = np.vstack((scaled_raw_image.reshape(32*32*3,1),scaled_wavelet_image.reshape(32*32*1,1)))
        #len(cobined_image) is (32*32*3) +(32*32*1) 
        final_image = combined_image.reshape(1,len(combined_image)).astype(float)

        result.append({
            'class': class_number_to_name(model.predict(final_image)[0]),
            'class_probability': np.around(model.predict_proba(final_image)*100,2).tolist()[0],
            'class_dictionary': __class_name_to_number
        })
        print(result)
        return result

# image = cv.imread(r"D:\Study\Projects\ImageClassification\PremierLeaguePlayersClassifier\ronaldo_test.jpg")
# plt.imshow(image)
# classify_image(image)
 


