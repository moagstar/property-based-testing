# std
import io
import os
import fnmatch
import logging
import subprocess
# 3rd party
import yaml
import nbformat
from selenium import webdriver


def get_cells_from_files_in_path(path):
    """
    Generate a nbformat.v4 cells from .py files in the given path.

    :param path: The path to search for python files.

    :return: List of nbformat.v4 cells.
    """
    all_file_names = os.scandir('.')
    py_file_names = sorted(fnmatch.filter((x.name for x in all_file_names), '*.py'))
    cells = []
    for file_name in py_file_names:
        logging.debug(file_name)
        file_path = os.path.join(path, file_name)
        cells += [cell_factory(cell_kwargs) for cell_kwargs in get_cells_from_file(file_path)]
    return cells


def cell_factory(cell_kwargs):
    """
    Generate an nbformat.v4 cell from keyword arguments

    :param cell_kwargs: Keyword arguments for generating the cell.

    :return: nbformat.v4 cell
    """
    cell_type = cell_kwargs.pop('cell_type')
    return getattr(nbformat.v4, f'new_{cell_type}_cell')(**cell_kwargs)


def parse_cell_kwargs(source_lines):
    """
    Parses the yaml which defines a cell

    :param source_lines: The lines from the py file which should be parsed.

    :return: dict containing a cell definition.
    """
    with io.StringIO() as f:
        stripped = (x[2:] for x in source_lines) # strip leading # and spacce
        f.write(''.join(stripped))
        f.seek(0)
        return yaml.load(f)


def get_cells_from_file(file_path):
    """
    Parse a python file and generate a list of ipynb cells

    :param file_path:

    :return: A generator which yields the kwargs which can be used to generate an ipynb cell.
    """
    with open(file_path, encoding='utf-8') as f:
        source_lines, cell_kwargs, in_cell = [], {}, False
        for line in f:
            if line.startswith('#%'):
                # start of a cell
                if not in_cell:
                    in_cell = True
                # start of cell definition
                elif not cell_kwargs:
                    cell_kwargs = parse_cell_kwargs(source_lines)
                    if 'source' in cell_kwargs:
                        yield cell_kwargs
                        source_lines, cell_kwargs, in_cell = [], {}, False
                    else:
                        source_lines = []
                # source defined by what follows the header
                else:
                    cell_kwargs['source'] = ''.join(source_lines).strip()
                    yield cell_kwargs
                    source_lines, cell_kwargs, in_cell = [], {}, False
            elif in_cell:
                source_lines.append(line)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    with open('presentation.ipynb', 'w') as f:
        cells = get_cells_from_files_in_path('.')
        notebook = nbformat.v4.new_notebook(cells=cells)
        nbformat.write(notebook, f)

    import time
    from selenium import webdriver
    import furl

    def start_jupyter():
        proc = subprocess.Popen(['jupyter', 'notebook', '--no-browser'], stderr=subprocess.PIPE)
        for out in proc.stderr:
            out = out.decode('ascii')
            for line in out.split('\n'):
                url = line.strip()
                if url.startswith('http://'):
                    return proc, url

    jupyter, url = start_jupyter()

    driver = webdriver.Firefox()
    driver.get(url)
    url = furl.furl(url)
    url = str(url.remove(['token'])) + 'notebooks/presentation.ipynb'
    driver.get(url)
    # TODO : run all
    # TODO : clear output
    # TODO : start RISE
    # TODO : remove menu
    # TODO : full screen

    try:
        while 1: time.sleep(1)
    finally:
        jupyter.kill()
        driver.close()
