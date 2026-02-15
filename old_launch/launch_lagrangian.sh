#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:l40s:1 #gpu:l40s:1                          # GPU request
#SBATCH --job-name=lagrangian_met                       # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=50G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"

#xp_name="GC_15m_4th_h"

conda activate bench_env
#conda activate woc_env

#srun python run_lagrangian.py "$xp_name" #--> Add a mask and correct saving with daily output

xp_names=(
    ""unet_uv_drifters_aoml_15m_10y_11d_bathy_no_sst_mae_neurost""
)

for xp_name in "${xp_names[@]}"; do
    srun python run_lagrangian.py "$xp_name"
done


#srun python run_spectrum.py "$xp_name" #--> Add a mask and correct saving with daily output

#srun python plot_lagrangian_and_spectrum_15m.py "$xp_name" # 


