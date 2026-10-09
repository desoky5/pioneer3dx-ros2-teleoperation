import sys
import termios
import tty
import select

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

HELP = """
Pioneer teleop
  w / s : forward / backward
  a / d : turn left / right
  space : stop
  q     : quit
"""
LIN_SPEED = 0.3 #M/S
ANG_SPEED = 0.8 #rad/sec

#inheriting the node teleop_node from the base class Node w
class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.pub = self.create_publisher(Twist,'/cmd_vel',10)
        
    def send(self,lin,ang):
        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.pub.publish(msg)
        
def get_key(settings,timeout=0.1):
	tty.setraw(sys.stdin.fileno())
	ready, _, _=select.select([sys.stdin],[],[],timeout)
	key=sys.stdin.read(1) if ready else ''
	termios.tcsetattr(sys.stdin,termios.TCSADRAIN,settings)
	return key
	
def main(args=None):
	rclpy.init(args=args)
	node = TeleopNode()
	settings = termios.tcgetattr(sys.stdin)
	print(HELP)
	
	keys = { 
	'w':(LIN_SPEED,0.0),
	's':(-LIN_SPEED,0.0),
	'a':(0.0,ANG_SPEED),
	'd':(0.0,-ANG_SPEED),
	' ':(0.0,0.0),
	}
	
	try :
		while rclpy.ok():
			key = get_key(settings)
			if key == 'q' or key == '\x03':
				break
			if key in keys:
				node.send(*keys[key])
	
	finally:
		node.send(0.0,0.0)
		termios.tcsetattr(sys.stdin,termios.TCSADRAIN,settings)
		node.destroy_node()
		rclpy.shutdown()
		

if __name__ == 'main':
	main()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

