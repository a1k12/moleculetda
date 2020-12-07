import argparse
from read_file import *
from construct_pd import *
from vectorize_pds import *

#############################
# Possible user arguments
#############################
parser = argparse.ArgumentParser(description='molecule-tda')

parser.add_argument('--filename', type=str, default=None)

parser.add_argument('--supercell_size', default=None, \
    help='Use if wanting all systems to be a certain cubic size. Only works if lattice constants exist.')

# Vectorization parameters
parser.add_argument('--spread', type=float, default=0.15, help='Gaussian spread for vectorizing persistence diagram transformation.')

parser.add_argument('--weighting', type=str, help='Weighing scheme.')

args = parser.parse_args()

#############################
# Construct PD
#############################
if args.supercell_size:
    coords = read_data(args.filename, size=int(args.supercell_size), supercell=True)
else:
    coords = read_data(args.filename, size=None, supercell=False)

dgms = construct_pds(coords)

#############################
# Calculate types of distance metrics between PDs
#############################

#############################
# Vectorize PD example
#############################
np_dgms = diagrams_to_arrays(dgms)

# separate dgms into 0D, 1D, 2D
dgm_0d = np_dgms['dim0']
dgm_1d = np_dgms['dim1']
dgm_2d = np_dgms['dim2']

# example calculating bounds
bounds = []

max_birth = np.max(dgm_2d['birth'])
max_pers  = np.max(dgm_2d['death'] - dgm_2d['birth'])
max_death = np.max(dgm_2d['death'])
bounds.append([max_birth, max_pers, max_death])

pim = PersImage(spread=args.spread,
                pixels=[50, 50],
                specs = { 'maxB': bounds[0][0], 'maxP': bounds[0][1], 'minBD': 0 },
                weighting_type = args.weighting,
                verbose=False)

# vectorized persistence diagram
img = pim.transform([(x['birth'], x['death']) for x in dgm_1d])

if __name__ == '__main__':
    print(dgms)
    print(img)
