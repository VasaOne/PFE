#include "com_std.h"
#include <vector>
#include <iostream>

using namespace mn::CppLinuxSerial;

void data_wrapp(std::vector<uint8_t>& vect, char left_right, char back_for, char speed){
	static uint16_t id = 0;

	uint8_t byte_zero  = speed;
	uint8_t byte_one = 0;
	uint8_t byte_two = id >> 2;

	uint8_t id_bottom = (id && 0x03) << 6;
	uint8_t back_for_data = (back_for << 3) | (back_for);
	switch (left_right) 
	{
		case 0 : //means left
			byte_one = 0b00010010 | id_bottom | back_for_data;
			break;
		case 1 : //means center
			byte_one = 0b00110110 | id_bottom | back_for_data;
			break;
		case 2 : //means right
			byte_one = 0b00100100 | id_bottom | back_for_data;
			break;
		default : //center by default
			byte_one = 0b00110110 | id_bottom | back_for_data;
	}

	vect.push_back(byte_two);
	vect.push_back(byte_one);
	vect.push_back(byte_zero);

	id ++;
	if (id > 0x1111111111) id = 0;
}

ComSTD::ComSTD() : serial_port("/dev/ttyACM0", BaudRate::B_115200, NumDataBits::EIGHT, Parity::NONE, NumStopBits::ONE){
	serial_port.Open();
	return;

}

void ComSTD::for_right(){
	std::vector<uint8_t> vect= {0,0,0};
	data_wrapp(vect, 2, 1, 100);
	serial_port.WriteBinary(vect);
}

void ComSTD::for_center(){
        std::vector<uint8_t> vect= {};
        data_wrapp(vect, 1, 1, 100);
	//std::cout << "test:" << +(*vect.begin()) << std::endl;
	//std::cout << "test:" << +(*(++ vect.begin())) << std::endl;
	//std::cout << "test:" << +(*(++(++ vect.begin()))) << std::endl;
        serial_port.WriteBinary(vect);
}

void ComSTD::for_left(){
        std::vector<uint8_t> vect= {0,0,0};
        data_wrapp(vect, 0, 1, 100);
        serial_port.WriteBinary(vect);
}

void ComSTD::back_right(){
        std::vector<uint8_t> vect= {0,0,0};
        data_wrapp(vect, 2, 0, 100);
        serial_port.WriteBinary(vect);
}

void ComSTD::back_center(){
        std::vector<uint8_t> vect= {0,0,0};
        data_wrapp(vect, 1, 0, 100);
        serial_port.WriteBinary(vect);
}

void ComSTD::back_left(){
        std::vector<uint8_t> vect= {0,0,0};
        data_wrapp(vect, 0, 0, 100);
        serial_port.WriteBinary(vect);
}
