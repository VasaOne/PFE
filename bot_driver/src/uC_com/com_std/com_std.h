#include <CppLinuxSerial/SerialPort.hpp>

void data_wrapp(char left_right, char back_for, char speed);

class ComSTD {
	public :
	ComSTD();
	void for_right();
	void for_center();
	void for_left();
	void back_right();
	void back_center();
	void back_left();

	private : 
	mn::CppLinuxSerial::SerialPort serial_port;
};
