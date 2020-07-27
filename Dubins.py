import numpy as np
import dubins
from IShape import IShape
from PoseHelper import prepare_points_from_list, calculate_yaw
from PlotHelper import points_with_yaw_plot
import itertools

class Dubins(IShape):
    def __init__(self, points, orientation, turning_radius=1):
        self.points = prepare_points_from_list(points)
        self.orientation = prepare_points_from_list(orientation)
        self.sample_step = 0.1
        self.max_samples = 1000
        self.min_samples = 100
        self.is_points_valid = False
        self.validate_points()
        self.turning_radius = turning_radius

    def validate_points(self):
		if len(self.points) >= 2:
			self.is_points_valid = False
		else:
			self.is_points_valid = True

    def total_distance(self, path):
        return path.path_length()

    def sample_points(self):
		if self.is_points_valid is False:
			print "Warning : Only first two points considered..."

		path = dubins.shortest_path((self.points[0][0], self.points[0][1], self.orientation[0][0]), 
									(self.points[1][0], self.points[1][1], self.orientation[0][1]), 
									self.turning_radius)

		step_size, total_steps = self.sample_rate(self.total_distance(path))
		configurations, _ = path.sample_many(step_size)

		xPoints = np.array([point[0] for point in configurations])
		yPoints = np.array([point[1] for point in configurations])

		samples = yaw_samples = []
		samples = np.array((xPoints, yPoints)).T
		yaw_samples = np.array([point[2] for point in configurations])
		return samples, yaw_samples

if __name__ == '__main__':
    bz = Dubins([[1,2],[10.5, 4.5],[2,4]], [[1.2,1.3]], 2)
    samples, yaw_samples = bz.sample_points()
    points_with_yaw_plot(bz.name, bz.points, samples, yaw_samples)
