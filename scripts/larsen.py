# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.getcwd()+"/../")
from src.input_files.larsen_init import LarsenInit
from src.solvers.fixed_source.solvers import FixedSource
import matplotlib.pyplot as plt
import time
import numpy as np


if __name__ == "__main__":
    
    N           = 2**11
    Nx          = 5
    generator   = "sobol"
    solver      = "Picard"
    source_tilt = True
    data        = LarsenInit(N=N, Nx=Nx, generator=generator,
                             source_tilt=source_tilt)
    start       = time.time()
    maxit       = 10
    tol         = 1e-3
    phi1         = FixedSource(data,solver=solver, maxit=maxit, tol=tol, 
                              save_data=False)
    sol = data.true_flux
    stop = time.time()
    print("time: ",stop-start)
    plt.title('Solution')
    plt.plot(data.mesh.midpoints, phi1[:,0], label='iQMC')
    plt.plot(data.mesh.midpoints, sol, label='Sol')
    plt.legend()
    
    plt.figure(figsize=(6,4),dpi=300)
    plt.title('Source')
    q    = data.tallies.q
    mesh = data.mesh.edges
    mid  = data.mesh.midpoints
    x    = np.linspace(data.LB, data.RB, num=1000)
    n    = len(x)
    conditions = [(mesh[i] <= x) & (x <= mesh[i+1]) for i in range(Nx)]
    y1 = np.piecewise(x, conditions, q)
    plt.plot(x,y1, label=r'$a_j$')
    if (source_tilt):
        qdot        = data.tallies.qdot
        y2          = np.zeros_like(x)
        for i in range(n):
            zone = data.mesh.GetZone([x[i],0,0], [0,0,0])
            x_mid = data.mesh.midpoints[zone]
            y2[i] = q[zone] + qdot[zone]*(x[i] - x_mid)
        plt.plot(x,y2,label=r'$a_j + b_j(x)$')
    for i in range(len(mesh)):
        plt.axvline(mesh[i],linestyle='-',color='black')
    plt.legend()
    plt.tight_layout()
        
    
    
    