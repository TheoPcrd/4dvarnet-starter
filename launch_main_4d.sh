#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:a100:1                          # GPU request
#SBATCH --job-name=multivar                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel

HYDRA_FULL_ERROR=1 srun python main.py xp='base_rec_global_multivar_uv_glorys_15m_1y'
#HYDRA_FULL_ERROR=1 srun python main.py xp='base_rec_global_multivar_uv_glorys_15m_1y_unet_1patch'