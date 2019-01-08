cmake_minimum_required(VERSION 2.8)
project(ros_nagios_diagnostics)

find_package(catkin REQUIRED COMPONENTS rospy message_generation std_msgs)

add_service_files(DIRECTORY srv FILES GetDiagnostic.srv)

generate_messages(DEPENDENCIES
std_msgs)

catkin_package()

