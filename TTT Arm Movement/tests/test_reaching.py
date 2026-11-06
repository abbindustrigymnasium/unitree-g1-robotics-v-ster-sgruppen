import unittest

from reaching.observations import get_observation
from reaching.actions import process_actions
from reaching.target_generator import TargetGenerator

from reaching.rewards import (
    reaching_reward,
    success_reward,
    movement_penalty,
)

from reaching.terminations import (
    target_reached,
    episode_timeout,
    unsafe_joint_positions,
    should_terminate,
)

class TestReaching(unittest.TestCase):

    def test_target_within_bounds(self):
        generator = TargetGenerator(
            x_range=(0.3, 0.6),
            y_range=(-0.3, -0.1),
            z_range=(0.7, 0.9),
            seed=42
        )

        for _ in range(100):
            x, y, z = generator.generate_target()

            self.assertTrue(0.3 <= x <= 0.6)
            self.assertTrue(-0.3 <= y <= -0.1)
            self.assertTrue(0.7 <= z <= 0.9)


    def test_target_dimensions(self):
        generator = TargetGenerator()

        target = generator.generate_target()

        self.assertEqual(len(target), 3)


    def test_target_randomization(self):
        generator = TargetGenerator(seed=42)

        first = generator.generate_target()
        second = generator.generate_target()

        self.assertNotEqual(first, second)


    def test_target_reproducibility(self):
        generator_a = TargetGenerator(seed=123)
        generator_b = TargetGenerator(seed=123)

        targets_a = generator_a.generate_batch(10)
        targets_b = generator_b.generate_batch(10)

        self.assertEqual(targets_a, targets_b)


    def test_generate_batch(self):
        generator = TargetGenerator(seed=42)

        targets = generator.generate_batch(20)

        self.assertEqual(len(targets), 20)

        for target in targets:
            self.assertEqual(len(target), 3)

    def test_target_reached(self):
        self.assertTrue(
            target_reached(
                [0.50, 0.0, 0.8],
                [0.51, 0.0, 0.8]
            )
        )


    def test_target_not_reached(self):
        self.assertFalse(
            target_reached(
                [0.50, 0.0, 0.8],
                [0.60, 0.0, 0.8]
            )
        )


    def test_episode_timeout(self):
        self.assertTrue(
            episode_timeout(
                elapsed_time=12.0,
                max_duration=10.0
            )
        )


    def test_unsafe_joint_positions(self):
        self.assertTrue(
            unsafe_joint_positions(
                joint_positions=[0.2, 1.5],
                joint_limits=[
                    (-1.0, 1.0),
                    (-1.0, 1.0)
                ]
            )
        )


    def test_should_terminate_success(self):
        terminated, reason = should_terminate(
            hand_pos=[0.50, 0.0, 0.8],
            target_pos=[0.51, 0.0, 0.8],
            elapsed_time=3.0,
            joint_positions=[0.2, 0.4],
            joint_limits=[
                (-1.0, 1.0),
                (-1.0, 1.0)
            ]
        )

        self.assertTrue(terminated)
        self.assertEqual(reason, "success")

    def test_positive_action(self):
        targets = process_actions(
            actions=[1.0],
            current_positions=[0.5],
            joint_limits=[(-1.0, 1.0)]
        )

        self.assertAlmostEqual(targets[0], 0.55)


    def test_negative_action(self):
        targets = process_actions(
            actions=[-1.0],
            current_positions=[0.5],
            joint_limits=[(-1.0, 1.0)]
        )

        self.assertAlmostEqual(targets[0], 0.45)


    def test_action_clipping(self):
        targets = process_actions(
            actions=[5.0],
            current_positions=[0.5],
            joint_limits=[(-1.0, 1.0)]
        )

        self.assertAlmostEqual(targets[0], 0.55)


    def test_joint_limits(self):
        targets = process_actions(
            actions=[1.0],
            current_positions=[0.99],
            joint_limits=[(-1.0, 1.0)]
        )

        self.assertAlmostEqual(targets[0], 1.0)


    def test_multiple_joints(self):
        targets = process_actions(
            actions=[1.0, -1.0, 0.0],
            current_positions=[0.0, 0.5, -0.2],
            joint_limits=[
                (-1.0, 1.0),
                (-1.0, 1.0),
                (-1.0, 1.0)
            ]
        )

        self.assertEqual(len(targets), 3)

        self.assertAlmostEqual(targets[0], 0.05)
        self.assertAlmostEqual(targets[1], 0.45)
        self.assertAlmostEqual(targets[2], -0.2)

    def test_observation(self):
        joint_positions = [0.1, 0.2, 0.3]
        joint_velocities = [0.0, 0.0, 0.0]
        hand_position = [0.4, 0.1, 0.8]
        target_position = [0.5, 0.2, 0.8]
        previous_actions = [0.0, 0.0, 0.0]

        observation = get_observation(
            joint_positions,
            joint_velocities,
            hand_position,
            target_position,
            previous_actions
        )

        self.assertEqual(len(observation), 12)

        self.assertAlmostEqual(observation[6], 0.1)
        self.assertAlmostEqual(observation[7], 0.1)
        self.assertAlmostEqual(observation[8], 0.0)



    def test_perfect_reach(self):
        """
        The hand is exactly at the target.
        Reward should be 1.
        """

        hand = [0.5, 0.0, 0.8]
        target = [0.5, 0.0, 0.8]

        reward = reaching_reward(hand, target)

        self.assertAlmostEqual(reward, 1.0)


    def test_closer_is_better(self):
        """
        A closer hand should receive
        a higher reward.
        """

        target = [0.5, 0.0, 0.8]

        close = [0.48, 0.0, 0.8]
        far = [0.2, 0.0, 0.8]

        close_reward = reaching_reward(
            close,
            target
        )

        far_reward = reaching_reward(
            far,
            target
        )

        self.assertGreater(
            close_reward,
            far_reward
        )


    def test_success(self):
        """
        A hand within 2 cm should
        count as reaching the target.
        """

        hand = [0.5, 0.0, 0.8]
        target = [0.51, 0.0, 0.8]

        reward = success_reward(
            hand,
            target
        )

        self.assertEqual(reward, 1.0)


    def test_failure(self):
        """
        A hand farther than 2 cm
        should not receive success reward.
        """

        hand = [0.5, 0.0, 0.8]
        target = [0.6, 0.0, 0.8]

        reward = success_reward(
            hand,
            target
        )

        self.assertEqual(reward, 0.0)


    def test_movement_penalty(self):
        """
        Higher joint velocities should
        produce a larger penalty.
        """

        stationary = [0.0, 0.0, 0.0]
        moving = [1.0, 2.0, 3.0]

        stationary_penalty = movement_penalty(
            stationary
        )

        moving_penalty = movement_penalty(
            moving
        )

        self.assertLess(
            stationary_penalty,
            moving_penalty
        )


if __name__ == "__main__":
    unittest.main()