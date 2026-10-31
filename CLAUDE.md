# CLAUDE.md — proyecto-analitica-datos

Contexto para Claude. Léelo antes de tocar cualquier archivo.

## Proyecto
- **Pregunta:** ¿Qué hace que un producto electrónico tenga alta demanda en Amazon EE.UU.?
- **Formulación:** ¿Permiten `total_reviews`, `original_price` y `product_rating` identificar productos de alta demanda (`purchased_last_month` ≥ 400)?
  - H₀: precio y puntuación no mejoran la identificación respecto de usar solo reseñas.
  - H₁: sí la mejoran.
- **Curso:** Analítica de Datos · Magíster en Ciencia de Datos para la Innovación (MACI 2026)
- **Repo:** `keydenurbina/proyecto-analitica-datos` (privado, dueño: Keyden Urbina)
- **Ramas del equipo:** `keyden`, `mati`, `pancho`, `javier/trabajo` (Javier, trabajo con Claude)

## Estado actual (resumen del README)
- Dataset: Amazon Products Sales Dataset 42K Items 2025 (Kaggle), versión *uncleaned* (exigida por el curso).
- Embudo: 42.675 filas → 9.472 limpias → 8.825 productos únicos → 7.289 con las 4 variables.
- 5 modelos comparados (Naive Bayes, KNN, SVM, árbol, Random Forest). Ganador: KNN (k=201), AUC test 0,833, 74,3% bien clasificados.
- Se rechaza H₀: +0,034 AUC, IC 95% [+0,020; +0,049], p < 0,001.
- Límite: asociación, no causalidad (las reseñas son en parte consecuencia de las ventas).
- App prototipo en Streamlit (`app/app.py`) con semáforo de probabilidad.

## Entregas
- **Entrega 1 — Presentación de avance: viernes 6 de noviembre 2026** (pauta en `ppt/instrucciones.txt`)
  - Introducción 15% · Descripción del problema 15% · Metodología y plan de trabajo por semana 30%
  - Descripción de datos y EDA 30% · Resultados preliminares de ML 10%
- **Entrega final: sábado 19 de diciembre 2026**

## Estructura
| Ruta | Contenido | Regla |
|---|---|---|
| `data/raw/` | CSV original de Kaggle | Solo lectura. Nunca modificar |
| `data/procesado/` | Dataset limpio (lo genera el notebook 02) | Se regenera, no editar a mano |
| `notebooks/01–04` | Pipeline: obtención → limpieza → EDA → modelos e hipótesis | Ejecutar en orden; cada uno usa lo que genera el anterior |
| `notebooks/05–06` | Pruebas del modelo y de la app | |
| `notebooks/asin/` | Búsqueda de ASIN (ignorado en git) | Exploratorio |
| `modelos/modelo_demanda.joblib` | Modelo que usa la app (lo genera el notebook 04) | Si se reentrena, re-ejecutar 04 completo |
| `app/app.py` | App Streamlit: `streamlit run app/app.py` | No romper la ejecución |
| `figuras/` | Gráficos exportados por los notebooks | Nombres `NN_descripcion.png` |
| `ppt/` | Pautas e insumos de presentaciones | Fuente de verdad de cada entrega |

## Cómo trabajar
- **Nunca commitear directo a `main`.** Rama propia → PR → revisión de al menos un compañero.
- No tocar ramas de otros integrantes (`keyden`, `mati`, `pancho`).
- Antes de empezar: `git fetch origin && git merge origin/main`.
- Commits en español, verbo en imperativo ("Agrega gráfico de precios por categoría").
- Comentarios, conclusiones y textos de notebooks en español.
- Notebooks: limpiar outputs pesados antes de commitear.
- Entorno: `.venv` + `requirements.txt`.

## Estilo de análisis
- Cada gráfico con título, ejes rotulados y una línea de interpretación.
- Toda conclusión apoyada en una cifra o gráfico del notebook.
- Explicitar supuestos y limitaciones del dataset.
- Formato de números chileno en textos (1.500 · 0,833).

## Pendientes detectados (revisar con el equipo)
- `requirements.txt` no incluye `scikit-learn`, `streamlit`, `joblib` ni `kagglehub`, que usan los notebooks y la app.
- El README no menciona los notebooks 05 y 06.
- `.gitignore` excluye `data/raw/*` y `figuras/*.png`, pero el CSV y las figuras ya están versionados (se subieron antes de la regla).
- Hay archivos `.DS_Store` versionados en `data/`.
