import cv2

# تابع برای شناسایی و لیبل گذاری مستطیل ها
def detect_and_label_rectangles(image_path):
    # خواندن عکس
    image = cv2.imread(image_path)
    
    # تبدیل تصویر به مقیاس خاکستری (Grayscale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # تشخیص مستطیل ها با استفاده از الگوریتم CascadeClassifier
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    rectangles = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # لیبل گذاری مستطیل ها و نمایش رنگ آنها
    for (x, y, w, h) in rectangles:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi = image[y:y + h, x:x + w]
        avg_color_per_row = np.average(roi, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        color = tuple(map(int, avg_color))
        print("مستطیل با رنگ:", color)
    
    # نمایش عکس با مستطیل ها و رنگ آنها
    cv2.imshow("Detected Rectangles", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# فراخوانی تابع برای یک عکس خاص
image_path = "/home/mobiniqow/Downloads/a.png"
detect_and_label_rectangles(image_path)
