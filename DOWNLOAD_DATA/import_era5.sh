#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:rtx8000:3                          # GPU request
#SBATCH --job-name=import_era5                        # Job name
#SBATCH --output=./Test-GPU_%j.log # Standard output and error log (%j for jobid)

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate base

conda info --env
srun python import_data_era5.py > "output_era5.log" 2>&1
