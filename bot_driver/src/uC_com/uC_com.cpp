#include "rclcpp/rclcpp.hpp"


class comUc : public rclcpp::Node {

	public :
	
	comUc() : Node("uC_node") {
		RCLCPP_INFO(this->get_logger(), "uC_node init");
	}

};


int main(int argc, char* argv[]){
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<comUc>());
	rclcpp::shutdown();
	return 0;
}
