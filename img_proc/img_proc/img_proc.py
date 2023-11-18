import rclpy
from rclpy.node import Node
from sensor_msgs import Image
from std_msgs import String 
from ultralytics import YOLO
from cv_bridge import CvBridge

EXPECTED_DIM = 300 * 500
THRESHOLD_DIM = 300
THRESHOLD_X = 50

class YoloNode(Node):

    def __init__(self):
        super().__init__('yolo_node')
        self.publisher = self.create_publisher(String,"order_topic" ,10)
        self.subscription = self.create_subscription(Image, "msg_topic" ,self.img_rcv ,10)
        self.img_dim = (750, 1000)
        self.model = YOLO('yolov8n.pt')
        self.bidge = CvBridge()
        self.get_logger().info("yolo node initialized")



    def img_rcv(self, img):
        self.get_logger().info("image received")

        frame_cv = self.bridge.imgmsg_to_cv2(img, desired_encoding='rgb8')
        results = self.model.track(frame, persist=True)

        self.choose_obj(results)



    def choose_obj(self, results):
        for obj in results :
            if obj.boxe.cls == 1 : #means it is human 
                if obj.boxe.id == 1 :
                    send_order(obj.boxes.xzwh)
                    return 1
            else :
                self.get_logger().info("no human detected")




    def send_order(self, box_dim): #dim: x,y,w,h
        x_center = box_dim[0]
        y_center = box_dim[1]
        w = box_dim[2]
        h = box_dim[3]
        
        msg = String()
        msg.data = "nothing" 
        #surface part
        if ( (w * h) + THRESHOLD_DIM < 400 * 600) : 
            #moov forward
            self.get_logger().info("moov forward")
            msg.data = "forward"
        elif ( (w * h) - THRESHOLD_DIM > 400 * 600):
            #moov backward
            self.get_logger().info("moov backward")
            msg.data = "backward"

        #center part
        if (x + THRESHOLD_X < self.img_dim[0]) :
            #moov right
            self.get_logger().info("moov right")
            msg.data = "right"
        elif (x - THRESHOLD_X > self.img_dim[1]):
            #moov left
            self.get_logger().info("moov left")
            msg.data = "left"

        self.publisher.publish(msg)

        return 0



def main(args=None):
    rclpy.init(args=args)

    Yolo_node = YoloNode()

    rclpy.spin(Yolo_node)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
