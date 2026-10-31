# Guía de la Entrega 1 — Presentación de avance

**Fecha:** viernes 6 de noviembre de 2026 · **Archivo:** `ppt/presentacion_entrega1.pptx` (13 láminas, con notas del orador)

Esta guía explica, en simple, qué problema resuelve el proyecto, cómo se está resolviendo y por qué lo que ya está en el repositorio cubre todo lo que pide la pauta.

---

## 1. Cuál es el problema

En Amazon, el cliente decide qué comprar mirando la **página de resultados de búsqueda**: ahí ve el precio, el descuento, el rating, la cantidad de reseñas y distintivos como "Best Seller". Las ventas reales de cada producto, en cambio, no son públicas: Amazon solo muestra un aproximado por tramos ("100+ comprados el último mes", "1K+"…), y a veces ni eso.

Para alguien que quiere vender en Amazon (un revendedor) o analizar el mercado, la pregunta práctica es:

> **¿Se puede saber si un producto electrónico tiene alta demanda usando solo la información pública del listado?**

El proyecto lo formula así:

- **Pregunta:** ¿permiten las reseñas, el precio y el rating identificar los productos con alta demanda (400 o más compras en el último mes)?
- **H₀:** el precio y el rating **no** mejoran la identificación respecto de usar solo las reseñas.
- **H₁:** el precio y el rating **sí** la mejoran.

Las reseñas son el punto de partida porque son la variable más asociada a las compras. La hipótesis mide si precio y rating agregan información por encima de ellas.

---

## 2. Cómo se está resolviendo

El trabajo sigue un pipeline de 6 notebooks, cada uno usa lo que genera el anterior:

| Paso | Notebook | Qué hace | Resultado clave |
|---|---|---|---|
| Obtener | `01. data_collection_raw` | Contexto de mercado, ficha del dataset, verificación de integridad (huella MD5), diccionario de datos | 42.675 filas × 16 columnas, scraping de amazon.com del 21 al 30 de agosto de 2025 |
| Limpiar | `02. data_preprocessing_raw` | Diagnóstico de nulos y formatos, conversión de texto a números, extracción del ASIN desde la URL, categoría por palabras clave, eliminación de capturas repetidas | 9.472 filas limpias, 8.641 ASIN únicos |
| Explorar | `03. data_exploration_cleaned` | Estadística descriptiva, correlaciones, distribuciones de cada variable; formula pregunta e hipótesis | Reseñas vs. compras: Spearman 0,60 · Precio vs. compras: −0,55 · Rating casi sin variación |
| Modelar | `04. data_modeling_cleaned` | 5 modelos (Naive Bayes, KNN, SVM, árbol, Random Forest) con validación cruzada; el ganador se evalúa una sola vez en prueba | KNN (k=201), AUC 0,833 en productos nunca vistos, 74,3% bien clasificados |
| Probar H₀ | `05. data_testing_cleaned` | Bootstrap pareado de 2.000 remuestras: modelo solo con reseñas vs. reseñas + precio + rating | AUC de 0,799 a 0,833 (+0,034, IC 95% [0,020; 0,049], p < 0,001) → **se rechaza H₀** |
| Aplicar | `06. user_app_test` + `app/app.py` | Historia de usuario y app prototipo en Streamlit | Semáforo de probabilidad de alta demanda |

### Tres decisiones de método que conviene saber defender

1. **Una fila no es un producto.** El scraping registró cada *aparición* de un producto en una búsqueda, así que el mismo producto aparece muchas veces. Por eso se pasa de 42.675 filas a 8.825 productos, y el modelo trabaja con una fila por producto. Si no, el mismo producto podría caer en entrenamiento y en prueba, y el resultado se vería mejor de lo que es.
2. **El corte de 400 es la mediana.** Deja dos clases casi del mismo tamaño (53,3% alta y 46,7% baja en los 7.289 productos del modelo). Los 1.124 productos sin dato de compras se excluyen: no tener el dato no significa vender poco.
3. **El conjunto de prueba se usa una sola vez.** Los modelos se comparan con validación cruzada; solo el ganador se evalúa en los 1.458 productos de prueba. Validación (0,828) y prueba (0,833) casi coinciden: no hay sobreajuste.

### Qué dicen los resultados

