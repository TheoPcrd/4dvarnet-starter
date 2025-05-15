#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:rtx8000:3                          # GPU request
#SBATCH --job-name=import-data                       # Job name
#SBATCH --output=./Test-GPU_%j.log # Standard output and error log (%j for jobid)

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate env-dc-global-ose1

conda info --env

for year in {2010..2010}


do 
    echo $year
    srun python import_data_glorys_15m_year.py "$year"
done