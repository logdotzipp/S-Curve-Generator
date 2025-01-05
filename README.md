# S Curve Generator

This small python script takes:
initial position
initial velocity

desired move velocity
desired move acceleration

final position

It then generates a smooth position curve to move from the current position to the final position. This curve is then plotted for visualization.

![image](https://github.com/user-attachments/assets/804a18d0-6714-47b1-9891-e11a465dfe02)


Given the inputs, the curve fit calculates the time for each time segment (aka gate) for the acceleration, constant velocity, and deceleration portions of the move.
This is done based on information from: https://medium.com/@clozoya1729/trapezoidal-velocity-profile-f1892c720cd7
This motion is called "trapezoidal" due to the shape of the velocity curve.

For the purposes of this code, the variables have the following physical meaning:

![image](https://github.com/user-attachments/assets/b5ec8492-7e23-4086-8d16-4abeabb976ff)

In some cases if acceleration is especially slow, or if the distance between the initial and final position is small, the target velocity will never be achieved.
In this case, the motion is triangular, due to the velocity curve forming a triangle shape.
This calculation is slightly different than the trapezoidal, and only contains two segments rather than three.

![image](https://github.com/user-attachments/assets/c25ef2ba-a99f-43b3-ab62-4bbbd6e843cf)

This script is intended to be adapted to robotic motion systems, wherein the axis is under a position loop on the motor controller/drive and the commanded position from the s curve is fed incrementally from the main cpu.
