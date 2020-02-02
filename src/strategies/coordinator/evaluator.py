#!/usr/bin/env python
"""
盤面の評価値算出方法
"""

import sys
sys.path.append('../../')

from strategies.common import AbstractEvaluator
from strategies.coordinator import TableScorer, PossibilityScorer, OpeningScorer, WinLoseScorer, NumberScorer


class Evaluator_T(AbstractEvaluator):
    """
    盤面の評価値をTableで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5):
        self.scorer = TableScorer(size, corner, c, a1, a2, b, x, o)  # Tableによる評価値算出

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        return self.scorer.get_score(kwargs['color'], kwargs['board'])


class Evaluator_P(AbstractEvaluator):
    """
    盤面の評価値を配置可能数で算出
    """
    def __init__(self, wp=5):
        self.scorer = PossibilityScorer(wp)  # 配置可能数による評価値算出

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        return self.scorer.get_score(kwargs['possibles_b'], kwargs['possibles_w'])


class Evaluator_O(AbstractEvaluator):
    """
    盤面の評価値を開放度で算出
    """
    def __init__(self, wo=-0.75):
        self.scorer = OpeningScorer(wo)  # 開放度による評価値算出

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        return self.scorer.get_score(kwargs['board'])


class Evaluator_W(AbstractEvaluator):
    """
    盤面の評価値を勝敗で算出
    """
    def __init__(self, ww=10000):
        self.scorer = WinLoseScorer(ww)  # 勝敗による評価値算出

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        return self.scorer.get_score(kwargs['board'], kwargs['possibles_b'], kwargs['possibles_w'])


class Evaluator_N(AbstractEvaluator):
    """
    盤面の評価値を石数で算出
    """
    def __init__(self):
        self.scorer = NumberScorer()  # 石数による評価値算出

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        return self.scorer.get_score(kwargs['board'])


class Evaluator_TP(AbstractEvaluator):
    """
    盤面の評価値をTable+配置可能数で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5, wp=5):
        self.t = Evaluator_T(size,corner, c, a1, a2, b, x, o)
        self.p = Evaluator_P(wp)

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)

        return score_t + score_p


class Evaluator_TPO(AbstractEvaluator):
    """
    盤面の評価値をTable+配置可能数+開放度で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5, wp=5, wo=-0.75):
        self.t = Evaluator_T(size, corner, c, a1, a2, b, x, o)
        self.p = Evaluator_P(wp)
        self.o = Evaluator_O(wo)

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)
        score_o = self.o.evaluate(*args, **kwargs)

        return score_t + score_p + score_o


class Evaluator_NW(AbstractEvaluator):
    """
    盤面の評価値を石数+勝敗で算出
    """
    def __init__(self, ww=10000):
        self.n = Evaluator_N()
        self.w = Evaluator_W(ww)

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_n = self.n.evaluate(*args, **kwargs)

        return score_n


class Evaluator_PW(AbstractEvaluator):
    """
    盤面の評価値を配置可能数+勝敗で算出
    """
    def __init__(self, wp=5, ww=10000):
        self.p = Evaluator_P(wp)
        self.w = Evaluator_W(ww)

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_p = self.p.evaluate(*args, **kwargs)

        return score_p


class Evaluator_TPW(AbstractEvaluator):
    """
    盤面の評価値をTable+配置可能数+勝敗で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5, wp=5, ww=10000):
        self.t = Evaluator_T(size, corner, c, a1, a2, b, x, o)
        self.p = Evaluator_P(wp)
        self.w = Evaluator_W(ww)

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)

        return score_t + score_p


class Evaluator_TPOW(Evaluator_TPO):
    """
    盤面の評価値をTable+配置可能数+開放度+勝敗で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5, wp=5, wo=-0.75, ww=10000):
        self.t = Evaluator_T(size, corner, c, a1, a2, b, x, o)
        self.p = Evaluator_P(wp)
        self.o = Evaluator_O(wo)
        self.w = Evaluator_W(ww)

    def evaluate(self, *args, **kwargs):
        """
        評価値の算出
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)
        score_o = self.o.evaluate(*args, **kwargs)

        return score_t + score_p + score_o


if __name__ == '__main__':
    from board import Board

    board8 = Board(8)
    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 2)
    board8.put_stone('black', 2, 3)
    board8.put_stone('white', 4, 2)
    board8.put_stone('black', 1, 1)
    board8.put_stone('white', 0, 0)

    possibles_b = board8.get_possibles('black', True)
    possibles_w = board8.get_possibles('white', True)

    print(board8)

    #----------------------------------------------------------------
    # Evaluator_T
    evaluator = Evaluator_T()

    score_b = evaluator.evaluate(color='black', board=board8)
    score_w = evaluator.evaluate(color='white', board=board8)
    print('black score', score_b)
    print('white score', score_w)
    assert score_b == -22
    assert score_w == -22

    #----------------------------------------------------------------
    # Evaluator_TP
    evaluator = Evaluator_TP()

    score_b = evaluator.evaluate(color='black', board=board8, possibles_b=possibles_b, possibles_w=possibles_w)
    print('black score', score_b)
    assert score_b == -17

    #----------------------------------------------------------------
    # Evaluator_TPO
    evaluator = Evaluator_TPO()

    score_b = evaluator.evaluate(color='black', board=board8, possibles_b=possibles_b, possibles_w=possibles_w)
    print('black score', score_b)
    assert score_b == -25.25

    #----------------------------------------------------------------
    # Evaluator_TPOW
    evaluator = Evaluator_TPOW()

    score_b = evaluator.evaluate(color='black', board=board8, possibles_b=[], possibles_w=[])
    print('black score', score_b)
    assert score_b == -10006

    score_b = evaluator.evaluate(color='black', board=board8, possibles_b=possibles_b, possibles_w=possibles_w)
    print('black score', score_b)
    assert score_b == -25.25

    #----------------------------------------------------------------
    # Evaluator_PW
    evaluator = Evaluator_PW()

    score = evaluator.evaluate(board=board8, possibles_b=[], possibles_w=[])
    print('score', score)
    assert score == -10006

    score = evaluator.evaluate(board=board8, possibles_b=possibles_b, possibles_w=possibles_w)
    print('score', score)
    assert score == 5
    #----------------------------------------------------------------
    # Evaluator_N
    evaluator = Evaluator_N()

    score_b = evaluator.evaluate(color='black', board=board8, possibles_b=[], possibles_w=[])
    print('black score', score_b)
    assert score_b == -6

    #----------------------------------------------------------------
    # Evaluator_NW
    evaluator = Evaluator_NW()

    score = evaluator.evaluate(board=board8, possibles_b=[], possibles_w=[])
    print('score', score)
    assert score == -10006

    score = evaluator.evaluate(board=board8, possibles_b=possibles_b, possibles_w=possibles_w)
    print('score', score)
    assert score == -6