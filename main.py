from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QLineEdit, QDoubleSpinBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

app = QApplication([])

window = QWidget()
window.setWindowTitle("Մաթեմատիկական Ֆունկցիայի Հաշվիչ")
window.setMinimumSize(650, 600)

main_layout = QVBoxLayout()
main_layout.setSpacing(12)
main_layout.setContentsMargins(20, 20, 20, 20)

# --- Վերնագիր ---
title = QLabel("Ֆունկցիայի Հաշվիչ")
title.setFont(QFont("Arial", 15, QFont.Weight.Bold))
title.setAlignment(Qt.AlignmentFlag.AlignCenter)

# --- Ֆունկցիա մուտքագրում ---
func_layout = QHBoxLayout()
func_label = QLabel("f(x) =")
func_label.setFont(QFont("Arial", 13))
func_label.setFixedWidth(55)

func_input = QLineEdit()
func_input.setPlaceholderText("օր.՝  x**2 + 3*x - 5  կամ  sin(x)  կամ  x**3")
func_input.setFont(QFont("Courier New", 12))
func_input.setStyleSheet("padding: 6px; border-radius: 5px; border: 1px solid #aaa;")

func_layout.addWidget(func_label)
func_layout.addWidget(func_input)

# --- x արժեք + կոճակներ ---
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

calc_btn = QPushButton("▶  Հաշվել")
calc_btn.setStyleSheet("""
    QPushButton {
        background-color: #2196F3; color: white;
        font-size: 13px; padding: 7px 18px;
        border-radius: 6px; border: none;
    }
    QPushButton:hover { background-color: #1976D2; }
    QPushButton:pressed { background-color: #0D47A1; }
""")

graph_btn = QPushButton("📈  Գրաֆիկ")
graph_btn.setStyleSheet("""
    QPushButton {
        background-color: #9C27B0; color: white;
        font-size: 13px; padding: 7px 18px;
        border-radius: 6px; border: none;
    }
    QPushButton:hover { background-color: #7B1FA2; }
    QPushButton:pressed { background-color: #4A148C; }
""")

analyze_btn = QPushButton("🔍  Վերլուծել")
analyze_btn.setStyleSheet("""
    QPushButton {
        background-color: #FF6F00; color: white;
        font-size: 13px; padding: 7px 18px;
        border-radius: 6px; border: none;
    }
    QPushButton:hover { background-color: #E65100; }
    QPushButton:pressed { background-color: #BF360C; }
""")

derivative_btn = QPushButton("∂  Ածանցյալ")
derivative_btn.setStyleSheet("""
    QPushButton {
        background-color: #00897B; color: white;
        font-size: 13px; padding: 7px 18px;
        border-radius: 6px; border: none;
    }
    QPushButton:hover { background-color: #00695C; }
    QPushButton:pressed { background-color: #004D40; }
""")

x_layout.addWidget(x_label)
x_layout.addWidget(x_input)
x_layout.addSpacing(10)
x_layout.addWidget(calc_btn)
x_layout.addWidget(graph_btn)
x_layout.addWidget(analyze_btn)
x_layout.addWidget(derivative_btn)
x_layout.addStretch()

# --- Արդյունք ---
result_label = QLabel("Արդյունք՝  —")
result_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
result_label.setStyleSheet("""
    QLabel {
        background-color: #f0f0f0; border-radius: 8px;
        padding: 10px; border: 1px solid #ddd;
    }
""")

# --- Matplotlib Canvas ---
fig, ax = plt.subplots(figsize=(6, 4))
fig.patch.set_facecolor("#fafafa")
canvas = FigureCanvas(fig)
canvas.setMinimumHeight(280)
ax.set_visible(False)

# --- Safe ֆունկցիաներ ---
SAFE_FUNCS = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "sqrt": np.sqrt, "log": np.log, "log10": np.log10,
    "exp": np.exp, "abs": np.abs, "pi": np.pi, "e": np.e,
}

def get_expr():
    return func_input.text().strip()

def calculate():
    expr = get_expr()
    if not expr:
        result_label.setText("⚠️  Ֆունկցիա մուտքագրիր")
        return
    x = x_input.value()
    try:
        result = eval(expr, {"__builtins__": {}}, {**SAFE_FUNCS, "x": x})
        result_label.setText(f"f({x}) = {result:.6g}")
        result_label.setStyleSheet("""
            QLabel { background-color: #e8f5e9; border-radius: 8px;
                     padding: 10px; border: 1px solid #a5d6a7; color: #2e7d32; }
        """)
    except Exception as e:
        result_label.setText(f"❌  Սխալ՝ {e}")
        result_label.setStyleSheet("""
            QLabel { background-color: #ffebee; border-radius: 8px;
                     padding: 10px; border: 1px solid #ef9a9a; color: #c62828; }
        """)

