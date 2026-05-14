"""Build the plain (single-column) paper.pdf from paper.md.

pdflatex doesn't speak Unicode without per-symbol macros, and lualatex
is missing luaotfload in this image. We pre-process paper.md to:

  - replace Unicode in prose with TeX math-mode equivalents
    (μ → $\mu$, → → $\rightarrow$, Σ → $\Sigma$, ...)
  - replace Unicode in code spans/blocks with ASCII transliterations
    (μ → mu, σ → sigma, Σ → Sum, → → ->, ...) so pdflatex's verbatim
    and \texttt environments can render them

then hand off to pandoc + pdflatex.

Output: paper.pdf at the repo root.
"""
from __future__ import annotations
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'paper.md'
TMP_MD = ROOT / 'paper.normalized.md'
OUT = ROOT / 'paper.pdf'

# Substitutions for prose. Use raw-TeX `\(...\)` math instead of `$...$`
# because pandoc's tex_math_dollars heuristics drop the dollars around
# bare macros like `$\approx$` next to punctuation (caption text, etc.).
def _m(tex: str) -> str:
    return r'\(' + tex + r'\)'


PROSE_MAP = {
    '→': _m(r'\rightarrow'),
    '←': _m(r'\leftarrow'),
    '↔': _m(r'\leftrightarrow'),
    '×': _m(r'\times'),
    '≤': _m(r'\le'),
    '≥': _m(r'\ge'),
    '±': _m(r'\pm'),
    '—': '---',
    '–': '--',
    '−': _m('-'),
    '‘': "`",
    '’': "'",
    '“': "``",
    '”': "''",
    '…': r'\ldots ',
    '·': _m(r'\cdot'),
    '≈': _m(r'\approx'),
    'Δ': _m(r'\Delta'),
    '∈': _m(r'\in'),
    'Σ': _m(r'\Sigma'),
    'θ': _m(r'\theta'),
    'α': _m(r'\alpha'),
    'β': _m(r'\beta'),
    'λ': _m(r'\lambda'),
    'ε': _m(r'\epsilon'),
    'μ': _m(r'\mu'),
    'σ': _m(r'\sigma'),
    'ν': _m(r'\nu'),
    'ψ': _m(r'\psi'),
    '′': _m("'"),
    '₀': _m('_0'), '₁': _m('_1'), '₂': _m('_2'), '₃': _m('_3'), '₄': _m('_4'),
    '₅': _m('_5'), '₆': _m('_6'), '₇': _m('_7'), '₈': _m('_8'), '₉': _m('_9'),
    'ₐ': _m('_a'), 'ᵢ': _m('_i'), 'ₖ': _m('_k'),
    'R̂': _m(r'\hat{R}'),
    '̂': '',
    'η': _m(r'\eta'),
    '⁰': _m('^0'), '¹': _m('^1'), '²': _m('^2'), '³': _m('^3'), '⁴': _m('^4'),
    '⁵': _m('^5'), '⁶': _m('^6'), '⁷': _m('^7'), '⁸': _m('^8'), '⁹': _m('^9'),
    '⁻': _m('^-'),
    '∞': _m(r'\infty'),
    '√': _m(r'\surd'),
    'ᵀ': _m('^T'),
    '⁻¹': _m('^{-1}'),
    ' ': ' ',
    '§': r'\S{}',
}

# ASCII fallbacks for code spans / fenced code (no math mode available).
CODE_MAP = {
    '→': '->',
    '←': '<-',
    '↔': '<->',
    '×': 'x',
    '≤': '<=',
    '≥': '>=',
    '±': '+/-',
    '—': '--',
    '–': '-',
    '−': '-',
    '‘': "'",
    '’': "'",
    '“': '"',
    '”': '"',
    '…': '...',
    '·': '*',
    '≈': '~',
    'Δ': 'Delta',
    '∈': ' in ',
    'Σ': 'Sum',
    'θ': 'theta',
    'α': 'alpha',
    'β': 'beta',
    'λ': 'lambda',
    'ε': 'eps',
    'μ': 'mu',
    'σ': 'sigma',
    'ν': 'nu',
    'ψ': 'psi',
    '′': "'",
    '₀': '_0', '₁': '_1', '₂': '_2', '₃': '_3', '₄': '_4',
    '₅': '_5', '₆': '_6', '₇': '_7', '₈': '_8', '₉': '_9',
    'ₐ': '_a', 'ᵢ': '_i', 'ₖ': '_k',
    'R̂': 'R_hat',
    '̂': '',
    'η': 'eta',
    '⁰': '^0', '¹': '^1', '²': '^2', '³': '^3', '⁴': '^4',
    '⁵': '^5', '⁶': '^6', '⁷': '^7', '⁸': '^8', '⁹': '^9',
    '⁻': '^-',
    '∞': 'inf',
    '√': 'sqrt',
    'ᵀ': '^T',
    '⁻¹': '^-1',
    ' ': ' ',
    '§': 'S',
}


def replace(s: str, table: dict[str, str]) -> str:
    for ch, repl in table.items():
        s = s.replace(ch, repl)
    return s


CODE_RE = re.compile(
    r'(```.*?```)'             # fenced code
    r'|(`[^`\n]+`)'            # inline code
    r'|(!\[[^\]]*\]\([^)]*\))',  # image alt text (pandoc escapes $ inside)
    flags=re.DOTALL,
)


def normalize(src: str) -> str:
    parts = []
    last = 0
    for m in CODE_RE.finditer(src):
        # Prose chunk before this code span.
        parts.append(replace(src[last:m.start()], PROSE_MAP))
        # Code span itself: ASCII transliteration.
        parts.append(replace(m.group(0), CODE_MAP))
        last = m.end()
    parts.append(replace(src[last:], PROSE_MAP))
    out = ''.join(parts)
    # pandoc's tex_math_single_backslash requires a non-letter/non-digit
    # character after `\)`. Source like `≈2.2 σ` becomes `\(\approx\)2.2`
    # which fails to parse. Insert a thin space.
    out = re.sub(r'\\\)([A-Za-z0-9])', r'\\)\\,\1', out)
    return out


def main() -> None:
    src = SRC.read_text()
    TMP_MD.write_text(normalize(src))
    try:
        subprocess.run([
            'pandoc', str(TMP_MD),
            '-o', str(OUT),
            '--from=markdown+tex_math_single_backslash+raw_tex',
            '--pdf-engine=pdflatex',
            '-V', 'geometry:margin=1in',
            '-V', 'linkcolor:blue',
            '-V', 'urlcolor:blue',
            '--resource-path', f'.:{ROOT}:{ROOT / "figures"}',
            '--metadata', 'title=Evolvable Decision Programs',
        ], check=True, cwd=ROOT)
        print(f'OK -> {OUT}')
    finally:
        TMP_MD.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
