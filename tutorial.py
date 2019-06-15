"""
FEniCS tutorial demo program: Diffusion of a Gaussian hill.
  u'= Laplace(u) + f  in a square domain
  u = u_D             on the boundary
  u = u_0             at t = 0
  u_D = f = 0
The initial condition u_0 is chosen as a Gaussian hill.
"""

from __future__ import print_function
from fenics import *
import time
from mpi4py import MPI

# Communicator
mpi_comm = MPI.COMM_WORLD
# Rank 
rank = mpi_comm.Get_rank()

if rank == 0:
    start_time = time.time()

CRITICAL  = 50 # errors that may lead to data corruption and suchlike
ERROR     = 40 # things that go boom
WARNING   = 30 # things that may go boom later
INFO      = 20 # information of general interest
PROGRESS  = 16 # what's happening (broadly)
TRACE     = 13 # what's happening (in detail)
DBG       = 10 # sundry

set_log_level(WARNING)

T = 2.0            # final time
num_steps = 55     # number of time steps
dt = T / num_steps # time step size

# Create mesh and define function space
nx = ny = 55
mesh = RectangleMesh(Point(-2, -2), Point(2, 2), nx, ny)
V = FunctionSpace(mesh, 'P', 1)
meshfile = File('heat_gaussian/mesh.pvd')
meshfile << mesh


# Define boundary condition
def boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(V, Constant(0), boundary)

# Define initial value
u_0 = Expression('exp(-a*pow(x[0], 2) - a*pow(x[1], 2))',
                degree=2, a=5)
u_n = interpolate(u_0, V)

# Define variational problem
u = TrialFunction(V)
v = TestFunction(V)
f = Constant(0)

F = u*v*dx + dt*dot(grad(u), grad(v))*dx - (u_n + dt*f)*v*dx
a, L = lhs(F), rhs(F)

# Create VTK file for saving solution
vtkfile = File('heat_gaussian/solution.pvd')

# Time-stepping
u = Function(V)
t = 0
print('OK')

for n in range(num_steps):

    # Update current time
    t += dt

    # Compute solution
    solve(a == L, u, bc)

######################################################################
    # processes = [mp.Process(target=solve, args=(a == L, u, bc)) for i in range(4)]
    # #Run processes
    # for p in processes:
    #     p.start()

    # # Exit the completed processes
    # for p in processes:
    #     p.join()
##########################################################

    # Get process results from the output queue
    #umix = [u.get() for p in processes]

    # Save to file and plot solution
    vtkfile << (u, t)

    # Update previous solution
    u_n.assign(u)

if rank == 0:
    end_time = time.time()
    print(str(end_time-start_time)+' s')