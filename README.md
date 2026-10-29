# 📐 Investigación Operativa y Optimización Matemática (Exactas - UBA)

Modelos matemáticos, formulaciones y resoluciones computacionales en **Python (`PySCIPOpt` & `SciPy`)** correspondientes a los contenidos de **Investigación Operativa** en la **Licenciatura en Ciencias de Datos (FCEN - UBA)**.

---

## 📂 Modelos Implementados

### 1. [`01_programacion_lineal_dualidad.py`](./01_programacion_lineal_dualidad.py) — Programación Lineal Continua, Simplex y Dualidad
Formulación primal y dual de un problema de planificación de producción y asignación de recursos escasos:
$$\max \; c^T x \quad \text{sujeto a} \quad A x \le b, \; x \ge 0$$
$$\min \; b^T y \quad \text{sujeto a} \quad A^T y \ge c, \; y \ge 0$$
- Resolución exacta del problema Primal y Dual.
- Verificación del **Teorema de Dualidad Fuerte** ($c^T x^* = b^T y^*$) y de las condiciones de **Holgura Complementaria**:
  $$y_i^* (b_i - A_i x^*) = 0 \quad \forall i, \qquad x_j^* (A_j^T y^* - c_j) = 0 \quad \forall j$$
- Interpretación económica de las variables duales como **precios sombra** (costo de oportunidad marginal de cada recurso).

### 2. [`02_programacion_entera_milp.py`](./02_programacion_entera_milp.py) — Programación Lineal Entera Mixta (`PySCIPOpt`)
Modelado con variables binarias de decisión, restricciones lógicas y técnica de **Big-M**:
- **Localización de Instalaciones con Capacidad (*Capacitated Facility Location Problem - CFLP*)**:
  - Variables binarias $y_i \in \{0, 1\}$ de apertura de centros logísticos con costo fijo $f_i$ y variables continuas/enteras $x_{i,j} \ge 0$ de flujo hacia clientes.
  - Restricciones de activación acopladas: $\sum_{j} x_{i,j} \le C_i y_i$.
- **Cobertura de Conjuntos (*Set Covering*) y Restricciones de Disyunción**.

### 3. [`03_transporte_asignacion_flujo.py`](./03_transporte_asignacion_flujo.py) — Redes, Transporte y Asignación
- **Problema de Transporte de Hitchcock** y **Asignación Bipartita de Costo Mínimo**.
- Propiedad de **Unimodularidad Total** de la matriz de incidencia nodo-arco: demostración práctica de por qué la relajación lineal produce soluciones enteras exactas sin necesidad de *Branch & Bound*.

---

## 🔗 Proyecto Relacionado
- 🎯 **[`sudoku-cv-solver`](https://github.com/FelaBoucai/sudoku-cv-solver)**: Aplicación de **Programación Lineal Binaria (`PySCIPOpt`)** en un sistema de visión artificial en tiempo real que modela un tablero de Sudoku como un sistema de factibilidad entera en $\mathbb{Z}_2^{9 \times 9 \times 9}$.

---

## 🚀 Ejecución

```bash
pip install pyscipopt scipy numpy
python 01_programacion_lineal_dualidad.py
python 02_programacion_entera_milp.py
python 03_transporte_asignacion_flujo.py
```
