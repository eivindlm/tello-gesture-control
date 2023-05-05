import cv2
import time

from djitellopy import Tello

tello = Tello()
tello.connect()
tello.streamon()

cap = tello.get_frame_read()




if __name__ == "__main__":
    count = 0
    while True:

        # Capture frame
        frame = cap.frame


        # Save image file with sequence number
        filename = f'image_{count}.jpg'
        cv2.imwrite(filename, frame)
        count += 1

        time.sleep(1)
    
        # Display the resulting frame
        cv2.imshow('frame', frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Release everything if job is finished
    cv2.destroyAllWindows()
