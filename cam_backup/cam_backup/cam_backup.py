import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class CamBackup(Node):

        def __init__(self):
            super().__init__("cam_python_driver")
            self.video_path = "/dev/video0"
            self.video_capture = cv2.VideoCapture(self.video_path, cv2.CAP_V4L2)
            self.bridge = CvBridge()
            self.publisher = self.create_publisher(Image ,"msg_topic",3)
            if self.video_capture.isOpened():
                self.get_logger().info("camera detected, video stream started")
                self.cam_reader()
            else :
                self.get_logger().error("camera not detected")

        def cam_reader(self):
#            window_title = "USB_CAM"
#            window_handle = cv2.namedWindow( window_title, cv2.WINDOW_AUTOSIZE )
            while True:
                #read value from cam
                ret_val, frame_cv = self.video_capture.read()
                #convert from opencv frame to ros frame 
                frame_ros = self.bridge.cv2_to_imgmsg(frame_cv, encoding='rgb8')
                #send through msg_topic
                self.publisher.publish(frame_ros)
#                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
#                    cv2.imshow(window_title, frame_cv)
#                else:
#                    break
#                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
 #               if keyCode == 27 or keyCode == ord('q'):
 #                   break

            self.video_capture.release()
            self.destroyAllWindows()
                

def main(args=None):
    rclpy.init(args=args)
    cam_backup = CamBackup()
    rclpy.spin(cam_backup)
    cam_backup.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
