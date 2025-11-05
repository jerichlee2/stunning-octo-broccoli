#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
import os
import re
from typing import Dict, List, Optional, Union

import sympy as sp
from sympy.parsing.latex import parse_latex as _sympy_parse_latex  # fallback

# --------------------------------------------------------------------------------------
# Parser with normalization, logging, and fallback
# --------------------------------------------------------------------------------------

_SPACING_CMDS = r'(?:\\,|\\!|\\;|\\:|\\quad|\\qquad)'

_SUB_BARE = re.compile(r'_(?!\{)([A-Za-z0-9])')     # x_i  -> x_{i}
_EXP_BARE = re.compile(r'\^([A-Za-z0-9])')          # M^2  -> M^{2}
_BRACK_GROUP = re.compile(r'\[([^\[\]]+)\]')        # [ ... ] -> ( ... )

def _balanced(s: str) -> bool:
    st: List[str] = []
    for ch in s:
        if ch == '{':
            st.append(ch)
        elif ch == '}':
            if not st:
                return False
            st.pop()
    return not st

def _normalize_text_subscripts(s: str) -> str:
    # (BASE)_{\text{ns}} -> BASE_{ns}
    s = re.sub(
        r'\(\s*([A-Za-z\\]+(?:_\{[^}]+\})?)\s*\)_\{\\text\{([^}]+)\}\}',
        r'\1_{\2}', s
    )
    # (BASE)_{ns} -> BASE_{ns}
    s = re.sub(
        r'\(\s*([A-Za-z\\]+(?:_\{[^}]+\})?)\s*\)_\{([^}]+)\}',
        r'\1_{\2}', s
    )
    # X_{\text{inj}}  -> X_{inj}
    s = re.sub(r'_\{\\text\{([^}]+)\}\}', r'_{\1}', s)
    # X_{\mathrm{inj}} -> X_{inj}
    s = re.sub(r'_\{\\mathrm\{([^}]+)\}\}', r'_{\1}', s)
    # _{a,b} -> _{a_b}
    while True:
        s2 = re.sub(r'_\{([^{}]+),\s*([^{}]+)\}', r'_{\1_\2}', s)
        if s2 == s:
            break
        s = s2
    return s

def _normalize_dots(s: str) -> str:
    # \dot{W} -> Wdot ; \dot{p_c} -> p_cdot
    return re.sub(
        r'\\dot\{([A-Za-z](?:_[A-Za-z0-9]+|\_\{[^}]+\})?)\}',
        r'\1dot', s
    )

def _normalize_for_parsers(s: str) -> str:
    # strip thin/space commands
    s = re.sub(_SPACING_CMDS, '', s)
    # strip \left \right
    s = re.sub(r'\\left\s*', '', s)
    s = re.sub(r'\\right\s*', '', s)
    # remove alignment tabs
    s = s.replace('&', '')
    # friendlier subscripts and dotted symbols
    s = _normalize_text_subscripts(s)
    s = _normalize_dots(s)
    # brace bare subscripts/exponents
    s = _SUB_BARE.sub(r'_{\1}', s)
    s = _EXP_BARE.sub(r'^{\1}', s)
    # treat [ ... ] as grouping if present
    s = _BRACK_GROUP.sub(r'(\1)', s)
    # collapse whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# lazy primary parser (latex2sympy2 if available)
def _primary_parse(s: str) -> sp.Expr:
    import latex2sympy2 as l2s  # type: ignore
    return l2s.latex2sympy(s)

# --- Fast-path tokenization for simple cases (avoid latex parsers) --------------------

_SIMPLE_NAME_RE = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')

def _latex_name_to_symbol(s: str) -> Optional[sp.Symbol]:
    """
    Convert very simple LaTeX identifiers to a single SymPy Symbol
    WITHOUT invoking latex parsers. Returns None if not a simple name.

      Examples admitted:
        Wdot           -> Symbol('Wdot')
        p_{t}          -> Symbol('p_t')
        p_{cns}        -> Symbol('p_cns')
        \\epsilon      -> Symbol('epsilon')
        v_{x}          -> Symbol('v_x')
    """
    s = s.strip()
    # normalize greek: \epsilon -> epsilon
    if s.startswith('\\') and s[1:].isalpha():
        s = s[1:]

    # collapse subscripts {...} -> _...
    s = (s
         .replace('{', '')
         .replace('}', '')
         .replace('\\mathrm', '')
         .replace('\\text', ''))

    # p_c parsed already by your normalizer; ensure spaces removed
    s = re.sub(r'\s+', '', s)

    if _SIMPLE_NAME_RE.match(s):
        return sp.Symbol(s)
    return None

