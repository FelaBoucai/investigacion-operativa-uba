"""
Programación Lineal Entera Mixta (MILP): Localización de Instalaciones con Capacidad (CFLP).
Modelado con variables binarias y restricciones de activación en PySCIPOpt.
Investigación Operativa — Lic. en Ciencias de Datos (Exactas - UBA)
"""

from pyscipopt import Model, quicksum


def resolver_localizacion_instalaciones():
    plantas = ["Pilar", "Nuñez", "Avellaneda", "Morón"]
    clientes = ["C1", "C2", "C3", "C4", "C5"]

    costo_fijo = {"Pilar": 1200, "Nuñez": 1500, "Avellaneda": 1000, "Morón": 1100}
    capacidad = {"Pilar": 120, "Nuñez": 100, "Avellaneda": 90, "Morón": 110}
    demanda = {"C1": 45, "C2": 60, "C3": 35, "C4": 50, "C5": 40}

    costo_envio = {
        ("Pilar", "C1"): 4, ("Pilar", "C2"): 6, ("Pilar", "C3"): 9, ("Pilar", "C4"): 5, ("Pilar", "C5"): 7,
        ("Nuñez", "C1"): 5, ("Nuñez", "C2"): 3, ("Nuñez", "C3"): 4, ("Nuñez", "C4"): 6, ("Nuñez", "C5"): 5,
        ("Avellaneda", "C1"): 8, ("Avellaneda", "C2"): 5, ("Avellaneda", "C3"): 3, ("Avellaneda", "C4"): 4, ("Avellaneda", "C5"): 6,
        ("Morón", "C1"): 6, ("Morón", "C2"): 7, ("Morón", "C3"): 6, ("Morón", "C4"): 3, ("Morón", "C5"): 4,
    }

    model = Model("Facility_Location_MILP")
    model.hideOutput()

    # y[i] in {0, 1}: 1 si se abre la planta i
    y = {i: model.addVar(vtype="B", name=f"abrir_{i}") for i in plantas}

    # x[i, j] >= 0: unidades enviadas desde la planta i al cliente j
    x = {(i, j): model.addVar(vtype="C", lb=0.0, name=f"flujo_{i}_{j}") for i in plantas for j in clientes}

    # 1. Satisfacer la demanda de cada cliente
    for j in clientes:
        model.addCons(quicksum(x[i, j] for i in plantas) == demanda[j], name=f"demanda_{j}")

    # 2. Capacidad y acoplamiento lógico (Big-M / Capacidad): sum_j x[i,j] <= Capacidad[i] * y[i]
    for i in plantas:
        model.addCons(quicksum(x[i, j] for j in clientes) <= capacidad[i] * y[i], name=f"cap_{i}")

    # Función objetivo: Minimizar costos fijos de apertura + costos variables de transporte
    model.setObjective(
        quicksum(costo_fijo[i] * y[i] for i in plantas)
        + quicksum(costo_envio[i, j] * x[i, j] for i in plantas for j in clientes),
        "minimize",
    )

    model.optimize()
    sol = model.getBestSol()

    print(f"Costo Total Óptimo: ${model.getObjVal():.2f}")
    for i in plantas:
        abierta = sol[y[i]] > 0.5
        estado = "ABIERTA" if abierta else "CERRADA"
        print(f"\nPlanta {i:10s}: {estado}")
        if abierta:
            for j in clientes:
                enviado = sol[x[i, j]]
                if enviado > 1e-5:
                    print(f"  -> Envía {enviado:5.1f} u. a {j}")


if __name__ == "__main__":
    resolver_localizacion_instalaciones()
