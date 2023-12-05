import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2 as cv 
import sys
import cmd 

class BotShell(cmd.Cmd):
    intro = "Bot shell started. Type help or ? to list commands. \n"


    def __init__(self, pub_img, pub_order):
        super().__init__()
        self.publisher_img = pub_img
        self.publisher_order = pub_order


    def do_moov(self, arg):
        #arg could be left, right, backward, forward
        msg = String()
        msg.data = str(arg)

        self.publisher_order.publish(msg)
        print("bot mooving" + str(arg))


    def do_img(self, arg):
        #load image as cvMat obj
        img = cv.imread(cv.samples.findFile("human.jpg"), IMREAD_GRAYSCALE)
        cv.imshow("photo to send", img)
        cv.waitKey(0)
        cv.destroyAllWindows()

        #convert img to ros2 msg
        bridge = CvBridge()
        image_message = bridge.cv2_to_imgmsg(cv_image, encoding="mono8")

        #send image through topic to YoloNode
        self.publisher_img.publish(image_message)
        print("send images to bot")


    def do_see(self, arg):
        print("bot start streaming")


    def do_quit(self,arg):
        print("Bot shell closed, see you later aligator \n")
        self.close()
        return True


class ShellNode(Node):

    def __init__(self):
        super().__init__("shell_node")
        self.publisher_img = self.create_publisher(Image, "msg_topic", 999)
        self.publisher_order = self.create_publisher(String, "order_topic", 999)
        shell = BotShell(self.publisher_img, self.publisher_order)
        shell.cmdloop()



def main(args=None):
    rclpy.init(args=args)

    shell_node = ShellNode()

    rclpy.spin(shell_node)

    shell_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()

