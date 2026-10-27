# app.py -- Prototipo: ¿este producto de Amazon tiene perfil de alta demanda?
# Va en la carpeta app/. Ejecutar desde la carpeta del proyecto con:  streamlit run app/app.py
import re
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st

MODELO = joblib.load(Path(__file__).parent.parent / "modelos" / "modelo_demanda.joblib")   # sube de app/ al proyecto
miles = lambda n: f"{n:,.0f}".replace(",", ".")                                      # 1500 -> "1.500"

# 1. Encabezado
st.set_page_config(page_title="Demanda Amazon", page_icon="📦")
st.title("📦 ¿Este producto tiene perfil de alta demanda?")
st.caption("Electrónica en Amazon EE.UU. · Alta demanda = 400 o más compras en el último mes")

# 2. Formulario: los 3 datos que ingresa el revendedor
with st.form("producto"):
    asin = st.text_input("ASIN del producto", placeholder="B0DSCFVFZ5").strip().upper()
    resenas = st.number_input("Número de reseñas", min_value=0, step=1)
    precio = st.number_input("Precio de lista (US$)", min_value=0.0, step=1.0,
                             help="Precio SIN descuento ('List Price' o 'Typical price'). Si no hay descuento, el precio normal.")
    evaluar = st.form_submit_button("Evaluar producto")

# 3. Resultado
if evaluar:
    if resenas < 1 or precio <= 0:
        st.error("Ingresa el número de reseñas y el precio de lista.")
        st.stop()
    if asin and not re.fullmatch(r"[A-Z0-9]{10}", asin):
        st.warning("Un ASIN tiene 10 letras o números. Revisa que esté bien copiado.")
    if not (5 <= resenas <= 94_000 and 7 <= precio <= 1_700):
        st.warning("Valores fuera de lo que conoce el modelo (5 a 94.000 reseñas; US\\$7 a US\\$1.700): resultado poco confiable.")

    entrada = pd.DataFrame({"log_reseñas": [np.log10(resenas)], "log_precio": [np.log10(precio)]})
    prob = float(MODELO.predict_proba(entrada)[0, 1])                # probabilidad de alta demanda

    if prob >= 0.60:
        st.success("🟢 **Alta demanda**: probablemente vende 400 o más unidades al mes")
    elif prob >= 0.40:
        st.warning("🟡 **Zona gris**: no hay una señal clara, el resultado es incierto")
    else:
        st.error("🔴 **Baja demanda**: probablemente vende menos de 400 unidades al mes")
    st.metric(f"Probabilidad de alta demanda{' · ' + asin if asin else ''}", f"{prob:.0%}")
    st.progress(prob)

    # Explicación: comparación con el perfil típico de alta demanda (reglas del árbol de decisión)
    st.markdown("**Comparado con el perfil típico de alta demanda:**")
    st.markdown(f"- Reseñas: **{miles(resenas)}** " + ("✅ alcanza" if resenas >= 1_500 else "⚠️ no alcanza") + " las ~1.500 típicas")
    st.markdown(f"- Precio de lista: **US\\${miles(precio)}** " + ("✅ bajo" if precio <= 110 else "⚠️ sobre") + " los US\\$110 típicos")   # \\$ evita que Streamlit lo lea como fórmula

# 4. Advertencias fijas
st.divider()
st.caption("Acierta 3 de cada 4 productos (74%) · Solo electrónica en Amazon EE.UU. · No sirve para productos sin reseñas · "
           "Identifica el perfil actual del producto: no garantiza ventas futuras ni recomienda cambiar el precio.")
