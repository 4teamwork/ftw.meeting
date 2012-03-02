"""
Extends the DatagridWidget with an additional attribute for
the "select all" function

New attr: select_all_column

"""

from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget
from Products.DataGridField import DataGridWidget


class DataGridWidgetExtended(DataGridWidget):
    """
    This is the extended DataGridWidget
    """

    _properties = TypesWidget._properties.copy()
    _properties.update({
            'macro': "datagridwidgetextended",
            'helper_css': ('datagridwidget.css',),
            'helper_js': ('datagridwidgetextended.js',),
            'show_header': True,
            'auto_insert': False,
            'select_all_column': '',  # column for the select all button
            'columns': {},  # Sequence of Column instances
            })


__all__ = ('DataGridWidgetExtended')

registerWidget(DataGridWidget,
               title='Data Grid extended',
               description=('A spreadsheet like table'),
               used_for=('Products.DataGridField.DataGridField',)
               )
