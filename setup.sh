set -e

VKIST_3D=$(pwd)  # Store current directory in VKIST_3D
cd "$VKIST_3D"   # Change to the stored path

# Check CUDA is available before proceeding
if ! command -v nvcc &> /dev/null; then
    echo "CUDA Toolkit not found. Please install it before running this script."
    exit 1
fi

# Install dependencies for COLMAP and OpenMVS
sudo apt-get update -qq && sudo apt-get install -qq -y
sudo apt-get -y install \
     git \
     ninja-build \
     build-essential \
     libboost-program-options-dev \
     libboost-filesystem-dev \
     libboost-graph-dev \
     libboost-system-dev \
     libboost-iostreams-dev \
     libboost-serialization-dev \
     libeigen3-dev \
     libflann-dev \
     libfreeimage-dev \
     libmetis-dev \
     libgoogle-glog-dev \
     libgtest-dev \
     libsqlite3-dev \
     libglew-dev \
     qtbase5-dev \
     libqt5opengl5-dev \
     libcgal-dev \
     libcgal-qt5-dev \
     libceres-dev \
     libpng-dev \
     libjpeg-dev \
     libtiff-dev \
     libglu1-mesa-dev \
     libopencv-dev \
     libnanoflann-dev \
     python3.10-dev \
     python3.10-venv \
     python3-pip \
     meshlab

# Install CMake (v3.28.3)
sudo cp "$VKIST_3D/libs/cmake-3.28.3-linux-x86_64.sh" /opt/
cd /opt/
sudo chmod +x /opt/cmake-3.28.3-linux-x86_64.sh
sudo bash /opt/cmake-3.28.3-linux-x86_64.sh  # Press q then y to accept (path: /opt/cmake-3.28.3-...)
sudo ln -s /opt/cmake-3.28.3-linux-x86_64/bin/* /usr/local/bin

# Move back to libraries folder
cd "$VKIST_3D/libs"

# Install OpenMVS (v2.3.0)

# Eigen (v3.4.90)
git clone https://gitlab.com/libeigen/eigen.git
mkdir -p "$VKIST_3D/libs/eigen_build" && cd "$VKIST_3D/libs/eigen_build"
cmake ../eigen
make -j$(nproc) && sudo make install
cd "$VKIST_3D/libs"

# VCGLib
git clone https://github.com/cdcseacave/VCG.git vcglib

# OpenMVS (v2.3.0)
git clone --branch v2.3.0 --depth 1 https://github.com/cdcseacave/openMVS.git openMVS
mkdir -p "$VKIST_3D/libs/openMVS_build" && cd "$VKIST_3D/libs/openMVS_build"
cmake ../openMVS -DCMAKE_BUILD_TYPE=Release -DCMAKE_CUDA_ARCHITECTURES=native -DVCG_ROOT="../vcglib"
make -j$(nproc) && sudo make install
sudo ln -s /usr/local/bin/OpenMVS/* /usr/local/bin
cd "$VKIST_3D/libs"

echo "System dependencies and OpenMVS installed successfully."
echo "Now run setup_env.sh to create the Conda environment."
