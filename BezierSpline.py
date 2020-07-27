import numpy as np
from math import atan2
import scipy.interpolate as inter
import scipy as si
from IShape import IShape
from PoseHelper import prepare_points_from_list, calculate_yaw
from PlotHelper import points_with_yaw_plot

class BezierSpline(IShape):
    def __init__(self, points, order=None, is_periodic=False):
        self.is_periodic = is_periodic
        self.points = prepare_points_from_list(points, is_periodic)
        self.sample_step = 0.4
        self.max_samples = 1000
        self.min_samples = 100
        self.is_points_valid = False
        self.validate_points()
        if order is None:
            self.order = (len(self.points) - 1)
        else:
            self.order = order

    def validate_points(self):
        for i in range(1,len(self.points)):
            if np.linalg.norm(self.points[i-1] - self.points[i]) < 0.01:
                self.is_points_valid = False
            else:
                self.is_points_valid = True

    def bspline(self, n, degree):
        self.points = np.asarray(self.points)
        count = self.points.shape[0]
        degree = np.clip(degree,1,count-1)
        kv = np.clip(np.arange(count+degree+1)-degree,0,count-degree)
        max_param = count - (degree * (1-False))
        spl = inter.BSpline(kv, self.points, degree)
        return spl(np.linspace(0,max_param,n))

    def sample_points(self):
        if self.is_points_valid is False:
            print "Error : Please check the points..."
            return None, None

        step_size, total_steps = self.sample_rate()
        t = np.linspace(0.0, 1.0, total_steps)
        samples = self.bspline(total_steps, self.order)
        yaw_samples = calculate_yaw(samples)
        return samples, yaw_samples

if __name__ == '__main__':
    bz = BezierSpline([[1,2],[10.5, 4.5],[5,6],[23.5,15.5],[20,2],[30.5,5.5]], is_periodic=True)
    samples, yaw_samples = bz.sample_points()
    points_with_yaw_plot(bz.name, bz.points, samples, yaw_samples)
