#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:h200:1 #gpu:rtx8000:1 #gpu:l40s:1 #gpu:h100:1 #gpu:rtx8000:1 #gpu:a40:3 #gpu:rtx8000:3 #gpu:l40s:4  #gpu:a40:3  #gpu:h100:2  #                           # GPU request
#SBATCH --job-name=rec_uv                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=50G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel


xp_name="unet_uv_aoml_15m_10y_11d_bathy_no_sst_mae_neurost_RonanUnet"

for year in {2010..2019}; do

    srun python concat_rec_saving_filter.py "${year}" "${xp_name}"

done