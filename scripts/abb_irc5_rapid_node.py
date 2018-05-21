import rospy
from rpi_abb_irc5 import RAPID
from rpi_arm_composites_manufacturing_abb_egm_controller.srv import \
    RapidStart, RapidStartRequest, RapidStartResponse, \
    RapidStop, RapidStopRequest, RapidStopResponse, \
    RapidGetStatus, RapidGetStatusRequest, RapidGetStatusResponse, \
    RapidGetDigitalIO, RapidGetDigitalIORequest, RapidGetDigitalIOResponse, \
    RapidSetDigitalIO, RapidSetDigitalIORequest, RapidSetDigitalIOResponse, \
    RapidReadEventLog, RapidReadEventLogRequest, RapidReadEventLogResponse
    
from rpi_arm_composites_manufacturing_abb_egm_controller.msg import RapidEventLogMessage
from datetime import datetime

import traceback

def rapid_start(req):
    r=RapidStartResponse()
    try:
        if req.reset_pp:
            rapid.resetpp()
        cycle='asis'
        if len(req.cycle) > 0:
            cycle=req.cycle
        rapid.start(cycle)  
        r.success=True
        return r
    except:
        traceback.print_exc()
        r.success=False
        return r

def rapid_stop(req):
    r=RapidStopResponse()
    try:
        rapid.stop()        
        r.success=True
        return r
    except:
        traceback.print_exc()
        r.success=False
        return r

def rapid_get_status(req):
    r=RapidGetStatusResponse()
    try:
        s=rapid.get_execution_state()
        r.running=s.ctrlexecstate=='running'
        r.cycle=s.cycle
        r.opmode=rapid.get_operation_mode()  
        r.ctrlstate=rapid.get_controller_state() 
        r.success=True
        return r
    except:
        traceback.print_exc()
        r.success=False
        return r
def rapid_get_digital_io(req):
    r=RapidGetDigitalIOResponse()
    try:
        r.lvalue=rapid.get_digital_io(req.signal)
        r.success=True
        return r
    except:
        traceback.print_exc()
        r.success=False
        return r

def rapid_set_digital_io(req):
    r=RapidSetDigitalIOResponse()
    try:
        rapid.set_digital_io(req.signal, req.lvalue)
        r.success=True
        return r
    except:
        traceback.print_exc()
        r.success=False
        return r
    
        
def rapid_read_event_log(req):
    r=RapidReadEventLogResponse()
    try:
        rapid_msgs=rapid.read_event_log()
        msgs2=[]
        for m in rapid_msgs:
            m2=RapidEventLogMessage()
            m2.msgtype=m.msgtype
            m2.code=m.code
            m2.tstamp = rospy.Time.from_sec((m.tstamp - datetime.utcfromtimestamp(0)).total_seconds())                        
            m2.args=m.args
            m2.title=m.title
            m2.desc=m.desc
            m2.conseqs=m.conseqs
            m2.causes=m.causes
            m2.actions=m.actions
            msgs2.append(m2)
        r.messages=msgs2
        r.success=True
        return r            
    except:
        traceback.print_exc()
        r.success=False
        return r
    


if __name__ == '__main__':
    global rapid
    
    rospy.init_node('abb_irc5_rapid')
    
    #robot_host=rospy.get_param('~abb_irc5_host')
    robot_host='http://192.168.11.58'
    
    rapid=RAPID(robot_host)
    
    rospy.Service('rapid/start', RapidStart, rapid_start)
    rospy.Service('rapid/stop', RapidStop, rapid_stop)
    rospy.Service('rapid/status', RapidGetStatus, rapid_get_status)
    rospy.Service('rapid/get_digital_io', RapidGetDigitalIO, rapid_get_digital_io)
    rospy.Service('rapid/set_digital_io', RapidSetDigitalIO, rapid_set_digital_io)
    rospy.Service('rapid/read_event_log', RapidReadEventLog, rapid_read_event_log)
    
    rospy.spin()