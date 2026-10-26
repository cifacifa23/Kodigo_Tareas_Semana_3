"""
Actividad: IA como Herramienta, no como Autor
Script: Analizador de Logs y Validacion Automatica de Eventos
Archivo: analizador_logs.py
"""

import os
import re
import sys
from datetime import datetime

# [Decision Clave]: Forzar salida UTF-8 para evitar errores de renderizado en terminales Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def validar_calendario_real(fecha_str: str) -> bool:
    """
    [Decision Tecnica Clave]:
    RegEx verifica solo la forma \d{4}-\d{2}-\d{2}, permitiendo dias inexistentes
    (como 2026-02-30 o 2026-11-31). Se complementa con datetime.strptime
    para asegurar validez semantica en el calendario gregoriano.
    """
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def analizar_archivo_logs(ruta_archivo: str, modo: str):
    """
    Lee linea por linea el log, previene desbordamiento de memoria RAM en archivos masivos,
    y clasifica cada registro segun el filtro solicitado por el usuario.
    """
    if not os.path.exists(ruta_archivo):
        print(f"\n[!] Error: El archivo '{ruta_archivo}' no existe.")
        return

    # Patrones de expresion regular precompilados para optimizar el rendimiento en bucles
    patron_completo = re.compile(
        r"^\[(INFO|WARNING|ERROR)\]\s+(\d{4}-\d{2}-\d{2})\s+(.+)$"
    )
    patron_sin_fecha = re.compile(r"^\[(INFO|WARNING|ERROR)\]\s+(.+)$")

    total_lineas = 0
    eventos_validos = []
    lineas_con_error = []
    conteo_severidad = {"INFO": 0, "WARNING": 0, "ERROR": 0}

    # errors='replace' evita caidas abruptas si el log contiene caracteres binarios corruptos
    with open(ruta_archivo, "r", encoding="utf-8", errors="replace") as archivo:
        for num_linea, linea in enumerate(archivo, start=1):
            linea_limpia = linea.strip()

            # Descartar lineas vacias para no contaminar la metrica de errores sintacticos
            if not linea_limpia:
                continue

            total_lineas += 1

            # Nivel 1: Formato ideal [SEVERIDAD] YYYY-MM-DD MENSAJE
            match_completo = patron_completo.match(linea_limpia)
            if match_completo:
                severidad, fecha_str, mensaje = match_completo.groups()

                if validar_calendario_real(fecha_str):
                    conteo_severidad[severidad] += 1
                    eventos_validos.append(
                        f"Linea {num_linea} | [{severidad}] {fecha_str} -> {mensaje}"
                    )
                else:
                    lineas_con_error.append(
                        f"Linea {num_linea} [ERROR FECHA]: Fecha inexistente '{fecha_str}' en '{linea_limpia}'"
                    )
                continue

            # Nivel 2: Severidad valida pero sin estampa de tiempo
            match_sin_fecha = patron_sin_fecha.match(linea_limpia)
            if match_sin_fecha:
                lineas_con_error.append(
                    f"Linea {num_linea} [SIN FECHA]: Falta la fecha obligatoria YYYY-MM-DD en '{linea_limpia}'"
                )
                continue

            # Nivel 3: Severidad no admitida (ej. CRITICAL, DEBUG), texto plano o corchetes rotos
            lineas_con_error.append(
                f"Linea {num_linea} [SINTAXIS]: Formato o nivel desconocido en '{linea_limpia}'"
            )

    # Presentacion de resultados en consola segun el modo del menu
    nombre_archivo = os.path.basename(ruta_archivo)
    print("\n" + "=" * 70)
    print(f"ARCHIVO: {nombre_archivo}")
    print("=" * 70)

    if modo == "todo":
        print(f"Total lineas procesadas:        {total_lineas}")
        print(f"Total eventos validos:          {len(eventos_validos)}")
        print(f"Total anomalias / errores:      {len(lineas_con_error)}")
        print("\nDesglose de Eventos Validos:")
        for tipo, cant in conteo_severidad.items():
            print(f"  - [{tipo}]: {cant}")

        if lineas_con_error:
            print("\nDetalle de Lineas con Observaciones:")
            for err in lineas_con_error:
                print(f"  * {err}")
        else:
            print("\nSin anomalias detectadas.")

    elif modo == "validos":
        print(f"Eventos validos encontrados: {len(eventos_validos)}")
        if eventos_validos:
            for ev in eventos_validos:
                print(f"  [OK] {ev}")
        else:
            print("  (No existen eventos validos en este archivo)")

    elif modo == "errores":
        print(f"Eventos observados con fallas: {len(lineas_con_error)}")
        if lineas_con_error:
            for err in lineas_con_error:
                print(f"  [X] {err}")
        else:
            print("  (No se encontraron anomalias)")

    print("=" * 70)


def obtener_archivos_logs(directorio: str) -> list:
    """
    [Decision Tecnica Clave]:
    Evita la solicitud manual de rutas por consola escaneando en batch los archivos
    con extension .log o .txt en la raiz del script.
    """
    extensiones = (".log", ".txt")
    return [
        os.path.join(directorio, f)
        for f in os.listdir(directorio)
        if f.lower().endswith(extensiones)
        and os.path.isfile(os.path.join(directorio, f))
    ]


def main():
    directorio_raiz = os.path.dirname(os.path.abspath(__file__))
    archivos = obtener_archivos_logs(directorio_raiz)

    if not archivos:
        print(f"\n[!] No se encontraron archivos .log o .txt en: {directorio_raiz}")
        return

    while True:
        print("\n" + "#" * 50)
        print("   MENU DE AUDITORIA Y VALIDACION DE LOGS")
        print("#" * 50)
        print(f"Archivos detectados en la raiz ({len(archivos)}):")
        for ruta in archivos:
            print(f"  * {os.path.basename(ruta)}")
        print("-" * 50)
        print("1. Validar TODO (Reporte estadistico y resumen general)")
        print("2. Mostrar SOLO eventos validos")
        print("3. Mostrar SOLO lineas con error / anomalias")
        print("4. Salir")
        print("-" * 50)

        opcion = input("Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            for ruta in archivos:
                analizar_archivo_logs(ruta, modo="todo")
        elif opcion == "2":
            for ruta in archivos:
                analizar_archivo_logs(ruta, modo="validos")
        elif opcion == "3":
            for ruta in archivos:
                analizar_archivo_logs(ruta, modo="errores")
        elif opcion == "4":
            print("\nFinalizando ejecucion del programa...")
            break
        else:
            print("\n[!] Opcion invalida. Ingrese un numero del 1 al 4.")


if __name__ == "__main__":
    main()