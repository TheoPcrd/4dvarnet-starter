#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:h100:1 #gpu:rtx8000:1 #gpu:a40:3 #gpu:rtx8000:3 #gpu:l40s:4  #gpu:a40:3  #gpu:h100:2  #                           # GPU request
#SBATCH --job-name=rec_uv                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=30G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel
import hydra

xp_name="neurost_sst_ssh_15m_8th"

#conda activate woc_env
conda activate bench_env

srun python run_rmse_no_json.py "$xp_name" # --> Compute rmse score in rec/ 

srun python run_spectrum.py "$xp_name" # 

srun python run_lagrangian.py "$xp_name" # 

srun python plot_lagrangian_and_spectrum_15m.py "$xp_name" # 
