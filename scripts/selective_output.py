#!/usr/bin/env python
#
# By Neil Nie
# (c) 2018, All Rights Reserved

import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy


class SelectiveOutput(object):

    def __init__(self):

        self.output = None
        self.left_stick_y = None
        rospy.init_node('selective_output')

        rospy.Subscriber('/sensor/joystick/joy', Joy, callback=self.joystick_input_callback, queue_size=5)
        self.publisher1 = rospy.Publisher('/sensor/joystick/left_stick_x', data_class=Float32, queue_size=5)
        self.publisher2 = rospy.Publisher('/sensor/joystick/right_stick_y', data_class=Float32, queue_size=5)
        rate = rospy.Rate(30)

        while not rospy.is_shutdown():

            if self.output is not None and self.left_stick_y is not None:
                data = Float32()
                data.data = self.output
                self.publisher1.publish(data)

                data2 = Float32()
                data2.data = self.left_stick_y
                self.publisher2.publish(data2)

            rate.sleep()

    def joystick_input_callback(self, data):

        inputs = data.axes
        self.output = inputs[0]
        self.left_stick_y = inputs[4]
        # rospy.loginfo(self.output)


if __name__ == "__main__":

    try:
        SelectiveOutput()
    except rospy.ROSInterruptException:
        pass