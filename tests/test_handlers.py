# File Handler Unit Tests
# -----------------------

import sys

sys.path.append("handlers")

import request_handler as rh
import file_handler as fh
import azureml_handler as ah


FILE_INPUT = "./tests/hello-world.txt"

CONDA_INPUT = "./tests/conda-files/inputs/hello-world.yml"
CONDA_OUTPUT = "./tests/conda-files/outputs/hello-world.yml"

NOTEBOOK_INPUT = "./tests/notebooks/inputs/hello-world.ipynb"
NOTEBOOK_OUTPUT = "./tests/notebooks/outputs/hello-world.ipynb"

def test_get_file_str():

    assert fh.set_file_str(FILE_INPUT, "hello world")
    assert fh.get_file_str(FILE_INPUT) == "hello world"


def test_inject_pip_dependency():

    assert fh.inject_pip_dependency(fh.get_file_str(CONDA_INPUT), "test-pip-dependency") == fh.get_file_str(CONDA_OUTPUT)


def test_inject_notebook_try_catches():

    assert fh.inject_notebook_try_catches(fh.get_file_str(NOTEBOOK_INPUT)) == fh.get_file_str(NOTEBOOK_OUTPUT)


def test_inject_notebook_params(): 

    assert True