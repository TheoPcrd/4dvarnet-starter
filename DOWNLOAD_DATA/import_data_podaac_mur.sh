#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:rtx8000:3                          # GPU request
#SBATCH --job-name=Test-srun                        # Job name
#SBATCH --output=./import_MUR_%j.log # Standard output and error log (%j for jobid)

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda base

conda info --env
srun import_data_mur.sh
#podaac-data-downloader -c MUR-JPL-L4-GLOB-v4.1 -d ../data/. --start-date 2019-01-01T00:00:00Z --end-date 2019-01-02T00:00:00Z -e ""
