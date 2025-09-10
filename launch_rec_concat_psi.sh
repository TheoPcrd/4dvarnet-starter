#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:a40:3 #gpu:l40s:4                          # GPU request
#SBATCH --job-name=rec_uv                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=180G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel
import hydra

HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4' +params='ose_pipeline_1y_1'

HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4' +params='ose_pipeline_1y_2'


## Chemin vers votre fichier YAML
YAML_FILE="/Odyssey/private/t22picar/multivar_uv/config/xp/ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4.yaml"
## Utiliser grep et awk pour extraire la valeur de xp_name
xp_name=$(grep -m 1 'xp_name:' "$YAML_FILE" | awk '{print $2}')
srun python concat_rec_saving_filter_psi.py "$xp_name" #--> Add a mask and correct saving with daily output

#conda activate woc_env
#srun python run_rmse.py "$xp_name" # --> Compute rmse score in rec/ 





