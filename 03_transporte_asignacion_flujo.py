"""
Problema de Asignación Bipartita y Transporte de Costo Mínimo.
Verificación de Unimodularidad Total en la relajación lineal.
Investigación Operativa — Lic. en Ciencias de Datos (Exactas - UBA)
"""

import numpy as np
from scipy.optimize import linear_sum_assignment, linprog


def verificar_unimodularidad_asignacion():
    # Matriz de costos de asignación (4 agentes x 4 tareas)
    C = np.array([
        [14, 5, 8, 7],
        [2, 12, 6, 5],
        [7, 8, 3, 9],
        [2, 4, 6, 10],
    ], dtype=float)
    n = C.shape[0]

    # 1. Resolución mediante Relajación Lineal Continua (0 <= x_ij <= 1)
    c_vec = C.flatten()
    A_eq = []
    b_eq = []

    # Restricciones de fila: cada agente toma exactamente 1 tarea
    for i in range(n):
        row = np.zeros((n, n))
        row[i, :] = 1.0
        A_eq.append(row.flatten())
        b_eq.append(1.0)

    # Restricciones de columna: cada tarea es asignada a 1 agente
    for j in range(n):
        col = np.zeros((n, n))
        col[:, j] = 1.0
        A_eq.append(col.flatten())
        b_eq.append(1.0)

    res_lp = linprog(c=c_vec, A_eq=A_eq, b_eq=b_eq, bounds=(0, 1), method="highs")
    X_lp = res_lp.x.reshape((n, n))

    # 2. Resolución combinatoria (Algoritmo Húngaro / Kuhn-Munkres)
    row_ind, col_ind = linear_sum_assignment(C)

    print("=== SOLUCIÓN DE LA RELAJACIÓN LINEAL CONTINUA ===")
    print(X_lp)
    es_entera = np.all(np.isclose(X_lp, np.round(X_lp)))
    print(f"¿La relajación lineal dio solución 100% entera (0/1)? -> {es_entera}")
    print(f"Costo óptimo LP: {res_lp.fun:.2f} | Costo Algoritmo Húngaro: {C[row_ind, col_ind].sum():.2f}")


if __name__ == "__main__":
    verificar_unimodularidad_asignacion()
