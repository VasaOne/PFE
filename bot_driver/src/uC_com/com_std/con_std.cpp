#include "com_std.h"
#include <CppLinuxSerial/SerialPort.hpp>
#include <vector>

void data_wrapp(std::vector<uint8_t>& vect, char left_right, char back_for, char speed){
	static uint16_t id = 0;

	uint8_t byte_zero  = speed;
	uint8_t byte_one = 0;
	uint8_t byte_two = id >> 2;

	char id_bottom = (id && 0x03) << 6;
	char back_for_data = (back_for << 4) || (back_for << 1);
	switch (left_right) 
	{
		case 0 : //means left
			byte_one = 0b00010010 || id_bottom || back_for_data;
		case 1 : //means center
			byte_one = 0b00110110 || id_bottom || back_for_data;
		case 2 : //means right
			byte_one = 0b00100100 || id_bottom || back_for_data;
		default : //center by default
	}

	vect.push_back(byte_zero);
	vect.push_back(byte_one);
	vect.push_back(byte_two);

	id ++;
	if (id > 0x1111111111) id = 0;
}

ComUc::ComUc {
	serial_port("/dev/ttyACM0", BaudRate::B_115200, NumDataBits::EIGHT, Parity::NONE, NumStopBits::ONE);

}

void ComUc::for_right(){
	std::vector<uint8_t> vect= {0,0,0};
	data_wrapp(vect, 2, 1, 100);
	serial_port.WriteBinary(vect);
}

void ComUc::for_center(){
        std::vector<uint8_t> vect= {0,0,0};
        data_wrapp(vect, 1, 1, 100);
        serial_port.WriteBinary(vect);
}

void ComUc::for_left(){
        std::vector<uint8_t> vect= {0,0,0};
        data_wrapp(vect, 0, 1, 100);
        serial_port.WriteBinary(vect);
}

void ComUc::back_right(){
        std::vector<uint8_t> vect= {0,0,0};
        data_wrapp(vect, 2, 0, 100);
        serial_port.WriteBinary(vect);
}

void ComUc::back_center(){
        std::vector<uint8_t> vect= {0,0,0};
        data_wrapp(vect, 1, 0, 100);
        serial_port.WriteBinary(vect);
}

void ComUc::back_left(){
        std::vector<uint8_t> vect= {0,0,0};
        data_wrapp(vect, 0, 0, 100);
        serial_port.WriteBinary(vect);
}
