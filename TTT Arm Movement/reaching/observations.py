def get_observation(
    joint_positions,
    joint_velocities,
    hand_position,
    target_position,
    previous_actions
):
    """
    Build the observation vector for the reaching policy.

    All positions use metres.
    Joint positions use radians.
    Joint velocities use radians/second.
    """

    position_error = [
        target - hand
        for target, hand in zip(target_position, hand_position)
    ]

    observation = (
        list(joint_positions)
        + list(joint_velocities)
        + list(position_error)
        + list(previous_actions)
    )

    return observation