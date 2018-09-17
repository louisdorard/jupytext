import os
import subprocess
import pytest
import mock
import jupytext
from .utils import list_notebooks
from .utils import skip_if_dict_is_not_ordered


@pytest.mark.parametrize('nb_file', list_notebooks())
def test_nbconvert_and_read(nb_file):
    # Load notebook
    nb = jupytext.readf(nb_file)

    # Export to Rmd using jupytext package
    rmd1 = jupytext.writes(nb, ext='.Rmd')

    # Export to Rmd using nbconvert exporter
    rmd_exporter = jupytext.RMarkdownExporter()
    (rmd2, resources) = rmd_exporter.from_notebook_node(nb)

    assert rmd1 == rmd2


@pytest.mark.parametrize('nb_file', list_notebooks('ipynb_py'))
def test_nbconvert_and_read_py(nb_file):
    # Load notebook
    nb = jupytext.readf(nb_file)

    # Export to py using jupytext package
    py1 = jupytext.writes(nb, ext='.py')

    # Export to py using nbconvert exporter
    py_exporter = jupytext.LightPythonExporter()
    (py2, resources) = py_exporter.from_notebook_node(nb)

    assert py1 == py2


@pytest.mark.parametrize('nb_file', list_notebooks('ipynb_julia'))
def test_nbconvert_and_read_julia(nb_file):
    # Load notebook
    nb = jupytext.readf(nb_file)

    # Export to py using jupytext package
    julia = jupytext.writes(nb, ext='.jl')

    # Export to py using nbconvert exporter
    julia_exporter = jupytext.LightJuliaExporter()
    (julia2, resources) = julia_exporter.from_notebook_node(nb)

    assert julia == julia2


@pytest.mark.parametrize('nb_file', list_notebooks('ipynb_R'))
def test_nbconvert_and_read_r(nb_file):
    # Load notebook
    nb = jupytext.readf(nb_file)

    # Export to py using jupytext package
    r1 = jupytext.writes(nb, ext='.R')

    # Export to py using nbconvert exporter
    r_exporter = jupytext.RKnitrSpinExporter()
    (r2, resources) = r_exporter.from_notebook_node(nb)

    assert r1 == r2


pytest.importorskip('jupyter')
pytestmark = skip_if_dict_is_not_ordered


@pytest.mark.parametrize('nb_file', list_notebooks('ipynb_py'))
def test_nbconvert_cmd_line(nb_file, tmpdir):
    rmd_file = str(tmpdir.join('notebook.Rmd'))

    subprocess.call(['jupyter', 'nbconvert', '--to', 'rmarkdown',
                     nb_file, '--output', rmd_file])

    assert os.path.isfile(rmd_file)

    nb = jupytext.readf(nb_file)
    with mock.patch('jupytext.header.INSERT_AND_CHECK_VERSION_NUMBER', True):
        rmd1 = jupytext.writes(nb, ext='.Rmd')
    with open(rmd_file) as fp:
        rmd2 = fp.read()

    assert rmd1 == rmd2


@pytest.mark.parametrize('nb_file', list_notebooks('ipynb_py'))
def test_nbconvert_cmd_line_py(nb_file, tmpdir):
    py_file = str(tmpdir.join('notebook.py'))

    subprocess.call(['jupyter', 'nbconvert', '--to', 'pynotebook',
                     nb_file, '--output', py_file])

    assert os.path.isfile(py_file)

    nb = jupytext.readf(nb_file)
    with mock.patch('jupytext.header.INSERT_AND_CHECK_VERSION_NUMBER', True):
        py1 = jupytext.writes(nb, ext='.py')
    with open(py_file) as fp:
        py2 = fp.read()

    assert py1 == py2


@pytest.mark.parametrize('nb_file', list_notebooks('ipynb_R'))
def test_nbconvert_cmd_line_R(nb_file, tmpdir):
    r_file = str(tmpdir.join('notebook.R'))

    subprocess.call(['jupyter', 'nbconvert', '--to', 'rnotebook',
                     nb_file, '--output', r_file])

    assert os.path.isfile(r_file)

    nb = jupytext.readf(nb_file)
    with mock.patch('jupytext.header.INSERT_AND_CHECK_VERSION_NUMBER', True):
        r = jupytext.writes(nb, ext='.R')
    with open(r_file) as fp:
        r2 = fp.read()

    assert r == r2
