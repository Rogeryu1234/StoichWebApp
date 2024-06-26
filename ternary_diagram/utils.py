

# I slightly change the code, to make it do not use pyplot.
# Therefore, it can be used in a different thread. 
# (Matplotlib is not thread safe)
# 

from matplotlib.axes._subplots import Axes
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple

def check_ax(ax, fig):
    """check ax

    Parameters
    ----------
    ax : None or Axes object
    fig : figure.Figure
        

    Returns
    -------
    Axes object

    Raises
    ------
    TypeError
        
    """
    if ax is None:
        ax = fig.subplots()
    elif isinstance(ax, Axes):
        ax = ax
    else:
        raise TypeError('`ax` is None or Axes object.\nThis `ax` is ({}).'.format(ax.__class__))
    return ax, fig

def check_2d_vector(vector, scale:bool=True) -> np.ndarray:
    """check 2d vector

    Parameters
    ----------
    vector : array | shape = (n, 3)
        ratio
    scale : bool, optional
        do minmaxscale or not, by default True

    Returns
    -------
    numpy.ndarray | shape = (n, 3)

    Raises
    ------
    ValueError
        when shape is not (n, 3)
    """
    vector = np.array(vector)
    if vector.shape[1] != 3:
        raise ValueError("`vector`'s shape must be (n, 3)")
    if scale:
        vector = vector / np.sum(vector, axis = 1, keepdims = True) # 今回keepdims = Trueは.reshape(-1, 1)と同義
    return vector

def check_1d_vector(vector, scale:bool=True) -> np.ndarray:
    """check 1d vector

    Parameters
    ----------
    vector : [type]
        [description]
    scale : bool, optional
        [description], by default True

    Examples
    --------
    >>> check_1d_vector([1, 2, 3], scale=False)
    array([[1, 2, 3]])

    >>> check_1d_vector([2, 2, 4], scale=True)
    array([[0.25, 0.25, 0.5 ]])

    Returns
    -------
    np.ndarray
        2d array

        shape is (1, 3)
    """
    vector = np.array(vector).ravel()
    if len(vector) == 3:
        return check_2d_vector(np.array([vector]), scale=scale)
    else:
        raise ValueError("`vector`'s length must be 3.")

def three2two(vector) -> Tuple[np.ndarray, np.ndarray]:
    """
    Converted 3D proportions to 2D in order to generate a triangular diagram.

    Parameters
    ----------
    vector : array | shape = (n, 3)
        ratio

    Examples
    --------
    >>> three2two(check_2d_vector([[2, 2, 4]]))
    (array([0.625]), array([0.21650635]))

    Returns
    -------
    numpy.ndarray shape = (n, 2)
    """
    return (2 * vector[:, 2] + vector[:, 0]) / 2, np.sqrt(3) / 2 * vector[:, 0]

def get_label(compound_name:str) -> str:
    """
    Convert the chemical composition to LaTeX notation.

    Parameters
    ----------
    compound_name : str
        A compound name, like 'Li2O'

    Returns
    -------
    str
        Chemical composition converted to LaTeX notation.
    
    Examples
    --------
    >>> get_label('Li2O')
    'Li$_{2}$O'

    >>> get_label('(LiLa)0.5TiO3')
    '(LiLa)$_{0.5}$TiO$_{3}$'

    Raises
    ------
    ValueError
        when `compound_name` is not str.
    """
    if not isinstance(compound_name, str):
        raise ValueError('The `compound_name` must be string.')
    f = '$_{'
    b = '}$'
    N = len(compound_name)
    lst_compound_name = list(compound_name) + ['']   # outputするために変えていく．

    # １文字ずつ取り出して
    i = 0
    while i < N:
        l = compound_name[i] # l: letter
        if l.isdigit():
            j = i + 1
            while j < N + 1:
                try:
                    float(compound_name[i:j])
                except ValueError:
                    break
                else:
                    j += 1
            j -= 1
            lst_compound_name[i] = f + lst_compound_name[i]
            lst_compound_name[j] = b + lst_compound_name[j]
            i = j
        i += 1
    return ''.join(lst_compound_name)

if __name__ == '__main__':
    from doctest import testmod
    testmod(verbose=True)