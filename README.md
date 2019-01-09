# ros_nagios_diagnostics

This package provides integration of ROS diagnostics messages with
nagios.



## Installation

### Get the code

You will need to have a function ROS/catkin workspace. In this example, a
workspace is created under /usr/local/nagios

    sudo mkdir /usr/local/nagios
	chown  -R your_user_id:your_user_id /usr/local/nagios
    cd /usr/local/nagios
	mkdir src
	cd src
    git clone  https://github.com/berndpfrommer/ros_nagios_diagnostics.git


### Install the nagios plugin

Copy the nagios plugin to a location of your choice:

    plugin_dir=/usr/local/nagios/plugins
    sudo mkdir -p $plugin_dir
	cp	/usr/local/nagios/src/ros_nagios_diagnostics/check_ros_diagnostic_server $plugin_dir/

## Run the diagnostics server

    cd /usr/local/nagios/
	catkin build
	. devel/setup.bash
	roslaunch ros_nagios_diagnostics diagnostic_server.launch

## Configure and run the diagnostic aggregator

ROS uses diagnostic aggregators to reduce the traffic that is
typically seen on the ``/diagnostics`` topic. There is an example analyzer provided,
look at the launch script and customize the config file to your needs:

    roslaunch ros_nagios_diagnostics aggregator.launch


## Basic testing

If all works, the following line should produce some output (change the ``/cameras`` path!):

    /usr/local/nagios/plugins/check_ros_diagnostic_server -r /usr/local/nagios/devel/setup.bash -n /cameras
    OK: OK

## Configure nagios

This example is for nagios3, as shipped with Ubuntu 16.04. In ``/etc/nagios3/conf.d/``,
customize and append the following to the config of the host that is running the nagios server:

    # Define a command that runs the plugin
    define command {
         command_name check_ros
         command_line /usr/local/nagios/plugins/check_ros_diagnostic_server -r /usr/local/nagios/devel/setup.bash -n $ARG1$
	}
	#
    # Define a service that checks for errors under the /cameras path.
	# This path must match what is configured for the ROS diagnostic_aggregator
	# you are running
	
    define service{
      use                             generic-service
      host_name                       aviary
      service_description             Cameras
      check_command                   check_ros!/cameras
    }

	#
    # Define another service that checks for errors under the /sensors path
    #
	
    define service{
      use                             generic-service
      host_name                       aviary
      service_description             Environmental
      check_command                   check_ros!/sensors
    }


Restart nagios:

    systemctl restart nagios3.service


