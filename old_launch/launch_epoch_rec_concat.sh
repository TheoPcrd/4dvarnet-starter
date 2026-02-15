#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:h100:2 #gpu:l40s:4  #gpu:a40:3  #gpu:h100:2  #                           # GPU request
#SBATCH --job-name=rec_uv                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=480G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel
import hydra

#!/bin/bash

# Fichier YAML à modifier
YAML_FILE_GEN="/Odyssey/private/t22picar/multivar_uv/config/xp/ose_pipeline_2019_global_4th_1patch_L4_generic.yaml"
YAML_FILE="/Odyssey/private/t22picar/multivar_uv/config/xp/ose_pipeline_2019_global_4th_1patch_L4_epoch.yaml"


# Chemin vers le dossier
#DOSSIER="/Odyssey/private/t22picar/multivar_uv/outputs/saved/base_rec_global_multivar_uv_glorys_15m_10y_unet_1patch_wind_11d_ageos_epoch/base_rec_global_multivar_uv_glorys_15m_10y_unet_1patch_wind_11d_ageos_epoch/checkpoints"
DOSSIER="/Odyssey/private/t22picar/multivar_uv/outputs/saved/Ageos"
# Boucle for pour afficher chaque fichier dans le dossier
for fichier in "$DOSSIER"/*; do
    if [ -f "$fichier" ]; then

        cp $YAML_FILE_GEN $YAML_FILE
        conda activate 4dvarnet-daniel
        import hydra

        #echo "Fichier trouvé : $fichier"
        # Extraire le nom du fichier sans le chemin
        nom_fichier=$(basename "$fichier")
        # Extraire la partie avant .ckpt
        nom_sans_extension="${nom_fichier%.ckpt}"
        # Extraire les trois derniers caractères avant .ckpt
        epoch="${nom_sans_extension: -3}"
        echo $epoch

        # Définir les nouveaux termes
        NEW_XP_NAME="ssh_duacs_sst_w_to_u_v_11d_15m_ageos_$epoch"
        NEW_CONFIG_PATH="/Odyssey/private/t22picar/multivar_uv/config/xp/base_rec_global_multivar_uv_glorys_wind_11d_duacs_norm_ageos.yaml"
        NEW_CKPT_PATH="$fichier"

        # Utiliser sed pour remplacer les termes
        sed -i "s/XP_NAME/$NEW_XP_NAME/g" "$YAML_FILE"
        sed -i "s|CONFIG_PATH|$NEW_CONFIG_PATH|g" "$YAML_FILE"
        sed -i "s|CKPT_PATH|$NEW_CKPT_PATH|g" "$YAML_FILE"


        HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_2019_global_4th_1patch_L4_epoch' +params='ose_pipeline_1y_1'

        HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_2019_global_4th_1patch_L4_epoch' +params='ose_pipeline_1y_2'

        ## Utiliser grep et awk pour extraire la valeur de xp_name
        xp_name=$(grep -m 1 'xp_name:' "$YAML_FILE" | awk '{print $2}')

        ##cd rec/
        srun python concat_rec_saving_filter_ageo.py "$xp_name" # 

        conda activate woc_env

        srun python run_rmse.py "$xp_name" # --> Compute rmse score in rec/ 
                
    fi
done