def _fast_path_expr(s: str) -> Optional[sp.Expr]:
    """
    Recognize and build a SymPy expression for a few very common LHS/RHS forms
    without touching latex2sympy2 / SymPy LaTeX parser:

      - simple name
      - ratio: \\frac{name}{name}
      - product of simple names: name*name (rare in your LHS, but cheap to support)
    """
    t = s.strip()

    # Simple name
    sym = _latex_name_to_symbol(t)
    if sym is not None:
        return sym

    # Simple ratio \frac{...}{...}
    m = re.match(r'^\\frac\{([^{}]+)\}\{([^{}]+)\}$', t)
    if m:
        a = _latex_name_to_symbol(m.group(1))
        b = _latex_name_to_symbol(m.group(2))
        if a is not None and b is not None:
            return a / b

    # Parenthesized simple name  ( ... )
    m = re.match(r'^\(\s*([^\(\)]+)\s*\)$', t)
    if m:
        return _fast_path_expr(m.group(1))

    # Very small products like name * name (after our normalizer has removed spaces)
    # Accept forms like A_x / A_t that our ratio rule missed due to spaces
    if '/' in t:
        num, den = t.split('/', 1)
        a = _latex_name_to_symbol(num)
        b = _latex_name_to_symbol(den)
        if a is not None and b is not None:
            return a / b

    return None

def _parse_latex_expr(raw: str) -> sp.Expr:
    """
    Try a fast-path for simple identifiers/ratios first (avoids latex2sympy2 bugs),
    then attempt latex2sympy2, then SymPy's parse_latex.
    """
    s = _normalize_for_parsers(raw)

    # Fast path: handles Wdot, p_t, v_x, \epsilon, A_x/A_t, v_x/v_t, etc.
    fp = _fast_path_expr(s)
    if fp is not None:
        return fp

    if not _balanced(s):
        raise ValueError('Unbalanced braces in LaTeX: ' + s)

    # Prefer latex2sympy2, fall back to SymPy parser
    try:
        return _primary_parse(s)
    except Exception as e_l2s:
        # Show exactly what failed, then try SymPy's parser
        print('\nLATEX2SYMPY FAIL ON:\n>>>', s, '\n<<<', file=sys.stderr)
        try:
            return _sympy_parse_latex(s)
        except Exception as e_sympy:
            # If both fail, raise the SymPy error but include the l2s context
            raise RuntimeError(
                f"LaTeX parse failed for: {s}\n"
                f" latex2sympy2: {type(e_l2s).__name__}: {e_l2s}\n"
                f" sympy.parse_latex: {type(e_sympy).__name__}: {e_sympy}"
            )

# --------------------------------------------------------------------------------------
# Extract \begin{equation}...\tag{...}\end{equation} and optional \begin{aligned}...\end{aligned}
# --------------------------------------------------------------------------------------

_EQN_BLOCK_RE = re.compile(
    r'\\begin\{equation\}(?P<body>.*?)\\tag\{(?P<tag>[^\}]+)\}.*?\\end\{equation\}',
    flags=re.S | re.M
)

_ALIGNED_RE = re.compile(
    r'\\begin\{aligned\}(?P<content>.*?)\\end\{aligned\}',
    flags=re.S | re.M
)

# --------------------------------------------------------------------------------------
# CoreEqs container
# --------------------------------------------------------------------------------------

ExprOrEq = Union[sp.Expr, sp.Eq]

