import os
import pyximport
pyximport.install()


SLOW_MODE = True

try:
    if 'FORCE_BITBOARD_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_BITBOARD_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ...strategies.TableMethods.GetScoreFast import get_score
    SLOW_MODE = False
except ImportError:
    from ...strategies.TableMethods.GetScore import get_score


__all__ = [
    'get_score',
]
