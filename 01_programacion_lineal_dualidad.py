"""
Programación Lineal Continua, Dualidad Fuerte y Precios Sombra (Holgura Complementaria).
Investigación Operativa — Lic. en Ciencias de Datos (Exactas - UBA)
"""

import numpy as np
from scipy.optimize import linprog


def resolver_primal_dual():
    # Problema Primal: Maximizar utilidad de 3 productos con 3 recursos limitados
    # max c^T x  s.a.  A x <= b, x >= 0
    c = np.array([40.0, 30.0, 50.0])
    A = np.array([
        [2.0, 1.0, 3.0],   # Horas de maquinado
        [1.0, 2.0, 2.0],   # Horas de ensamblaje
        [3.0, 1.0, 1.0],   # Materia prima crítica
    ])
    b = np.array([180.0, 160.0, 210.0])

    # linprog minimiza por defecto, por lo que minimizamos -c^T x
    res_primal = linprog(c=-c, A_ub=A, b_ub=b, bounds=(0, None), method="highs")
    x_opt = res_primal.x
    z_opt = -res_primal.fun

    # Problema Dual: min b^T y  s.a.  A^T y >= c  (<=> -A^T y <= -c), y >= 0
    res_dual = linprog(c=b, A_ub=-A.T, b_ub=-c, bounds=(0, None), method="highs")
    y_opt = res_dual.x
    w_opt = res_dual.fun

    holgura_primal = b - A @ x_opt
    holgura_dual = (A.T @ y_opt) - c

    print("=== SOLUCIÓN PRIMAL ===")
    for j, val in enumerate(x_opt, 1):
        print(f"  x_{j}* = {val:.4f}  | Costo reducido (A^T y - c)_{j} = {holgura_dual[j-1]:.4f}")
    print(f"  Valor óptimo Primal (z*) = {z_opt:.4f}\n")

    print("=== SOLUCIÓN DUAL (PRECIOS SOMBRA) ===")
    for i, val in enumerate(y_opt, 1):
        print(f"  y_{i}* = {val:.4f}  | Holgura del recurso (b - Ax)_{i} = {holgura_primal[i-1]:.4f}")
    print(f"  Valor óptimo Dual   (w*) = {w_opt:.4f}\n")

    print("=== VERIFICACIÓN DE TEOREMAS ===")
    print(f"  Dualidad Fuerte |z* - w*| = {abs(z_opt - w_opt):.2e}")
    comp_primal = np.max(np.abs(y_opt * holgura_primal))
    comp_dual = np.max(np.abs(x_opt * holgura_dual))
    print(f"  Holgura Complementaria Primal max|y_i * s_i| = {comp_primal:.2e}")
    print(f"  Holgura Complementaria Dual   max|x_j * e_j| = {comp_dual:.2e}")


if __name__ == "__main__":
    resolver_primal_dual()
