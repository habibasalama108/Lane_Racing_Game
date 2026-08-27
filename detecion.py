import cv2

# Steer (open palm)
vid1 = cv2.VideoCapture("steer_video/WIN_20260827_17_13_40_Pro.mp4")
count1, saved1, success1 = 0, 0, True
while success1:
    success1, image1 = vid1.read()
    if success1 and count1 % 10 == 0:
        cv2.imwrite(f"steer_frame{saved1}.jpg", image1)
        saved1 += 1
    count1 += 1
vid1.release()

# Kachow boost (peace sign)
vid2 = cv2.VideoCapture("kachow_video/WIN_20260827_17_19_56_Pro.mp4")
count2, saved2, success2 = 0, 0, True
while success2:
    success2, image2 = vid2.read()
    if success2 and count2 % 10 == 0:
        cv2.imwrite(f"kachow_frame{saved2}.jpg", image2)
        saved2 += 1
    count2 += 1
vid2.release()

# Negative (wrong gestures / no hand)
vid3 = cv2.VideoCapture("negative_video/WIN_20260827_17_24_01_Pro.mp4")
count3, saved3, success3 = 0, 0, True
while success3:
    success3, image3 = vid3.read()
    if success3 and count3 % 10 == 0:
        cv2.imwrite(f"negative_frame{saved3}.jpg", image3)
        saved3 += 1
    count3 += 1
vid3.release()

print("All frames extracted successfully!")