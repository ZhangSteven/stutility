"""
The module aims to provide Excel related functions.
"""
import logging
from functools import partial
from itertools import takewhile
from datetime import datetime, timedelta

from xlrd import open_workbook
from openpyxl import load_workbook
from toolz.functoolz import compose


__all__ = ('get_ymd_date_from_oridinal', 'workbook_to_lines',
           'lines_to_positions', 'workbook_to_positions',
           'xls_workbook_to_lines', 'xls_lines_to_positions'
           'xls_workbook_to_positions')


def get_ymd_date_from_oridinal(ordinal):
    """
    [Float] excel ordinal => [String] date (yyyy-mm-dd)

    In Excel, a date is represented by a float number (ordinal), where the
    integral part represents the date and the decimal part represents the 
    time of that day. This function converts it to a date string.

    This function is useful when we use xlrd to read xls files, the
    cells with Date format will be read as Excel ordinals (float).

    Code sample comes from:
    https://stackoverflow.com/questions/29387137/
        how-to-convert-a-given-ordinal-number-from-excel-to-a-date
    """
    return compose(
        lambda dt: dt.strftime('%Y-%m-%d'),
        lambda ordinal: \
            (datetime(1899, 12, 31)
             + timedelta(days=ordinal)).replace(microsecond=0),
        lambda x: (x - 1) if x > 59 else x
    )(ordinal)


def workbook_to_positions(file, skip_rows=0):
    """
    [String] excel xlsx file,
    [Int] skip rows (number of starting rows to skip)
        => [Iterator] ([Dictionary] position)
    """
    return lines_to_positions(workbook_to_lines(file, skip_rows))


def workbook_to_lines(file, skip_rows=0):
    """
    [String] excel file (xlsx format),
    [Int] skip rows (number of starting rows to skip)
        => [Iterator] ([Tuple] line)

    Open an xlsx workbook and return all lines from its first worksheet.

    For cells that contain formula, only the values will be returned.
    """
    logging.info(f'open file: {file}')
    ws = load_workbook(filename=file, data_only=True).active
    for idx, row in enumerate(ws.values):
        if idx < skip_rows:
            continue
        else:
            yield row


def lines_to_positions(lines):
    """
    [Iterator] ([Tuple] line) => [Iterator] ([Dictionary] position)

    Where the first line is treated as headers, remaining lines are
    data rows.
    """
    try:
        headers = next(lines)
    except StopIteration as exc:
        raise ValueError('lines empty') from exc

    headers = list(takewhile(lambda el: el != None, headers))
    if not headers:
        raise ValueError('headers empty')

    line_to_position = compose(dict, partial(zip, headers))
    return map(
        line_to_position,
        takewhile(
            lambda line: len(line) > 0 and line[0] != None, 
            lines
        )
    )


def xls_workbook_to_positions(file, skip_rows=0):
    """
    [String] excel xlsx file,
    [Int] skip rows (number of starting rows to skip)
        => [Iterator] ([Dictionary] position)
    """
    return xls_lines_to_positions(xls_workbook_to_lines(file, skip_rows))


def xls_workbook_to_lines(file, skip_rows=0):
    """
    [String] excel file (xls format),
    [Int] skip rows (number of starting rows to skip)
        => [Iterator] ([List] line)

    Open an old version xls workbook and return all lines from its first 
    worksheet.

    The optional argument skip_rows specifies number of starting rows
    to skip.
    """
    logging.info(f'open file: {file}')
    ws = open_workbook(file).sheet_by_index(0)
    return map(partial(_xls_row_to_list, ws), range(skip_rows, ws.nrows))


def xls_lines_to_positions(lines):
    """
    [Iterator] lines => [Iterator] ([Dictionary] position)

    Where the first line is treated as headers, remaining lines are
    data rows.
    """
    try:
        headers = next(lines)
    except StopIteration as exc:
        raise ValueError('lines empty') from exc

    not_empty_string = lambda x: not isinstance(x, str) or x.strip() != ''
    headers = list(takewhile(not_empty_string, headers))
    if not headers:
        raise ValueError('headers empty')

    line_to_position = compose(dict, partial(zip, headers))
    return map(
        line_to_position,
        takewhile(
            lambda line: len(line) > 0 and not_empty_string(line[0]), 
            lines
        )
    )


def _xls_row_to_list(ws, row):
    return list(map(
                    lambda col: ws.cell_value(row, col), 
                    range(0, ws.ncols)
                ))