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
from scipy.misc import comb
from IShape import IShape
from PoseHelper import prepare_points_from_list, calculate_yaw
from PlotHelper import points_with_yaw_plot

def bernstein_poly(i, n, t):
    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i

class Bezier(IShape):
    def __init__(self, points, is_periodic=False):
        self.is_periodic = is_periodic
        self.points = prepare_points_from_list(points, self.is_periodic)
        self.sample_step = 0.4
        self.max_samples = 1000
        self.min_samples = 100
        self.is_points_valid = False
        self.validate_points()

    def validate_points(self):
        for i in range(1,len(self.points)):
            if np.linalg.norm(self.points[i-1] - self.points[i]) < 0.01:
                self.is_points_valid = False
            else:
                self.is_points_valid = True

    def sample_points(self):
        xPoints = np.array([point[0] for point in self.points])
        yPoints = np.array([point[1] for point in self.points])
        nPoints = len(self.points)

        step_size, total_steps = self.sample_rate()
        self.samples = []
        t = np.linspace(0.0, 1.0, total_steps)

        polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

        xvals = np.dot(xPoints, polynomial_array)
        yvals = np.dot(yPoints, polynomial_array)

        samples = np.array((xvals, yvals)).T
        samples = samples[::-1]
        yaw_samples = calculate_yaw(samples)
        return (samples, yaw_samples)

if __name__ == '__main__':
    bz = Bezier([[1,2],[10.5, 4.5],[5,6],[23.5,15.5],[20,2],[30.5,5.5]], True)
    samples, yaw_samples = bz.sample_points()
    points_with_yaw_plot(bz.name, bz.points, samples, yaw_samples)