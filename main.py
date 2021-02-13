#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configargparse

import cv2 as cv

from gestures.tello_gesture_controller import TelloGestureController
from utils import CvFpsCalc

from djitellopy import Tello
from gestures import GestureRecognition, GestureBuffer


def get_args():
    print('## Reading configuration ##')
    parser = configargparse.ArgParser(default_config_files=['config.txt'])

    parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    parser.add("--device", type=int)
    parser.add("--width", help='cap width', type=int)
    parser.add("--height", help='cap height', type=int)
    parser.add('--use_static_image_mode', action='store_true', help='True if running on photos')
    parser.add("--min_detection_confidence",
               help='min_detection_confidence',
               type=float)
    parser.add("--min_tracking_confidence",
               help='min_tracking_confidence',
               type=float)

    args = parser.parse_args()

    return args


def main():
    # Argument parsing
    args = get_args()

    # Camera preparation
    tello = Tello()
    tello.connect()
    tello.streamon()

    print(tello.get_battery())

    # Take-off drone
    tello.takeoff()

    cap = tello.get_frame_read()

    tello_controller = TelloGestureController(tello)
    gesture_detector = GestureRecognition(args.use_static_image_mode, args.min_detection_confidence,
                                          args.min_tracking_confidence)
    gesture_buffer = GestureBuffer(buffer_len=5)

    # FPS Measurement
    cv_fps_calc = CvFpsCalc(buffer_len=10)

    mode = 0
    number = -1

    tello.move_down(20)

    while True:
        fps = cv_fps_calc.get()
        tello.move_forward(0)

        # Process Key (ESC: end)
        key = cv.waitKey(10)
        if key == 27:  # ESC
            break

        # Camera capture
        image = cap.frame

        debug_image, gesture_id = gesture_detector.recognize(image)
        debug_image = gesture_detector.draw_info(debug_image, fps, mode, number)

        gesture_buffer.add_gesture(gesture_id)

        # Screen reflection
        cv.imshow('Hand Gesture Recognition', debug_image)

        tello_controller.gesture_control(gesture_buffer)

    tello.land()
    tello.end()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
