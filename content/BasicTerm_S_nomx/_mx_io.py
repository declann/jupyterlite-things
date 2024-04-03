ios = (
{'disc_rate_ann.xlsx': {'type': 'PandasIO', 'file_type': 'excel'},
 'model_point_table.xlsx': {'type': 'PandasIO', 'file_type': 'excel'},
 'mort_table.xlsx': {'type': 'PandasIO', 'file_type': 'excel'}})

iospecs = (
{130832267088880: {'type': 'PandasData',
                   'io': 'disc_rate_ann.xlsx',
                   'kwargs': {'read_args': {'index_col': 0,
                                            'engine': 'openpyxl'},
                              'squeeze': True,
                              'name': 'zero_spot',
                              'sheet': None}},
 130832267285872: {'type': 'PandasData',
                   'io': 'model_point_table.xlsx',
                   'kwargs': {'read_args': {'index_col': 0,
                                            'engine': 'openpyxl'},
                              'squeeze': False,
                              'name': None,
                              'sheet': None}},
 130832251796208: {'type': 'PandasData',
                   'io': 'mort_table.xlsx',
                   'kwargs': {'read_args': {'index_col': 0,
                                            'engine': 'openpyxl'},
                              'squeeze': False,
                              'name': None,
                              'sheet': None}}})
