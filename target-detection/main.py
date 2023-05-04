import cv2
import numpy as np

# Create a video capture object
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Get the height and width of the frame
    height, width, _ = frame.shape

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Canny
    edges = cv2.Canny(gray_blur, 80, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are detected, find the most likely square
    if contours:
        squares = []
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4 and cv2.isContourConvex(approx):
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
                cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
                cv2.putText(frame, "Center ({:.2f}, {:.2f})".format(cX_norm, cY_norm), (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the frame with the most likely square drawn
    cv2.imshow("Square Detector", frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close the window
cap.release()
cv2.destroyAllWindows()

