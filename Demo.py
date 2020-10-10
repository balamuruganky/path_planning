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

from math import pi
from Bezier import Bezier
from BezierSpline import BezierSpline
from CubicSpline import CubicSpline
from Dubins import Dubins
from Line import Line
from Ellipse import Ellipse
from PlotHelper import points_with_yaw_plot

POINTS = [[1,2],[10.5, 4.5],[5,6],[23.5,15.5],[20,2],[30.5,5.5]]
ELLIPSE_POINTS = [[0,0],[1,2],[3,1]]
CIRCLE_POINTS  = [[1,1],[1,2],[2,1]]
ORIENTATION = [[180, 90]]
ANGLES = [0, 90, 180, 270]

def create_objs():
	obj_list = []
	obj_list.append(Bezier(POINTS, True))
	obj_list.append(BezierSpline(POINTS, order=3, is_periodic=True))
	obj_list.append(BezierSpline(POINTS, order=(len(POINTS)+1), is_periodic=True))
	obj_list.append(CubicSpline(POINTS))
	obj_list.append(Dubins(POINTS,ORIENTATION,2))
	obj_list.append(Line(POINTS, False))
	for rot_angle in ANGLES:
		obj_list.append(Ellipse(ELLIPSE_POINTS, rot_angle, 0, 360))
		obj_list.append(Ellipse(CIRCLE_POINTS, rot_angle, 0, 360))
	for rot_angle in ANGLES:
		for angle in ANGLES:
			obj_list.append(Ellipse(ELLIPSE_POINTS, rot_angle, angle, (angle + 90)))
			obj_list.append(Ellipse(CIRCLE_POINTS, rot_angle, angle, (angle + 90)))
	return obj_list

if __name__ == '__main__':
	objs = create_objs()
	for obj in objs:
		samples = yaw_samples = []
		samples, yaw_samples = obj.sample_points()
		points_with_yaw_plot(obj.name, obj.points, samples, yaw_samples)
