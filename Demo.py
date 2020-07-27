from math import pi
from Bezier import Bezier
from BezierSpline import BezierSpline
from CubicSpline import CubicSpline
from Dubins import Dubins
from Line import Line
from PlotHelper import points_with_yaw_plot

POINTS = [[1,2],[10.5, 4.5],[5,6],[23.5,15.5],[20,2],[30.5,5.5]]
ORIENTATION = [[pi, (pi/2)]]

def create_objs():
	obj_list = []
	obj_list.append(Bezier(POINTS, True))
	obj_list.append(BezierSpline(POINTS, order=3, is_periodic=True))
	obj_list.append(CubicSpline(POINTS))
	obj_list.append(Dubins(POINTS,ORIENTATION,2))
	obj_list.append(Line(POINTS, False))
	return obj_list

if __name__ == '__main__':
	objs = create_objs()
	for obj in objs:
		samples, yaw_samples = obj.sample_points()
		points_with_yaw_plot(obj.name, obj.points, samples, yaw_samples)

