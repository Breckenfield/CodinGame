import sys
import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Entity:
    def __init__(self, x, y, vx, vy, _id):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self._id = _id

    def distance_to_coordinate(self, x, y):
        p = [self.x, self.y]
        q = [x, y]
        distance = math.dist(p, q)
        return distance

    def distance_to_entity(self, entity):
        distance = self.distance_to_coordinate(entity.x, entity.y)
        return distance

    def vector_to_coordinate(self, x, y):
        norm = self.distance_to_coordinate(x, y)
        direction = [(x - self.x)/norm, (y - self.y)/norm]
        vector = [direction[0] * math.sqrt(2), direction[1] * math.sqrt(2)]
        return vector[0], vector[1] 
    
    def vector_to_entity(self, entity):
        vx, vy = self.vector_to_coordinate(entity.x, entity.y)
        return vx, vy
    
    def angle_to_coordinate(self, x, y):
        vx, vy = self.vector_to_coordinate(x, y)
        rad = np.arctan2(vx, vy)
        degree = np.mod(np.degrees(rad), 360)
        return degree
    
    def angle_of_vector(self, vx, vy):
        rad = np.arctan2(vx, vy)
        degree = np.mod(np.degrees(rad), 360)
        return degree
    
    def angle_to_entity(self, entity):
        degree = self.angle_to_coordinate(entity.x, entity.y)
        return degree

    def velocity(self):
        velocity = math.sqrt(self.vx**2 + self.vy**2)
        return velocity
        

class Checkpoint(Entity):
    def __init__(self, x, y, vx, vy, _id):
        super().__init__(x, y, vx, vy, _id)
        self.radius = 600

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

class Pod(Entity):
    def __init__(self, x, y, vx, vy, angle, checkpoint, _id):
        super().__init__(x, y, vx, vy, _id)
        self.checkpoint = checkpoint
        self.angle = angle
        self.boost = 1
        self.radius = 400

    def action_accelerate(self, x, y, thrust):
        if thrust > 100:
            thrust = 100
        elif thrust < 0:
            thrust = 0
        print("{} {} {}".format(x, y, thrust))

    def action_boost(self, x, y):
        print("{} {} {}".format(x, y, "BOOST"))
    
    def action_shield(self, x, y):
        print("{} {} {}".format(x, y, "SHIELD"))

laps = int(input())
checkpoint_count = int(input())
checkpoints = []
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    checkpoint = Checkpoint(checkpoint_x, checkpoint_y, 0, 0, i)
    checkpoints.append(checkpoint)

first_lap = True
# game loop
while True:
    my_pods = []
    op_pods = []
    for i in range(2):
        # x: x position of your pod
        # y: y position of your pod
        # vx: x speed of your pod
        # vy: y speed of your pod
        # angle: angle of your pod
        # next_check_point_id: next check point id of your pod
        x, y, vx, vy, angle, next_check_point_id = [int(j) for j in input().split()]
        pod = Pod(x, y, vx, vy, angle, next_check_point_id, i)
        my_pods.append(pod)
    for i in range(2):
        # x_2: x position of the opponent's pod
        # y_2: y position of the opponent's pod
        # vx_2: x speed of the opponent's pod
        # vy_2: y speed of the opponent's pod
        # angle_2: angle of the opponent's pod
        # next_check_point_id_2: next check point id of the opponent's pod
        x, y, vx, vy, angle, next_check_point_id = [int(j) for j in input().split()]
        pod = Pod(x, y, vx, vy, angle, next_check_point_id, i)
        op_pods.append(pod)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    for my_pod in my_pods:
        next_checkpoint = checkpoints[my_pod.checkpoint]
        checkpoint_vector = my_pod.vector_to_entity(next_checkpoint)
        final_vector = [checkpoint_vector[0] - my_pod.vx, checkpoint_vector[1] - my_pod.vy]
        final_position_x = int(next_checkpoint.x + final_vector[0]*2)
        final_position_y = int(next_checkpoint.y + final_vector[1]*2)
        checkpoint_distance = my_pod.distance_to_entity(next_checkpoint)
        distance_scaler = checkpoint_distance/(next_checkpoint.radius*4)
        angle_checkpoint = my_pod.angle_to_entity(next_checkpoint)
        angle_heading = my_pod.angle_of_vector(my_pod.vx, my_pod.vy)
        angle_scaler = abs(angle_heading - angle_checkpoint)/45

        if my_pod._id == 0 and my_pod.boost > 0:
            my_pod.action_boost(final_position_x, final_position_y)
        else:
            my_pod.action_accelerate(final_position_x, final_position_y, int(100*distance_scaler))