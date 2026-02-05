ros2 launch vesc_driver vesc_driver_node.launch.py &
ros2 launch vesc_ackermann ackermann_to_vesc_node.launch.xml &
# python3 speed_controller/speed_ramp_publisher.py
python3 speed_controller/skidpad_hardcode.py
