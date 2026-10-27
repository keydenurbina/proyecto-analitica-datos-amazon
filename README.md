# ¿Qué hace que un producto electrónico tenga alta demanda en Amazon?

Proyecto de Analítica de Datos · MACI 2026 · Keyden Urbina P.

Clasificación de productos electrónicos de Amazon EE.UU. en **alta** o **baja demanda** a partir de sus reseñas, precio y puntuación, con 5 modelos de machine learning, una prueba de hipótesis y una app prototipo para revendedores.

## Pregunta de investigación

¿Permiten las reseñas (`total_reviews`), el precio (`original_price`) y la puntuación (`product_rating`) identificar los productos con alta demanda (`purchased_last_month` ≥ 400)?

| | Hipótesis |
|---|---|
| **H₀** | El precio y la puntuación no mejoran la identificación de productos de alta demanda respecto de usar solo las reseñas |
| **H₁** | El precio y la puntuación sí mejoran la identificación respecto de usar solo las reseñas |

## Resultados principales

| Resultado | Valor |
|---|---|
| Modelo ganador | KNN (k = 201), elegido entre Naive Bayes, KNN, SVM, árbol de decisión y Random Forest |
| AUC en productos nunca vistos (prueba) | **0,833** |
| Productos bien clasificados | 74,3% |
| Prueba de hipótesis | **Se rechaza H₀**: +0,034 de AUC, IC 95% [+0,020; +0,049], p < 0,001 |
| Variables clave | Reseñas (principal) y precio (relación inversa). La puntuación aporta poco |
| Robustez | Contando los productos sin dato de compras como baja demanda (cobertura 94,4%), H₀ se sigue rechazando |

**Límite principal:** el resultado muestra asociación, no causa. Las reseñas son en parte consecuencia de las ventas.

## Datos

- **Fuente:** [Amazon Products Sales Dataset 42K Items 2025](https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025) (Kaggle). Revisar la licencia en la página del dataset.
- **Archivo usado:** `amazon_products_sales_data_uncleaned.csv` (versión sin limpiar, exigida por el proyecto).
- **Embudo:** 42.675 filas → 9.472 tras la limpieza → 8.825 productos únicos → 7.289 productos con las 4 variables.

## Estructura

```
├── app/
│   └── app.py                     # app prototipo (Streamlit)
├── data/
│   ├── raw/                       # dataset original de Kaggle
│   └── procesado/                 # dataset limpio (lo genera el notebook 02)
├── figuras/                       # gráficos generados por los notebooks
├── modelos/
│   └── modelo_demanda.joblib      # modelo que usa la app (lo genera el notebook 04)
├── notebooks/
│   ├── 01. data_collection_raw.ipynb        # origen y obtención de los datos
│   ├── 02. data_preprocessing_raw.ipynb     # limpieza
│   ├── 03. data_exploration_cleaned.ipynb   # exploración
│   └── 04. data_modeling_cleaned.ipynb      # modelos, hipótesis y modelo para la app
├── requirements.txt
└── README.md
```

## Cómo reproducirlo

**1. Crear el entorno e instalar las librerías** (una sola vez, desde la carpeta del proyecto):

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**2. Descargar el dataset:** copiar `amazon_products_sales_data_uncleaned.csv` desde Kaggle a `data/raw/`. El notebook 01 también puede descargarlo solo con `kagglehub`.

**3. Ejecutar los notebooks en orden** (01 → 04), cada uno con *Run All* y el kernel `.venv`. Cada notebook usa lo que genera el anterior.

**4. Abrir la app:**

```bash
streamlit run app/app.py
```

Se abre en el navegador (`http://localhost:8501`). Se ingresan el número de reseñas y el precio de lista del producto, y la app entrega la probabilidad de alta demanda con un semáforo (🟢 ≥ 60% · 🟡 40–60% · 🔴 < 40%).

> Si la app muestra `InconsistentVersionWarning`, el modelo se guardó con otra versión de scikit-learn: volver a ejecutar el notebook 04 con el entorno activo.