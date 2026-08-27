import random
import time


class Item:
    def __init__(self, lane, y, item_type, speed):
        self.lane = lane
        self.y = y
        self.type = item_type
        self.speed = speed

    def move(self):
        self.y += self.speed


class ObstacleManager:
    def __init__(self, lanes, speed=5):
        self.lanes = lanes
        self.speed = speed
        self.items = []

        self.nitro_points = 0

        # Kachow Boost
        self.boost_active = False
        self.boost_end_time = 0


    # Spawn Obstacle
    def spawn_obstacle(self):
        lane = random.randrange(self.lanes)

        obstacle = Item(
            lane=lane,
            y=0,
            item_type="obstacle",
            speed=self.speed
        )

        self.items.append(obstacle)

    # Spawn Nitro
    def spawn_nitro(self):
        lane = random.randrange(self.lanes)

        nitro = Item(
            lane=lane,
            y=0,
            item_type="nitro",
            speed=self.speed
        )

        self.items.append(nitro)


    # Random Spawn
    def random_spawn(self):
        if random.random() < 0.7:
            self.spawn_obstacle()
        else:
            self.spawn_nitro()

    # Move Items
    def update(self):
        for item in self.items:
            item.move()

        self.update_boost()


    # Collision / Pickup
    def check_collision(self, mcqueen_lane, mcqueen_y):

        for item in self.items[:]:

            if item.lane != mcqueen_lane:
                continue

            # Distance between McQueen and item
            if abs(item.y - mcqueen_y) < 50:

                # Nitro pickup
                if item.type == "nitro":
                    self.nitro_points += 1
                    self.items.remove(item)

                    return "nitro"

                # Obstacle collision
                if item.type == "obstacle":

                    # Boost protects McQueen
                    if self.boost_active:
                        self.items.remove(item)
                        return "destroyed"

                    self.items.remove(item)
                    return "collision"

        return None


    # Kachow Boost
    def activate_kachow(self, mcqueen_lane):

        # No Nitro available
        if self.nitro_points <= 0:
            return False

        # Consume one Nitro
        self.nitro_points -= 1

        # Activate boost
        self.boost_active = True
        self.boost_end_time = time.time() + 2

        # Remove obstacles from current lane
        self.items = [
            item for item in self.items
            if not (
                item.type == "obstacle"
                and item.lane == mcqueen_lane
            )
        ]
        return True
    
    # Boost Timer
    def update_boost(self):

        if self.boost_active:

            if time.time() >= self.boost_end_time:
                self.boost_active = False

    # Check Boost Status  
    def is_boost_active(self):
        return self.boost_active