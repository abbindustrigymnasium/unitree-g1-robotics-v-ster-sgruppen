import math


def target_reached(
    hand_pos,
    target_pos,
    tolerance=0.02
):
    """
    Check whether the hand is within
    the specified distance of the target.

    Default tolerance: 2 cm.
    """

    distance = math.dist(hand_pos, target_pos)

    return distance < tolerance


def episode_timeout(
    elapsed_time,
    max_duration=10.0
):
    """
    Check whether the episode has exceeded
    its maximum duration.

    Time is measured in seconds.
    """

    return elapsed_time >= max_duration


def unsafe_joint_positions(
    joint_positions,
    joint_limits
):
    """
    Check whether any joint is outside
    its allowed range.
    """

    if len(joint_positions) != len(joint_limits):
        raise ValueError(
            "Positions and limits must have equal lengths."
        )

    for position, (minimum, maximum) in zip(
        joint_positions,
        joint_limits
    ):
        if position < minimum or position > maximum:
            return True

    return False


def should_terminate(
    hand_pos,
    target_pos,
    elapsed_time,
    joint_positions,
    joint_limits
):
    """
    Return whether the episode should end
    and why.

    Returns:
        (terminated, reason)
    """

    if unsafe_joint_positions(
        joint_positions,
        joint_limits
    ):
        return True, "unsafe"

    if target_reached(hand_pos, target_pos):
        return True, "success"

    if episode_timeout(elapsed_time):
        return True, "timeout"

    return False, None