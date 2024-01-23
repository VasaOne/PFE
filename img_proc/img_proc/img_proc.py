import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int8, Bool 
from ultralytics import YOLO
from cv_bridge import CvBridge
import cv2 as cv

EXPECTED_DIM = 300 * 500
THRESHOLD_DIM = 300
THRESHOLD_X = 50


class YoloNode(Node):

    def __init__(self):
        super().__init__('yolo_node')
        self.publisher = self.create_publisher(Int8,"order_topic" ,10)
        self.subscription = self.create_subscription(Image, "msg_topic" ,self.img_rcv ,1)
        self.subscription_record = self.create_subscription(Bool, "manager_topic", self.record_manager, 10)
        self.is_recording = True
        self.recordVideo = []
        self.img_dim = (750, 1000)
        self.model = YOLO('best.pt')
        self.bridge = CvBridge()
        self.id_follow = None
        self.get_logger().info("yolo node initialized")

    def record_manager(self, msg_bool):
        if not msg_bool.data : #if we stop a recording 
            #store the video
            video_obj = cv.VideoWriter("record.avi", cv.VideoWriter_fourcc(*"XVID"), 10, self.img_dim)
            for frame in self.recordVideo :
                print(str(self.img_dim) + " " + str(frame.shape))
                frame_color = cv.cvtColor(frame,cv.COLOR_RGB2BGR)
                video_obj.write(frame_color)
            video_obj.release()

            #initialize the list
            self.recordVideo = []
        self.is_recording = msg_bool.data
        self.get_logger().info("record state changed " + str(self.is_recording))

    def img_rcv(self, img):
        self.get_logger().info("image received")
        
        frame = self.bridge.imgmsg_to_cv2(img, desired_encoding='rgb8')
        results = self.model.track(frame, persist=True, conf = 0.4)
        
        if self.is_recording : #for recording part
            annoted_frame = results[0].plot()
            self.recordVideo.append(annoted_frame)
        
        self.img_dim = (frame.shape[1], frame.shape[0])
        self.choose_obj(results)



    def choose_obj3(self, results):
        self.get_logger().info( "lenght of boxes: " + str(len(results[0].boxes.cls)) )
        for i in range(len(results[0].boxes.cls)):
        
            if results[0].boxes.cls[i] == 0: #means it is human
                self.get_logger().info("duster detected! classes: " + str(results[0].boxes.cls[i]))
                if results[0].boxes.id[i] == 1:
                    self.send_order(results[0].boxes.xywh[i])
                    return 1
            else :
                self.get_logger().info("no duster detected")

    def choose_obj2(self, results):
        if results[0].boxes.id is not None :
            self.get_logger().info("tracking available len of classes: " + str(len(results[0].boxes.cls)))
            for i in range(len(results[0].boxes.cls)):
                self.get_logger().info("classes detected : " + str(results[0].boxes.cls[i]))
                if results[0].boxes.cls[i] == 0: #means it is a duster
                    self.get_logger().info("duster detected id: ")
                    if results[0].boxes.id[i] == 0:
                        self.get_logger().info("send order forduster tracking")
                        self.send_order(results[0].boxes.xywh[i])
                        return 1
        else :
            self.get_logger().info("tracking unable, please relaunch ros2")

    def debug_obj(self, results):
        self.get_logger().info("detected " + str(len(results[0].boxes.cls)) + " classes")
        for i in range(len(results[0].boxes.cls)):
            self.get_logger().info("classes " + str(i) + " val = " + str(results[0].boxes.cls[i]))

        if results[0].boxes.id is not None :
            self.get_logger().info("tracking available, id llen: " + str(len(results[0].boxes.cls)) )
            for i in range(len(results[0].boxes.cls)):
                self.get_logger().info("id " + str(i) + " val = " + str(results[0].boxes.id[i]))

        else :
            self.get_logger().info("tracking unable")

    def choose_obj(self, results):
        if len(results[0].boxes.cls) == 0 : #means nothing identified
            self.send_stop()
            return 
        if results[0].boxes.id is not None :
            self.get_logger().info("tracking available")

            if self.id_follow is not None : # robot is following someone
                for i in range(len(results[0].boxes.id)):
                    if results[0].boxes.id[i] == self.id_follow :
                        self.send_order(results[0].boxes.xywh[i])
            else : #robot is following now one, it will follow first obj
                self.id_follow = results[0].boxes.id[0]
                self.get_logger().info("follow new id: " + str(self.id_follow))
                self.send_order(results[0].boxes.xywh[0])
        else :
            self.get_logger().info("tracking unable, folow first duster")
            self.id_follow = None #reset id_folow
            self.send_order(results[0].boxes.xywh[0])

    def send_stop(self):
        msg = Int8()
        msg.data = 0
        self.get_logger().info("robot stoped")
        self.publisher.publish(msg)

    def send_order(self, box_dim): #dim: x,y,w,h
        x_center = box_dim[0] + box_dim[2]/2
        y_center = box_dim[1] + box_dim[3]/2
        w = box_dim[2]
        h = box_dim[3]
        self.get_logger().info("x_center: " + str(x_center) + " y_center: " + str(y_center) + "size: " + str(self.img_dim[0]) + "," + str(self.img_dim[1]))
        msg = Int8()
        msg.data = 0 #means stop, by default robot wants to stop
        #surface part, I know it is ugly 
        if ( (w * h) + THRESHOLD_DIM < 400 * 600) : 
            #moov forward
            self.get_logger().info("moov forward")
            msg.data = 1
        elif ( (w * h) - THRESHOLD_DIM > 400 * 600):
            #moov backward
            self.get_logger().info("moov backward")
            msg.data = 11

        #center part
        if (x_center + THRESHOLD_X > self.img_dim[0]) :
            #moov right
            self.get_logger().info("moov right")
            msg.data += 4
        elif (x_center - THRESHOLD_X < self.img_dim[1]):
            #moov left
            self.get_logger().info("moov left")
            msg.data += 5

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
