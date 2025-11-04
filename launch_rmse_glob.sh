#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:rtx8000:1 #gpu:rtx8000:1 #gpu:a40:3 #gpu:l40s:4                          # GPU request
#SBATCH --job-name=rmse_glob_neu                       # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=150G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"

#xp_name="drifters_unet_15m_cmems"
xp_name="neurost_sst_ssh_00m_10th"
#xp_name="drifters_ssh_duacs_sst_w_to_u_v_11d_15m_aoml_old_norm"
#conda activate woc_env
conda activate bench_env

srun python run_rmse_glob.py "$xp_name" # --> Compute rmse score in rec/ 