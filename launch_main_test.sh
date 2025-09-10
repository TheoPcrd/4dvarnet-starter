#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:rtx8000:3 #gpu:h100:2 #gpu:l40s:4 #gpu:h100:2 #gpu:rtx8000:3 #gpu:l40s:4 #gpu:h100:2 #gpu:rtx8000:3 #gpu:h100:2 #gpu:rtx8000:3  # #gpu:h100:2             # GPU request
#SBATCH --job-name=multivar_test                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=100G #480G #180G #300G #180G #480G #180G #200G #480G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel

HYDRA_FULL_ERROR=1 srun python main.py xp='multivar_uv_glorys_15m_10y_unet_1patch_wind_11d_psi'
#HYDRA_FULL_ERROR=1 srun python main.py xp='multivar_uv_drifters_15m_10y_unet_1patch_11d'
