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