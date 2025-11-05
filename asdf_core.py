#!/usr/bin/env python3
# Auto-generated on 2025-11-04T23:49:43
# Source: asdf-equations.tex
# NOTE: This file is standalone; it reconstructs SymPy expressions from srepr strings.
from __future__ import annotations
from typing import Dict, List
import sympy as sp

__all__ = ["asdf_Core"]

class asdf_Core:
    """Callable symbolic core equations.

    Access:
      - tags() -> List[str]
      - residual(tag: str, i: int, **subs) -> sp.Expr
      - symbols(tag: str, i: int) -> List[sp.Symbol]
      - eq_all(tag: str) -> List[sp.Expr]
      - Convenience per-line methods: eq_<tag>_<i>(**subs)
    """

    _SREPR: Dict[str, List[str]] = {
        '1.10': [
            "Add(Mul(Integer(-1), Symbol('C_p'), Add(Symbol('T_i'), Mul(Integer(-1), Symbol('T_x')))), Mul(Pow(Mul(Integer(2), Symbol('J'), Symbol('g')), Integer(-1)), Add(Mul(Integer(-1), Pow(Symbol('v_i'), Integer(2))), Pow(Symbol('v_x'), Integer(2)))))",
        ],
        '1.11': [
            "Add(Mul(Integer(-1), Pow(Mul(Integer(144), Symbol('V_x')), Integer(-1)), Mul(Symbol('A_x'), Symbol('v_x'))), Mul(Pow(Mul(Integer(144), Symbol('V_i')), Integer(-1)), Mul(Symbol('A_i'), Symbol('v_i'))))",
        ],
        '1.12': [
            "Add(Mul(Pow(Symbol('V_i'), Symbol('gamma')), Symbol('p_i')), Mul(Integer(-1), Pow(Symbol('V_x'), Symbol('gamma')), Symbol('p_x')))",
        ],
        '1.14': [
            "Add(Mul(Symbol('p_{cinj}'), Pow(Symbol('p_{cns}'), Integer(-1))), Mul(Integer(-1), Add(Mul(Pow(Symbol('M_i'), Integer(2)), Symbol('gamma')), Integer(1)), Pow(Pow(Add(Mul(Pow(Integer(2), Integer(-1)), Pow(Symbol('M_i'), Integer(2)), Add(Symbol('gamma'), Integer(-1))), Integer(1)), Mul(Symbol('gamma'), Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1)))), Integer(-1))))",
        ],
        '1.15': [
            "Add(Mul(Integer(-1), Pow(Symbol('M_i'), Integer(2)), Symbol('gamma')), Integer(-1), Mul(Pow(Symbol('p_i'), Integer(-1)), Symbol('p_{inj}')))",
        ],
        '1.16': [
            "Add(Mul(Symbol('p_t'), Pow(Symbol('p_{cns}'), Integer(-1))), Mul(Integer(-1), Pow(Mul(Integer(2), Pow(Add(Symbol('gamma'), Integer(1)), Integer(-1))), Mul(Symbol('gamma'), Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1))))))",
        ],
        '1.17': [
            "Add(Symbol('v_e'), Mul(Integer(-1), Pow(Add(Mul(Symbol('R'), Symbol('T_i'), Mul(Integer(2), Symbol('g'), Symbol('gamma')), Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1)), Pow(Add(Mul(Integer(-1), Symbol('p_e'), Pow(Symbol('p_i'), Integer(-1))), Integer(1)), Mul(Pow(Symbol('gamma'), Integer(-1)), Add(Symbol('gamma'), Integer(-1))))), Pow(Symbol('v_i'), Integer(2))), Rational(1, 2))))",
        ],
        '1.18': [
            "Add(Symbol('v_e'), Mul(Integer(-1), Pow(Mul(Integer(2), Symbol('R'), Symbol('T_{cns}'), Symbol('g'), Symbol('gamma'), Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1)), Pow(Add(Mul(Integer(-1), Symbol('p_e'), Pow(Symbol('p_{cns}'), Integer(-1))), Integer(1)), Mul(Pow(Symbol('gamma'), Integer(-1)), Add(Symbol('gamma'), Integer(-1))))), Rational(1, 2))))",
        ],
        '1.19': [
            "Add(Mul(Integer(-1), Symbol('A_t'), Symbol('p_{cns}'), Pow(Mul(Pow(Mul(Symbol('R'), Symbol('T_{cns}')), Integer(-1)), Mul(Symbol('g'), Symbol('gamma'), Pow(Mul(Integer(2), Pow(Add(Symbol('gamma'), Integer(1)), Integer(-1))), Mul(Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1)), Add(Symbol('gamma'), Integer(1)))))), Rational(1, 2))), Symbol('Wdot'))",
        ],
        '1.20': [
            "Add(Mul(Symbol('A_e'), Pow(Symbol('A_t'), Integer(-1))), Mul(Integer(-1), Mul(Pow(Mul(Integer(2), Pow(Add(Symbol('gamma'), Integer(1)), Integer(-1))), Mul(Integer(1), Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1)))), Pow(Mul(Pow(Symbol('p_e'), Integer(-1)), Symbol('p_{cns}')), Mul(Integer(1), Pow(Symbol('gamma'), Integer(-1))))), Pow(Pow(Mul(Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1)), Add(Symbol('gamma'), Integer(1)), Pow(Add(Mul(Integer(-1), Symbol('p_e'), Pow(Symbol('p_{cns}'), Integer(-1))), Integer(1)), Mul(Pow(Symbol('gamma'), Integer(-1)), Add(Symbol('gamma'), Integer(-1))))), Rational(1, 2)), Integer(-1))))",
        ],
        '1.21': [
            "Add(Symbol('p_t'), Mul(Integer(-1), Symbol('p_{cns}'), Pow(Mul(Integer(2), Pow(Add(Symbol('gamma'), Integer(1)), Integer(-1))), Mul(Symbol('gamma'), Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1))))))",
        ],
        '1.22': [
            "Add(Symbol('v_t'), Mul(Integer(-1), Pow(Mul(Integer(2), Symbol('R'), Symbol('T_{cns}'), Symbol('g'), Symbol('gamma'), Pow(Add(Symbol('gamma'), Integer(1)), Integer(-1))), Rational(1, 2))))",
        ],
        '1.24': [
            "Add(Mul(Integer(-1), Pow(Symbol('M_x'), Integer(-1)), Pow(Mul(Integer(2), Pow(Add(Symbol('gamma'), Integer(1)), Integer(-1)), Add(Mul(Pow(Integer(2), Integer(-1)), Pow(Symbol('M_x'), Integer(2)), Add(Symbol('gamma'), Integer(-1))), Integer(1))), Mul(Pow(Mul(Integer(2), Add(Symbol('gamma'), Integer(-1))), Integer(-1)), Add(Symbol('gamma'), Integer(1))))), Mul(Pow(Symbol('A_t'), Integer(-1)), Symbol('A_x')))",
        ],
        '1.25': [
            "Add(Mul(Integer(-1), Mul(Pow(Mul(Integer(2), Pow(Add(Symbol('gamma'), Integer(1)), Integer(-1))), Mul(Integer(1), Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1)))), Pow(Mul(Pow(Symbol('p_x'), Integer(-1)), Symbol('p_{cns}')), Mul(Integer(1), Pow(Symbol('gamma'), Integer(-1))))), Pow(Pow(Mul(Add(Integer(1), Mul(Integer(-1), Pow(Mul(Symbol('p_x'), Pow(Symbol('p_{cns}'), Integer(-1))), Mul(Pow(Symbol('gamma'), Integer(-1)), Add(Symbol('gamma'), Integer(-1)))))), Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1)), Add(Symbol('gamma'), Integer(1))), Rational(1, 2)), Integer(-1))), Mul(Pow(Symbol('A_t'), Integer(-1)), Symbol('A_x')))",
        ],
        '1.26': [
            "Add(Symbol('v_x'), Mul(Integer(-1), Pow(Mul(Integer(2), Symbol('R'), Symbol('T_{cns}'), Symbol('g'), Symbol('gamma'), Add(Integer(1), Mul(Integer(-1), Pow(Mul(Symbol('p_x'), Pow(Symbol('p_{cns}'), Integer(-1))), Mul(Pow(Symbol('gamma'), Integer(-1)), Add(Symbol('gamma'), Integer(-1)))))), Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1))), Rational(1, 2))))",
        ],
        '1.27': [
            "Add(Mul(Integer(-1), Pow(Mul(Pow(Add(Symbol('gamma'), Integer(-1)), Integer(-1)), Add(Symbol('gamma'), Integer(1)), Pow(Add(Mul(Integer(-1), Symbol('p_x'), Pow(Symbol('p_{cns}'), Integer(-1))), Integer(1)), Mul(Pow(Symbol('gamma'), Integer(-1)), Add(Symbol('gamma'), Integer(-1))))), Rational(1, 2))), Mul(Pow(Symbol('v_t'), Integer(-1)), Symbol('v_x')))",
        ],
        '1.9': [
            "Add(Mul(Integer(-1), Symbol('RT_x')), Mul(Integer(144), Symbol('V_x'), Symbol('p_x')))",
        ],
    }

    _SYMNAMES: Dict[str, List[List[str]]] = {
        '1.10': [['C_p', 'J', 'T_i', 'T_x', 'g', 'v_i', 'v_x']],
        '1.11': [['A_i', 'A_x', 'V_i', 'V_x', 'v_i', 'v_x']],
        '1.12': [['V_i', 'V_x', 'gamma', 'p_i', 'p_x']],
        '1.14': [['M_i', 'gamma', 'p_{cinj}', 'p_{cns}']],
        '1.15': [['M_i', 'gamma', 'p_i', 'p_{inj}']],
        '1.16': [['gamma', 'p_t', 'p_{cns}']],
        '1.17': [['R', 'T_i', 'g', 'gamma', 'p_e', 'p_i', 'v_e', 'v_i']],
        '1.18': [['R', 'T_{cns}', 'g', 'gamma', 'p_e', 'p_{cns}', 'v_e']],
        '1.19': [['A_t', 'R', 'T_{cns}', 'Wdot', 'g', 'gamma', 'p_{cns}']],
        '1.20': [['A_e', 'A_t', 'gamma', 'p_e', 'p_{cns}']],
        '1.21': [['gamma', 'p_t', 'p_{cns}']],
        '1.22': [['R', 'T_{cns}', 'g', 'gamma', 'v_t']],
        '1.24': [['A_t', 'A_x', 'M_x', 'gamma']],
        '1.25': [['A_t', 'A_x', 'gamma', 'p_x', 'p_{cns}']],
        '1.26': [['R', 'T_{cns}', 'g', 'gamma', 'p_x', 'p_{cns}', 'v_x']],
        '1.27': [['gamma', 'p_x', 'p_{cns}', 'v_t', 'v_x']],
        '1.9': [['RT_x', 'V_x', 'p_x']],
    }


    def __init__(self) -> None:
        self._cache: Dict[tuple, sp.Expr] = {}

    def tags(self) -> List[str]:
        return sorted(self._SREPR.keys())

    def _expr(self, tag: str, i: int) -> sp.Expr:
        key = (tag, i)
        if key in self._cache:
            return self._cache[key]
        try:
            s = self._SREPR[tag][i]
        except (KeyError, IndexError) as e:
            raise KeyError(f"Unknown equation index for tag '{tag}' i={i}") from e
        expr = eval(s, {}, vars(sp))   # reconstruct SymPy expr from srepr
        self._cache[key] = expr
        return expr

    def symbols(self, tag: str, i: int) -> List[sp.Symbol]:
        names = self._SYMNAMES.get(tag, [])
        if i < 0 or i >= len(names):
            raise KeyError(f"Unknown equation index for tag '{tag}' i={i}")
        return [sp.Symbol(n) for n in names[i]]

    def residual(self, tag: str, i: int, **subs) -> sp.Expr:
        expr = self._expr(tag, i)
        return expr.subs(subs) if subs else expr

    def eq_all(self, tag: str) -> List[sp.Expr]:
        return [ self._expr(tag, i) for i in range(len(self._SREPR.get(tag, []))) ]

    def eq_t_1_10_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.10, line 0."""
        return self.residual('1.10', 0, **subs)

    def eq_t_1_11_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.11, line 0."""
        return self.residual('1.11', 0, **subs)

    def eq_t_1_12_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.12, line 0."""
        return self.residual('1.12', 0, **subs)

    def eq_t_1_14_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.14, line 0."""
        return self.residual('1.14', 0, **subs)

    def eq_t_1_15_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.15, line 0."""
        return self.residual('1.15', 0, **subs)

    def eq_t_1_16_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.16, line 0."""
        return self.residual('1.16', 0, **subs)

    def eq_t_1_17_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.17, line 0."""
        return self.residual('1.17', 0, **subs)

    def eq_t_1_18_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.18, line 0."""
        return self.residual('1.18', 0, **subs)

    def eq_t_1_19_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.19, line 0."""
        return self.residual('1.19', 0, **subs)

    def eq_t_1_20_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.20, line 0."""
        return self.residual('1.20', 0, **subs)

    def eq_t_1_21_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.21, line 0."""
        return self.residual('1.21', 0, **subs)

    def eq_t_1_22_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.22, line 0."""
        return self.residual('1.22', 0, **subs)

    def eq_t_1_24_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.24, line 0."""
        return self.residual('1.24', 0, **subs)

    def eq_t_1_25_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.25, line 0."""
        return self.residual('1.25', 0, **subs)

    def eq_t_1_26_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.26, line 0."""
        return self.residual('1.26', 0, **subs)

    def eq_t_1_27_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.27, line 0."""
        return self.residual('1.27', 0, **subs)

    def eq_t_1_9_0(self, **subs) -> sp.Expr:
        """Residual for tag 1.9, line 0."""
        return self.residual('1.9', 0, **subs)

if __name__ == "__main__":
    core = asdf_Core()
    print("Tags:", core.tags())
    for t in core.tags():
        print(f"\nTag {t} has", len(core._SREPR[t]), "equation(s).")
        if core._SREPR[t]:
            print(" First residual:", core.residual(t, 0))
