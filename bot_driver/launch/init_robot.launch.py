from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description() :
    ld = LaunchDescription()

    proc_node = Node( package="img_proc"  , executable="img_node", name="img_node")
    com_node  = Node( package="bot_driver", executable="com_node", name="com_node")
    cam_node  = Node( package="bot_driver", executable="cam_node", name="cam_node")
    ld.add_action(proc_node)
    ld.add_action(com_node)
    ld.add_action(cam_node)

    return ld


