#   CODE TEST CHIỀU DÀI
# import cv2
# import numpy as np

# # Config Variables - Enter their values according to your Object Image
# image_name = 'data_input/1.jpg' # Image Name

# class calculateDistance(object):
#     def __init__(self) -> None:
#         super().__init__()

#         self.pointd1 = []
#         self.pointd2 = []
#         self.interrupt = False

#         self.frameId = 0

#         self.intrinsics = np.load('C:\\Users\\ThuyLe\\Desktop\\Camera-Calibration-Release\\Camera-Calibration-Release\\output\\mtx.npy')
#         self.extrinsics = np.load('C:\\Users\\ThuyLe\\Desktop\\Camera-Calibration-Release\\Camera-Calibration-Release\\output\\M_ext.npy')

#     def getMouseClicks(self, event, x, y, flags, params):
#         if event == cv2.EVENT_LBUTTONDOWN:
#             print('Point clicked: {}, {}'.format(x, y))
#             if not self.pointd1:
#                 self.pointd1 = [x, y]
#             else:
#                 self.pointd2 = [x, y]
#                 dx = self.pointd1[0] - self.pointd2[0]
#                 dy = self.pointd1[1] - self.pointd2[1]
#                 dist = np.sqrt(dx**2 + dy**2)
#                 print('\33[1m' + '\33[32m' + 'Distance in Pixels = {0:2.2f}'.format(dist*4) + '\33[0m')
#                 self.interrupt = True

#     def main(self):
#         cv2.namedWindow("Get Points")
#         cv2.setMouseCallback('Get Points', self.getMouseClicks)
#         while True:
#             image = cv2.imread(image_name)
#             size = (480, 640)
#             tile = 4
#             resize_image = cv2.resize(image, size , interpolation=cv2.INTER_AREA)
#             cv2.imshow("Get Points", resize_image)
#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break
#             elif self.interrupt:
#                 break
#         cv2.destroyAllWindows()
#         while True:
#             if self.pointd1 and self.pointd2 and self.interrupt:
#                 cv2.line(resize_image, tuple(self.pointd1),tuple(self.pointd2), (0, 0, 255), 2)
#                 cv2.imshow('Distance', resize_image)
#                 aux = self.distanceBetweenTwoPixels()
#                 dist = np.sqrt((aux[0])**2 + (aux[1])**2)
#                 print('\33[1m' + '\33[34m' + 'Calculated distance in Size (mm) = {}'.format(dist*tile) + '\33[0m')
#                 self.interrupt = False
#             if cv2.waitKey(0):
#                 break

#     def realDistanceCalculator(self, x, y):
#         pseudo_inv_extrinsics = np.linalg.pinv(self.extrinsics)
#         intrinsics_inv = np.linalg.inv(self.intrinsics)
#         pixels_matrix = np.array((x, y, 1))
#         ans = np.matmul(intrinsics_inv, pixels_matrix)
#         ans = np.matmul(pseudo_inv_extrinsics, ans)
#         ans /= ans[-1]
#         return ans

#     def distanceBetweenTwoPixels(self):
#         p1 = self.realDistanceCalculator(self.pointd1[0], self.pointd1[1])
#         p2 = self.realDistanceCalculator(self.pointd2[0], self.pointd2[1])
#         aux = p2 - p1
#         self.pointd1.clear()
#         self.pointd2.clear()
#         return aux

# if __name__ == '__main__':
#     BT = calculateDistance()
#     BT.main()

#_________________________________________________MAIN CODE_________________________________________________#
import cv2
import numpy as np
import matplotlib.pyplot as plt

class calculateDistance(object):
    def __init__(self) -> None:
        super().__init__()
        self.interrupt = False

        self.frameId = 0
        # 2 ma trận này đã đc tính sẵn ở calib.ipynb, lưu trong 'out'
        self.intrinsics = np.load('C:\\Users\\ThuyLe\\Desktop\\Camera-Calibration-Release\\Camera-Calibration-Release\\output\\mtx.npy')
        self.extrinsics = np.load('C:\\Users\\ThuyLe\\Desktop\\Camera-Calibration-Release\\Camera-Calibration-Release\\output\\M_ext.npy')

    def main(self, pointA, pointB, pointC):
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC
        self.interrupt = True

        aux1 = self.distanceBetweenTwoPixels(self.pointA, self.pointB)
        dist1 = np.sqrt(aux1[0] ** 2 + aux1[1] ** 2)
        print('\33[1m' + '\33[34m' + 'Tung độ Center (mm) = {}'.format(dist1 * tile) + '\33[0m')

        aux2 = self.distanceBetweenTwoPixels(self.pointA, self.pointC)
        dist2 = np.sqrt(aux2[0] ** 2 + aux2[1] ** 2) # pitago
        print('\33[1m' + '\33[34m' + 'Hoành độ Center (mm) = {}'.format(dist2 * tile) + '\33[0m')
    
    def realDistanceCalculator(self, x, y): # convert (ma trận nghịch đảo)
        inv_extrinsics = np.linalg.pinv(self.extrinsics)
        intrinsics_inv = np.linalg.inv(self.intrinsics)
        pixels_matrix = np.array((x, y, 1))
        ans = np.matmul(intrinsics_inv, pixels_matrix) # M_int ^ -1
        ans = np.matmul(inv_extrinsics, ans) #M_ext^-1
        ans /= ans[-1] # chia cho phần tử cuối cùng
        return ans

    def distanceBetweenTwoPixels(self, point1, point2): # tính toán khoảng cách giữa 2 điểm pixel
        p1 = self.realDistanceCalculator(point1[0], point1[1])
        p2 = self.realDistanceCalculator(point2[0], point2[1])
        result  = p2 - p1
        return result


# Đọc ảnh
image = cv2.imread('12.jpg')
size = (480, 640)
tile = 4
image = cv2.resize(image, size , interpolation=cv2.INTER_AREA)

# Ngưỡng màu để xác định vật trên bàn cờ, được chọn phụ thuộc vào màu của vật đã được tính toán ở trên
lower_threshold = np.array([70, 80, 110], dtype=np.uint8)
upper_threshold = np.array([100, 120, 140], dtype=np.uint8)

# Tạo mask
mask = cv2.inRange(image, lower_threshold, upper_threshold)

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
    # Tính tâm của bounding box
    center_x = x + w // 2
    center_y = y + h // 2
    print(f'Tâm của vật có tọa độ pixel: ({center_x}, {center_y})')
    center_point = np.array([center_x, center_y])
    # Vẽ bounding box và tâm lên ảnh
    image_with_max_bounding_box = cv2.rectangle(image.copy(), (x, y), (x + w, y + h), (0, 255, 0), 2)
    image_with_center = cv2.circle(image_with_max_bounding_box, (center_x, center_y), 3, (0, 0, 255), -1)
 
    org = (center_x - 50, center_y - 10)  # Điều chỉnh vị trí của văn bản
    cv2.putText(image_with_center, f'({center_x}, {center_y})', org,
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (155, 0, 255), 2, cv2.LINE_AA)
    plt.imshow(cv2.cvtColor(image_with_center, cv2.COLOR_BGR2RGB))
    plt.title('Bounding Box Object and Center Object')
    plt.show()


if __name__ == '__main__':
    BT = calculateDistance()

    pointA = [center_x, center_y]
    pointB = [center_x, 0]
    pointC = [0, center_y]
    BT.main(pointA, pointB, pointC)
