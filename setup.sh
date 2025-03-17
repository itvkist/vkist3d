VKIST_3D=$(pwd)  # Store current directory in VKIST_3D
cd "$VKIST_3D"   # Change to the stored path

#install dependencies for colmap and openMVS
sudo apt-get update -qq && sudo apt-get install -qq
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
     python3-dev \
     meshlab

cd "$VKIST_3D"/libs

#install CMAKE (v3.28.3)
sudo cp ./cmake-3.28.3-linux-x86_64.sh /opt/
cd /opt/
sudo chmod +x /opt/cmake-3.28.3-linux-x86_64.sh
sudo bash /opt/cmake-3.28.3-linux-x86_64.sh #press q then y to accept (path: /opt/cmake-3.28.3-...)
sudo ln -s /opt/cmake-3.28.3-linux-x86_64/bin/* /usr/local/bin

#move back to libraries folder
cd "$VKIST_3D"/libs

######################
#Creat anaconda environment
conda create -n vkist3d python=3.9 #press y then enter

#install colmap (v3.11) using conda (recommend)
conda activate vkist3d
conda install conda-forge::colmap

#Deactivate anaconda before continuing
conda deactivate

#install colmap (v3.10/v3.9) (if not install using conda - ONLY PICK ONE TYPE)
# git clone https://github.com/colmap/colmap.git
# cd colmap
# mkdir build && cd build
# cmake .. -GNinja DCMAKE_CUDA_ARCHITECTURES=native
# ninja -j4 && sudo ninja install
# cd "$VKIST_3D"/libs

#install openMVS (v2.3.0)

#Eigen (v3.4.90)
git clone https://gitlab.com/libeigen/eigen.git
mkdir eigen_build && cd eigen_build
cmake ../eigen
make && sudo make install
cd "$VKIST_3D"/libs

#VCGLib
git clone https://github.com/cdcseacave/VCG.git vcglib

#openMVS (v2.3.0)
git clone -b master --single-branch https://github.com/cdcseacave/openMVS.git openMVS
mkdir openMVS_build && cd openMVS_build
cmake ../openMVS -DCMAKE_BUILD_TYPE=Release -DVCG_ROOT="../vcglib"
# cmake ../openMVS -DCMAKE_BUILD_TYPE=Release -DVCG_ROOT="../vcglib" -DCGAL_DIR="/usr/include/CGAL"
make -j4 && sudo make install
sudo ln -s /usr/local/bin/OpenMVS/* /usr/local/bin
cd "$VKIST_3D"/libs


#install nodejs and npm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh
source ~/.bashrc
nvm install v14.10.0

#move back to main project
cd "$VKIST_3D"
