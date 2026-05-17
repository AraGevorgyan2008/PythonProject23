import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QLineEdit, QDoubleSpinBox,
    QFileDialog, QGroupBox, QGridLayout, QTextEdit, QSplitter
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


x_sym = sp.Symbol('x', real=True)

app = QApplication([])

window = QWidget()
window.setWindowTitle("Մաթեմատիկական Ֆունկցիայի Հաշվիչ")
window.setMinimumSize(800, 750)

main_layout = QVBoxLayout()
main_layout.setSpacing(10)
main_layout.setContentsMargins(20, 20, 20, 20)


title = QLabel("Ֆունկցիայի Հաշվիչ")
title.setFont(QFont("Arial", 15, QFont.Weight.Bold))
title.setAlignment(Qt.AlignmentFlag.AlignCenter)


func_layout = QHBoxLayout()
func_label = QLabel("f(x) =")
func_label.setFont(QFont("Arial", 13))
func_label.setFixedWidth(55)

func_input = QLineEdit()
func_input.setPlaceholderText("օր.՝  x**2 + 3*x - 5  կամ  sin(x)  կամ  sqrt(x)")
func_input.setFont(QFont("Courier New", 12))
func_input.setStyleSheet("padding: 6px; border-radius: 5px; border: 1px solid #aaa;")

func_layout.addWidget(func_label)
func_layout.addWidget(func_input)

func_btn_group = QGroupBox("Ֆունկցիաներ")
func_btn_group.setFont(QFont("Arial", 10))
func_btn_group.setStyleSheet("""
    QGroupBox {
        border: 1px solid #ccc; border-radius: 6px;
        margin-top: 6px; padding-top: 4px;
    }
    QGroupBox::title {
        subcontrol-origin: margin; left: 10px;
        padding: 0 4px; color: #555;
    }
""")

func_btn_layout = QGridLayout()
func_btn_layout.setSpacing(5)
func_btn_layout.setContentsMargins(8, 8, 8, 8)

FUNC_BUTTONS = [
    ("√x",     "sqrt(",   "#388E3C"),
    ("x²",     "**2",     "#1565C0"),
    ("xⁿ",     "**",      "#1565C0"),
    ("|x|",    "Abs(",    "#6A1B9A"),
    ("sin",    "sin(",    "#AD1457"),
    ("cos",    "cos(",    "#AD1457"),
    ("tan",    "tan(",    "#AD1457"),
    ("arcsin", "asin(",   "#C62828"),
    ("arccos", "acos(",   "#C62828"),
    ("arctan", "atan(",   "#C62828"),
    ("ln",     "log(",    "#E65100"),
    ("log₁₀",  "log(",    "#E65100"),
    ("eˣ",     "exp(",    "#00838F"),
    ("π",      "pi",      "#4527A0"),
    ("e",      "E",       "#4527A0"),
    ("( )",    "()",      "#37474F"),
]

