import csv
import requests
import time
from io import StringIO

def descargar_csv(liga, temporada):
    url = f"https://fixturedownload.com/download/la-liga-{temporada}-{liga}-UTC.csv"
    print(f"Descargando datos desde: {url}")
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Error al descargar el archivo. Verifique la liga o temporada.")
        exit(1)
    return resp.text

def procesar_resultados(csv_texto):
    """Procesa los resultados y calcula estadísticas"""
    equipos = {}
    partidos = []

    time.sleep(1)

    reader = csv.DictReader(StringIO(csv_texto))
    for fila in reader:
        home = fila["Home Team"]
        away = fila["Away Team"]
        res = fila["Result"].strip()

        if not res or "-" not in res:
            continue

        try:
            home_goals, away_goals = map(int, res.split("-"))
        except:
            continue

        for team in (home, away):
            if team not in equipos:
                equipos[team] = {
                    "GF": 0, "GC": 0, "PTS": 0,
                    "Directos": {},
                }

        equipos[home]["GF"] += home_goals
        equipos[home]["GC"] += away_goals
        equipos[away]["GF"] += away_goals
        equipos[away]["GC"] += home_goals

        if home_goals > away_goals:
            equipos[home]["PTS"] += 3
            resultado = (3, 0)
        elif home_goals < away_goals:
            equipos[away]["PTS"] += 3
            resultado = (0, 3)
        else:
            equipos[home]["PTS"] += 1
            equipos[away]["PTS"] += 1
            resultado = (1, 1)

        equipos[home]["Directos"].setdefault(away, []).append((home_goals, away_goals))
        equipos[away]["Directos"].setdefault(home, []).append((away_goals, home_goals))

        partidos.append((home, away, home_goals, away_goals))

    return equipos, partidos

def diferencia_directos(equipos, eq1, eq2):
    if eq2 not in equipos[eq1]["Directos"]:
        return 0
    goles_favor = sum(gf for gf, _ in equipos[eq1]["Directos"][eq2])
    goles_contra = sum(gc for _, gc in equipos[eq1]["Directos"][eq2])
    return goles_favor - goles_contra

def ordenar_tabla(equipos):
    def clave(eq):
        data = equipos[eq]
        return (
            data["PTS"],
            data["GF"] - data["GC"],
            data["GF"],
        )

    orden = sorted(equipos.keys(), key=lambda eq: clave(eq), reverse=True)

    i = 0
    while i < len(orden) - 1:
        eq1, eq2 = orden[i], orden[i+1]
        if equipos[eq1]["PTS"] == equipos[eq2]["PTS"]:
            diff_dir = diferencia_directos(equipos, eq1, eq2)
            if diff_dir < 0:
                orden[i], orden[i+1] = orden[i+1], orden[i]
        i += 1

    return orden

def main():
    print("Clasificación de Ligas")
    liga = input("Ingrese la equipo: ").strip().lower()
    temporada = input("Ingrese la temporada: ").strip()

    csv_texto = descargar_csv(liga, temporada)
    equipos, partidos = procesar_resultados(csv_texto)

    print("\n(a) Goles a favor por equipo")
    for eq, data in equipos.items():
        print(f"{eq}: {data['GF']} goles a favor")

    orden = ordenar_tabla(equipos)
    print("\n(b) Tabla Clasificatoria Final")
    print(f"{'Pos':<4}{'Equipo':<25}{'Pts':<5}{'GF':<5}{'GC':<5}{'DG':<5}")
    for i, eq in enumerate(orden, 1):
        data = equipos[eq]
        dg = data["GF"] - data["GC"]
        print(f"{i:<4}{eq:<25}{data['PTS']:<5}{data['GF']:<5}{data['GC']:<5}{dg:<5}")

    print("\n(c) Criterios de desempate aplicados")
    print("1. Diferencia de goles en enfrentamientos directos")
    print("2. Diferencia de goles general")
    print("3. Goles marcados")

if __name__ == "__main__":
    main()
