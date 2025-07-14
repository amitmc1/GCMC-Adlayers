import os
from dscribe.descriptors import MBTR
from ase.io import read
import numpy as np


def calculate_mbtr(structure, species, periodic):
    # Setup the MBTR descriptor
    mbtr = MBTR(
        species=species,
        geometry={"function": "distance"},  # Two-body descriptors
        grid={"min": 0, "max": 10, "n": 5, "sigma": 0.1},
        weighting={"function": "exp", "scale": 0.5, "threshold": 1e-3},
        periodic=periodic,
        normalization="none",
        dtype="float64"
    )

    # Calculate the MBTR descriptor for the structure
    return mbtr.create(structure)


# Function to process all XYZ files in the frames folder
def process_all_xyz_files(frames_folder, species, output_file):
    descriptors_list = []
    filenames_list = []

    # Walk through all subdirectories
    for root, _, files in os.walk(frames_folder):
        for file in files:
            if file.endswith(".xyz"):
                xyz_path = os.path.join(root, file)
                print(f"Processing: {xyz_path}")

                # Read all frames in the XYZ file
                structures = read(xyz_path, index=":")

                for i, structure in enumerate(structures):
                    # Extract metadata for periodic boundary conditions
                    pbc = structure.info.get("pbc", "F F F")
                    pbc_flags = pbc.replace('"', '').split()
                    periodic = not all(flag == "F" for flag in pbc_flags)  # Check if any PBC flag is "T"

                    # Calculate MBTR descriptor
                    mbtr_descriptor = calculate_mbtr(structure, species, periodic)

                    # Flatten the descriptor and store it
                    descriptors_list.append(mbtr_descriptor.flatten())
                    filenames_list.append(f"{file}_frame_{i + 1}")  # Store filename with frame index

    # Convert descriptors list to a 2D NumPy array
    descriptors_array = np.vstack(descriptors_list)

    # Create a header with filenames
    header = "Filename," + ",".join([f"D{i + 1}" for i in range(descriptors_array.shape[1])])

    # Save to a text file with filenames as the first column
    with open(output_file, "w") as f:
        f.write(header + "\n")
        for filename, descriptor in zip(filenames_list, descriptors_array):
            f.write(f"{filename}," + ",".join(f"{val:.6f}" for val in descriptor) + "\n")

    print(f"Descriptors saved to {output_file}")


# Set parameters
frames_folder = r"/nfshome/store01/users/c.c21127846/phd/week1/JM/GCMC_MBTR/frames"  # Folder containing XYZ subdirectories
output_file = "mbtr_all_descriptors_GCMC.txt"  # Output file
species = ["O", "S", "Ni"]  # Define species for MBTR calculation

# Run the processing function
process_all_xyz_files(frames_folder, species, output_file)
