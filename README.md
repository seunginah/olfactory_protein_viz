# olfactory_protein_viz
Data Days Summer 2017, collaboration w Professor Arie Mobley from the Department of Neuroscience at Western New England University


# manage environment with conda
1. download conda: https://repo.continuum.io/archive/Anaconda3-5.0.1-MacOSX-x86_64.pkg
2. create virtual environment
   $ conda create --name venv python=3.4 anaconda
3. activate virtual env
   $ source activate venv
3. install stuff into it
   (venv) $ conda

4. to keep requirements.txt updated:
   $ conda list --export > requirements.txt


packages installed:
conda install scikit-image
conda install bokeh
sudo conda install -c bokeh nodejs


#issues
 sudo chmod o+r '/Users/mm40108/anaconda3/envs/venv/lib/python3.4/site-packages/llvmlite-0.15.0-py3.4.egg-info/PKG-INFO'
 sudo chmod o+r '/Users/mm40108/anaconda3/envs/venv/lib/python3.4/site-packages/numba-0.30.1-py3.4-macosx-10.6-x86_64.egg-info/PKG-INFO'
