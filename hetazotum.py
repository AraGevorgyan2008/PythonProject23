import sympy as sp
import math
import numpy as np
import matplotlib.pyplot as plt

x = sp.Symbol('x', real=True)

# -------------------------------
# ROOT CONDITION HANDLER
# -------------------------------
def handle_roots(f):
    conditions = []

    for term in sp.preorder_traversal(f):
        if isinstance(term, sp.Pow):
            base, exp = term.as_base_exp()

            # even root (sqrt, 4th root, etc.)
            if exp.is_Rational and exp.q % 2 == 0:
                conditions.append(base >= 0)

    return conditions


# -------------------------------
# MAIN ANALYZER
# -------------------------------
def analyze_function(expr_str):
    f = sp.sympify(expr_str)

    print("\n🔷 FUNCTION:", f)

    # 1. DOMAIN
    domain = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)

    root_conditions = handle_roots(f)
    if root_conditions:
        print("\n⚠️ Արմատային սահմանափակումներ կան")
        print("   Պայմաններ:", root_conditions)

    print("\n1. Որոշման տիրույթ:", domain)

    # 2. RANGE (approx / symbolic if possible)
    try:
        rng = sp.calculus.util.function_range(f, x, sp.S.Reals)
        print("2. Արժեքների տիրույթ:", rng)
    except:
        print("2. Արժեքների տիրույթ: չի հաջողվել ամբողջությամբ գտնել")

    # 3. EVEN / ODD
    f_neg = f.subs(x, -x)

    if sp.simplify(f_neg - f) == 0:
        print("3. Զույգ ֆունկցիա")
    elif sp.simplify(f_neg + f) == 0:
        print("3. Կենտ ֆունկցիա")
    else:
        print("3. Ոչ զույգ, ոչ կենտ")

    # 4. PERIODICITY
    try:
        period = sp.periodicity(f, x)
        print("4. Պարբերական է:", period)
    except:
        print("4. Պարբերական չէ")

    # 5. DERIVATIVE
    df = sp.diff(f, x)
    print("5. Ածանցյալ:", df)

    # 6. SIGN INTERVALS
    try:
        print("6. f > 0:", sp.solve_univariate_inequality(f > 0, x))
        print("   f < 0:", sp.solve_univariate_inequality(f < 0, x))
    except:
        print("6. Աճման և նվազման միջակայքեր: դժվար հաշվարկ")

    # 7. INCREASING / DECREASING
    try:
        inc = sp.solve_univariate_inequality(df > 0, x)
        dec = sp.solve_univariate_inequality(df < 0, x)
        print("7. Increasing:", inc)
        print("   Decreasing:", dec)
    except:
        print("7. Չի հաջողվել")

    # 8. INTERCEPTS
    print("8. Oy intercept:", (0, f.subs(x, 0)))

    try:
        roots = sp.solve(f, x)
        print("   Ox intercepts:", roots)
    except:
        print("   Ox intercepts: չի ստացվել")

    # 9. CRITICAL POINTS + EXTREMA
    df = sp.diff(f, x)
    d2 = sp.diff(df, x)

    try:
        crit = sp.solve(df, x)
        print("9. Critical points:", crit)

        extrema = []

        for c in crit:
            val = f.subs(x, c)
            sec = d2.subs(x, c)

            if sec > 0:
                extrema.append((c, val, "min"))
            elif sec < 0:
                extrema.append((c, val, "max"))
            else:
                extrema.append((c, val, "unknown"))

        print("   Extrema:", extrema)

    except:
        print("9. Extrema չի հաջողվել")

    # 10. MIN / MAX
    try:
        vals = [v for _, v, _ in extrema if v.is_real]

        if vals:
            print("10. Min:", min(vals))
            print("   Max:", max(vals))
    except:
        print("10. Min/Max չի ստացվել")

    # -------------------------------
    # 11. ABS (MODUL) DETECTION
    # -------------------------------
    if f.has(sp.Abs):
        print("\n⚠️ Մոդուլային ֆունկցիա (|x|) հայտնաբերվել է")
        print("👉 Կարող է պահանջել piecewise վերլուծություն")

        break_points = sp.solve(sp.Eq(x, 0), x)
        print("   Break points:", break_points)

    print("\n✅ Վերլուծությունը ավարտված է\n")

#
x = sp.Symbol('x', real=True)

def plot_function(expr_str, xmin=-10, xmax=10):
    f = sp.sympify(expr_str)

    # convert to numpy function
    f_lambdified = sp.lambdify(x, f, "numpy")

    # generate x values
    xs = np.linspace(xmin, xmax, 1000)

    # compute y values safely
    ys = []
    for val in xs:
        try:
            y = f_lambdified(val)
            if np.isfinite(y):
                ys.append(y)
            else:
                ys.append(np.nan)
        except:
            ys.append(np.nan)

    ys = np.array(ys)

    # plot
    plt.figure()
    plt.plot(xs, ys)

    plt.axhline(0)
    plt.axvline(0)

    plt.title(f"Graph of f(x) = {expr_str}")
    plt.xlabel("x")
    plt.ylabel("f(x)")

    plt.grid(True)
    plt.show()


# EXAMPLE
plot_function(abs(x))

# -------------------------------
# TEST
# -------------------------------
analyze_function(x**2)
