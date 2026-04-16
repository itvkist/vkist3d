set -e

# Create and activate the Conda environment
conda create -n vkist3d python=3.10 -y

# Install COLMAP (v3.13.0) via Conda
conda run -n vkist3d conda install conda-forge::colmap==3.13.0 -y

# Install Python dependencies
conda run -n vkist3d pip install -r requirements.txt

echo "Conda environment 'vkist3d' is ready."
echo "Activate it with: conda activate vkist3d"
echo "Then start the backend with: python server.py"
