import threading

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray


class SensorViz(Node):
    def __init__(self):
        super().__init__('sensor_viz')
        self.latest = [0.0] * 16
        self.sub = self.create_subscription(Float32MultiArray,'/ultrasonic_sensors',self.callback,10)   

    def callback(self, msg):
        if len(msg.data)==16:
            self.latest = list(msg.data)
       		 


def main(args=None):
    rclpy.init(args=args)
    node = SensorViz()

    spin_thread = threading.Thread(target=rclpy.spin,args=(node,),daemon=True)
    spin_thread.start()
    
    fig , ax = plt.subplots()
    bars = ax.bar(range(16),node.latest)
    ax.set_ylim(0,1)
    ax.set_xticks(range(16))
    ax.set_xlabel('Sensor index')
    ax.set_ylabel('Distance (m)')
    ax.set_title('Pioneer 3-DX ultrasonic sensors')
    
    def update(frame):
        for bar, height in zip(bars, node.latest):
            bar.set_height(height)
        return bars

    ani = FuncAnimation(fig, update, interval=100, blit=False,
                        cache_frame_data=False)
    try:
        plt.show()   # blocks until the window is closed
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
