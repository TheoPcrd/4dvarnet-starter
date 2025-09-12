#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:rtx8000:1 #gpu:h100:1 #gpu:rtx8000:1 #gpu:h100:1 #gpu:rtx8000:1 #gpu:h100:1 #gpu:rtx8000:1 #gpu:a40:3 #gpu:rtx8000:3 #gpu:l40s:4  #gpu:a40:3  #gpu:h100:2  #                           # GPU request
#SBATCH --job-name=rec_uv_glorys                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=100G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel
import hydra

# Chemin vers votre fichier YAML
YAML_FILE="/Odyssey/private/t22picar/multivar_uv/config/xp/ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4.yaml"
# Utiliser grep et awk pour extraire la valeur de xp_name
xp_name=$(grep -m 1 'xp_name:' "$YAML_FILE" | awk '{print $2}')
echo $xp_name

HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4' +params='ose_pipeline_1y_1'

HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4' +params='ose_pipeline_1y_2'

#cd rec/
srun python concat_rec_saving_filter.py "$xp_name" # 

#srun python concat_rec_saving_filter.py #--> Add a mask and correct saving with daily output

#conda activate woc_env
conda activate bench_env

srun python run_rmse.py "$xp_name" # --> Compute rmse score in rec/ 

srun python run_spectrum.py "$xp_name" # 

srun python run_lagrangian.py "$xp_name" # 

srun python plot_lagrangian_and_spectrum_15m.py "$xp_name" # 
