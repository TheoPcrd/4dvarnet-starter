#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:a100:1 #gpu:a100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1                        # GPU request
#SBATCH --job-name=rec_no_bathy                      # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=100G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel
import hydra

xp_name="unet_uv_aoml_15m_10y_11d_bathy_no_sst_bathy_mae_duacs_RonanUnet"

srun python concat_rec_saving_filter.py "$xp_name" # 

conda activate bench_env

srun python run_rmse_glob.py "$xp_name" # --> Compute rmse score in rec/ 