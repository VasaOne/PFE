import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int8, Bool
from cv_bridge import CvBridge
import cv2 as cv 
import sys
import os
import cmd 


class BotShell(cmd.Cmd):
    intro = "Bot shell started. Type help or ? to list commands. \n"


    def __init__(self, pub_img, pub_order, pub_rec):
        super().__init__()
        self.publisher_img = pub_img
        self.publisher_order = pub_order
        self.publisher_rec = pub_rec
        self.record = False


    def do_moov(self, param):
        #arg could be left, right, backward, forward
        msg = Int8()
        arg = str(param)
        if (arg == "forward") :
            msg.data = 1
        elif(arg == "backward"):
            msg.data = 11
        elif(arg == "for_right"):
            msg.data = 5
        elif(arg == "for_left"):
            msg.data = 6
        elif(arg == "back_right"):
            msg.data = 15
        elif(arg == "back_left"):
            msg.data = 16
        elif(arg == "stop"):
            msg.data = 0
        else :
            msg.data = 0 #by default it sends a stop
        self.publisher_order.publish(msg)
        print("bot mooving" + arg)


    def do_img(self, arg):
        #load image as cvMat obj
        img = cv.imread(cv.samples.findFile("src/PFE/imgLib/humans.jpeg"), cv.IMREAD_GRAYSCALE)
        cv.imshow("photo to send", img)
        cv.waitKey(0)
        cv.destroyAllWindows()

        #convert img to ros2 msg
        bridge = CvBridge()
        image_message = bridge.cv2_to_imgmsg(img, encoding="mono8")

        #send image through topic to YoloNode
        self.publisher_img.publish(image_message)
        print("send images to bot")

    def do_see(self, arg):
        print("bot start streaming")
    
    def do_record(self, arg):
        self.record = not self.record
        print("record state:" + str(self.record))

        msg = Bool()
        msg.data = self.record
        self.publisher_rec.publish(msg)
        



    def do_quit(self,arg):
        print("Bot shell closed, see you later aligator \n")
        self.close()
        return True


class ShellNode(Node):

    def __init__(self):
        super().__init__("shell_node")
        print(os.getcwd())
        self.publisher_img = self.create_publisher(Image, "msg_topic", 999)
        self.publisher_order = self.create_publisher(Int8, "order_topic", 999)
        self.publisher_rec = self.create_publisher(Bool, "manager_topic", 999)
        shell = BotShell(self.publisher_img, self.publisher_order, self.publisher_rec)
        shell.cmdloop()



def main(args=None):
    rclpy.init(args=args)

    shell_node = ShellNode()

    rclpy.spin(shell_node)

    shell_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()

