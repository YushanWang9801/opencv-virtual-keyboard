import cv2
from cvzone.HandTrackingModule import HandDetector
import Key
from pynput.keyboard import Controller
from time import sleep

SECOND_FINGER_TIP = 8
WIDTH, HEIGHT = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
video = VideoWriter('webcam.avi', VideoWriter_fourcc(*'MP42'), 25.0, (WIDTH, HEIGHT))

detector = HandDetector(detectionCon=0.85)
keyboard = Controller()

global running_program, caps_lock, num_lock, clickedText
clickedText = ""
running_program = True
caps_lock = True
num_lock = False

def draw_button_on_click(img, button, det_x, det_y):
    x,y = button.pos
    w,h = button.size
    if x < det_x < x+w and y < det_y < y+h:
        cv2.rectangle(img, (x,y), (x+w,y+h),
                        (200,200,200), cv2.FILLED)
        cv2.putText(img, button.text, button.text_pos, 
                cv2.FONT_ITALIC, 1.0, (0,0,0), 2)
        return img, True
    return img, False

def handle_detection(detectionList, img):
    global num_lock, caps_lock, clickedText
    finger_close = True if detector.findDistance(8, 12, img)[0] < 30 else False
    if num_lock:
        img, is_click = draw_button_on_click(img, Key.abc_key, 
                                detectionList[8][0], detectionList[8][1])
        if is_click and finger_close:    
            num_lock = False
            sleep(0.2)
            return img
        
        for row in Key.num_keys:
            for key in row:
                img, is_click = draw_button_on_click(img, key, 
                                detectionList[8][0], detectionList[8][1])
                if is_click and finger_close:
                    keyboard.press(key.text)
                    cv2.rectangle(img, key.pos, 
                        (key.pos[0]+key.size[0], key.pos[1]+key.size[1]), 
                        (0,0,0), cv2.FILLED)
                    cv2.putText(img, key.text, key.text_pos, 
                                    cv2.FONT_ITALIC, 1.0, (255, 255, 255), 2)
                    clickedText += key.text
                    sleep(0.2)
                    return img
    else:
        # Handle Num Key
        img, is_click = draw_button_on_click(img, Key.num_key, 
                                detectionList[8][0], detectionList[8][1])
        if is_click and finger_close:
            keyboard.press(key.text)
            num_lock = True
            sleep(0.2)
            return img
        
        for row in Key.upper_letter_keys:
            for key in row:
                img, is_click = draw_button_on_click(img, key, 
                                detectionList[8][0], detectionList[8][1])
                if is_click and finger_close:
                    cv2.rectangle(img, key.pos, 
                        (key.pos[0]+key.size[0], key.pos[1]+key.size[1]), 
                        (0,0,0), cv2.FILLED)
                    cv2.putText(img, key.text, key.text_pos, 
                                    cv2.FONT_ITALIC, 1.0, (255, 255, 255), 2)
                    clickedText += key.text
                    sleep(0.5)
                    return img
        
        # Handle Deletion
        img, is_click = draw_button_on_click(img, Key.del_key, 
                                    detectionList[8][0], detectionList[8][1])
        if is_click and finger_close:
            cv2.rectangle(img, Key.del_key.pos, 
            (Key.del_key.pos[0]+Key.del_key.size[0], Key.del_key.pos[1]+Key.del_key.size[1]), 
                            (0,0,0), cv2.FILLED)
            cv2.putText(img, Key.del_key.text, Key.del_key.text_pos, 
                            cv2.FONT_ITALIC, 1.0, (255, 255, 255), 2)
            if clickedText != "":
                clickedText = clickedText[:len(clickedText)-1]
            sleep(0.5)
            return img

        # Handle Clear
        img, is_click = draw_button_on_click(img, Key.clr_key, 
                                    detectionList[8][0], detectionList[8][1])
        if is_click and finger_close:
            cv2.rectangle(img, Key.clr_key.pos, 
            (Key.clr_key.pos[0]+Key.clr_key.size[0], Key.clr_key.pos[1]+Key.clr_key.size[1]), 
                            (0,0,0), cv2.FILLED)
            cv2.putText(img, Key.clr_key.text, Key.clr_key.text_pos, 
                            cv2.FONT_ITALIC, 1.0, (255, 255, 255), 2)
            clickedText = ""
            sleep(0.2)
            return img
        
        # Handle Space
        img, is_click = draw_button_on_click(img, Key.spc_key, 
                                    detectionList[8][0], detectionList[8][1])
        if is_click and finger_close:
            cv2.rectangle(img, Key.spc_key.pos, 
            (Key.spc_key.pos[0]+Key.spc_key.size[0], Key.spc_key.pos[1]+Key.spc_key.size[1]), 
                            (0,0,0), cv2.FILLED)
            cv2.putText(img, Key.spc_key.text, Key.spc_key.text_pos, 
                            cv2.FONT_ITALIC, 1.0, (255, 255, 255), 2)
            clickedText += " "
            sleep(0.5)
            return img
    return img

from numba import jit, cuda
# function optimized to run on gpu 
@jit
def handle_capture(img):
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    detectionList, bboxInfo = detector.findPosition(img)
    img = Key.draw_all_Keys(img, caps_lock, num_lock)
    
    if detectionList:
        img = handle_detection(detectionList, img)

    cv2.rectangle(img, (250,350), (1000,415), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, clickedText, (260,405), 
                cv2.FONT_ITALIC, 1.0, (0, 0, 0), 2)
    Key.draw_border(img, (240, 40), (1010, 430), (0,0,0), 4, 10, 25)

    return img

while True:
    success, img = cap.read()
    img = handle_capture(img)
    cv2.imshow("Image", img)
    video.write(img)
    if cv2.waitKey(1) & 0xFF == 27: break

cv2.destroyAllWindows()
cap.release()
video.release()


