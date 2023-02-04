import cv2
GAP = 75

class Key():
    def __init__(self, text, pos, size=[60,60], text_pos=None):
        self.pos = pos
        self.text = text
        self.size = size
        self.rect_size = [size[0]+pos[0], size[1]+pos[1]]
        if text_pos:
            self.text_pos = text_pos
        else: 
            self.text_pos = [self.pos[0]+20, self.rect_size[1]-20]

    def draw(self, img):
        cv2.rectangle(img, self.pos, self.rect_size, (255,255,255), cv2.FILLED)
        cv2.putText(img, self.text, self.text_pos, 
                    cv2.FONT_ITALIC, 1.0, (0,0,0), 2)
        return img


lower_letters = {'first_row': ['q', 'w', 'e', 'r', 't', 'y','u','i','o','p'],
                    'second_row': ['a', 's','d','f','g','h','j','k','l', ],
                    'third_row': ['z','x','c','v','b','n','m',]}

upper_letters = {'first_row': ['Q','W','E','R','T','Y','U','I','O','P'],
                    'second_row': ['A','S','D','F','G','H','J','K','L',],
                    'third_row': ['Z','X','C','V','B','N','M',]}

num_letters = {'first_row': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                    'second_row': ['-','/',':',';','(',')','$','&','@',],
                    'third_row': ['.',',','?','!','"','*','#',]}

lower_letter_keys = [ [Key(l, [250+GAP*i, 50]) for i, l in enumerate(lower_letters['first_row'])], 
                   [Key(l, [275+GAP*i, 50+GAP*1]) for i, l in enumerate(lower_letters['second_row'])],
                   [Key(l, [350+GAP*i, 50+GAP*2]) for i, l in enumerate(lower_letters['third_row'])]]       

upper_letter_keys = [ [Key(l, [250+GAP*i, 50]) for i, l in enumerate(upper_letters['first_row'])], 
                   [Key(l, [275+GAP*i, 50+GAP*1]) for i, l in enumerate(upper_letters['second_row'])],
                   [Key(l, [350+GAP*i, 50+GAP*2]) for i, l in enumerate(upper_letters['third_row'])]]   


num_keys = [ [Key(l, [250+GAP*i, 50]) for i, l in enumerate(num_letters['first_row'])], 
                   [Key(l, [275+GAP*i, 50+GAP*1]) for i, l in enumerate(num_letters['second_row'])],
                   [Key(l, [350+GAP*i, 50+GAP*2]) for i, l in enumerate(num_letters['third_row'])]]   


Key_list ={ True: upper_letter_keys, False: lower_letter_keys }


# Function Keys
cap_key = Key('CAP', [250, 50+GAP*2], [85, 60], [260, 90+GAP*2])
del_key = Key('DEL', [200+GAP*9, 50+GAP*2], [85, 60], [GAP*9+210, 90+GAP*2])

# Last Row Key
num_key = Key('123',   [250,       50+GAP*3], [85, 60], [260, 90+GAP*3])
abc_key = Key('ABC',   [250,       50+GAP*3], [85, 60], [260, 90+GAP*3])
spc_key = Key('SPACE', [275+GAP,   50+GAP*3], [450, 60], [525, 90+GAP*3])
clr_key = Key('CLEAR', [225+GAP*8, 50+GAP*3], [130, 60], [235+GAP*8, 90+GAP*3])
func_keys = [del_key, spc_key, clr_key]

def draw_all_Keys(img, draw_caps=True, draw_num=False):
    if draw_num:
        for row in num_keys:
            for letter in row:
                img = letter.draw(img)
        img = abc_key.draw(img)      
    else:
        for row in Key_list[draw_caps]:
            for letter in row:
                img = letter.draw(img)
        img = cap_key.draw(img)
        img = num_key.draw(img)

    for key in func_keys:
        img = key.draw(img)
    return img

import numpy as np
def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1,y1 = pt1
    x2,y2 = pt2
    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)
    return img