import numpy as np
from math import atan2
from IShape import IShape
from PoseHelper import prepare_points_from_list, calculate_yaw, start_angle, distance
from PlotHelper import points_with_yaw_plot

class Ellipse(IShape):
    def __init__(self, points, rotation_angle = 0, start_angle = 0, end_angle = 360):
        self.points = prepare_points_from_list(points)
        self.sample_step = 0.05
        self.max_samples = 1000
        self.min_samples = 100
        self.rotation_angle = rotation_angle
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.validate_points()

    def validate_points(self):
        for i in range(1,len(self.points)):
            if np.linalg.norm(self.points[i-1] - self.points[i]) < 0.01:
                self.is_points_valid = False
            else:
                if len(self.points) >= 4:
                    self.is_points_valid = False
                else:
                    self.is_points_valid = True

    def ellipse(self, step_size):
        self.points = np.asarray(self.points)
        count = self.points.shape[0]
        xSamples = []
        ySamples = []
        centerX = self.points[0][0]
        centerY = self.points[0][1]
        dist1 = distance(self.points[1], self.points[0])
        dist2 = distance(self.points[2], self.points[0])
        if (dist1 < dist2):
            minor_axis = dist1
            major_axis = dist2
        else:
            minor_axis = dist2
            major_axis = dist1

        rotationAngle = np.deg2rad(self.rotation_angle);
        startPoint = np.deg2rad(self.start_angle)
        endPoint = np.deg2rad(self.end_angle)
        arc_length = 0
        prev_x = 0
        prev_y = 0
        perimeter = 0

        inc = startPoint
        while (inc < endPoint):
            xPos = centerX + (major_axis * np.cos(inc)) * np.sin(rotationAngle) + (minor_axis * np.sin(inc)) * np.cos(rotationAngle)
            yPos = centerY + (minor_axis * np.sin(inc)) * np.sin(rotationAngle) + (major_axis * np.cos(inc)) * np.cos(rotationAngle)
            xSamples.append(xPos)
            ySamples.append(yPos)

            arc_length = start_angle(centerX, centerY, xPos, yPos);
            a = (prev_x - xPos)
            b = (prev_y - yPos)
            if (prev_x != 0 and prev_y != 0):
                perimeter += np.sqrt( a*a + b*b )

            prev_x = xPos
            prev_y = yPos
            inc += step_size
        return (xSamples, ySamples)

    def sample_points(self):
        if self.is_points_valid is False:
            print "Warning : Error in points (or) first 3 points are being considered"

        step_size, total_steps = self.sample_rate()
        t = np.linspace(0.0, 1.0, total_steps)
        x, y = self.ellipse(step_size)
        samples = np.array((x, y)).T
        yaw_samples = calculate_yaw(samples)
        return samples, yaw_samples

if __name__ == '__main__':
    rot_angles = [0, 90, 180, 270]

    for rot_angle in rot_angles:
        es = Ellipse([[0,0],[1,2],[3,1]], rot_angle, 0, 360)
        samples, yaw_samples = es.sample_points()
        points_with_yaw_plot(es.name, es.points, samples, yaw_samples)

    for rot_angle in rot_angles:
        for angle in rot_angles:
            es = Ellipse([[0,0],[1,2],[3,1]], rot_angle, angle, (angle + 90))
            samples, yaw_samples = es.sample_points()
            points_with_yaw_plot(es.name, es.points, samples, yaw_samples)

    for rot_angle in rot_angles:
        cl = Ellipse([[1,1],[1,2],[2,1]], rot_angle, 0, 360)
        samples, yaw_samples = cl.sample_points()
        points_with_yaw_plot(cl.name, cl.points, samples, yaw_samples)

    for rot_angle in rot_angles:
        for angle in rot_angles:
            cl = Ellipse([[1,1],[1,2],[2,1]], rot_angle, angle, (angle + 90))
            samples, yaw_samples = cl.sample_points()
            points_with_yaw_plot(cl.name, cl.points, samples, yaw_samples)