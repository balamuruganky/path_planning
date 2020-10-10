# ROS Navigation - Path Planning
ROS Path Planning (Bezier, Bezier Spline, Cubic Spline, Dubins, Line, Circle, Ellipse, Arc)

## Dependencies
  * Numpy (pip install numpy)
  * Scipy (pip install scipy)
  * Matplotlib (pip install matplotlib)
  * Dubins (pip install dubins)
  
## Execute 
  * python Demo.py
  
## Goal
The goal of this project is to plan the robot path with given set of points as list. The grometry shape path will be created with yaw angles.
The resultant points and yaw angles can generate geometry_msgs/Pose Message (http://docs.ros.org/melodic/api/geometry_msgs/html/msg/Pose.html)

## Result
### Bezier
![image](https://github.com/balamuruganky/path_planning/blob/master/result/Bezier_cfbc19fb-8b5f-43f4-aef5-d0bf0cc3d062.png?raw=true)
### Bezier Spline (Piecewise Bezier)
#### Order : 3
![image](https://github.com/balamuruganky/path_planning/blob/master/result/BezierSpline_b8c68740-9369-4673-9df2-0dc1d9b7a7f8.png?raw=true)
#### Order : Number of points + 1
![image](https://github.com/balamuruganky/path_planning/blob/master/result/BezierSpline_d10298f1-8349-4a71-9c76-82ef35af48d6.png?raw=true)
### Cubic Spline
![image](https://github.com/balamuruganky/path_planning/blob/master/result/CubicSpline_77515d3f-d61b-472e-82a0-b41ff43c8d06.png?raw=true)
### Line
![image](https://github.com/balamuruganky/path_planning/blob/master/result/Line_61fc3746-29e5-47ef-a9eb-d91d1f90a30a.png?raw=true)
### Dubins
![image](https://github.com/balamuruganky/path_planning/blob/master/result/Dubins_3a753c04-0fb6-4af3-a53a-5a130855ee40.png?raw=true)
### Ellipse
#### No Rotation applied
![image](https://github.com/balamuruganky/path_planning/blob/master/result/Ellipse_66c194c8-0129-4eec-bfa3-f59a8f18be3d.png?raw=true)
#### 90 deg Rotated
![image](https://github.com/balamuruganky/path_planning/blob/master/result/Ellipse_d490e7da-dfdc-42ce-a352-2f81a28b857f.png?raw=true)
### Circle
![image](https://github.com/balamuruganky/path_planning/blob/master/result/Ellipse_44b00b4f-53c3-40d4-9c75-b82001daaf60.png?raw=true)
### Ellptic Arc
![image](https://github.com/balamuruganky/path_planning/blob/master/result/Ellipse_125c3315-c0ca-4a4a-bdec-a3881d2fbdb4.png?raw=true)
### Circle Arc
![image](https://github.com/balamuruganky/path_planning/blob/master/result/Ellipse_3a50a702-4a82-401d-aff7-d9d10f25d441.png?raw=true)
