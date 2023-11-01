#include "rclcpp/rclcpp.hpp"
#include "com_std.h"

class comUc : public rclcpp::Node {

	public :
	
	comUc() : Node("uC_node"), com_std() {
		RCLCPP_INFO(this->get_logger(), "uC_node init");
		com_std.for_center();
	}

	private :
	ComSTD com_std;

};


int main(int argc, char* argv[]){
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<comUc>());
	rclcpp::shutdown();
	return 0;
}
