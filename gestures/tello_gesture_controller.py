from djitellopy import Tello
import time

#from target_detection.square import find_target as find_square_target
from target_detection.consultant import find_target
from motion_planning.simple import vertical_motion


#def find_target(cap) -> tuple:
    # Input: image
    # Output: image coordinate of target (x, y) \in [-1,1]^2. negative values if not found.

#    # TODO, add switch or something to select algo
#    return find_square_target(cap)

def motion_from_target(ix, iy) -> tuple:
    # Input: image coordinate (ix,iy) \in [0,1]^2
    # Output drone vector x, y, z, yaw
    
    # TODO, add switch or something to select algo
    return vertical_motion(ix, iy)




class TelloGestureController:
    def __init__(self, tello: Tello):
        self.tello = tello
        self._is_landing = False

        # RC control velocities
        self.forw_back_velocity = 0
        self.up_down_velocity = 0
        self.left_right_velocity = 0
        self.yaw_velocity = 0

    def navigate_to_target(self, gesture_buffer):
        # Crash and burn control loop

        cap = self.tello.get_frame_read()

        while True:
            gesture_id = gesture_buffer.get_gesture()
            print("GESTURE", gesture_id)

            if self._is_landing or gesture_id == 3: # LAND will abort
                return
            
            ix, iy = find_target(cap)
            print(f"TARGET: {ix}, {iy}")

            if -1 <= ix <= 1 and -1 <= iy <= 1:
                mx, my, mz, myaw = motion_from_target(ix, iy)
                print(f"MOTION: {mx}, {my}, {mz}, {myaw}")
                self.tello.send_rc_control(int(mx), int(my), int(mz), int(myaw))
                #time.sleep(0.5)  # TODO, adjust
                #self.tello.send_rc_control(0, 0, 0, 0)



    def gesture_control(self, gesture_buffer):
        gesture_id = gesture_buffer.get_gesture()
        print("GESTURE", gesture_id)

        self.forw_back_velocity = self.up_down_velocity = \
            self.left_right_velocity = self.yaw_velocity = 0

        if not self._is_landing:
            if gesture_id == 0:  # Forward
                self.forw_back_velocity = 30
            elif gesture_id == 1:  # STOP
                self.navigate_to_target(gesture_buffer)

            
            elif gesture_id == 5:  # Back
                self.forw_back_velocity = -30

            elif gesture_id == 2:  # UP
                self.up_down_velocity = 25
            elif gesture_id == 4:  # DOWN
                self.up_down_velocity = -25

            elif gesture_id == 3:  # LAND
                self._is_landing = True
                self.forw_back_velocity = self.up_down_velocity = \
                    self.left_right_velocity = self.yaw_velocity = 0
                self.tello.land()

            elif gesture_id == 6: # LEFT
                self.left_right_velocity = 20
            elif gesture_id == 7: # RIGHT
                self.left_right_velocity = -20

            elif gesture_id == -1:
                self.forw_back_velocity = self.up_down_velocity = \
                    self.left_right_velocity = self.yaw_velocity = 0

            self.tello.send_rc_control(self.left_right_velocity, self.forw_back_velocity,
                                       self.up_down_velocity, self.yaw_velocity)
