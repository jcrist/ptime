ptime
=====

A tool for measuring serial and parallel execution, and comparing the results.
Provides an `IPython magic
<http://ipython.readthedocs.io/en/stable/interactive/magics.html>`_ ``%ptime``.
This can be useful for measuring the benefits of parallelizing code, including
measuring the effect of the `Global Interpreter Lock
<https://wiki.python.org/moin/GlobalInterpreterLock>`_ (GIL).

Example
-------

.. code::

    In [1]: %load_ext ptime

    In [2]: import numpy as np

    In [3]: x = np.ones((5000, 10000))

    In [4]: %ptime x + x
    Total serial time:   0.42 s
    Total parallel time: 0.25 s
    For a 1.67X speedup across 2 threads

    In [5]: %ptime -n4 x + x  # use 4 threads
    Total serial time:   0.82 s
    Total parallel time: 0.31 s
    For a 2.60X speedup across 4 threads

    In [6]: res = %ptime -o x + x  # Get the result
    Total serial time:   0.41 s
    Total parallel time: 0.25 s
    For a 1.66X speedup across 2 threads

    In [7]: res.speedup
    Out[7]: 1.6610825669011922

    In [8]: %%ptime  # Use as a cell magic
    ...: x = np.ones((5000, 10000))
    ...: y = x + x
    ...:
    Total serial time:   0.72 s
    Total parallel time: 0.47 s
    For a 1.54X speedup across 2 threads

Install
-------

This package is available via pip:

.. code::

    pip install ptime
