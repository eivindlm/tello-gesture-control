import cv2
import numpy as np

def find_target(cap):
    ix, iy = process_frame(cap.frame)
    return ix, iy


def process_frame(frame):
    height, width, _ = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray_blur, 80, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ix, iy = 9999, 9999

    if contours:
        squares = []
        min_area = 500  # Set a minimum area threshold for square detection
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4 and cv2.isContourConvex(approx) and cv2.contourArea(approx) > min_area:
                squares.append(approx)

        if squares:
            areas = [cv2.contourArea(square) for square in squares]
            max_index = np.argmax(areas)
            max_square = squares[max_index]
            cv2.drawContours(frame, [max_square], 0, (0, 255, 0), 2)
            M = cv2.moments(max_square)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cX_norm = cX / width
                cY_norm = cY / height
                ix = cX_norm * 2 - 1
                iy = cY_norm * 2 - 1
                cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
                cv2.putText(frame, "Center ({:.2f}, {:.2f})".format(cX_norm, cY_norm), (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    #cv2.imshow("Square Detector", frame)

    return ix, iy

if __name__ == "__main__":
    
    cap = cv2.VideoCapture(0)

    while True:
        find_target(cap)

        cv2.waitKey(1)
