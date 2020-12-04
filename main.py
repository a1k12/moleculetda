import argparse
from read_file import *
from construct_pd import *

#############################
# Possible user arguments
#############################
parser = argparse.ArgumentParser(description='tda-for-science')

parser.add_argument('--filename', type=str, default=None)

parser.add_argument('--supercell_size', type=int, default=1, \
    help='Use if wanting all systems to be a certain cubic size. Only works if lattice constants exist.')

args = parser.parse_args()

#############################
# Construct PD
#############################
if args.supercell_size:
    coords = read_data(args.filename, args.supercell_size, supercell=True)
else:
    coords = read_data(args.filename, args.supercell_size=None, supercell=False)
dgms = construct_pds(coords)

#############################
# Calculate distances between PDs        
#############################

#############################
# Vectorize PD
#############################
