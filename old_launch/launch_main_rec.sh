#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:l40s:1 # #gpu:h100:1  #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:a100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:a100:1 #gpu:l40s:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:a100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:a100:1 #gpu:l40s:1 #gpu:a100:1 #gpu:l40s:1 #gpu:a100:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:a100:1 #gpu:a100:1  #gpu:h100:1 #gpu:a100:1  #gpu:l40s:1 #gpu:a100:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:a100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:a100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:a100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:a100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:1 #gpu:rtx8000:1 #gpu:h100:1 #gpu:rtx8000:1 #gpu:h100:1 # #gpu:h100:1 #gpu:rtx8000:1 #gpu:h100:1 #gpu:l40s:1  #gpu:l40s:1 #gpu:a100:1 #gpu:h100:1 #gpu:l40s:1 #gpu:a100:1 #gpu:l40s:1 #gpu:h100:1 #gpu:l40s:4 #gpu:h100:2 #gpu:h100:2 #gpu:rtx8000:3 #gpu:rtx8000:3  #gpu:a40:3 #gpu:h100:2 #gpu:rtx8000:3          # GPU request
#SBATCH --job-name=multi_4th_rec  #multi_8th_2010_neu           # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=480G #200G #180G #200G # #200G #180G #250G #480G #180G #300G #180G #480G #180G #200G #480G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel

xp_name='unet_uv_aoml_15m_10y_11d_bathy_no_sst_mae_neurost_rec'


echo $xp_name

HYDRA_FULL_ERROR=1 srun python main.py xp=$xp_name +params='test_2015_2020' #--config-name=sweep_test.yaml --config-dir=./config/params