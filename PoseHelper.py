# 
# This file is part of the GNU General Public License v3.0 distribution 
# https://github.com/balamuruganky/path_planning
# Copyright (c) 2020 Balamurugan Kandan
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
import math
from geometry_msgs.msg import Pose, PoseStamped
from tf.transformations import euler_from_quaternion, quaternion_from_euler

def get_position(points):
    pts = np.zeros([len(points),2])
    for pt in range(len(points)):
        pts[pt][0] = points[pt].position.x
        pts[pt][1] = points[pt].position.y
    return pts

def prepare_pose(x, y, yaw = None):
    pose = Pose()
    pose.position.x = x
    pose.position.y = y
    pose.position.z = 0.0
    if yaw != None:
        quat = quaternion_from_euler(0.0,0.0,yaw)
        pose.orientation.x = quat[0]
        pose.orientation.y = quat[1]
        pose.orientation.z = quat[2]
        pose.orientation.w = quat[3]
    return pose

def prepare_posestamped(x, y, yaw = None):
    pose_stamped = PoseStamped()
    pose_stamped.pose.position.x = x
    pose_stamped.pose.position.y = y
    pose_stamped.pose.position.z = 0.0
    if yaw != None:
        quat = quaternion_from_euler(0.0,0.0,yaw)
        pose_stamped.pose.orientation.x = quat[0]
        pose_stamped.pose.orientation.y = quat[1]
        pose_stamped.pose.orientation.z = quat[2]
        pose_stamped.pose.orientation.w = quat[3]
    return pose_stamped

def start_angle(cx, cy, x, y):
    dStart = (180 / np.pi) * np.arctan2(y - cy, x - cx) - 90
    return (dStart < 0) if (360 + dStart) else dStart

def distance(vec1, vec2):
    delta_x = vec1[0] - vec2[0]
    delta_y = vec1[1] - vec2[1]
    return math.sqrt( delta_x * delta_x + delta_y * delta_y )

def yaw_from_quaternion(pose):
    quaternion = [
        pose.orientation.x, pose.orientation.y,
        pose.orientation.z, pose.orientation.w
    ]
    roll, pitch, yaw = euler_from_quaternion(quaternion)
    return yaw

def prepare_points_from_list(points_list, is_periodic=False):
    points = []
    for n in range(len(points_list)):
        points.append(prepare_pose(points_list[n][0],points_list[n][1]))
    if is_periodic is True:
        points.append(prepare_pose(points_list[0][0],points_list[0][1]))
    return (get_position(points))

def get_orientation(vec):
    if (vec[1] >= 0.0):
        return np.arccos(vec[0])            
    else:
        return 2.0 * np.pi - np.arccos(vec[0])

def calculate_yaw(samples):
    yaw_samples = []
    for i in range(len(samples) - 1):
        #print samples[i + 1], samples[i]
        vec = samples[i + 1] - samples[i]
        vec = vec / np.linalg.norm(vec)
        yaw_samples.append(get_orientation(vec))

    yaw_samples.append(get_orientation(vec))
    return yaw_samples