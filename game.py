import cv2
import numpy as np

from lane_manager import LaneManager


WIDTH = 600
HEIGHT = 400

NUM_LANES = 3

lane_manager = LaneManager(WIDTH, NUM_LANES)


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


while True:

    # Create screen
    frame = np.zeros(
        (HEIGHT, WIDTH, 3),
        dtype=np.uint8
    )

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

    # Show game
    cv2.imshow("Lightning McQueen", frame)

    # Keyboard control
    key = cv2.waitKey(30) & 0xFF

    if key == ord("q"):
        break


cv2.destroyAllWindows()