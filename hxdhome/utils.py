"""
Basic utilities for hxdhome
"""
############
# Standard #
############

###############
# Third Party #
###############


##########
# Module #
##########

def columns_per_page(page_width, column_width, spacing):
    """
    Find the number of widgets you can fit horizontally in a given window

    If the width of the column exceeds the page, the value 1 is returned

    Parameters
    ----------
    page_width : int
        Width of overall page

    column_width : int
        Width of each individual column

    spacing : int
        Desired spacing between each column

    Returns
    -------
    columns : int
        Number of columns that can fit on page
    """
    return max((page_width + spacing)//(column_width+spacing), 1)


def columnize(widgets, column_size):
    """
    Split a number of widgets into a list of lists, trying to fill each column
    before moving to the next
    """
    return [widgets[i:i+column_size] for i in range(0,len(widgets),column_size)]

