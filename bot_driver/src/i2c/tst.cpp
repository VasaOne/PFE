#include <i2c/i2c.h>
#include <iostream>
#include <cstring>

int main(){
	I2CDevice device;
	memset(&device, 0, sizeof(device));

	int bus;
	int device_addr = 0x50;

	std::cout << "start com" << std::endl;

	bus = i2c_open("/dev/i2c-0");

	if (bus == -1){
		std::cout << "failed" << std::endl;
		return 0;
	}

	std::cout << "bus initialization done : " << bus << std::endl;

	device.addr = device_addr;
	device.iaddr_bytes = 1;
	device.page_bytes = 16;

	//com part
	
        unsigned char buffer_snd[1];
        ssize_t size_snd = sizeof(buffer_snd);
        memset(buffer_snd, 0, sizeof(buffer_snd));


	unsigned char buffer[256];
	ssize_t size = sizeof(buffer);
	memset(buffer, 0, sizeof(buffer));

	i2c_write(&device,0x00,buffer_snd,size_snd);

	if ((i2c_read(&device, 0x0, buffer, size)) != size) {

		std::cout << "error while receivind msg" << std::endl;
		return 0;
	}
	std::cout << "message received :" << std::endl;
	for(int i = 0; i<256;i++){
		std::cout << buffer[i] << " , ";
	}
}
