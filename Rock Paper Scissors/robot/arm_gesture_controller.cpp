// Unitree G1 arm fallback gestures for rock-paper-scissors.
// Build requirements: Unitree G1 SDK headers and libraries.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstring>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>

#include <unitree/idl/hg/LowCmd_.hpp>
#include <unitree/idl/hg/LowState_.hpp>
#include <unitree/robot/channel/channel_publisher.hpp>
#include <unitree/robot/channel/channel_subscriber.hpp>

namespace {

constexpr float kPi = 3.141592654f;
constexpr float kPi2 = 1.57079632679f;
const std::string kTopicArmSDK = "rt/arm_sdk";
const std::string kTopicState = "rt/lowstate";

enum JointIndex {
    kLeftHipPitch = 0,
    kLeftHipRoll = 1,
    kLeftHipYaw = 2,
    kLeftKnee = 3,
    kLeftAnkle = 4,
    kLeftAnkleRoll = 5,
    kRightHipPitch = 6,
    kRightHipRoll = 7,
    kRightHipYaw = 8,
    kRightKnee = 9,
    kRightAnkle = 10,
    kRightAnkleRoll = 11,
    kWaistYaw = 12,
    kWaistRoll = 13,
    kWaistPitch = 14,
    kLeftShoulderPitch = 15,
    kLeftShoulderRoll = 16,
    kLeftShoulderYaw = 17,
    kLeftElbowPitch = 18,
    kLeftElbowRoll = 19,
    kRightShoulderPitch = 22,
    kRightShoulderRoll = 23,
    kRightShoulderYaw = 24,
    kRightElbowPitch = 25,
    kRightElbowRoll = 26,
    kNotUsedJoint = 29,
};

struct GestureTarget {
    std::array<float, 13> joints;
};

GestureTarget restTarget() {
    return GestureTarget{{0.f, 0.f, 0.f, 0.f, 0.f,
                          0.f, 0.f, 0.f, 0.f, 0.f,
                          0.f, 0.f, 0.f}};
}

GestureTarget gestureTarget(const std::string& gesture) {
    // Order: left shoulder pitch/roll/yaw/elbow pitch/roll,
    // right shoulder pitch/roll/yaw/elbow pitch/roll, waist yaw/roll/pitch.
    if (gesture == "ROCK") {
        return GestureTarget{{0.2f,  kPi2, 0.f, kPi2, 0.f,
                              0.2f, -kPi2, 0.f, kPi2, 0.f,
                              0.f, 0.f, 0.f}};
    }
    if (gesture == "PAPER") {
        return GestureTarget{{0.f,  kPi2, 0.f, 0.f, 0.f,
                              0.f, -kPi2, 0.f, 0.f, 0.f,
                              0.f, 0.f, 0.f}};
    }
    if (gesture == "SCISSORS") {
        return GestureTarget{{0.f,  kPi2, 0.f, 0.f, 0.f,
                              0.2f, -kPi2, 0.f, kPi2, 0.f,
                              0.f, 0.f, 0.f}};
    }
    throw std::invalid_argument("gesture must be ROCK, PAPER, or SCISSORS");
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0]
                  << " <network-interface> <ROCK|PAPER|SCISSORS>" << std::endl;
        return 2;
    }

    GestureTarget target;
    try {
        target = gestureTarget(argv[2]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << std::endl;
        return 2;
    }

    unitree::robot::ChannelFactory::Instance()->Init(0, argv[1]);

    unitree::robot::ChannelPublisherPtr<unitree_hg::msg::dds_::LowCmd_> publisher;
    publisher.reset(
        new unitree::robot::ChannelPublisher<unitree_hg::msg::dds_::LowCmd_>(kTopicArmSDK));
    publisher->InitChannel();

    unitree_hg::msg::dds_::LowState_ state_msg;
    unitree::robot::ChannelSubscriberPtr<unitree_hg::msg::dds_::LowState_> subscriber;
    subscriber.reset(
        new unitree::robot::ChannelSubscriber<unitree_hg::msg::dds_::LowState_>(kTopicState));
    subscriber->InitChannel([&](const void* msg) {
        std::memcpy(&state_msg, msg, sizeof(unitree_hg::msg::dds_::LowState_));
    }, 1);

    const std::array<JointIndex, 13> arm_joints = {
        kLeftShoulderPitch, kLeftShoulderRoll, kLeftShoulderYaw,
        kLeftElbowPitch, kLeftElbowRoll,
        kRightShoulderPitch, kRightShoulderRoll, kRightShoulderYaw,
        kRightElbowPitch, kRightElbowRoll,
        kWaistYaw, kWaistRoll, kWaistPitch
    };

    unitree_hg::msg::dds_::LowCmd_ msg;
    constexpr float control_dt = 0.02f;
    constexpr float max_joint_velocity = 0.5f;
    constexpr float max_joint_delta = max_joint_velocity * control_dt;
    const auto sleep_time = std::chrono::milliseconds(20);

    std::array<float, 13> current_target{};
    for (std::size_t i = 0; i < arm_joints.size(); ++i) {
        current_target[i] = state_msg.motor_state().at(arm_joints[i]).q();
    }

    msg.motor_cmd().at(kNotUsedJoint).q(1.0f);

    for (int step = 0; step < 250; ++step) {
        for (std::size_t i = 0; i < arm_joints.size(); ++i) {
            current_target[i] += std::clamp(target.joints[i] - current_target[i],
                                            -max_joint_delta, max_joint_delta);
            msg.motor_cmd().at(arm_joints[i]).q(current_target[i]);
            msg.motor_cmd().at(arm_joints[i]).dq(0.f);
            msg.motor_cmd().at(arm_joints[i]).kp(60.f);
            msg.motor_cmd().at(arm_joints[i]).kd(1.5f);
            msg.motor_cmd().at(arm_joints[i]).tau(0.f);
        }
        publisher->Write(msg);
        std::this_thread::sleep_for(sleep_time);
    }

    for (int step = 0; step < 100; ++step) {
        for (std::size_t i = 0; i < arm_joints.size(); ++i) {
            msg.motor_cmd().at(arm_joints[i]).q(target.joints[i]);
            msg.motor_cmd().at(arm_joints[i]).dq(0.f);
            msg.motor_cmd().at(arm_joints[i]).kp(60.f);
            msg.motor_cmd().at(arm_joints[i]).kd(1.5f);
            msg.motor_cmd().at(arm_joints[i]).tau(0.f);
        }
        publisher->Write(msg);
        std::this_thread::sleep_for(sleep_time);
    }

    GestureTarget neutral = restTarget();
    for (int step = 0; step < 250; ++step) {
        for (std::size_t i = 0; i < arm_joints.size(); ++i) {
            current_target[i] += std::clamp(neutral.joints[i] - current_target[i],
                                            -max_joint_delta, max_joint_delta);
            msg.motor_cmd().at(arm_joints[i]).q(current_target[i]);
        }
        publisher->Write(msg);
        std::this_thread::sleep_for(sleep_time);
    }

    msg.motor_cmd().at(kNotUsedJoint).q(0.f);
    publisher->Write(msg);
    return 0;
}
