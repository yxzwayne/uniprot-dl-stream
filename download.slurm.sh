#!/bin/bash
#SBATCH --job-name=download_protease
#SBATCH --output=download_protease.out
#SBATCH --error=download_protease.err

python /path/to/uniprot_dl.py
