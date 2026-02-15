#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:a100:1                          # GPU request
#SBATCH --job-name=multivar                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel

cd rec/
path_rec="multivar_mapping_ssh_neurostv2_sst_w_to_u_v_L4_10y_11d_mdt"
srun python concat_rec.py "$path_rec"