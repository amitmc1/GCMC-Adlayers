#!python3 -u

from susmost import *
import susmost.mc as mc
from mpi4py import MPI
import sys

def print_means(m, prop:str):
  global mu_O_fcc, mu_S_fcc
  print('Means', prop, f'{mu_S_fcc:06.2f}', f'{mu_O_fcc:06.2f}', ' '.join([f'{x:7.3f}' for x in m.means(prop)]))

#lt = load_lattice_task('./S-Ni111')
lt = load_lattice_task('./Final-Ni111')

# model parameters
mu_S_delta = -0.183
mu_O_delta = -0.370
mu_SO_hcp_delta = 3.48
mu_SO_fcc_delta = 3.93
kB = 0.000086

# free variables
#mu_S_fcc = -0.3
#mu_O_fcc = -0.6

mu_S_fcc = float(sys.argv[1])
mu_O_fcc = float(sys.argv[2])

# dependent variables
mu_S_hcp = mu_S_fcc - mu_S_delta
mu_O_hcp = mu_O_fcc - mu_O_delta
mu_SO_fcc = mu_S_fcc + mu_O_fcc + mu_SO_fcc_delta
mu_SO_hcp = mu_S_hcp + mu_O_hcp + mu_SO_hcp_delta

lt.set_ads_energy('S-fcc-Ni111', mu_S_fcc)
lt.set_ads_energy('S-hcp-Ni111', mu_S_hcp)
lt.set_ads_energy('O-fcc-Ni111', mu_O_fcc)
lt.set_ads_energy('O-hcp-Ni111', mu_O_hcp)
#lt.set_ads_energy('SO-fcc-Ni111', mu_SO_fcc)
#lt.set_ads_energy('SO-hcp-Ni111', mu_SO_hcp)

coverages = {
  "S-fcc-Ni111":1, 
  "S-hcp-Ni111":1, 
  "O-fcc-Ni111":1, 
  "O-hcp-Ni111":1, 
#  "SO-fcc-Ni111":1, 
#  "SO-hcp-Ni111":1
}

lt.set_property('coverage', coverages)
lt.set_property('S_cnt', {"S-fcc-Ni111":1, "S-hcp-Ni111":1})
lt.set_property('O_cnt', {"O-fcc-Ni111":1, "O-hcp-Ni111":1})
#lt.set_property('SO_cnt', {"SO-fcc-Ni111":1, "SO-hcp-Ni111":1})


Ts=[300, 400, 600, 800, 1000, 1200, 1500, 1700]

m = mc.make_metropolis(lt, 30, Ts, kB)
m.phys_difusion=False
m.diff_cui_min=1
m.diff_cui_max=3

mc.run(m, 10, 100000, traj_fns=[f'traj_{mu_S_fcc:06.2f}_{mu_O_fcc:06.2f}_{T:04d}.xyz' for T in Ts])

if MPI.COMM_WORLD.Get_rank( ) == 0:
	print_means(m, 'energy')
	print_means(m, 'S_cnt')
	print_means(m, 'O_cnt')
	#print (m.means('SO_cnt'))

#mc.stat_digest(m)