class CoreEqs:
    def __init__(self):
        self.eqs: Dict[str, List[ExprOrEq]] = {}
        self.residuals: Dict[str, List[sp.Expr]] = {}
        self.symbols: Dict[str, List[List[sp.Symbol]]] = {}

    @staticmethod
    def _lines_from_block(body: str) -> List[str]:
        m = _ALIGNED_RE.search(body)
        payload = m.group('content') if m else body
        payload = re.sub(r'\\tag\{[^\}]+\}', '', payload)
        lines = re.split(r'\\\\', payload)
        return [ln.strip() for ln in lines if ln.strip()]

    @staticmethod
    def _to_expr_or_eq(line: str) -> ExprOrEq:
        cleaned = _normalize_for_parsers(line)
        if '=' in cleaned:
            lhs, rhs = cleaned.split('=', 1)
            return sp.Eq(_parse_latex_expr(lhs), _parse_latex_expr(rhs))
        return _parse_latex_expr(cleaned)

    @staticmethod
    def _residual_of(obj: ExprOrEq) -> sp.Expr:
        return obj.lhs - obj.rhs if isinstance(obj, sp.Eq) else sp.sympify(obj)

    @staticmethod
    def _symbols_of(expr: sp.Expr) -> List[sp.Symbol]:
        return sorted(expr.free_symbols, key=lambda s: s.name)

    @classmethod
    def from_tex(cls, tex_path: str) -> 'CoreEqs':
        with open(tex_path, 'r', encoding='utf-8') as f:
            src = f.read()

        out = cls()

        for m in _EQN_BLOCK_RE.finditer(src):
            body = m.group('body')
            tag = m.group('tag').strip()
            lines = cls._lines_from_block(body)

            exprs: List[ExprOrEq] = []
            residuals: List[sp.Expr] = []
            sym_lists: List[List[sp.Symbol]] = []

            for line in lines:
                try:
                    obj = cls._to_expr_or_eq(line)
                except Exception as e:
                    print(f"[core_eqs] Skipping unparsable line for tag {tag!r}: {line!r}", file=sys.stderr)
                    print(f"[core_eqs] Reason: {type(e).__name__}: {e}", file=sys.stderr)
                    continue
                exprs.append(obj)
                rr = cls._residual_of(obj)
                residuals.append(rr)
                sym_lists.append(cls._symbols_of(rr))

            out.eqs[tag] = exprs
            out.residuals[tag] = residuals
            out.symbols[tag] = sym_lists

        return out

    # ---------------- convenience API ----------------

    def tags(self) -> List[str]:
        return sorted(self.eqs.keys())

    def substitute(self, tag: str, subs: dict) -> List[sp.Expr]:
        if tag not in self.residuals:
            raise KeyError(f"Unknown tag {tag!r}. Available: {self.tags()}")
        return [r.subs(subs) for r in self.residuals[tag]]

    def solve_for(self, tag: str, var: Union[sp.Symbol, str], params: Optional[dict] = None):
        if tag not in self.residuals:
            raise KeyError(f"Unknown tag {tag!r}. Available: {self.tags()}")
        var_sym = sp.Symbol(var) if isinstance(var, str) else var
        eqs = self.residuals[tag]
        if params:
            eqs = [e.subs(params) for e in eqs]
        if len(eqs) == 1:
            return sp.solve(sp.Eq(eqs[0], 0), var_sym, dict=True)
        return sp.solve([sp.Eq(e, 0) for e in eqs], [var_sym], dict=True)

# --------------------------------------------------------------------------------------
# CLI utility
# --------------------------------------------------------------------------------------

def _default_equations_path() -> str:
    me = os.path.abspath(__file__)
    stem = os.path.splitext(os.path.basename(me))[0]
    cand = os.path.join(os.path.dirname(me), f'{stem}.tex')
    if os.path.exists(cand):
        return cand
    if stem.endswith('-equations'):
        cand = os.path.join(os.path.dirname(me), f'{stem}.tex')
        if os.path.exists(cand):
            return cand
    raise FileNotFoundError("Could not locate a sibling '*-equations.tex' file.")

def main():
    import argparse
    ap = argparse.ArgumentParser(description='Load core equations into SymPy.')
    ap.add_argument('--tex', default=None, help='Path to *-equations.tex (defaults to sibling)')
    ap.add_argument('--show', action='store_true', help='Pretty-print tags and equations')
    args = ap.parse_args()

    tex = args.tex or _default_equations_path()
    ce = CoreEqs.from_tex(tex)

    print('Loaded tags:', ', '.join(ce.tags()))
    if args.show:
        for tag in ce.tags():
            print(f'\nTag {tag}:')
            for i, (obj, rr, syms) in enumerate(zip(ce.eqs[tag], ce.residuals[tag], ce.symbols[tag])):
                print(f'  [{i}] sympy: {obj!s}')
                print(f'      residual: {rr!s}')
                print(f'      symbols: {[s.name for s in syms]}')

if __name__ == '__main__':
    main()