def draw_graph():
    expr = get_expr()
    if not expr:
        result_label.setText("⚠️  Ֆունկցիա մուտքագրիր")
        return
    try:
        x_vals = np.linspace(-10, 10, 500)
        y_vals = eval(expr, {"__builtins__": {}}, {**SAFE_FUNCS, "x": x_vals})
        ax.set_visible(True)
        ax.clear()
        ax.plot(x_vals, y_vals, color="#2196F3", linewidth=2)
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_title(f"f(x) = {expr}", fontsize=11)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        canvas.draw()
        result_label.setText(f"✅  Գրաֆիկը կառուցվեց  |  f(x) = {expr}")
        result_label.setStyleSheet("""
            QLabel { background-color: #f3e5f5; border-radius: 8px;
                     padding: 10px; border: 1px solid #ce93d8; color: #6a1b9a; }
        """)
    except Exception as e:
        result_label.setText(f"❌  Սխալ գրաֆիկում՝ {e}")


# ╔══════════════════════════════════════════════════════╗
# ║         ԱՅՍ ՖՈՒՆԿՑԻԱՆ ԴՈՒ ԿԸ ԼՐԱՑՆԵՍ             ║
# ╠══════════════════════════════════════════════════════╣
# ║  get_expr()       → մուտքագրած արտահայտությունը    ║
# ║  x_input.value()  → x-ի արժեքը                     ║
# ║  result_label.setText(...)  → ցուցադրիր արդյունքը  ║
# ║  canvas.draw()    → թարմացրու գրաֆիկը              ║
# ╚══════════════════════════════════════════════════════╝
def analyze():
    expr = get_expr()
    x = x_input.value()

    # ➡️ Այստեղ գրիր քո լոգիկան
    pass


# ╔══════════════════════════════════════════════════════╗
# ║      ԱՅՍ ՖՈՒՆԿՑԻԱՆ ԴՈՒ ԿԸ ԼՐԱՑՆԵՍ                ║
# ╠══════════════════════════════════════════════════════╣
# ║  get_expr()       → մուտքագրած արտահայտությունը    ║
# ║  x_input.value()  → x-ի արժեքը                     ║
# ║  result_label.setText(...)  → ցուցադրիր արդյունքը  ║
# ║  ax, fig, canvas  → գրաֆիկի օբյեկտներ              ║
# ╚══════════════════════════════════════════════════════╝
def draw_derivative():
    expr = get_expr()
    x = x_input.value()

    if not expr:
        result_label.setText("⚠️  Ֆունկցիա մուտքագրիր")
        return

    try:
        h = 1e-5

        f_x_plus = eval(
            expr,
            {"__builtins__": {}},
            {**SAFE_FUNCS, "x": x + h}
        )

        f_x_minus = eval(
            expr,
            {"__builtins__": {}},
            {**SAFE_FUNCS, "x": x - h}
        )

        derivative = (f_x_plus - f_x_minus) / (2 * h)

        # --- Գրաֆիկ ---
        x_vals = np.linspace(-10, 10, 500)
        y_vals = eval(
            expr,
            {"__builtins__": {}},
            {**SAFE_FUNCS, "x": x_vals}
        )

        ax.set_visible(True)
        ax.clear()

        # Հիմնական ֆունկցիա
        ax.plot(
            x_vals,
            y_vals,
            label="f(x)",
            color="#2196F3",
            linewidth=2
        )

        # Հպման կետ
        y0 = eval(
            expr,
            {"__builtins__": {}},
            {**SAFE_FUNCS, "x": x}
        )

        ax.scatter(
            [x],
            [y0],
            color="red",
            s=70,
            zorder=5
        )

        # Շոշափող գիծ
        tangent = derivative * (x_vals - x) + y0

        ax.plot(
            x_vals,
            tangent,
            "--",
            color="#FF6F00",
            linewidth=2,
            label="Շոշափող"
        )

        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")

        ax.set_title(f"Ածանցյալ  |  f(x) = {expr}", fontsize=11)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True, alpha=0.3)
        ax.legend()

        fig.tight_layout()
        canvas.draw()

        # --- Արդյունք ---
        result_label.setText(
            f"∂  f'({x}) = {derivative:.6g}"
        )

        result_label.setStyleSheet("""
            QLabel {
                background-color: #e0f2f1;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #80cbc4;
                color: #004d40;
            }
        """)

    except Exception as e:
        result_label.setText(f"❌  Ածանցյալի սխալ՝ {e}")

        result_label.setStyleSheet("""
            QLabel {
                background-color: #ffebee;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #ef9a9a;
                color: #c62828;
            }
        """)


analyze_btn.clicked.connect(analyze)
derivative_btn.clicked.connect(draw_derivative)
calc_btn.clicked.connect(calculate)
graph_btn.clicked.connect(draw_graph)
func_input.returnPressed.connect(calculate)

# --- Layout ---
main_layout.addWidget(title)
main_layout.addLayout(func_layout)
main_layout.addLayout(x_layout)
main_layout.addWidget(result_label)
main_layout.addWidget(canvas)

window.setLayout(main_layout)
window.show()

app.exec()