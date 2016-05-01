wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p /home/travis/miniconda
export PATH="/home/travis/miniconda/bin:$PATH"
#hash -r
#conda config --set always_yes yes --set changeps1 no
conda update --yes conda

