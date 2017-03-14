import collections
import yaml
import six
import contextlib


class Cell:
    def __init__(self):
        self.header = []
        self.source = []

with open('test_all.py', encoding='utf-8') as f:

    in_cell, in_cell_source = False, False
    cells, cell = [], Cell()

    for line in f:

        if line.startswith('#%'):

            if not in_cell:
                in_cell = True
            elif not in_cell_source:
                with contextlib.closing(six.StringIO()) as f:
                    f.write(''.join(x.strip('# ') for x in cell.header))
                    f.seek(0)
                    cell.header = yaml.load(f)
                    if 'source' in cell.header:
                        in_cell, in_cell_source = False, False
                        cell.source = cell.header.pop('source')
                        cells.append(cell)
                        cell = Cell()
                    else:
                        in_cell_source = True
            else:
                in_cell, in_cell_source = False, False
                cell.source = ''.join(cell.source)
                cells.append(cell)
                cell = Cell()

        elif in_cell:

            if in_cell_source:
                cell.source.append(line)
            else:
                cell.header.append(line)

    print(cells)