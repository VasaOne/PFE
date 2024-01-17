#include "rclcpp/rclcpp.hpp"
#include "com_std.h"
#include "std_msgs/msg/int8.hpp"

class comUc : public rclcpp::Node {

	public :
	
	comUc() : Node("uC_node"), com_std() {
		RCLCPP_INFO(this->get_logger(), "uC_node init");
		sub = this->create_subscription<std_msgs::msg::Int8>("order_topic", 9, std::bind(&comUc::order_selector,this, std::placeholders::_1));
//com_std.for_center();
	}

	private :
	ComSTD com_std;
	rclcpp::Subscription<std_msgs::msg::Int8>::SharedPtr sub;
	void order_selector(std_msgs::msg::Int8 msg){
		switch(msg.data){
			case 0: 
				RCLCPP_INFO(this->get_logger(), "nothing to do");
				com_std.stop();
				break;
			case 1:
				RCLCPP_INFO(this->get_logger(), "moov forward");
				com_std.for_center();
				break;
			case 11:
				RCLCPP_INFO(this->get_logger(), "moov backward");
				com_std.back_center();
				break;
			case 5:
				RCLCPP_INFO(this->get_logger(), "moov forward right");
				com_std.for_right();
				break;
			case 6:
				RCLCPP_INFO(this->get_logger(), "moov forward left");
				com_std.for_left();
				break;
			case 15:
				RCLCPP_INFO(this->get_logger(), "moov backward right");
				com_std.back_right();
				break;
			case 16:
				RCLCPP_INFO(this->get_logger(), "moov backward left");
				com_std.back_left();
				break;
			case 7:
				RCLCPP_INFO(this->get_logger(), "moov right");
				//not yet
				break;
			case 8:
				RCLCPP_INFO(this->get_logger(), "moov left");
				//not yet
				break;
			default:
				RCLCPP_ERROR(this->get_logger(), "wrong message value: %i", msg.data);
		}
		RCLCPP_INFO(this->get_logger(), "order received: %i", msg.data);
		

	}

};


int main(int argc, char* argv[]){
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<comUc>());
	rclcpp::shutdown();
	return 0;
}
