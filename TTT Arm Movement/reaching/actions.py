def process_actions(
    actions,
    current_positions,
    joint_limits,
    action_scale=0.05
):
    """
    Convert RL actions into joint position targets.

    actions:
        Values between -1 and 1.

    current_positions:
        Current joint angles in radians.

    joint_limits:
        List of (minimum, maximum) joint angles.

    action_scale:
        Maximum joint adjustment per action.
        Default: 0.05 radians.

    Returns:
        List of target joint angles.
    """

    if not (
        len(actions)
        == len(current_positions)
        == len(joint_limits)
    ):
        raise ValueError(
            "Actions, positions and limits must have equal lengths."
        )

    targets = []

    for action, current, limits in zip(
        actions,
        current_positions,
        joint_limits
    ):

        # Keep action between -1 and 1
        action = max(-1.0, min(1.0, action))

        # Calculate target position
        target = current + action * action_scale

        # Enforce joint limits
        minimum, maximum = limits

        target = max(
            minimum,
            min(maximum, target)
        )

        targets.append(target)

    return targets