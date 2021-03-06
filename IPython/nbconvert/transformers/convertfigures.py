"""Module containing a transformer that converts outputs in the notebook from 
one format to another.
"""
#-----------------------------------------------------------------------------
# Copyright (c) 2013, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from .base import Transformer
from IPython.utils.traitlets import Unicode

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

class ConvertFiguresTransformer(Transformer):
    """
    Converts all of the outputs in a notebook from one format to another.
    """

    from_format = Unicode(config=True, help='Format the converter accepts')
    to_format = Unicode(config=True, help='Format the converter writes')

    def __init__(self, **kw):
        """
        Public constructor
        """
        super(ConvertFiguresTransformer, self).__init__(**kw)


    def convert_figure(self, data_format, data):
        raise NotImplementedError()


    def transform_cell(self, cell, resources, cell_index):
        """
        Apply a transformation on each cell,
        
        See base.py
        """

        #Loop through all of the datatypes of the outputs in the cell.
        for index, cell_out in enumerate(cell.get('outputs', [])):
            for data_type, data in cell_out.items():

                #Get the name of the file exported by the extract figure 
                #transformer.  Do not try to convert the figure if the extract
                #fig transformer hasn't touched it
                filename = cell_out.get(data_type + '_filename', None)
                if filename:
                    figure_name = filename[:filename.rfind('.')]
                    self._convert_figure(cell_out, figure_name, resources, data_type, data)
        return cell, resources


    def _convert_figure(self, cell_out, resources, figure_name, data_type, data):
        """
        Convert a figure and output the results to the cell output
        """

        if not self.to_format in cell_out:
            if data_type == self.from_format:
                filename = figure_name + '.' + self.to_format
                if filename not in resources['figures']:

                    #On the cell, make the figure available via 
                    #   cell.outputs[i].pdf_filename  ... etc (PDF in example)
                    cell_out[self.to_format + '_filename'] = filename

                    #In the resources, make the figure available via
                    #   resources['figures']['filename'] = data
                    resources['figures'][filename] = self.convert_figure(data_type, data)
