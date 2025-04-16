import cv2
import numpy as np

def get_points(im):
    # Загрузка изображения
    image = im
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Диапазон красного цвета в HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Создание маски
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Улучшение маски
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Удаление шума
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Сглаживание контуров

    # Поиск контуров
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        # Проверка формы (опционально)
        perimeter = cv2.arcLength(max_contour, True)
        approx = cv2.approxPolyDP(max_contour, 0.04 * perimeter, True)

        if len(approx) == 4:  # Если объект четырёхугольный
            # Определение крайних точек
            points = np.squeeze(approx)
            points = sorted(points, key=lambda x: x[0])
            left = tuple(points[0])
            right = tuple(points[-1])
            points = sorted(points, key=lambda x: x[1])
            top = tuple(points[0])
            bottom = tuple(points[-1])

            # Рисование точек и линий
            for pt in [left, right, top, bottom]:
                cv2.circle(image, pt, 10, (0, 255, 0), -1)

            cv2.drawContours(image, [approx], -1, (255, 0, 0), 3)
        # else:
        #     print("Объект не является квадратом")

    # else:
    #     print("Красный квадрат не найден")
    return image, left, right, top, bottom