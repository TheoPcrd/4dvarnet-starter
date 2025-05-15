#!/bin/bash
#SBATCH --partition=Odyssey                         # Partition name
#SBATCH --gres=gpu:rtx8000:3                          # GPU request
#SBATCH --job-name=mport_podaac                       # Job name
#SBATCH --output=./import_podaac_%j.log # Standard output and error log (%j for jobid)

export HOME=/Odyssey/private/t22picar/
source "/Odyssey/private/t22picar/miniforge3/etc/profile.d/conda.sh"
conda activate env-dc-global-ose1

conda info --env
srun import_data_neurost_sst_ssh.sh
#srun podaac-data-downloader -c NEUROST_SSH-SST_L4_V2024.0 -d ../data/ssh_L4 --start-date 2010-01-01T00:00:00Z --end-date 2010-01-08T00:00:00Z -e ""