#!/bin/dash

ENV_NAME="telerehab"

check_miniconda_installed() {
  if ! command -v conda >/dev/null 2>&1; then
    echo "miniconda not found, installing miniconda..."
    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm ~/miniconda3/miniconda.sh
    . ~/miniconda3/bin/activate
    conda init --all
  else
    echo "miniconda already installed."
  fi
}

env_exists() {
  # Ensure conda is in PATH
  export PATH="$HOME/.miniconda/bin:$PATH"

  if conda info --envs | grep -q "^$ENV_NAME"; then
    return 0
  else
    return 1
  fi
}

create_env() {
  echo "creating conda environment: $ENV_NAME..."
  conda create -n $ENV_NAME -y python=3.11 pandas "numpy<2" tensorflow opencv matplotlib scipy
  . ~/miniconda3/bin/activate
  conda activate $ENV_NAME
  conda install -c opensim-org opensim
  echo
  echo "=========================================="
  echo "    environment '$ENV_NAME' created!      "
  echo "------------------------------------------"
  echo "             to activate, run:            "
  echo "        -> conda activate $ENV_NAME       "
  echo "=========================================="
}

check_miniconda_installed
if ! env_exists; then
  create_env
else
  echo
  echo "=========================================="
  echo "     environment '$ENV_NAME' exists!      "
  echo "------------------------------------------"
  echo "             to activate, run:            "
  echo "        -> conda activate $ENV_NAME       "
  echo "=========================================="
fi

