"""
Build the ICML-style PDF from paper.md.

Splits paper.md into:
  - paper-abstract.tex  (the abstract, no heading)
  - paper-body.tex      (everything from Section 1 onward)
Pandoc converts both to LaTeX, and pdflatex builds paper-icml.pdf.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
PAPER_DIR = ROOT / 'paper'
MD = PAPER_DIR / 'paper.md'
ABSTRACT_TEX = PAPER_DIR / 'paper-abstract.tex'
BODY_TEX = PAPER_DIR / 'paper-body.tex'
ABSTRACT_MD = PAPER_DIR / 'paper-abstract.md'
BODY_MD = PAPER_DIR / 'paper-body.md'

src = MD.read_text()

# Normalize Unicode that pdflatex T1+inputenc can't handle natively.
# Map to ASCII or LaTeX commands. Applied AFTER pandoc so the LaTeX is
# left untouched by pandoc's escaping.
UNICODE_MAP = {
    '→': r'$\rightarrow$',  # →
    '←': r'$\leftarrow$',
    '↔': r'$\leftrightarrow$',
    '×': r'$\times$',        # ×
    '≤': r'$\le$',
    '≥': r'$\ge$',
    '±': r'$\pm$',
    '—': '---',              # em-dash
    '–': '--',               # en-dash
    '−': '$-$',              # minus sign U+2212
    '‘': "`",                # ‘
    '’': "'",                # ’
    '“': "``",               # “
    '”': "''",               # ”
    '…': r'\ldots ',
    '·': r'$\cdot$',         # ·
    '≈': r'$\approx$',
    'Δ': r'$\Delta$',
    '∈': r'$\in$',
    'Σ': r'$\Sigma$',
    'θ': r'$\theta$',
    'α': r'$\alpha$',
    'β': r'$\beta$',
    'λ': r'$\lambda$',
    'ε': r'$\epsilon$',
    'μ': r'$\mu$',           # μ
    'σ': r'$\sigma$',        # σ
    'ν': r'$\nu$',           # ν
    'ψ': r'$\psi$',
    '′': r"$'$",
    '₀': r'$_0$',
    '₁': r'$_1$',
    '₂': r'$_2$',
    '₃': r'$_3$',
    '₄': r'$_4$',
    '₅': r'$_5$',
    '₆': r'$_6$',
    '₇': r'$_7$',
    '₈': r'$_8$',
    '₉': r'$_9$',
    'ₐ': r'$_a$',
    'ᵢ': r'$_i$',           # ᵢ
    'ₖ': r'$_k$',
    'R̂': r'$\hat{R}$',     # combining-circumflex on R
    '̂': '',                  # bare combining-circumflex (drop)
    'η': r'$\eta$',
    '⁰': r'$^0$',
    '¹': r'$^1$',
    '²': r'$^2$',
    '³': r'$^3$',
    '⁴': r'$^4$',
    '⁵': r'$^5$',
    '⁶': r'$^6$',
    '⁷': r'$^7$',
    '⁸': r'$^8$',
    '⁹': r'$^9$',
    '⁻': r'$^-$',
    '∞': r'$\infty$',
    '√': r'$\surd$',
    'θ': r'$\theta$',
    'ᵀ': r'$^T$',
    '⁻¹': r'$^{-1}$',
    '·': r'$\cdot$',
    '×': r'$\times$',
    '√': r'$\surd$',
    ' ': ' ',                # non-breaking space
}
def normalize_unicode(s):
    for ch, repl in UNICODE_MAP.items():
        s = s.replace(ch, repl)
    return s


# Find the "## Abstract" block and the start of "## 1. Introduction"
m = re.search(r'## Abstract\s*\n(.*?)\n## 1\. Introduction', src, flags=re.DOTALL)
if not m:
    print('Could not parse abstract / body split', file=sys.stderr)
    sys.exit(1)
abstract_md = m.group(1).strip() + '\n'
body_md = src[m.end() - len('## 1. Introduction'):]
# Demote levels: ICML wants Section 1 as section, Subsection 5.1 as subsection
# pandoc default: '## 1. Introduction' -> \section{1. Introduction}
# We want clean numbering, so strip the "1." prefixes.
body_md = re.sub(r'^(##+ )(\d+(?:\.\d+)*[a-z]?)\.?\s+',
                  lambda m: m.group(1), body_md, flags=re.MULTILINE)

ABSTRACT_MD.write_text(abstract_md)
BODY_MD.write_text(body_md)

def pandoc(in_path, out_path):
    subprocess.run([
        'pandoc', str(in_path),
        '--from=markdown',
        '--to=latex',
        '--top-level-division=section',
        '--wrap=preserve',
        '-o', str(out_path),
    ], check=True)


def longtable_to_tabular(tex: str) -> str:
    """
    Replace pandoc's longtable blocks with simple tabular blocks. We count
    columns from the first data row's & separators (not by parsing pandoc's
    \\columnwidth-based spec, which is finicky).
    """
    # Find each longtable block and replace it (handles multi-line spec
    # with brace-matching).
    def find_blocks():
        i = 0
        while True:
            start = tex.find(r'\begin{longtable}', i)
            if start < 0:
                break
            # Skip over optional [...] argument
            cur = start + len(r'\begin{longtable}')
            if cur < len(tex) and tex[cur] == '[':
                close_b = tex.find(']', cur)
                if close_b < 0:
                    break
                cur = close_b + 1
            # Now expect { ... } column spec with brace-counting
            if cur >= len(tex) or tex[cur] != '{':
                break
            depth = 1
            cur += 1
            while cur < len(tex) and depth > 0:
                if tex[cur] == '{':
                    depth += 1
                elif tex[cur] == '}':
                    depth -= 1
                cur += 1
            spec_end = cur
            end_idx = tex.find(r'\end{longtable}', spec_end)
            if end_idx < 0:
                break
            yield (start, end_idx + len(r'\end{longtable}'), spec_end)
            i = end_idx

    blocks = list(find_blocks())
    if not blocks:
        return tex

    out = []
    cursor = 0
    for s, e, spec_end in blocks:
        out.append(tex[cursor:s])
        # strip everything from \begin{longtable} through the column spec
        body = tex[spec_end:e - len(r'\end{longtable}')]
        # remove pandoc longtable scaffolding lines
        body = re.sub(r'\\toprule\\noalign\{\}', '', body)
        body = re.sub(r'\\midrule\\noalign\{\}', '', body)
        body = re.sub(r'\\bottomrule\\noalign\{\}', '', body)
        body = re.sub(r'\\endhead', '', body)
        body = re.sub(r'\\endfirsthead', '', body)
        body = re.sub(r'\\endfoot', '', body)
        body = re.sub(r'\\endlastfoot', '', body)
        body = body.strip()
        # Count columns from the first row that has & ... \\
        first_row = None
        for ln in body.splitlines():
            if r'\\' in ln and '&' in ln:
                first_row = ln
                break
        if first_row is None:
            # single column or weird; default to l
            ncols = 1
        else:
            # count & at top level (ignore those inside braces)
            depth = 0
            cnt = 0
            for ch in first_row.split(r'\\')[0]:
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                elif ch == '&' and depth == 0:
                    cnt += 1
            ncols = cnt + 1
        spec = 'l' + 'r' * (ncols - 1)  # first column left, rest right (paper convention)
        # Wide tables (>4 cols) span both columns via table*; small tables
        # stay inline. Also wrap in resizebox to fit the available width.
        if ncols > 4:
            out.append(r'\begin{table*}[t]' + '\n')
            out.append(r'\centering\small' + '\n')
            out.append(r'\resizebox{\textwidth}{!}{' + '\n')
            out.append(r'\begin{tabular}{' + spec + '}\n')
            out.append(r'\toprule' + '\n')
            out.append(body + '\n')
            out.append(r'\bottomrule' + '\n')
            out.append(r'\end{tabular}}' + '\n')
            out.append(r'\end{table*}' + '\n')
        else:
            out.append(r'\begin{center}\small' + '\n')
            out.append(r'\begin{tabular}{' + spec + '}\n')
            out.append(r'\toprule' + '\n')
            out.append(body + '\n')
            out.append(r'\bottomrule' + '\n')
            out.append(r'\end{tabular}' + '\n')
            out.append(r'\end{center}' + '\n')
        cursor = e
    out.append(tex[cursor:])
    return ''.join(out)


def widen_figures(tex: str) -> str:
    """
    Convert pandoc's \\begin{figure}...\\end{figure} into figure* (both-column
    floats) and force \\includegraphics[width=\\textwidth]{...} so figures
    don't overflow the column.
    """
    tex = tex.replace(r'\begin{figure}', r'\begin{figure*}[t]')
    tex = tex.replace(r'\end{figure}', r'\end{figure*}')
    # Force-set width on bare \includegraphics{...}
    tex = re.sub(r'\\includegraphics\{', r'\\includegraphics[width=\\textwidth]{', tex)
    return tex


pandoc(ABSTRACT_MD, ABSTRACT_TEX)
pandoc(BODY_MD, BODY_TEX)
ABSTRACT_TEX.write_text(normalize_unicode(ABSTRACT_TEX.read_text()))
BODY_TEX.write_text(
    normalize_unicode(widen_figures(longtable_to_tabular(BODY_TEX.read_text())))
)

# pdflatex twice for refs / TOC
for run in range(2):
    print(f'pdflatex run {run+1}...')
    r = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'paper-icml.tex'],
        cwd=str(PAPER_DIR),
        capture_output=True)
    if r.returncode != 0:
        print('pdflatex FAILED. last 60 lines:')
        out = r.stdout.decode('utf-8', errors='replace')
        print('\n'.join(out.splitlines()[-60:]))
        sys.exit(2)
print(f'OK -> {PAPER_DIR / "paper-icml.pdf"}')
