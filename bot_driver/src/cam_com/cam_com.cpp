#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"

class Cam_publisher : public rclcpp::Node {

	public :
	Cam_publisher () : Node("cam_pub") {
		publisher_img = this->create_publisher<sensor_msgs::msg::Image>("msg_topic",999);
		RCLCPP_INFO(this->get_logger(), "cam publisher init");
	}

	private :
	rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_img;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Cam_publisher>());
  rclcpp::shutdown();
  return 0;
}
