# -*- coding: utf-8 -*-

''' Generation of Trapezoidal Motion Curves'''
''' Logan Femling - 2025'''

import numpy as np
import matplotlib.pyplot as plt

def main():
  
    plt.clf()
    plt.close('all') # Close all plots
    
    # Variables that define a curve
    t0 = 0 # Curve generation time. In a real time application, this would be given by the system clock
    x0 = 0 # initial position (in)
    v0 = 0 # initial velocity (in/s)
    v = 10 # steady state velocity (in/s)
    a = 2 # acceleration (in/s^2)
    xf = 100 # final position (in)
    tscale = 1000 # time scale for the curve. In this case the system clock is in ms, so time is divided by 1000 to get seconds. This is necessary so that velocity and acceleration have units of in/s and in/s^2, respectively.
    
    # Create an array of times from 0 to 20000ms at 50ms intervals for testing
    time_array = np.arange(0, 20001, 50)
    pos_array = np.zeros_like(time_array)
    
    curve = CurveGenerator(x0, v0, a, v, xf, t0, tscale)
    
    
    #loop through time and calculate distance. This would be done every tick in a realtime setting
    for i in range(len(time_array)):
        pos_array[i] = curve.getCurvePos(time_array[i])
    
    
    #plot the curve
    plt.scatter(time_array, pos_array, color='blue', marker='o', s=1)
    
    # Add labels and title
    plt.xlabel('Time (ms)')
    plt.ylabel('Position (in)')
    plt.title('Trapezoidal Velocity S Curve')
    
    plt.show()



class CurveGenerator:
    def __init__(self, x0, v0, a, v, xf, t0, tscale):
        self.x0 = x0
        self.v0 = v0
        self.a = a
        self.v = v
        self.xf = xf
        self.t0 = t0
        self.tscale = tscale
    
        #Create a signed verison of acceleration/velocity depending on whether the motion is positive or negative relative to the starting position
        self.a_s = self.a * abs(self.xf - self.x0)/(self.xf - self.x0)
        self.v_s = self.v * abs(self.a_s)/self.a_s
        
        # Upon Inititalization, the class will calculate the time it takes to reach the final position
        # As well as the timing gates for each curve transition
    
        
        # Assume that the motion is trapezoidal, not triangular
        
        # First, Calculate the time from gate 0 to gate 1 using initial velocity, ss velocity and acceleration
        dt1 = abs(self.v_s - self.v0) / self.a
        # given that at gate 0, t=0, then dt1 = t1
        self.t1 = dt1
        # Calculate the incremental distance covered by gate 0 to gate 1
        # This distance is the area under the velocity curve.
        dx1 = (self.a_s/2)*self.t1**2 + self.v0*self.t1
        # Absolute position of the mass at the end of gate 1
        self.x1 = self.x0 + dx1
        
        # Calculate the time from gate 2 to 3 assuming starting with ss velocity
        dt3 = abs(self.v/a)
        # Calculate the incremental distance covered by gate 2 to gate 3
        dx3 = (self.v_s * dt3)/2
        
        # Calculate the distance from gate 1 to gate 2 by subtracting d1 and d3
        #self.d2 = abs(self.xf - self.x0) - (self.d1 + self.d3)
        dx2 = (-self.x1 +(self.xf - dx3))
        # caculate the time from gate 1 to gate 2 using the distance covered by d2
        dt2 = abs(dx2)/self.v
        self.t2 = dt2 + self.t1
    
        # Given t2 and dt3, calculate t3 (end time of curve)
        self.t3 = self.t2 + dt3
      
        print("Trapezoid Calculation Complete")
        print("dt1: " + str(dt1) + "  dt2: " + str(dt2) + "  dt3: " + str(dt3))
        print("t1: " + str(self.t1) + "  t2: " + str(self.t2) + "  t3: " + str(self.t3))
        print("dx1: " + str(dx1) + "  dx2: " + str(dx2) + "  dx3: " + str(dx3))
        # Need to check if dx2 matches the sign of the velocity
        
        # This occurs when the mass never reaches ss velocity during its move
        # This means that the curve is not trapezoidal, and must be calculated differently
        if (dx2 > 0 and self.v_s > 0) or (dx2 < 0 and self.v_s < 0):
            
            self.trapezoidal = True
            print("Trapezoid Confirmed")
    
        else:
    
            self.trapezoidal = False
            print("Triangle Motion Identified")
            # SS velocity will not be achieved with a trapezoidal curve
            # Motion will instead be triangular
            
            # Solve for the peak velocity. This should be less than the defined steady state velocity
            self.v1 = (self.a_s*(self.xf - self.x0) + (self.v0**2)/2)**(0.5) * (abs(self.a_s)/self.a_s)
            self.t1 = (self.v1-self.v0)/self.a_s
            self.t2 = (self.v1/self.a_s) + self.t1
            
            print("v1: " + str(self.v1) + " t1: " + str(self.t1) + " t2: " + str(self.t2))
            

        

    def getCurvePos(self, tc):
        # This function will return the position of the curve given the current time
        t = (tc - self.t0)/self.tscale # Calculate the time since the start of the curve. Additionally, scale the time to be in seconds 
        #if tc is in milliseconds, divide by 1000
        
        if(self.trapezoidal):
            # Check if the time is before the zero gate
            if(t < 0):
                raise Exception("Negative time inserted, curve generation error")
              
            elif(t < self.t1):
                # Curve is between gate zero and 1
                # Here the velocity is linear, and the position is parabolic
                x = self.a_s/2 * t**2 + self.v0 * t + self.x0
              
            elif(t < self.t2):
                # Curve is between gate 1 and 2
                # Here the velocity is constant, and the position is linear
                x1 = (self.a_s/2 * self.t1**2 + self.v0 * self.t1 + self.x0) # end position of gate 0-1, start postition of gate 1-2
                x = x1 + (t - self.t1) * self.v_s # position of gate 1-2
              
            elif(t < self.t3):
                # Curve is between gate 2 and 3
                # Here the velocity is linear, and the position is parabolic
                x1 = self.a_s/2 * self.t1**2 + self.v0 * self.t1 + self.x0 # end position of gate 0-1, start postition of gate 1-2
                x2 = x1 + (self.t2 - self.t1) * self.v_s # end position of gate 1-2, start position of gate 2-3
                x = -self.a_s/2*(t-self.t2)**2 + self.v_s*(t-self.t2) + x2
              
            else:
                # Curve is beyond t3, should be complete, therefore
                x = self.xf
        else:
            # Triangular motion
            if(t < 0):
                raise Exception("Negative time inserted, curve generation error")
            elif(t < self.t1):
                # Curve is between gate 0 and 1
                # Here the velocity is linear, and position is parabolic
                x = self.a_s/2 * t**2 + self.v0 * t + self.x0
                
            elif(t < self.t2):
                # Curve is between gate 1 and 2
                # Here the velocity is linear and position is parabolic
                x1 = self.a_s/2 * self.t1**2 + self.v0 * self.t1 + self.x0
                x = -self.a_s/2*(t-self.t1)**2 + self.v1*(t-self.t1) + x1
                
            else:
                # Curve is beyond t2, should be complete
                x = self.xf
        return x


if __name__=="__main__":
    main()