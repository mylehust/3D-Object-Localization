# import cv2
# import urllib.request
# import numpy as np

# url = 'http://192.168.55.254:8080/video'

# cap = cv2.VideoCapture(url)

# while True:
#     # Đọc frame từ webcam
#     ret, frame = cap.read()

#     # Hiển thị frame
#     cv2.imshow('Android Webcam', frame)

#     # Nhấn phím 'q' để thoát khỏi vòng lặp
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import urllib.request
import numpy as np

def process_frame(frame):
    size = (480, 640)
    frame = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)

    # Ngưỡng màu để xác định vật trên bàn cờ
    lower_threshold = np.array([70, 80, 110], dtype=np.uint8)
    upper_threshold = np.array([100, 120, 140], dtype=np.uint8)
    mask = cv2.inRange(frame, lower_threshold, upper_threshold)

    # Tìm contours trong mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tìm bounding box có diện tích lớn nhất
    max_area = 0
    max_box = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_box = cv2.boundingRect(cnt)

    center_x, center_y = None, None
    if max_box is not None:
        x, y, w, h = max_box
        # Tính center của object
        center_x = x + w // 2
        center_y = y + h // 2
        print(f'Tâm của vật có tọa độ pixel: ({center_x}, {center_y})')

        # Vẽ bounding box và tâm lên ảnh
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frame = cv2.circle(frame, (center_x, center_y), 3, (0, 0, 255), -1)

        org = (center_x - 50, center_y - 10)  # Điều chỉnh vị trí của văn bản
        cv2.putText(frame, f'({center_x}, {center_y})', org,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (155, 0, 255), 2, cv2.LINE_AA)

    return frame

# IP androi
url = 'http://192.168.1.6:8080/video'

cap = cv2.VideoCapture(url)

while True:
    # Đọc frame từ webcam
    ret, frame = cap.read()
    if not ret:
        break
    processed_frame = process_frame(frame)

    cv2.imshow('Object Tracking', processed_frame)

    # Nhấn 'q' để thoát khỏi vòng lặp
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


