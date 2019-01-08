#!/usr/bin/env python
#
# 2018 Bernd Pfrommer
#
# node to make ros diagnostics available as a service
#

import rospy
import argparse
from ros_nagios_diagnostics.srv import *
from diagnostic_msgs.msg import DiagnosticArray


diag = {}

def handleGetDiagnostic(req):
    if req.name in diag:
        r = diag[req.name]
        return GetDiagnosticResponse(level=r.level, message=r.message,
                                     hardware_id=r.hardware_id)
    
    print "cannot find diagnostics for ", req.name
    return GetDiagnosticResponse(level=-1, message='NOT_FOUND',
                                 hardware_id='INVALID')

def handleDiagnosticCallback(msg):
    for status in msg.status:
        diag[status.name] = status;
#        print status.name, status.level, status.message, status.hardware_id


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ros service to allow diagnostics reading')
    parser.add_argument('--cfgfile', '-c', action='store', default="diagnostic_server.yaml",
                        help='name of the config file.')
    args = parser.parse_args(rospy.myargv()[1:])

    rospy.init_node('diagnostic_server')
    server = rospy.Service('get_diagnostic', GetDiagnostic, handleGetDiagnostic)
    subscriber = rospy.Subscriber('/diagnostics_agg', DiagnosticArray, handleDiagnosticCallback);

    rospy.loginfo("diagnostic server started up!")
    while not rospy.is_shutdown():
        rospy.spin()
    
