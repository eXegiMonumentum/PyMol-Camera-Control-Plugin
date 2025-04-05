
import pyautogui
import cv2
import time
import mediapipe as mp
import depthai as dai
from gesture_utils import *


pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

GESTURE_DELAY = 1.0
CURSOR_SMOOTHING = 0.05

def is_pointing(landmarks):
    return landmarks[8].y < landmarks[6].y

def run_oak_plugin():

    show_camera = True
    data_collection_enabled = True

    last_action_time = 0
    last_action_label = ""
    last_cursor_pos = None

    rota_hold_start_time = None
    mov_hold_start_time = None
    movz_hold_start_time = None
    movz_detected_start_time = None

    scroll_active_start_time = None
    slab_scroll_start_time = None
    scroll_direction = 0

    overlay_message = ""
    overlay_start_time = 0
    scroll_overlay_message = ""
    scroll_overlay_start_time = 0


    pipeline = dai.Pipeline()
    cam_rgb = pipeline.createColorCamera()
    xout_video = pipeline.createXLinkOut()

    cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)
    cam_rgb.setVideoSize(1280, 720)
    cam_rgb.setFps(30)
    cam_rgb.setInterleaved(False)
    xout_video.setStreamName("video")
    cam_rgb.video.link(xout_video.input)

    try:
        device = dai.Device(pipeline)
    except Exception as e:
        print(f"Podłącz kamerę OAK-DS2 \n {e}")
        return

    video_queue = device.getOutputQueue("video", maxSize=4, blocking=False)

    with mp_hands.Hands(model_complexity=0, max_num_hands=2,
                        min_detection_confidence=0.6, min_tracking_confidence=0.5) as hands:
        while True:
            in_frame = video_queue.get()
            if in_frame is None:
                continue

            frame = in_frame.getCvFrame()
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            h, w, _ = frame.shape
            left_hand = None
            right_hand = None

            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    label = results.multi_handedness[idx].classification[0].label
                    if label == "Left":
                        left_hand = hand_landmarks.landmark
                    else:
                        right_hand = hand_landmarks.landmark
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            now = time.time()

            # Lewa ręka - ruch kursora
            if data_collection_enabled:
                if left_hand and is_pointing(left_hand):
                    screen_w, screen_h = pyautogui.size()
                    x = left_hand[8].x
                    y = left_hand[8].y
                    raw_x = int(screen_w * x)
                    raw_y = int(screen_h * y)

                    if last_cursor_pos:
                        new_x = int(last_cursor_pos[0] * (1 - CURSOR_SMOOTHING) + raw_x * CURSOR_SMOOTHING)
                        new_y = int(last_cursor_pos[1] * (1 - CURSOR_SMOOTHING) + raw_y * CURSOR_SMOOTHING)
                    else:
                        new_x, new_y = raw_x, raw_y

                    pyautogui.moveTo(new_x, new_y)
                    last_cursor_pos = (new_x, new_y)
                    cv2.circle(frame, (int(x * w), int(y * h)), 10, (0, 255, 255), -1)

            # Prawa ręka - gesty
            if data_collection_enabled:
                if right_hand:
                    if is_okay_gesture(right_hand) and now - last_action_time > GESTURE_DELAY:
                        pyautogui.mouseDown(button='left')
                        rota_hold_start_time = now
                        last_action_label = "ROTA"
                        last_action_time = now
                        overlay_message = "Executing: ROTA"
                        overlay_start_time = now



                    elif is_v_gesture(right_hand) and now - last_action_time > GESTURE_DELAY:

                        # Przerwanie scrolla, jeśli trwa
                        scroll_active_start_time = None
                        scroll_direction = 0
                        pyautogui.mouseDown(button='middle')
                        mov_hold_start_time = now
                        last_action_label = "MOV"
                        last_action_time = now
                        overlay_message = "Executing: MOV"
                        overlay_start_time = now

                    if is_four_fingers_no_thumb(right_hand):
                        if movz_detected_start_time is None:
                            movz_detected_start_time = now
                        elif now - movz_detected_start_time > 0.3 and movz_hold_start_time is None:
                            pyautogui.mouseDown(button='right')
                            movz_hold_start_time = now
                            last_action_label = "MOV-Z"
                            last_action_time = now
                            overlay_message = "Executing: MOV-Z"
                            overlay_start_time = now
                    else:
                        movz_detected_start_time = None

                    # SLAB – WHEEL GESTURE
                    SCROLL_INTERVAL = 0.1
                    SCROLL_DURATION = 2.0
                    SCROLL_STEP = 10

                    scroll_label = ""

                    if scroll_active_start_time is None:
                        if is_fist_with_thumb_180(right_hand):
                            scroll_direction = -SCROLL_STEP
                            scroll_label = "WHEEL DOWN"
                            scroll_active_start_time = now
                            slab_scroll_start_time = now
                        elif is_thumb_up_l_shape(right_hand):
                            scroll_direction = SCROLL_STEP
                            scroll_label = "WHEEL UP"
                            scroll_active_start_time = now
                            slab_scroll_start_time = now

                        if scroll_label:
                            last_action_label = "SLAB"
                            last_action_time = now
                            overlay_message = f"Executing: {scroll_label}"
                            overlay_start_time = now
                            scroll_overlay_message = scroll_label
                            scroll_overlay_start_time = now

            # Automatyczne scrollowanie przez 2 sekundy
            if scroll_active_start_time:
                if now - scroll_active_start_time <= SCROLL_DURATION:
                    if now - slab_scroll_start_time >= SCROLL_INTERVAL:
                        pyautogui.scroll(scroll_direction)
                        slab_scroll_start_time = now
                else:
                    scroll_active_start_time = None
                    scroll_direction = 0

            # Zwolnienie przycisków
            if rota_hold_start_time and now - rota_hold_start_time >= 2.0:
                pyautogui.mouseUp(button='left')
                rota_hold_start_time = None

            if mov_hold_start_time and now - mov_hold_start_time >= 2.0:
                pyautogui.mouseUp(button='middle')
                mov_hold_start_time = None

            if movz_hold_start_time and now - movz_hold_start_time >= 2.0:
                pyautogui.mouseUp(button='right')
                movz_hold_start_time = None

            # Overlay info
            if overlay_message and now - overlay_start_time < 1.0:
                cv2.putText(frame, overlay_message, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (0, 0, 255), 3)
            elif overlay_message and now - overlay_start_time >= 1.0:
                overlay_message = ""

            if scroll_overlay_message and now - scroll_overlay_start_time < 0.5:
                cv2.putText(frame, scroll_overlay_message, (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 255, 0), 2)
            elif scroll_overlay_message and now - scroll_overlay_start_time >= 0.5:
                scroll_overlay_message = ""

            if show_camera and frame is not None:
                display_frame = frame.copy()

                if not data_collection_enabled:
                    cv2.putText(display_frame, "DATA COLLECTION DISABLED", (50, int(h / 2)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.putText(display_frame, "Press 'D' to enable data collection", (50, int(h / 2) + 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

                cv2.imshow("PyMOL Gesture Mouse Mode", display_frame)

            else:
                if frame is not None:
                    off_frame = np.zeros_like(frame)
                else:
                    off_frame = np.zeros((720, 1280, 3), dtype=np.uint8)  # zapasowy czarny ekran

                if data_collection_enabled:
                    msg1 = "PREVIEW DISABLED"
                    msg2 = "Press 'H' to enable preview"
                else:
                    msg1 = "PREVIEW AND DATA COLLECTION DISABLED"
                    msg2 = "Press 'H' and 'D' to enable both"

                cv2.putText(off_frame, msg1, (100, 300),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3, cv2.LINE_AA)
                cv2.putText(off_frame, msg2, (100, 350),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

                cv2.imshow("PyMOL Gesture Mouse Mode", off_frame)

            # Obsługa klawiszy
            key = cv2.waitKey(10) & 0xFF
            if key == 27:
                break
            elif key == ord('h'):
                show_camera = not show_camera
                print("🔁 Camera display toggled:", "ON" if show_camera else "OFF")
            elif key == ord('d'):
                data_collection_enabled = not data_collection_enabled
                print("📡 Data collection:", "ENABLED" if data_collection_enabled else "DISABLED")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_oak_plugin()
