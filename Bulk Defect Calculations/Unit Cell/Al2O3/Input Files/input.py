from ase import Atoms
from ase.calculators.aims import Aims
from ase.optimize import BFGS
from ase.io import read 

# Old method of settings variables
#import os
#os.environ['ASE_AIMS_COMMAND']="mpirun -np "+os.environ['SLURM_NTASKS']+" /home/scw1057/software/fhi-aims/bin/aims."+os.environ['VERSION']+".scalapack.mpi.x"
#os.environ['AIMS_SPECIES_DIR']="/home/scw1057/software/fhi-aims/species_defaults/light"   # Light settings

#New method:
from carmm.run.aims_path import set_aims_command
set_aims_command(hpc="archer2", basis_set="light", defaults=2020)

# Build molecule
CeO2an = read('alumina.cif')

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
calc = get_aims_calculator(dimensions=3, k_grid=(6,4,4), xc='PBE')
calc.set(
         #spin='none',
         #relativistic=('atomic_zora','scalar'),
         occupation_type=('gaussian','0.1'),
         sc_accuracy_etot=1e-6,
         sc_accuracy_eev=1e-3,
         sc_accuracy_rho=1e-6,
         sc_accuracy_forces=1e-4,
        )

CeO2an.set_calculator(calc)

# Setup optimisation
dynamics = BFGS(CeO2an, trajectory='Al2O3Opt.traj')

# Run optimisation
dynamics.run(fmax=0.01)
