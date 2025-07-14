from ase import Atoms
from ase.calculators.aims import Aims
from ase.optimize import BFGS
from ase.io import read 

# Old method of settings variables
#import os
#os.environ['ASE_AIMS_COMMAND']="mpirun -np "+os.environ['SLURM_NTASKS']+" /home/scw1057/software/fhi-aims/bin/aims."+os.environ['VERSION']+".scalapack.mpi.x"
#os.environ['AIMS_SPECIES_DIR']="/home/scw1057/software/fhi-aims/species_defaults/light"   # Light settings

import os
os.environ["AIMS_SPECIES_DIR"] = "/nfshome/store01/users/c.c21127846/phd/week1/JM_defects/basis"
os.environ['ASE_AIMS_COMMAND']="mpirun -np "+os.environ['SLURM_NTASKS']+" /scratch/c.c21127846/fh-iaims-amitc/build/aims."+os.environ['VERSION']+".scalapack.mpi.x"

# Build molecule
TiO2an = read('geometry.in')

# Old method of setting up calculator
#calc = Aims(xc='PBE',
#            output=['dipole'],
#            sc_accuracy_etot=1e-6,
#            sc_accuracy_eev=1e-3,
#            sc_accuracy_rho=1e-6,
#            sc_accuracy_forces=1e-4,
#           )

# New method that gives a default calculator
from carmm.run.aims_calculator import get_aims_calculator
calc = get_aims_calculator(dimensions=3, k_grid=(3,3,2), xc='mbeef')
calc.set(
         #spin='none',
         #relativistic=('atomic_zora','scalar'),
         occupation_type=('gaussian','0.1'),
         plus_u_petukhov_mixing= 1,
	 plus_u_use_hydros="True",
         plus_u_matrix_control="True",
         plus_u_matrix_release= 1E-3,
         #n_max_pulay=20,
         #charge_mix_param=0.05,
         sc_accuracy_etot=1e-6,
         sc_accuracy_eev=1e-3,
         sc_accuracy_rho=1e-6,
         sc_accuracy_forces=1e-4,
        )

TiO2an.set_calculator(calc)

# Setup optimisation
dynamics = BFGS(TiO2an, trajectory='TiO2AnOpt.traj')

# Run optimisation
dynamics.run(fmax=0.01)
