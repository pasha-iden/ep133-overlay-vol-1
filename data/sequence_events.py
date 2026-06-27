# sequence_events.py
# Все значения start и end смещены назад на 10.3 секунды

SQUARE_EVENTS = [
    {"start": 9.230,  "end": 12.021, "line": 0, "place": 1, "active": 1},
    {"start": 12.021,  "end": 14.811, "line": 0, "place": 2, "active": 1}, # старая сцена 1
    # {"start": 12.021,  "end": 14.811, "line": 0, "place": 2, "active": 0}, # старая сцена 0

    {"start": 12.021,  "end": 14.811, "line": 1, "place": 1, "active": 0}, # новая сцена 0
    # {"start": 12.021,  "end": 14.811, "line": 1, "place": 1, "active": 1}, # новая сцена 1
    {"start": 14.811,  "end": 17.602, "line": 1, "place": 2, "active": 1},
    {"start": 17.602,  "end": 20.393, "line": 1, "place": 3, "active": 1},
    {"start": 20.393,  "end": 23.183, "line": 1, "place": 4, "active": 1},
    {"start": 23.183,  "end": 25.947, "line": 1, "place": 5, "active": 1}, # старая сцена 1
    # {"start": 23.183,  "end": 25.947, "line": 1, "place": 5, "active": 0}, # старая сцена 0

    {"start": 23.183, "end": 25.947, "line": 2, "place": 1, "active": 0}, # новая сцена 0
    # {"start": 23.183, "end": 25.947, "line": 2, "place": 1, "active": 1}, # новая сцена 1
    {"start": 25.947,  "end": 28.765, "line": 2, "place": 2, "active": 1},
    {"start": 28.765,  "end": 31.555, "line": 2, "place": 3, "active": 1},
    {"start": 31.555,  "end": 34.346, "line": 2, "place": 4, "active": 1}, # старая сцена 1
    # {"start": 31.555,  "end": 34.346, "line": 2, "place": 4, "active": 0}, # старая сцена 0

    {"start": 31.555,  "end": 34.346, "line": 3, "place": 1, "active": 0}, # новая сцена 0
    # {"start": 31.555,  "end": 34.346, "line": 3, "place": 1, "active": 1}, # новая сцена 1
    {"start": 34.346,  "end": 37.137, "line": 3, "place": 2, "active": 1},
    {"start": 37.137,  "end": 39.927, "line": 3, "place": 3, "active": 1},
    {"start": 39.927,  "end": 42.718, "line": 3, "place": 4, "active": 1},
    {"start": 42.718,  "end": 45.509, "line": 3, "place": 5, "active": 1},
    {"start": 45.509,  "end": 48.299, "line": 3, "place": 6, "active": 1},
    {"start": 48.299,  "end": 51.090, "line": 3, "place": 7, "active": 1},
    {"start": 51.090,  "end": 53.881, "line": 3, "place": 8, "active": 1},
    {"start": 53.881,  "end": 56.671, "line": 3, "place": 9, "active": 1}, # старая сцена 1
    # {"start": 53.881,  "end": 56.671, "line": 3, "place": 9, "active": 0}, # старая сцена 0

    {"start": 53.881,  "end": 56.671, "line": 4, "place": 1, "active": 0}, # новая сцена 0
    # {"start": 53.881,  "end": 56.671, "line": 4, "place": 1, "active": 1}, # новая сцена 1
    {"start": 56.671,  "end": 59.462, "line": 4, "place": 2, "active": 1}, # старая сцена 1
    # {"start": 56.671,  "end": 59.462, "line": 4, "place": 2, "active": 0}, # старая сцена 0

    {"start": 56.671,  "end": 59.462, "line": 5, "place": 1, "active": 0}, # новая сцена 0
    # {"start": 56.671,  "end": 59.462, "line": 5, "place": 1, "active": 1}, # новая сцена 1
    {"start": 59.462,  "end": 62.253, "line": 5, "place": 2, "active": 1},
    {"start": 62.253,  "end": 65.043, "line": 5, "place": 3, "active": 1},
    {"start": 65.043,  "end": 67.834, "line": 5, "place": 4, "active": 1},
    {"start": 67.834,  "end": 70.625, "line": 5, "place": 5, "active": 1},
    {"start": 70.625,  "end": 73.415, "line": 5, "place": 6, "active": 1},
    {"start": 73.415,  "end": 76.206, "line": 5, "place": 7, "active": 1},
    {"start": 76.206,  "end": 78.997, "line": 5, "place": 8, "active": 1}, # старая сцена 1
    # {"start": 76.206,  "end": 78.997, "line": 5, "place": 8, "active": 0}, # старая сцена 0

    {"start": 76.206, "end": 78.997, "line": 6, "place": 1, "active": 0},  # новая сцена 0
    # {"start": 76.206, "end": 78.997, "line": 6, "place": 1, "active": 1},  # новая сцена 1
    {"start": 78.997,  "end": 81.787, "line": 6, "place": 2, "active": 1},
    {"start": 81.787,  "end": 84.578, "line": 6, "place": 3, "active": 1},
    {"start": 84.578,  "end": 87.369, "line": 6, "place": 4, "active": 1},
    {"start": 87.369,  "end": 90.159, "line": 6, "place": 5, "active": 1}, # старая сцена 1
    # {"start": 87.369,  "end": 90.159, "line": 6, "place": 5, "active": 0}, # старая сцена 0

    {"start": 87.369, "end": 90.159, "line": 1, "place": 6, "active": 0},  # новая сцена 0
    # {"start": 87.369, "end": 90.159, "line": 1, "place": 6, "active": 1},  # новая сцена 1
    {"start": 90.159, "end": 92.950, "line": 1, "place": 7, "active": 1},
    {"start": 92.950, "end": 95.741, "line": 1, "place": 8, "active": 1},
    {"start": 95.741, "end": 98.531, "line": 1, "place": 9, "active": 1},
    {"start": 98.531, "end": 101.322, "line": 1, "place": 10, "active": 1},
    {"start": 101.322, "end": 104.113, "line": 1, "place": 11, "active": 1}, # старая сцена 1
    # {"start": 101.322, "end": 104.113, "line": 1, "place": 11, "active": 0}, # старая сцена 1

    {"start": 101.322, "end": 104.113, "line": 2, "place": 5, "active": 0},  # новая сцена 0
    # {"start": 101.322, "end": 104.113, "line": 2, "place": 5, "active": 1},  # новая сцена 1
    {"start": 104.113, "end": 106.903, "line": 2, "place": 6, "active": 1},
    {"start": 106.903, "end": 109.694, "line": 2, "place": 7, "active": 1},
    {"start": 109.694, "end": 112.485, "line": 2, "place": 8, "active": 1}, # старая сцена 1
    # {"start": 109.694, "end": 112.485, "line": 2, "place": 8, "active": 0}, # старая сцена 1

    {"start": 109.694, "end": 112.485, "line": 3, "place": 10, "active": 0}, # новая сцена 0
    # {"start": 109.694, "end": 112.485, "line": 3, "place": 10, "active": 1}, # новая сцена 1
    {"start": 112.485, "end": 115.275, "line": 3, "place": 11, "active": 1},
    {"start": 115.275, "end": 118.066, "line": 3, "place": 12, "active": 1},
    {"start": 118.066, "end": 120.857, "line": 3, "place": 13, "active": 1},
    {"start": 120.857, "end": 123.647, "line": 3, "place": 14, "active": 1},
    {"start": 123.647, "end": 126.438, "line": 3, "place": 15, "active": 1},
    {"start": 126.438, "end": 129.229, "line": 3, "place": 16, "active": 1},
    {"start": 129.229, "end": 132.012, "line": 3, "place": 17, "active": 1},
    {"start": 132.012, "end": 134.810, "line": 3, "place": 18, "active": 1}, # старая сцена 1
    # {"start": 132.012, "end": 134.810, "line": 3, "place": 18, "active": 0}, # старая сцена 1

    {"start": 132.012, "end": 134.810, "line": 7, "place": 1, "active": 0}, # новая сцена 0
    # {"start": 132.012, "end": 134.810, "line": 7, "place": 1, "active": 1}, # новая сцена 1
    {"start": 134.810, "end": 137.601, "line": 7, "place": 2, "active": 1},

    # {"start": 134.810, "end": 137.601, "line": 1, "place": 16, "active": 1},
    # {"start": 137.601, "end": 140.390, "line": 1, "place": 16, "active": 1},
    # {"start": 140.390, "end": 143.182, "line": 1, "place": 16, "active": 1},
    # {"start": 143.182, "end": 145.973, "line": 1, "place": 16, "active": 1},
    # {"start": 145.973, "end": 148.763, "line": 1, "place": 16, "active": 1},

]