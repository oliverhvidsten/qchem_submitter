from pymatgen.io.qchem.outputs import QCOutput

import os
import json
import argparse

from utils import gather_names


def read_single_job_outputs():
    names = gather_names("./init_mols/")
    for name in names:
        read_output(name)


def read_multiple_job_outputs(job_names):
    names = gather_names("./init_mols/")
    for name in names:
        read_output(name, one_job_per_file=False, job_names=job_names)


def read_output(name, one_job_per_file=True, job_names=None):
    """ Read the data in ./outputs/{name}/{name}.qout and save it as a json file """
    
    # move into the correct directory
    cwd = os.getcwd()
    os.chdir(f"{cwd}/outputs/{name}/")

    # If only one job per file, simply write one output json
    if one_job_per_file:
        qout = QCOutput(f"{name}.qout")
        with open(f"{name}.json", "w") as f:
            json.dump(qout.as_dict(), f)
    # If there are multiple jobs per file, write one json per job
    else:
        qouts = QCOutput.multiple_outputs_from_file(f"{name}.qout")
        if job_names is None:
            print(f"({name}) Job names not specified, using default names")
            job_names = [f"{name}_{i}" for i in range(len(qouts))]
        elif len(job_names) != len(qouts):
            print(f"({name}) Job name list is of incorrect length, using default names")
            job_names = [f"{name}_{i}" for i in range(len(qouts))]

        for qout, job_name in zip(qouts, job_names):
            with open(f"{job_name}.json") as f:
                json.dump(qout.as_dict(), f)



    # return to original directory to allow future jobs to work as intended
    os.chdir(cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--multi_job", 
        help="Specify if Qout files have more than one job",
        action="store_true"
        )
    parser.add_argument(
        "n", "--job_names", 
        help="Naming schemes for jobs in comma-separated format (e.g. 'geom, freq, sp')",
        type=str
        )
    args = parser.parse_args()

    if args.multi_job:
        read_multiple_job_outputs(args.job_names)
    else:
        read_single_job_outputs()