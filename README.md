# 3D-Object-Localization
**Giới thiệu bài toán**
Bài toán chuyển đổi tọa độ ảnh 2D sang tọa độ ở trạng thái 3D trở thành một khía cạnh quan trọng để nâng cao khả năng tương tác của robot, đặc biệt là trong quá trình gắp vật ở môi trường sản xuất công nghiệp. Thay vì dựa vào thông tin hình ảnh 2D truyền thống, chúng ta cần một quy trình chuyển đổi thông tin đó thành không gian 3D, giúp robot có khả năng hiểu biết về hình dạng, kích thước và vị trí của vật thể trong không gian. Sự kết hợp giữa hình ảnh 2D và dữ liệu 3D cung cấp cho robot cái nhìn đa chiều, mở ra khả năng tối ưu hóa quá trình gắp vật, tránh va chạm không mong muốn.

<a name="_toc154356503"></a>**Mô hình, Lý thuyết và Thuật toán** 

1. <a name="_toc154356504"></a>**Mô phỏng hệ thống**

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/60f42e64-a6be-45d2-a0a9-355c20e0c080)

<a name="_toc154358570"></a>***Hình 1: Mô phỏng hệ thống***

Bài toán đưa ra với mục đích có thể ứng dụng trong công nghiệp, nên hệ thống sẽ bao gồm 1 camera được chiếu thẳng đứng từ trên xuống với khoảng cách là không đổi, một vật 3D vuông góc với camera và có hệ thống chiếu sáng đầy đủ để đạt được hiệu suất cao nhất.

1. <a name="_toc154356505"></a>**Lý thuyết**

Hiệu chỉnh máy ảnh là không thể thiếu trong các ứng dụng thị giác máy tính vì hầu hết các hệ thống thị giác máy tính đều bị ảnh hưởng nhiều bởi độ chính xác của việc hiệu chuẩn. Hiệu chuẩn liên quan đến những phát triển chính trong quá trình tái tạo 3D bao gồm khôi phục hình học của máy ảnh, trích xuất và phân tích thông tin 3D. Kỹ thuật này cũng được sử dụng để ước tính vị trí 3D và góc quay của camera so với các thông số bên ngoài và bên trong, cung cấp thông tin về tọa độ thế giới 3D và thể hiện các đặc tính quang học của camera tương ứng. 

Việc xác định các tham số của hàm để giải thích ánh xạ từ vị trí của một điểm trong tọa độ 3D đến vị trí của một điểm trên mặt phẳng ảnh là một trong những mục tiêu chính của việc hiệu chỉnh máy ảnh. Các tham số hình học, còn được gọi là tham số camera, xác định theo kinh nghiệm mối quan hệ giữa vị trí camera và tọa độ thế giới 3D.Bên cạnh đó việc sử dụng bàn cờ trong hiệu chỉnh máy ảnh, cho phép các thông số máy ảnh trích xuất thông tin chính xác hơn từ hình ảnh. 

Có 2 thông số chính trong máy ảnh:

- Thông số nội tại (thông số bên trong máy ảnh) cung cấp các đặc điểm hình học và quang học của máy ảnh bao gồm độ dài tiêu cự, tâm hình ảnh và độ biến dạng của ống kính 
- Thông số bên ngoài máy ảnh: cung cấp hướng và vị trí 3D của máy ảnh liên quan đến tọa độ thế giới

Trong bài báo cáo này, máy ảnh sẽ được hiệu chỉnh với với bàn cờ có kích thước là 13x9, với mỗi ô khoảng 17.5mm.

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/b3fb34c4-ae61-4f9e-9ebe-515c3685d4a3)


<a name="_toc154358571"></a>**Hình 2: Calibration chessboard**

1. <a name="_toc154356506"></a>**Toán học về ánh xạ tọa độ điểm ảnh từ không gian 2D sang không gian 3D**

Khi một vật thể 3D đi qua tia sáng, mối quan hệ của tọa độ vật và tọa độ ảnh 2D của phép chiếu sẽ được mô tả thông qua hình ảnh về pinhole [1] camera phía dưới:

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/2775e724-a3d2-4cca-b008-e3814a052ce0)


<a name="_toc154358572"></a>**Hình 3: Pinhole Camera**

Giả sử đã có tọa độ 2D điểm ảnh, mục đích của ta là cần tìm tọa độ 3D của vật ở ngoài thực tế. Để có thể làm được điều đó, chúng ta cần phải ánh xạ tọa độ điểm ảnh sang tọa độ camera, sau đó ánh xạ từ hệ camera sang hệ tọa độ thế giới.

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/b4654a6b-7947-4546-9877-fc281ff7f837)


<a name="_toc154358573"></a>**Hình 4: Sơ đồ ánh xạ**

- **Chuyển đổi từ hệ 2D pixel sang 2D mm**

  Đầu tiên, ta xét tọa độ điểm ảnh (2D) có tọa độ là (x,y) với đơn vị là pixel. Vì các tọa độ trên hệ camera và hệ thế giới được tính theo đơn vị mm, ta cần phải chuyển đổi từ hệ pixel sang hệ mm.** Ta chọn gốc của khung tham như hình vẽ. 

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/e0154cd4-68de-4b3e-a925-43aada3a98a3)


  <a name="_toc154358574"></a>**Hình 5: Sơ đồ chuyển đổi giữa hệ pixel và minimet**

  Từ đó, ta quy đổi được tọa độ của một điểm trong hệ quy chiếu dựa trên pixel:  

  ![](Aspose.Words.d566849a-569b-49f5-bf2b-d9b820d787ee.008.png);  mx, my là mật độ pixel theo trục x, y; f là tiêu cự máy ảnh

