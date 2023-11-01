import rclpy
from rclpy.node import Node
from sensor_msgs import Image
from std_msgs import String 

class YoloNode(Node):

    def __init__(self):
        super().__init__('yolo_node')
        self.publisher = self.create_publisher(String,"order_topic" ,10)
        self.subscription = self.create_subscription(Image, "msg_topic" ,self.img_rcv ,10)        
        self.get_logger().info("yolo node initialized")

    def img_rcv(self, img):
        self.get_logger().info("image received!")


def main(args=None):
    rclpy.init(args=args)

    Yolo_node = YoloNode()

    rclpy.spin(Yolo_node)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
