import math
import numpy as np
from pyspark import SparkContext

def Simulation(sc, ncells, nsteps, nprocs, leftX=-10., rightX=+10.,sigma=3., ao=1., coeff=. 375):
    def I(x):
        return ao*math.exp(-(x**2/(2*sigma**2)))

    x = np.linspace(-9.5, 10.5, ncells) # Create an array with ncells items from -9.5 to 10.5
    

    # Create an array with nsteps+1 items from 0th run # to nstpes th run. 
    # For our assignment: We should get totally 21 time steps from 0th to 20th
    t = np.linspace(0, nsteps, nsteps+1) 
    
    u = np.zeros(ncells) u_1 = np.zeros(ncells)
    for i in range(0, ncells):
        # Calculate the initial time value
        u_1[i] = I(x[i])
    
    # Update the value of n th run
    for n in range(1, nsteps+1):
        # Update the value of all cells except the bound points
        for i in range(1, ncells-1):
            u[i] = u_1[i] + coeff*(u_1[i-1] - 2*u_1[i] + u_1[i+1])
        u_1[:]= u
        u[0] = I(x[0]) # Keep the bound points unchanged #Print the result
        u[ncells-1] = I(x[ncells-1])
    for i in range(0,ncells): 
        print 'x',i,': ',u[i]
    
if __name__ == "__main__":
    sc = SparkContext(appName="SparkDiffusion") 
    Simulation(sc, 100, 20, 4)