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

from abc import ABCMeta, abstractmethod
import numpy as np

class IShape:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._points = []
        self._sample_step = 0.2
        self._min_samples = 100
        self._max_samples = 1000
        self._is_points_valid = False
        self._is_periodic = False

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    @property
    def sample_step(self):
        return self._sample_step

    @sample_step.setter
    def sample_step(self, value):
        self._sample_step = value

    @property
    def min_samples(self):
        return self._min_samples

    @min_samples.setter
    def min_samples(self, value):
        self._min_samples = value

    @property
    def max_samples(self):
        return self._max_samples

    @max_samples.setter
    def max_samples(self, value):
        self._max_samples = value

    @property
    def is_points_valid(self):
        return self._is_points_valid

    @is_points_valid.setter
    def is_points_valid(self, value):
        self._is_points_valid = value

    @property
    def is_periodic(self):
        return self._is_periodic

    @is_periodic.setter
    def is_periodic(self, value):
        self._is_periodic = value

    @property
    def name(self):
        return self.__class__.__name__

    def total_distance(self):
        length = 0
        for l in range(1,len(self.points)):
            length += np.linalg.norm(self.points[l-1] - self.points[l])
        return length

    def sample_rate(self, total_distance=None):
        if total_distance is None:
            total_distance = self.total_distance()

        total_steps = total_distance / self.sample_step
        step_size = self.sample_step

        if total_steps > self.max_samples:
            step_size = (total_distance / self.max_samples)
        if total_steps < self.min_samples:
            step_size = (total_distance / self.min_samples)
        total_steps = total_distance / step_size

        return step_size, total_steps

    @abstractmethod
    def sample_points(self):
        pass

    @abstractmethod
    def validate_points(self):
        pass
