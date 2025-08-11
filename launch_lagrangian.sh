#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:a40:3 #gpu:l40s:4                          # GPU request
#SBATCH --job-name=lagrangian_metric                       # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=180G
é
export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"

xp_name="ssh_duacs_sst_w_to_u_v_11d_15m_ageos_no_sst"

conda activate bench_env
#conda activate woc_env

srun python run_lagrangian.py "$xp_name" #--> Add a mask and correct saving with daily output


