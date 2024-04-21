
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # Đọc ảnh
# image = cv2.imread('9.jpg')
# size = (480, 640)
# tile = 4
# image = cv2.resize(image, size , interpolation=cv2.INTER_AREA)

# # Ngưỡng màu để xác định vật trên bàn cờ, được chọn phụ thuộc vào màu của vật đã được tính toán ở trên
# lower_threshold = np.array([70, 80, 110], dtype=np.uint8)
# upper_threshold = np.array([100, 120, 140], dtype=np.uint8)

# # Tạo mask
# mask = cv2.inRange(image, lower_threshold, upper_threshold)

# # Tìm contours trong mask
# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Tìm bounding box có diện tích lớn nhất
# max_area = 0
# max_box = None
# for cnt in contours:
#     area = cv2.contourArea(cnt)
#     if area > max_area:
#         max_area = area
#         max_box = cv2.boundingRect(cnt)
# center_point = []
# if max_box is not None:
#     x, y, w, h = max_box
#     # Tính tâm của bounding box
#     center_x = x + w // 2
#     center_y = y + h // 2
#     print(f'Tâm của vật có tọa độ pixel: ({center_x}, {center_y})')
#     center_point = np.array([center_x, center_y, 1])
#     # Vẽ bounding box và tâm lên ảnh
#     image_with_max_bounding_box = cv2.rectangle(image.copy(), (x, y), (x + w, y + h), (0, 255, 0), 2)
#     image_with_center = cv2.circle(image_with_max_bounding_box, (center_x, center_y), 10, (0, 0, 255), -1)
#     # Hiển thị ảnh với bounding box và tâm
#     plt.imshow(cv2.cvtColor(image_with_center, cv2.COLOR_BGR2RGB))
#     plt.title('Bounding Box Object')
#     plt.show()


# class calculateDistance(object):
#     def __init__(self) -> None:
#         super().__init__()
#         self.interrupt = False

#         self.frameId = 0
#         self.center_x = center_x
#         self.center_y = center_y

#         self.intrinsics = np.load('C:\\Users\\ThuyLe\\Desktop\\Camera-Calibration-Release\\Camera-Calibration-Release\\output\\mtx.npy')
#         self.extrinsics = np.load('C:\\Users\\ThuyLe\\Desktop\\Camera-Calibration-Release\\Camera-Calibration-Release\\output\\M_ext.npy')

#     def main(self):
#         if self.center_x is not None and self.center_y is not None and self.interrupt:
#             real_coordinate = self.realDistanceCalculator(self.center_x, self.center_y)
#             print('\33[1m' + '\33[34m' + 'Real coordinates: {}'.format(real_coordinate*tile) + '\33[0m')
#             self.interrupt = False


#     def realDistanceCalculator(self, x, y):
#         pseudo_inv_extrinsics = np.linalg.pinv(self.extrinsics)
#         intrinsics_inv = np.linalg.inv(self.intrinsics)
#         pixels_matrix = np.array((x, y, 1))
#         ans = np.matmul(intrinsics_inv, pixels_matrix)
#         ans = np.matmul(pseudo_inv_extrinsics, ans)
#         ans /= ans[-1]
#         return ans


# if __name__ == '__main__':
#     BT = calculateDistance()
#     BT.main()

import cv2
import numpy as np

class calculateDistance(object):
    def __init__(self) -> None:
        super().__init__()

        self.interrupt = False

        self.intrinsics = np.load(
            'C:\\Users\\ThuyLe\\Desktop\\Camera-Calibration-Release\\Camera-Calibration-Release\\output\\mtx.npy')
        self.extrinsics = np.load(
            'C:\\Users\\ThuyLe\\Desktop\\Camera-Calibration-Release\\Camera-Calibration-Release\\output\\M_ext.npy')

    def main(self, pointA, pointB, pointC):
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC
        self.interrupt = True

        aux1 = self.distanceBetweenTwoPixels(self.pointA, self.pointB)
        dist1 = np.sqrt(aux1[0] ** 2 + aux1[1] ** 2)
        print('\33[1m' + '\33[34m' + 'Calculated distance between A and B (mm) = {}'.format(dist1 * 4) + '\33[0m')

        aux2 = self.distanceBetweenTwoPixels(self.pointA, self.pointC)
        dist2 = np.sqrt(aux2[0] ** 2 + aux2[1] ** 2)
        print('\33[1m' + '\33[34m' + 'Calculated distance between A and C (mm) = {}'.format(dist2 * 4) + '\33[0m')

    def realDistanceCalculator(self, x, y):
        pseudo_inv_extrinsics = np.linalg.pinv(self.extrinsics)
        intrinsics_inv = np.linalg.inv(self.intrinsics)
        pixels_matrix = np.array((x, y, 1))
        ans = np.matmul(intrinsics_inv, pixels_matrix)
        ans = np.matmul(pseudo_inv_extrinsics, ans)
        ans /= ans[-1]
        return ans

    def distanceBetweenTwoPixels(self, point1, point2):
        p1 = self.realDistanceCalculator(point1[0], point1[1])
        p2 = self.realDistanceCalculator(point2[0], point2[1])
        aux = p2 - p1
        return aux

if __name__ == '__main__':
    # Thay thế xA, yA, xB, yB, xC, yC bằng tọa độ của điểm A, B và C
    xA, yA = 100, 200  # Thay thế bằng tọa độ của điểm A
    xB, yB = 300, 400  # Thay thế bằng tọa độ của điểm B
    xC, yC = 500, 600  # Thay thế bằng tọa độ của điểm C
    pointA = [xA, yA]
    pointB = [xB, yB]
    pointC = [xC, yC]

    BT = calculateDistance()
    BT.main(pointA, pointB, pointC)
