#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String
from geometry_msgs.msg import TwistStamped, Twist
from rviz_2d_overlay_msgs.msg import OverlayText

class Overlay(Node):
    def __init__(self):
        super().__init__('overlay')
        
        self.actual_speed = 0.0
        self.cmd_speed = 0.0
        self.actual_deg = 0.0
        self.cmd_deg = 0.0
        self.stop_sign_exists = False
        self.driving_state = "N/A"

        self.sub_status = self.create_subscription(
            Twist,
            '/vehicle_status',
            self.status_callback,
            10)
        
        self.sub_cmd = self.create_subscription(
            Twist,
            '/ctrl_cmd',
            self.cmd_callback,
            10)
        
        self.sub_stop_sign = self.create_subscription(
            Bool,
            '/stop_sign_exists',
            self.stop_sign_callback,
            10)
        self.sub_state = self.create_subscription(
            String,
            '/smState',
            self.state_callback,
            10)
        
        self.publisher_ = self.create_publisher(
            OverlayText, 
            '/overlay', 
            10)

        self.timer = self.create_timer(0.1, self.publish_overlay)

    def status_callback(self, msg):
        self.actual_speed = msg.linear.x
        self.actual_deg = math.degrees(msg.angular.z)

    def cmd_callback(self, msg):
        self.cmd_speed = msg.linear.x
        self.cmd_deg = math.degrees(msg.angular.z)

    def stop_sign_callback(self, msg):
        self.stop_sign_exists = msg.data

    def state_callback(self, msg):
        self.driving_state = msg.data

    def publish_overlay(self):
        actual_kmh = self.actual_speed * 3.6
        cmd_kmh = self.cmd_speed 
        overlay_msg = OverlayText()
        overlay_msg.action = OverlayText.ADD

        overlay_msg.text = (
            f"Vehicle Status: {actual_kmh:.1f} km/h ({self.actual_speed:.2f} m/s) {self.actual_deg:.1f} °deg\n"
            f"Ctrl Cmd: {cmd_kmh:.1f} km/h ({self.cmd_speed/3.6:.2f} m/s) {self.cmd_deg:.1f} °deg\n"
            f"Stop Sign Exists: {'Yes' if self.stop_sign_exists else 'No'}\n"
            f"Driving State: {self.driving_state}"
        )
        overlay_msg.width = 800
        overlay_msg.height = 350
        overlay_msg.text_size = 18.0

        overlay_msg.fg_color.r = 1.0
        overlay_msg.fg_color.g = 1.0
        overlay_msg.fg_color.b = 1.0
        overlay_msg.fg_color.a = 1.0

        overlay_msg.bg_color.r = 0.0
        overlay_msg.bg_color.g = 0.0
        overlay_msg.bg_color.b = 0.0
        overlay_msg.bg_color.a = 0.0
        self.publisher_.publish(overlay_msg)
   

def main(args=None):
    rclpy.init(args=args)
    node = Overlay()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()