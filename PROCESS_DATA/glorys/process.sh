#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:l40s:4                      # GPU request
#SBATCH --job-name=process                       # Job name
#SBATCH --output=./process_%j.log # Standard output and error log (%j for jobid)

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel

conda info --env
srun python glorys_9y_4th.py