def make_func_btn(label, insert_text, color):
    btn = QPushButton(label)
    btn.setFixedHeight(32)
    btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {color}22; color: {color};
            border: 1.5px solid {color}88; border-radius: 5px; padding: 2px 6px;
        }}
        QPushButton:hover  {{ background-color: {color}44; border-color: {color}; }}
        QPushButton:pressed {{ background-color: {color}66; }}
    """)

    def on_click():
        pos     = func_input.cursorPosition()
        current = func_input.text()
        if insert_text == "()":
            selected = func_input.selectedText()
            if selected:
                s, e = func_input.selectionStart(), func_input.selectionEnd()
                func_input.setText(current[:s] + "(" + selected + ")" + current[e:])
                func_input.setCursorPosition(e + 2)
            else:
                func_input.setText(current[:pos] + "()" + current[pos:])
                func_input.setCursorPosition(pos + 1)
        else:
            func_input.setText(current[:pos] + insert_text + current[pos:])
            func_input.setCursorPosition(pos + len(insert_text))
        func_input.setFocus()

    btn.clicked.connect(on_click)
    return btn

COLS = 8
for i, (lbl, code, color) in enumerate(FUNC_BUTTONS):
    r, c = divmod(i, COLS)
    func_btn_layout.addWidget(make_func_btn(lbl, code, color), r, c)
func_btn_group.setLayout(func_btn_layout)


x_layout = QHBoxLayout()

x_label = QLabel("x =")
x_label.setFont(QFont("Arial", 13))
x_label.setFixedWidth(30)

x_input = QDoubleSpinBox()
x_input.setRange(-1_000_000, 1_000_000)
x_input.setValue(0)
x_input.setDecimals(4)
x_input.setFont(QFont("Arial", 12))
x_input.setFixedWidth(130)
x_input.setStyleSheet("padding: 5px;")

def make_btn(text, bg, hov, prs):
    b = QPushButton(text)
    b.setStyleSheet(f"""
        QPushButton {{
            background-color: {bg}; color: white;
            font-size: 13px; padding: 7px 14px;
            border-radius: 6px; border: none;
        }}
        QPushButton:hover   {{ background-color: {hov}; }}
        QPushButton:pressed {{ background-color: {prs}; }}
    """)
    return b

calc_btn       = make_btn("▶  Հաշվել",    "#2196F3", "#1976D2", "#0D47A1")
graph_btn      = make_btn("📈  Գրաֆիկ",   "#9C27B0", "#7B1FA2", "#4A148C")
analyze_btn    = make_btn("🔍  Վերլուծել", "#FF6F00", "#E65100", "#BF360C")
derivative_btn = make_btn("∂  Ածանցյալ",  "#00897B", "#00695C", "#004D40")
save_btn       = make_btn("💾  Պահել",     "#546E7A", "#37474F", "#263238")

for w in [x_label, x_input]:
    x_layout.addWidget(w)
x_layout.addSpacing(8)
for w in [calc_btn, graph_btn, analyze_btn, derivative_btn, save_btn]:
    x_layout.addWidget(w)
x_layout.addStretch()


result_label = QLabel("Արդյունք՝  —")
result_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
result_label.setStyleSheet(
    "QLabel { background-color:#f0f0f0; border-radius:8px; padding:8px; border:1px solid #ddd; }"
)


analysis_box = QTextEdit()
analysis_box.setReadOnly(True)
analysis_box.setFont(QFont("Courier New", 10))
analysis_box.setMaximumHeight(180)
analysis_box.setPlaceholderText("🔍 Վերլուծության արդյունքները կհայտնվեն այստեղ...")
analysis_box.setStyleSheet("""
    QTextEdit {
        background-color: #fafafa;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 6px;
        color: #333;
    }
