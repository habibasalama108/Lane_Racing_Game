import cv2
import numpy as np
from obstacels_katchaw import ObstacleManager
from lane_manager import LaneManager
import time 
import random



WIDTH = 640
HEIGHT = 480
NUM_LANES = 3

lane_manager = LaneManager(WIDTH, NUM_LANES)
obstacle_manager = ObstacleManager(NUM_LANES, speed = 3)
last_spawn_time = 0
SPAWN_INTERVAL = 3

previous_gesture = None



# Fake hand position
hand_x = 60

# McQueen position
mcqueen_x = float(hand_x)
mcqueen_y = HEIGHT - 60

# McQueen size 
CAR_WIDTH = 60
CAR_HEIGHT = 40

# Keep McQueen inside the frame
MIN_X = CAR_WIDTH // 2
MAX_X = WIDTH - CAR_WIDTH // 2
# Smoothness
SMOOTHNESS = 0.08

def run_game(frame, hand_x, gesture):

        global mcqueen_x, last_spawn_time, previous_gesture
        

        # Draw lanes
        for i in range(1, NUM_LANES):

            x = int(i * lane_manager.lane_width)

            cv2.line(
                frame,
                (x, 0),
                (x, HEIGHT),
                (255, 255, 255),
                2
            )

        # Find current lane
        current_lane = lane_manager.get_lane_from_x(hand_x)
        if gesture == "kachow" and previous_gesture != "kachow":
        
            print("🔥 KACHOW DETECTED")
            print("Nitro BEFORE:", obstacle_manager.nitro_points)

            activated = obstacle_manager.activate_kachow(current_lane)

            print("Activated:", activated)
            print("Nitro AFTER:", obstacle_manager.nitro_points)
        previous_gesture = None

        obstacle_manager.update()
        event = obstacle_manager.check_collision(
        current_lane,
        mcqueen_y
        )
        if event == "nitro":
            print("🔥 NITRO COLLECTED!")
            print("NITRO COUNT:", obstacle_manager.nitro_points)

        cv2.putText(
            frame,
            f"Nitro: {obstacle_manager.nitro_points}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 0),
            2
            )

        for item in obstacle_manager.items:

        # Convert lane number to X position
            lane_x = (item.lane - 0.5) * lane_manager.lane_width

            x = int(lane_x)
            y = int(item.y)

            if item.type == "nitro":
                color = (17, 255, 37)    

            cv2.rectangle(
                frame,
                (x - 20, y - 20),
                (x + 20, y + 20),
                (17, 255, 37),
                -1
            )    

        

        current_time = time.time()

        if current_time - last_spawn_time >= SPAWN_INTERVAL:
            obstacle_manager.random_spawn()
            last_spawn_time = current_time

        

        # Draw obstacles and nitro
        for item in obstacle_manager.items:

            lane_center_x = int(
                item.lane * lane_manager.lane_width
                + lane_manager.lane_width / 2
            )

            y = int(item.y)

            if item.type == "obstacle":
                color = (10, 50, 155)
            # else:
            #     color = (45, 95, 55)

            cv2.rectangle(
                frame,
                (lane_center_x - 25, y - 25),
                (lane_center_x + 25, y + 25),
                (10, 50, 155),
                -1
            )



        # Target = actual hand position
        target_x = max(MIN_X, min(hand_x, MAX_X))

        # Smooth movement
        mcqueen_x += (target_x - mcqueen_x) * SMOOTHNESS

        # Draw McQueen
        x = int(mcqueen_x)

        cv2.rectangle(
            frame,
            (x - CAR_WIDTH // 2, mcqueen_y - CAR_HEIGHT // 2),
            (x + CAR_WIDTH // 2, mcqueen_y + CAR_HEIGHT // 2),
            (0, 0, 255),
            -1
        )

        # Information
        cv2.putText(
            frame,
            f"Hand X: {hand_x}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"McQueen X: {int(mcqueen_x)}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Lane: {current_lane}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        return frame