- Las **reseñas** son la variable principal (el AUC cae 0,062 sin ellas).
- El **precio** es la segunda, con relación inversa: lo barato se vende más (cae 0,034 sin él).
- El **rating** casi no aporta (0,002): casi todos los productos tienen entre 4,3 y 4,6 estrellas.
- Sumar descuento, patrocinio, cupón y categoría **no mejora** el modelo (p = 0,53).
- Cuatro de los cinco modelos empatan cerca de 0,83: el techo lo ponen las variables disponibles, no el algoritmo.

**Límite principal:** es asociación, no causa. Las reseñas son en parte consecuencia de las ventas pasadas.

---

## 3. Por qué el repositorio entrega todo lo necesario

La pauta pide cinco partes. Todas tienen respaldo en el repo y una lámina en la presentación:

| Parte de la pauta | Peso | Dónde está en el repo | Láminas |
|---|---:|---|---|
| Introducción | 15% | Notebook 01, etapas 1–3: contexto del mercado con fuentes | 1–2 |
| Descripción del problema | 15% | Notebook 03, pasos 10–11: pregunta e hipótesis | 3 |
| Metodología y plan por semana | 30% | Notebooks 04–05: preparación, separación 80/20, validación cruzada, 5 modelos, métricas y bootstrap | 9–10 |
| Descripción de datos y EDA | 30% | Notebook 01 (ficha y diccionario), 02 (calidad y limpieza), 03 (exploración, 20 gráficos) | 4–8 |
| Resultados preliminares de ML | 10% | Notebooks 04–05: comparación de modelos, matriz de confusión, prueba de hipótesis | 11–12 |

Todas las cifras de la presentación salen de los outputs de los notebooks, y los gráficos son los mismos que generan los notebooks 02 y 03. Cualquier número que pregunte el profesor se puede mostrar en el notebook correspondiente.

El proyecto, de hecho, va **más allá** de lo que pide un avance: ya tiene modelos evaluados, prueba de hipótesis y una app. Por eso el plan por semana no repite trabajo: pone a prueba y amplía lo que ya existe.

---

## 4. Lo que el equipo debe definir antes del viernes

1. **Validar el plan por semana (lámina 10).** Es una propuesta construida a partir de lo que falta en el repo. Debe reflejar lo que el equipo realmente va a hacer:

   | Semana | Foco | Por qué |
   |---|---|---|
   | S1 · 9–13 nov | Robustez del corte (300 / 400 / 1.000) | El resultado depende de un umbral elegido; hay que mostrar que no es frágil |
   | S2 · 16–20 nov | Modelo por tramos | Aprovecha toda la información de la variable objetivo, no solo alta/baja |
   | S3 · 23–27 nov | Producto nuevo, sin reseñas | Responde la crítica de causalidad y sirve para productos recién lanzados |
   | S4 · 30 nov–4 dic | Información del título (marca, palabras clave) | Única fuente de información nueva para superar el techo de 0,83 |
   | S5 · 7–11 dic | Modelo final y app | Cierre técnico |
   | S6 · 14–19 dic | Informe y presentación final | Entrega 19 de diciembre |

   No se incluyó "sumar más variables" porque el notebook 05 ya mostró que descuento, patrocinio, cupón y categoría no aportan.

2. **Repartir quién presenta cada parte.** Sugerencia por bloques: introducción y problema (láminas 1–3), datos y EDA (4–8), metodología, plan y resultados (9–13).
3. **Confirmar duración y formato** exigidos por el curso, y si hay plantilla institucional.

### Preguntas probables y cómo responderlas

| Pregunta | Respuesta corta |
|---|---|
| ¿Por qué 400 y no otro corte? | Es la mediana: deja clases balanceadas. La semana 1 prueba otros cortes |
| ¿Las reseñas no son consecuencia de las ventas? | Sí, por eso hablamos de asociación. La semana 3 modela el caso sin reseñas |
| ¿Por qué KNN si todos empatan? | Criterio explícito: mayor AUC en validación cruzada. Las diferencias son menores que la variación entre particiones |
| ¿Cómo evitaron filtrar información entre entrenamiento y prueba? | Una fila por producto (ASIN) y la prueba se usa una sola vez |
| ¿Qué pasa con los productos sin dato de compras? | Se excluyen del modelo (1.124). La app sirve justamente para estimarles la demanda |

---

## 5. Pendientes técnicos del repositorio (no bloquean el viernes)

- `requirements.txt` no incluye `scikit-learn`, `streamlit`, `joblib` ni `kagglehub`, que usan los notebooks y la app.
- El README no menciona los notebooks 05 y 06.
- `.gitignore` excluye `data/raw/*` y `figuras/*.png`, pero esos archivos ya estaban versionados antes de la regla.
