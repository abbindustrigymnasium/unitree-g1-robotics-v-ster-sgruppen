import math


def reaching_reward(hand_pos, target_pos):
    """
    Reward the robot for moving its hand
    closer to the target.

    Parameters:
        hand_pos: [x, y, z]
        target_pos: [x, y, z]

    Positions are measured in metres.

    Returns:
        Reward between 0 and 1.
    """

    distance = math.dist(hand_pos, target_pos)

    return math.exp(-10.0 * distance)


def success_reward(hand_pos, target_pos):
    """
    Reward the robot for reaching its target.

    Success means the hand is within
    2 centimetres of the target.
    """

    distance = math.dist(hand_pos, target_pos)

    if distance < 0.02:
        return 1.0

    return 0.0


def movement_penalty(joint_velocities):
    """
    Penalize excessive joint movement.

    Higher joint velocities produce
    a larger penalty.
    """

    return sum(
        velocity ** 2
        for velocity in joint_velocities
    )