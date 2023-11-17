#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>



std::string gstreamer_pipeline (int capture_width, int capture_height, int display_width, int display_height, int framerate, int flip_method) {
    return "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)" + std::to_string(capture_width) + ", height=(int)" +
           std::to_string(capture_height) + ", framerate=(fraction)" + std::to_string(framerate) +
           "/1 ! nvvidconv flip-method=" + std::to_string(flip_method) + " ! video/x-raw, width=(int)" + std::to_string(display_width) + ", height=(int)" +
           std::to_string(display_height) + ", format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink";
}


class Cam_publisher : public rclcpp::Node {

	public :
	Cam_publisher () : Node("cam_pub") {
		publisher_img = this->create_publisher<sensor_msgs::msg::Image>("msg_topic",999);
		RCLCPP_INFO(this->get_logger(), "cam publisher init");

		//publish image messages
		int status = this->images_publisher();
	}


	private :
	rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_img;
	int images_publisher() {
		//conexion to camera
		int capture_width = 1200;
		int capture_height = 720;
		int display_width = 1200;
		int display_height = 720;
		int framerate = 60;
		int flip_method = 0;

		std::string pipeline = gstreamer_pipeline (
				capture_width, 
				capture_height, 
				display_width, 
				display_height, 
				framerate, 
				flip_method);

		cv::VideoCapture cap(pipeline, cv::CAP_GSTREAMER);

		if(!cap.isOpened()){
			RCLCPP_ERROR(this->get_logger(), "failed to open camera");
			return -1;
		}

		cv::Mat img;

		RCLCPP_INFO(this->get_logger(), "start to send images");
		//emission of images
		while (true) {
			//read from camera
			if(!cap.read(img)){
				RCLCPP_WARN(this->get_logger(), "failed to read images");
			}
			
			//conversion from opencv img to ros2 message
			sensor_msgs::msg::Image::SharedPtr msg = cv_bridge::CvImage(std_msgs::msg::Header(), "mono8", img).toImageMsg();

			//image published
			publisher_img->publish(*msg.get());
		}
		return 1;
	}	
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Cam_publisher>());
  rclcpp::shutdown();
  return 0;
}
