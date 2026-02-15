#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:l40s:1 #gpu:l40s:1                          # GPU request
#SBATCH --job-name=rmse_hourly                       # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=50G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"

conda activate bench_env

xp_names=(
    "duacs_15m_8th" 
    "globcurrent_15m_4th"
)

for xp_name in "${xp_names[@]}"; do
    srun python run_rmse_hourly.py "$xp_name"
done


