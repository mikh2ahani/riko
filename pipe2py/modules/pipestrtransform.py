# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab
"""
    pipe2py.modules.pipestrtransform
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from functools import partial
from itertools import starmap
from twisted.internet.defer import inlineCallbacks, returnValue, maybeDeferred
from . import (
    get_dispatch_funcs, get_async_dispatch_funcs, get_splits, asyncGetSplits)
from pipe2py.lib import utils
from pipe2py.twisted.utils import asyncStarMap, asyncDispatch


# Common functions
def parse_result(conf, word, _pass):
    transformation = conf._fields[0]
    return word if _pass else getattr(str, transformation)(word)


# Async functions
@inlineCallbacks
def asyncPipeStrtransform(context=None, _INPUT=None, conf=None, **kwargs):
    """A string module that asynchronously splits a string into tokens
    delimited by separators. Loopable.

    Parameters
    ----------
    context : pipe2py.Context object
    _INPUT : twisted Deferred iterable of items or strings
    conf : {
        'capitalize': {'type': 'bool', value': <1>},
        'lower': {'type': 'bool', value': <1>},
        'upper': {'type': 'bool', value': <1>},
        'swapcase': {'type': 'bool', value': <1>},
        'title': {'type': 'bool', value': <1>},
    }

    Returns
    -------
    _OUTPUT : twisted.internet.defer.Deferred generator of tokenized strings
    """
    splits = yield asyncGetSplits(_INPUT, conf, listize=False, **kwargs)
    parsed = yield asyncDispatch(splits, *get_async_dispatch_funcs())
    _OUTPUT = yield asyncStarMap(partial(maybeDeferred, parse_result), parsed)
    returnValue(iter(_OUTPUT))


# Synchronous functions
def pipe_strtransform(context=None, _INPUT=None, conf=None, **kwargs):
    """A string module that splits a string into tokens delimited by
    separators. Loopable.

    Parameters
    ----------
    context : pipe2py.Context object
    _INPUT : iterable of items or strings
    conf : {
        'capitalize': {'type': 'bool', value': <1>},
        'lower': {'type': 'bool', value': <1>},
        'upper': {'type': 'bool', value': <1>},
        'swapcase': {'type': 'bool', value': <1>},
        'title': {'type': 'bool', value': <1>},
    }

    Returns
    -------
    _OUTPUT : generator of tokenized strings
    """
    splits = get_splits(_INPUT, conf, listize=False, **kwargs)
    parsed = utils.dispatch(splits, *get_dispatch_funcs())
    _OUTPUT = starmap(parse_result, parsed)
    return _OUTPUT
