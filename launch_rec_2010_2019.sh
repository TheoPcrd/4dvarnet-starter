#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:h100:1 #gpu:rtx8000:1 #gpu:l40s:1 #gpu:h100:1 #gpu:rtx8000:1 #gpu:a40:3 #gpu:rtx8000:3 #gpu:l40s:4  #gpu:a40:3  #gpu:h100:2  #                           # GPU request
#SBATCH --job-name=rec_uv                        # Job name
#SBATCH --cpus-per-gpu=12    # 12 CPUs for each GPU
#SBATCH --output=log/job_%j.log # Standard output and error log (%j for jobid)
#SBATCH --mem=300G

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate 4dvarnet-daniel
import hydra

for year in {2010..2019}; do
    year_start=$((year - 1))
    year_end=$((year + 1))

    echo "Lancement pour year=$year, year_start=$year_start, year_end=$year_end"
    HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_year' ++year="$year" ++year_start="$year_start" ++year_end="$year_end"
done

#HYDRA_FULL_ERROR=1 srun python main.py xp='ose_pipeline_year' ++year=2018 ++year_start=2017 ++year_end=2019
