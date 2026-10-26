# Analizador de Logs y Auditoría de Eventos en Python
> **Actividad:** IA como Herramienta, no como Autor: Desarrollo Guiado y Validado de un Script en Python  
> **Módulo:** Semana 3 – IA-first mindset  

---

## 📌 Descripción del Proyecto

Este proyecto consiste en un script de consola desarrollado en Python que procesa y audita archivos de registro (*logs*). El programa examina cada línea para categorizar el nivel de severidad (`INFO`, `WARNING`, `ERROR`), comprobar la coherencia sintáctica y validar que las fechas pertenezcan a un calendario gregoriano real.

El desarrollo se llevó a cabo aplicando un enfoque de **IA-first mindset**: la Inteligencia Artificial se utilizó como un asistente técnico para acelerar tareas repetitivas y proponer sintaxis preliminares, mientras que el control de las reglas de negocio, el diseño de la arquitectura y la validación de errores recayeron íntegramente en el desarrollador.

---

## 📂 Estructura del Repositorio

```text
.
├── analizador_logs.py          # Script principal ejecutable en Python
├── Evaluacion 3 - Desarrollo Guiado y Validado de un Script en Python Semana 3.pdf       # Documento de reflexión técnica (1 a 15 páginas)
├── logs_validos.txt            # Caso de prueba: registros limpios y bien formados
├── logs_con_errores.txt        # Caso de prueba: líneas con fallos, fechas inexistentes y anomalías
└── README.md                   # Documentación general y evidencias de ejecución
