import cv2
import cvzone
from cvzone.ClassificationModule import Classifier
from cvzone.SerialModule import SerialObject
import os

cap = cv2.VideoCapture(0)

classifier = Classifier('Model/keras_model.h5', 'Model/labels.txt')

arduino = SerialObject('COM3')

if not os.path.exists('captured_images'):
    os.makedirs('captured_images')

img_count = 0

rect_x, rect_y, rect_w, rect_h = 150, 150, 200, 200

while True:
    success, frame = cap.read()

    cvzone.cornerRect(frame, (rect_x, rect_y, rect_w, rect_h), l=30)
    cropped_img = frame[rect_y:rect_y + rect_h, rect_x:rect_x + rect_w]
    zoomed_img = cv2.resize(cropped_img, None, fx=2, fy=2)
    img_resized = cv2.resize(cropped_img, (224, 224))
    prediction, index = classifier.getPrediction(img_resized, draw=False)
    cv2.putText(frame, f'{index}', (rect_x, rect_y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f'{prediction}', (rect_x, rect_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if index == 0:
        arduino.sendData([1])
    else:
        arduino.sendData([0])

    cv2.imshow("Webcam Feed", frame)
    cv2.imshow("Zoomed Area", zoomed_img)

    key = cv2.waitKey(1)

    if key == ord('c'):
        img_count += 1
        filename = f'captured_images/capture_{img_count}.jpg'
        cv2.imwrite(filename, cropped_img)
        print(f"Image saved: {filename}")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
