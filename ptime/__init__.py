from __future__ import print_function, division

from timeit import default_timer
from threading import Thread
from collections import namedtuple

from IPython.core.magic import (Magics, line_cell_magic, magics_class,
                                needs_local_scope)

__version__ = '0.0.1'


def _exec(stmt, glob, local):
    exec(stmt, glob, local)


def time_exec_serial(stmt, glob, local, n):
    start = default_timer()
    for i in range(n):
        exec(stmt, glob, local.copy())
    stop = default_timer()
    return stop - start


def time_exec_parallel(stmt, glob, local, n):
    threads = [Thread(target=_exec, args=(stmt, glob, local.copy()))
               for i in range(n)]
    start = default_timer()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    stop = default_timer()
    return stop - start


class PTimeResult(namedtuple('_PTimeResult',
                             ('serial_total',
                              'parallel_total',
                              'nthreads'))):
    @property
    def percent_speedup(self):
        return 100 / self.speedup

    @property
    def speedup(self):
        return self.serial_total / self.parallel_total

    def __repr__(self):
        return ('Total serial time:   %.2f s\n'
                'Total parallel time: %.2f s\n'
                'For a %.2fX speedup across %d '
                'threads') % (self.serial_total,
                              self.parallel_total,
                              self.speedup,
                              self.nthreads)


@magics_class
class GILProfilerMagic(Magics):
    @needs_local_scope
    @line_cell_magic
    def ptime(self, line='', cell=None, local_ns=None):
        """Measure execution time in serial and parallel and compare.

        Usage, in line mode:
          %ptime [-n<N> -o -q] statement
        Usage, in cell mode:
          %%ptime [-n<N> -o -q] setup_code
          code...
          code...

        This function can be used both as a line and cell magic:

        - In line mode you can measure a single-line statement (though multiple
          ones can be chained with using semicolons).

        - In cell mode, the statement in the first line is used as setup code
          (executed but not measured) and the body of the cell is measured.
          The cell body has access to any variables created in the setup code.

        Options:
        -n<N>: number of threads to use. Default: 2

        -o: Return a PTimeResult object containing ptime run details

        -q: Quiet, do not print result

        Examples
        --------
        ::

            In [1]: import numpy as np

            In [2]: x = np.ones((5000, 10000))

            In [3]: %ptime x + x
            Total serial time:   0.42 s
            Total parallel time: 0.25 s
            For a 1.67X speedup across 2 threads

            In [4]: %%ptime  # Use as a cell magic
            ...: x = np.ones((5000, 10000))
            ...: y = x + x
            ...:
            Total serial time:   0.72 s
            Total parallel time: 0.47 s
            For a 1.54X speedup across 2 threads
        """
        opts, stmt = self.parse_options(line, 'n:oq', posix=False,
                                        strict=False)

        if cell is None:
            setup = ''
        else:
            setup = stmt
            stmt = cell

        nthreads = int(getattr(opts, 'n', 2))
        return_result = 'o' in opts
        quiet = 'q' in opts

        if local_ns:
            local = local_ns.copy()
        else:
            local = {}

        try:
            if setup:
                exec(setup, self.shell.user_ns, local)

            serial = time_exec_serial(stmt, self.shell.user_ns, local,
                                      nthreads)
            parallel = time_exec_parallel(stmt, self.shell.user_ns, local,
                                          nthreads)
        except:
            self.shell.showtraceback()
            return

        result = PTimeResult(serial, parallel, nthreads)

        if not quiet:
            print(result)

        if return_result:
            return result


def load_ipython_extension(ip):
    ip.register_magics(GILProfilerMagic)