""")


fig, ax = plt.subplots(figsize=(6, 3.8))
fig.patch.set_facecolor("#fafafa")
canvas = FigureCanvas(fig)
canvas.setMinimumHeight(240)
ax.set_visible(False)


SAFE_NP = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "asin": np.arcsin, "acos": np.arccos, "atan": np.arctan,
    "sqrt": np.sqrt, "log": np.log, "log10": np.log10,
    "exp": np.exp, "Abs": np.abs, "abs": np.abs,
    "pi": np.pi, "E": np.e, "e": np.e,
}


SP_MODULES = ["numpy", {"Abs": np.abs}]

def get_expr():
    return func_input.text().strip()

def set_result(text, style="neutral"):
    STYLES = {
        "success": "background-color:#e8f5e9;border:1px solid #a5d6a7;color:#2e7d32;",
        "error":   "background-color:#ffebee;border:1px solid #ef9a9a;color:#c62828;",
        "info":    "background-color:#f3e5f5;border:1px solid #ce93d8;color:#6a1b9a;",
        "deriv":   "background-color:#e0f2f1;border:1px solid #80cbc4;color:#004d40;",
        "analyze": "background-color:#fff3e0;border:1px solid #ffcc80;color:#e65100;",
        "neutral": "background-color:#f0f0f0;border:1px solid #ddd;color:#333;",
    }
    result_label.setText(text)
    result_label.setStyleSheet(
        "QLabel { border-radius:8px; padding:8px; " + STYLES.get(style, STYLES["neutral"]) + " }"
    )

def to_sympy(expr_str):
    """Ձևափոխիր տողը sympy արտահայտության"""
    local = {
        "x": x_sym, "pi": sp.pi, "E": sp.E, "e": sp.E,
        "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
        "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
        "sqrt": sp.sqrt, "log": sp.log, "exp": sp.exp,
        "Abs": sp.Abs, "abs": sp.Abs,
    }
    return sp.sympify(expr_str, locals=local)


def calculate():
    expr = get_expr()
    if not expr:
        set_result("⚠️  Ֆունկցիա մուտքագրիր", "error"); return
    xv = x_input.value()
    try:
        result = eval(expr, {"__builtins__": {}}, {**SAFE_NP, "x": xv})
        set_result(f"f({xv}) = {result:.6g}", "success")
    except Exception as ex:
        set_result(f"❌  Սխալ՝ {ex}", "error")


def draw_graph():
    expr = get_expr()
    if not expr:
        set_result("⚠️  Ֆունկցիա մուտքագրիր", "error"); return
    try:
        x_vals = np.linspace(-10, 10, 600)
        with np.errstate(all="ignore"):
            y_vals = eval(expr, {"__builtins__": {}}, {**SAFE_NP, "x": x_vals})
        y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)

        ax.set_visible(True); ax.clear()
        ax.plot(x_vals, y_vals, color="#2196F3", linewidth=2, label=f"f(x) = {expr}")
        ax.axhline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.5)
        ax.axvline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.5)
        ax.set_title(f"f(x) = {expr}", fontsize=11)
        ax.set_xlabel("x"); ax.set_ylabel("f(x)")
        ax.grid(True, alpha=0.3); ax.legend(fontsize=9)
        fig.tight_layout(); canvas.draw()
        set_result(f"✅  Գրաֆիկը կառուցվեց", "info")
    except Exception as ex:
        set_result(f"❌  Սխալ գրաֆիկում՝ {ex}", "error")


def analyze():
    expr_str = get_expr()
    if not expr_str:
        set_result("⚠️  Ֆունկցիա մուտքագրիր", "error"); return

    lines = []
    add   = lines.append

    try:
        f = to_sympy(expr_str)
        add(f"🔷 f(x) = {f}\n")


        try:
            domain = sp.calculus.util.continuous_domain(f, x_sym, sp.S.Reals)
            add(f"1️⃣  Որոշման տիրույթ :  {domain}")
        except:
            add("1️⃣  Տիրույթ : հաշվել չստացվեց")


        root_conds = []
        for term in sp.preorder_traversal(f):
            if isinstance(term, sp.Pow):
                base, exp = term.as_base_exp()
                if exp.is_Rational and exp.q % 2 == 0:
                    root_conds.append(f"{base} ≥ 0")
        if root_conds:
            add(f"   ⚠️ Արմատի պայմաններ :  {',  '.join(root_conds)}")


        try:
            rng = sp.calculus.util.function_range(f, x_sym, sp.S.Reals)
            add(f"2️⃣  Արժեքների տիրույթ :  {rng}")
        except:
            add("2️⃣  Արժեքների տիրույթ : հաշվել չստացվեց")


        f_neg = f.subs(x_sym, -x_sym)
        if sp.simplify(f_neg - f) == 0:
            parity = "Զույգ ֆունկցիա  (f(−x) = f(x))"
        elif sp.simplify(f_neg + f) == 0:
            parity = "Կենտ ֆունկցիա  (f(−x) = −f(x))"
        else:
            parity = "Ոչ զույգ, ոչ կենտ"
        add(f"3️⃣  Համաչափություն :  {parity}")


        try:
            period = sp.periodicity(f, x_sym)
            add(f"4️⃣  Պարբերություն :  {period if period else 'Պարբերական չէ'}")
        except:
            add("4️⃣  Պարբերականություն : հաշվել չստացվեց")


        df = sp.diff(f, x_sym)
        add(f"5️⃣  f′(x) =  {sp.simplify(df)}")


        try:
            inc = sp.solve_univariate_inequality(df > 0, x_sym, relational=False)
            dec = sp.solve_univariate_inequality(df < 0, x_sym, relational=False)
            add(f"6️⃣  Աճում է :  {inc}")
            add(f"   Նվազում է :  {dec}")
        except:
            add("6️⃣  Աճ/Նվազում : հաշվել չստացվեց")


        oy = f.subs(x_sym, 0)
        add(f"7️⃣  Oy կտրող (x=0) :  (0,  {oy})")
        try:
            ox_roots = sp.solve(f, x_sym)
            add(f"   Ox կտրող (f=0) :  x = {ox_roots}")
        except:
            add("   Ox կտրող : հաշվել չստացվեց")


        try:
            d2  = sp.diff(df, x_sym)
            crit = sp.solve(df, x_sym)
            add(f"8️⃣  Կրիտիկական կետեր :  {crit}")
            extrema_lines = []
            for c in crit:
                val = f.subs(x_sym, c)
                sec = d2.subs(x_sym, c)
                kind = "min" if sec > 0 else "max" if sec < 0 else "?"
                extrema_lines.append(f"x={c} → f={sp.simplify(val)}  [{kind}]")
            if extrema_lines:
                add("   Extrema :  " + "  |  ".join(extrema_lines))
        except:
            add("8️⃣  Extrema : հաշվել չստացվեց")


        try:
            lim_pos = sp.limit(f, x_sym,  sp.oo)
            lim_neg = sp.limit(f, x_sym, -sp.oo)
            add(f"9️⃣  x→+∞ :  {lim_pos}   |   x→−∞ :  {lim_neg}")
        except:
            add("9️⃣  Սահմաններ : հաշվել չստացվեց")


        if f.has(sp.Abs):
            add("🔟  ⚠️  Մոդուլային ֆունկցիա — piecewise վերլուծություն կարող է պահանջվել")

        add("\n✅  Վերլուծությունն ավարտված է")

    except Exception as ex:
        add(f"❌  Սխալ՝ {ex}")

    analysis_box.setText("\n".join(lines))
    set_result("🔍  Տես վերլուծությունը ստորև", "analyze")


def draw_derivative():
    expr_str = get_expr()
    if not expr_str:
        set_result("⚠️  Ֆունկցիա մուտքագրիր", "error"); return
    xv = x_input.value()
    try:
        f      = to_sympy(expr_str)
        df_sym = sp.diff(f, x_sym)
        df_sim = sp.simplify(df_sym)


        deriv_val = float(df_sym.subs(x_sym, xv).evalf())
        f_val     = float(f.subs(x_sym, xv).evalf())


        f_np  = sp.lambdify(x_sym, f,      SP_MODULES)
        df_np = sp.lambdify(x_sym, df_sym, SP_MODULES)

        x_vals = np.linspace(-10, 10, 600)
        with np.errstate(all="ignore"):
            y_f  = np.where(np.isfinite(f_np(x_vals)),  f_np(x_vals),  np.nan)
            y_df = np.where(np.isfinite(df_np(x_vals)), df_np(x_vals), np.nan)
        tangent = deriv_val * (x_vals - xv) + f_val

        ax.set_visible(True); ax.clear()
        ax.plot(x_vals, y_f,  color="#2196F3", linewidth=2,   label=f"f(x)", alpha=0.85)
        ax.plot(x_vals, y_df, color="#F44336", linewidth=2,   label=f"f′(x) = {df_sim}")
        ax.plot(x_vals, tangent, "--", color="#FF6F00", linewidth=1.5, label=f"Շոշափող x={xv:.3g}")
        ax.scatter([xv], [f_val], color="red", s=70, zorder=5)
        ax.axhline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.4)
        ax.axvline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.4)
        ax.set_title(f"f(x) = {expr_str}   |   f′(x) = {df_sim}", fontsize=10)
        ax.set_xlabel("x"); ax.set_ylabel("y")
        ax.grid(True, alpha=0.3); ax.legend(fontsize=8)
        fig.tight_layout(); canvas.draw()

        set_result(f"∂  f′(x) = {df_sim}   |   f′({xv:.4g}) = {deriv_val:.6g}", "deriv")

    except Exception as ex:
        set_result(f"❌  Ածանցյալի սխալ՝ {ex}", "error")


def save_graph():
    if not ax.get_visible() or not ax.lines:
        set_result("⚠️  Նախ կառուցիր գրաֆիկ", "error"); return
    path, _ = QFileDialog.getSaveFileName(
        window, "Պահել գրաֆիկը", "graph.png",
        "PNG (*.png);;JPEG (*.jpg);;SVG (*.svg);;PDF (*.pdf)"
    )
    if path:
        try:
            fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
            set_result(f"💾  Պահված է՝  {path}", "success")
        except Exception as ex:
            set_result(f"❌  Պահելու սխալ՝ {ex}", "error")


calc_btn.clicked.connect(calculate)
graph_btn.clicked.connect(draw_graph)
analyze_btn.clicked.connect(analyze)
derivative_btn.clicked.connect(draw_derivative)
save_btn.clicked.connect(save_graph)
func_input.returnPressed.connect(calculate)


main_layout.addWidget(title)
main_layout.addLayout(func_layout)
main_layout.addWidget(func_btn_group)
main_layout.addLayout(x_layout)
main_layout.addWidget(result_label)
main_layout.addWidget(analysis_box)
main_layout.addWidget(canvas)

window.setLayout(main_layout)
window.show()
app.exec()