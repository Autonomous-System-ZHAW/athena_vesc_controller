import math

import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped


class SpeedRampPublisher(Node):
    def __init__(self):
        super().__init__("speed_ramp_publisher")
        self.publisher = self.create_publisher(
            AckermannDriveStamped, "/ackermann_cmd", 10
        )

        # Steering/Timer
        self.dt = 0.1  # 10 Hz
        self.t = 0.0  # Zeitvariable für Sinus

        # Geschwindigkeitseinstellungen
        self.speed = 0.3  # Startgeschwindigkeit [m/s]
        self.speed_step = 0.01  # Erhöhung pro 0.1s
        self.max_speed = 0.5  # Zielgeschwindigkeit [m/s]
        self.steering_angle = 0.0

        self.timer = self.create_timer(self.dt, self.publish_speed)

    def publish_speed(self):
        # Geschwindigkeit langsam hochregeln bis 2.0
        if self.speed < self.max_speed:
            self.speed += self.speed_step

        # Lenkung sinusförmig hin und her
        steering_amplitude = 1.0 
        if self.t < 10 and self.steering_angle < 1:
            self.steering_angle += 0.05

        elif 20 > self.t > 10 and self.steering_angle > -1:
            self.steering_angle -= 0.05
        elif self.t > 20 and self.steering_angle < 0.5:
            self.steering_angle += 0.05

        msg = AckermannDriveStamped()
        msg.drive.speed = self.speed
        msg.drive.steering_angle = self.steering_angle

        self.publisher.publish(msg)
        self.get_logger().info(f"speed={self.speed:.2f}, steering={self.steering_angle:.2f}")

        self.t += self.dt

        if self.t > 25:
            self.destroy_node()


def main():
    rclpy.init()
    node = SpeedRampPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()