#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:a100:1 #gpu:rtx8000:1 #gpu:l40s:4                          # GPU request
#SBATCH --job-name=spectrum_metric                       # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=40G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"

xp_names=("duacs_15m_8th" 
"globcurrent_15m_4th" 
"neurost_sst_ssh_15m_10th" 
"unet_uv_aoml_15m_10y_11d_bathy_no_sst_mae_duacs_RonanUnet" 
"unet_uv_aoml_15m_10y_11d_bathy_no_sst_mae_neurost_RonanUnet" 
)

conda activate bench_env

for xp_name in "${xp_names[@]}"; do
    srun python run_spectrum_GL.py "$xp_name"
done