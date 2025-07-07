#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:l40s:4                          # GPU request
#SBATCH --job-name=multivar                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)


export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel
import hydra

HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4' +params='ose_pipeline_1y_1'

HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4' +params='ose_pipeline_1y_2'

cd rec/
path_rec="multivar_mapping_ssh_sst_w_to_u_v_L4_10y"
srun python concat_rec.py "$path_rec"