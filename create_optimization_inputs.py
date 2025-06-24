from pymatgen.io.qchem.inputs import QCInput
from pymatgen.core.structure import Molecule

import os
import json


def main():
    cwd = os.getcwd()
    mols = gather_molecules("./init_mols")

    for molecule_name, molecule_obj in mols.items():
        create_inputs(molecule_name, molecule_obj)
        os.chdir(cwd)
        



def create_inputs(name, mol_obj):
    """ Creates Q-Chem Input files for a molecule"""
    os.makedirs(f"./outputs/{name}")
    os.chdir(f"./outputs/{name}")

    qcin = QCInput(
        molecule=mol_obj,
        rem=rem,
        smx=smx,
        geom_opt=geom_opt
    )

    qcin.write_file(f"{name}.qin")
    script = submit_script(name)

    with open("submit.script", "w") as f:
        f.write(script)


def submit_script(name):
    """ Creates a submit script to submit the jobs to the cluster """
    lines = [
        "#!/bin/bash -l",
        "",
        "#SBATCH --nodes=1",
        "#SBATCH --qos=normal",
        "#SBATCH --time=24:00:00",
        "#SBATCH --partition=standard",
        "#SBATCH --account=silimorphous",
        "#SBATCH --job-name=geom_opt",
        "#SBATCH --output=FW_job-%j.out",
        "#SBATCH --error=FW_job-%j.error",
        "#SBATCH --ntasks=128",
        "",
        "source activate cms_atomate",
        "module load gcc",
        "module load q-chem/6.0",
        "",
        f"qchem {name}.qin {name}.qout"
    ]
    return "\n".join(lines)



def gather_molecules(dirpath):
    """ Gets all of the molecules from the desired folder"""
    # get charges
    all_molecules = dict()
    with open(f"{dirpath}/charge.json") as f:
        charges = json.load(f)
    for file in os.listdir(dirpath):
        if file.endswith(".xyz"):
            print(file)
            charge = charges[file]
            mol = Molecule.from_file(f"{dirpath}/{file}")
            mol.set_charge_and_spin(charge=charge)  # type: ignore

            file_pre = file[:-4]
            all_molecules[file_pre] = mol

    return all_molecules


# Set variables for Q-Chem job
rem = {
        'job_type':'opt',
        'basis': 'def2-svpd',
        'max_scf_cycles': 100,
        'gen_scfman': 'true',
        'xc_grid': 3,
        'thresh': 14,
        's2thresh': 16,
        'scf_algorithm': 'diis',
        'resp_charges': 'true',
        'symmetry': 'false',
        'sym_ignore': 'true',
        'method': 'wb97x-v',
        'solvent_method': 'smd',
        'ideriv': 1
    }
smx = {
    "solvent": "other",
    "epsilon": 18.5,
    "soln": 1.415,
    "sola": 0.0,
    "solb": 0.735,
    "solg": 20.2,
    "solc": 0.0,
    "solh": 0.0,
}

geom_opt = {
   "maxiter":200,
   "coordinates": "redundant",
   "max_displacement": 0.1,
   "optimization_restart": "false",
}

if __name__ == "__main__":
    main()