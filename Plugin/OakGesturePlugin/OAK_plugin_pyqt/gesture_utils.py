import numpy as np


def is_fist(landmarks):
    folded = lambda tip, pip: landmarks[tip].y > landmarks[pip].y
    return all(folded(t, p) for t, p in [(8, 6), (12, 10), (16, 14), (20, 18)])


def is_stop(landmarks):
    extended_fingers = [landmarks[4].y < landmarks[3].y,
                        landmarks[8].y < landmarks[6].y,
                        landmarks[12].y < landmarks[10].y,
                        landmarks[16].y < landmarks[14].y,
                        landmarks[20].y < landmarks[18].y]
    return all(extended_fingers)


def is_pointing(landmarks):
    return (landmarks[8].y < landmarks[6].y and
            all(landmarks[t].y > landmarks[p].y for t, p in [(12, 10), (16, 14), (20, 18)]))


def is_okay_gesture(landmarks):
    def distance(p1, p2):
        return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    touching = distance(landmarks[4], landmarks[8]) < 0.05
    middle_extended = landmarks[12].y < landmarks[10].y
    return touching and middle_extended


def is_v_gesture(landmarks):
    return (landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and
            landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y)



def is_four_fingers_no_thumb(landmarks):
    if landmarks is None:
        return False
    return (
        landmarks[8].y < landmarks[6].y and
        landmarks[12].y < landmarks[10].y and
        landmarks[16].y < landmarks[14].y and
        landmarks[20].y < landmarks[18].y and
        landmarks[4].x > landmarks[3].x
    )



# def is_slab_gesture(landmarks):
#     if landmarks is None:
#         return False
#
#     # Wyprostowane 3 palce
#     index = landmarks[8].y < landmarks[6].y
#     middle = landmarks[12].y < landmarks[10].y
#     ring = landmarks[16].y < landmarks[14].y
#
#     # Kciuk i pinky zgięte
#     thumb = landmarks[4].x > landmarks[3].x
#     pinky = landmarks[20].y > landmarks[18].y
#
#     # Odległości między końcówkami palców (x) – zbliżone
#     close_fingers = abs(landmarks[8].x - landmarks[12].x) < 0.05 and abs(landmarks[12].x - landmarks[16].x) < 0.05
#
#     return index and middle and ring and thumb and pinky and close_fingers

def is_fist_with_thumb_180(landmarks):
    if landmarks is None or len(landmarks) < 21:
        return False

    # Sprawdzenie, czy palce są zgięte (tip poniżej pip w układzie y)
    folded_fingers = all(
        landmarks[tip].y > landmarks[pip].y
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]
    )

    # Odległość pozioma między końcówką kciuka a jego sąsiednim punktem
    thumb_horizontal_distance = abs(landmarks[4].x - landmarks[3].x)

    # Opcjonalnie: przeskalowanie progu w zależności od szerokości dłoni
    # Można dodać np. skalowanie względem dystansu między nadgarstkiem (0) a MCP środkowego palca (9)

    is_thumb_extended = thumb_horizontal_distance >= 0.02


    return folded_fingers and is_thumb_extended



import math

def is_thumb_up_l_shape(landmarks):
    if landmarks is None or len(landmarks) < 21:
        return False

    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    # Palec wskazujący wyprostowany: odległość między tip a pip większa niż próg
    index_finger_length = distance(landmarks[8], landmarks[6])
    index_straight = index_finger_length > 0.05

    # Kciuk uniesiony: różnica w Y lub wystająca długość
    thumb_length = distance(landmarks[4], landmarks[3])
    thumb_up = landmarks[4].y < landmarks[3].y - 0.015 or thumb_length > 0.04

    # Pozostałe palce zgięte (tip poniżej pip)
    other_fingers_folded = all(
        landmarks[tip].y > landmarks[pip].y + 0.01
        for tip, pip in [(12, 10), (16, 14), (20, 18)]
    )

    return index_straight and thumb_up and other_fingers_folded