- **Chuyển đổi từ hệ pixel sang camera**

  Một điểm 2D được ký hiệu là m = [u, v]<sup>T</sup>. Và điểm 3D ánh xạ trên hệ camera là (Xc, Yc, Zc). Do 2 vecto khác nhau về chiều, nên chúng ta sẽ đồng nhất hệ tọa độ mặt phẳng bằng cách tăng cường bằng cách thêm 1 làm phần tử cuối cùng của vecto 2D: m<sub>e</sub> = [u, v, 1]<sup>T</sup>
![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/9b5aa618-9bf9-4302-907c-f4b0d7ed9888)


  <a name="_toc154358575"></a>**Hình 6: Chuyển đổi từ hệ 2D sang hệ camera**

  Đồng nhất tọa độ ta thu được công thức sau:

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/cb2adb26-82eb-407b-b48b-959241177cce)


  Đặt ma trận thông số nội tại của máy ảnh: ![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/1d7278eb-74bd-4d21-beb7-cb9ae32f7e41)
 **Intrinsic Matrix**

  Để chuyển đổi từ tọa độ camera sang tọa độ thực, vị trí mà chúng ta bàn tới sẽ bao gồm vector quay và Ma trận xoay

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/2e9c57f1-18a5-4a54-ba65-285d82d79cdb)


  <a name="_toc154358576"></a>**Hình 7: Chuyển đổi từ hệ Camera sang hệ thế giới thực**

  Trong đó ma trận xoay có dạng: ![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/dcc4e67b-c0f3-4232-91b1-c1ae3e707643)


  Với các hàng đại diện với hướng theo tứ tự xc yc zc trong tọa độ thế giới

  ![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/53745eed-f8e8-47a6-a838-d40fa1a51158)


Đồng nhất hệ tọa độ ta thu được công thức như sau:

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/8c7efac0-72d1-4ce3-9b07-a2cb2e419cc2)


Ma trận 4x4 trên còn được gọi là ma trận ngoài camera. Để chuyển từ ma trận thế giới sang trận camera, ta sẽ thông qua ma trận Extrinsic

Do đó, tổng quát để chuyển từ hệ tọa độ thực (3D) sang hệ tọa độ ảnh (2D):

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/1de2d673-9029-48cb-b4da-61f2a12ae232)


Trong đó R và t lần lượt là các phần tử quay và tịnh tiến của ma trận bên ngoài, trong khi K đại diện cho ma trận bên trong. Các tham số bên ngoài chuyển đổi tọa độ 3D thành tọa độ camera và sau đó các tham số bên trong chuyển đổi tọa độ camera thành mặt phẳng hình ảnh như hình dưới đây:

<a name="_toc154356507"></a>**Kết quả và đánh giá**

1. <a name="_toc154356508"></a>**Quá trình tìm tọa độ tâm của vật trên ảnh 2D:** 

   Được thực hiện bằng cách xét ngưỡng màu của vật, và tìm các cạnh biên của vật tương ứng. Sau đó ta bounding box vật và tìm tọa độ trọng tâm dựa vào hình bao.

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/62b47669-9db9-4168-95bd-d31e98b28389)


<a name="_toc154358578"></a>**Hình 9: Kết quả Bounding box & center object**

- **Nhận xét:** Bởi vì có dùng tới ngưỡng màu của vật, nên bài toán chỉ dùng trong một số trường hợp cụ thể, và ánh sáng cố định. Nếu ánh sáng bị thay đổi, sẽ ảnh hưởng tới kết quả bài ra và tọa độ tâm tìm được
1. <a name="_toc154356509"></a>**Ánh xạ tọa độ 2D sang tọa độ 3D**

   Sử dụng các kiến thức toán thuần, ta sẽ tính được các thông số trong và ngoài của camera. Từ đó ta sử dụng để có thể đưa vào trong quá trình tính toán kết quả đầu ra.

   Vì trong quá trình đo đạc trọng tâm ở thế giới thực có thể xảy ra sai số, trước tiên ta tiến hành đo độ dài cạnh của vật để kiểm gia sai số

![image](https://github.com/mylehust/3D-Object-Localization/assets/109675981/dce6069f-fa9e-45fa-a756-e61e8a42d40b)


- **Nhận xét:** Kết quả nhận được là 92.75mm, trong khi số đo thực tế là 91mm
- sai số chưa tới 2%

Khi đã có tọa độ tâm trong ảnh 2D (pixel), ta tiến hành nhân nghịch đảo với các ma trận K, R để tìm ra tọa độ trong thế giới thực 3D


<a name="_toc154358580"></a>**Hình 11: Thực nghiệm kết quả tọa độ vật 3D**

Sau khi tiến hành một loạt các data cho trước, ta nhận thấy rằng, sai số không quá 5%



