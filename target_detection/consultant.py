import cv2
import numpy as np

def find_target(cap):
    return track_blue_rectangle(cap.frame)

def track_blue_rectangle(frame):
    print("HELLO")
    height, width, _ = frame.shape
    # Define blue color range in HSV format
    lower_blue = (100, 0, 0)
    upper_blue = (120, 255, 255)

    # Open a new window to display the video stream
    #cv2.namedWindow("Debug")
    #cv2.namedWindow("Masked")

    ix, iy = 99999, 99999

    # Start capturing frames from the video stream
    #while True:
    #ret, frame = video_stream.read()

    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    normalized = np.zeros((height, width))
    cv2.normalize(hsv_frame, normalized)

    # Create a mask for blue color range
    blue_mask = cv2.inRange(normalized, lower_blue, upper_blue)

    # Find contours in the mask
    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(len(contours))
    candidates = []

    # If there is at least one contour
    for contour in contours:
        # Get the bounding rectangle for the largest contour
        ((x, y), (w, h), aor) = cv2.minAreaRect(contour)
        #print(ret)

        area = w*h
        if area < 2500:
            continue

        ar = max(w/h, h/w)

        candidates.append((x, y, w, h, abs(ar-2.3)))

    print(len(candidates))
    if len(candidates) > 0:
        max_index = np.argmin([c[4] for c in candidates])
        candidate = candidates[max_index]

        x, y, w, h, ar = candidate
        print(f"{w} {h} {w*h} {max(w/h, h/w)}")

        #cv2.drawContours(frame, [candidate], 0, (0, 255, 0), 2)
        
        # Draw a circle at the center coordinate
        cv2.circle(frame, (int(x), int(y)), 5, (255, 0, 0), -1)

        cX_norm = x / width
        cY_norm = y / height
        ix = cX_norm * 2 - 1
        iy = cY_norm * 2 - 1


    # Show the frame in the video stream window
    #cv2.imshow("Debug", blue_mask)


    # Check for the "q" key to be pressed, and break the loop if it is
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

    return ix, iy

    # Release the video stream and destroy the window
    #video_stream.release()
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    track_blue_rectangle(cap)
