FROM ros:humble as image

USER 0



RUN git clone https://github.com/gbmhunter/CppLinuxSerial.git
WORKDIR CppLinuxSerial
RUN mkdir build
WORKDIR build
RUN cmake .. && make && sudo make install

WORKDIR ../..

# install ros2 basics
RUN mkdir -p ~/workspace/ros2_ws/src
WORKDIR ~/workspace/ros2_ws
COPY best.pt .
WORKDIR src
COPY src/PFE/ .
RUN git clone https://github.com/ros-perception/vision_opencv.git




#install soft dependencies
RUN apt-get update && \ 
	apt-get install -y python3-pip  

RUN apt-get install libboost-all-dev libopencv-dev ros-humble-cv-bridge -y

RUN pip3 install lap lapx
	
RUN pip3 install ultralytics \
	opencv-python \
	setuptools==58.2.0


