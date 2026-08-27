
class LaneManager:

    # Initialize lane settings
    def __init__(self, screen_width, num_lanes):
        self.screen_width = screen_width
        self.num_lanes = num_lanes

        # Calculate width of each lane
        self.lane_width = screen_width / num_lanes


    # Get lane number from X position
    def get_lane_from_x(self, x):
        lane = int(x / self.lane_width) + 1

        # Keep lane witin valid range
        lane = max(1, min(lane,self.num_lanes ))
        return lane


    # Get center X of a lane
    def get_lane_center(self, lane):
        return int((lane - 0.5) * self.lane_width)

    