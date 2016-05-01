wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
#hash -r
#conda config --set always_yes yes --set changeps1 no
conda update --yes conda

conda install --yes python=$TRAVIS_PYTHON_VERSION numpy scipy

