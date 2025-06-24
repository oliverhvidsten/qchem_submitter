import os
import subprocess
import time



def main():
    names = gather_names("./init_mols/")
    for name in names:
        submit_job(name)


def gather_names(dirpath):
    """ Gets all names of the molecules from the input molecule folder """
    
    all_names = list()
    for file in os.listdir(dirpath):
        if file.endswith(".xyz"):
            all_names.append(file[:-4])

    return all_names


def submit_job(name):
    """ Submit the job contained in the folder ./outputs/{name}/ """
    
    # move into the correct directory
    cwd = os.getcwd()
    os.chdir(f"{cwd}/outputs/{name}/")

    # submit the job
    subprocess.run(["sbatch", "submit.script"])
    
    # sleep for a bit as to not cause issues with the HPC
    time.sleep(0.5)
    
    # return to original directory to allow future jobs to work as intended
    os.chdir(cwd)


if __name__ == "__main__":
    main()