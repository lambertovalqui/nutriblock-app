import streamlit as st
import pandas as pd
import os
import io

# Configuración de página con carga rápida
st.set_page_config(
    page_title="NUTRIBLOCK - Ganadería de Precisión",
    page_icon="🧊",
    layout="centered"
)

# Cargar estilos CSS estáticos (Optimizados para velocidad)
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff !important;
        padding-bottom: 90px !important;
    }
    .phone-notch {
        width: 130px;
        height: 18px;
        background-color: #0F2C59;
        margin: -10px auto 15px auto;
        border-bottom-left-radius: 12px;
        border-bottom-right-radius: 12px;
    }
    h1, h2, h3, h4, .section-header {
        color: #0F2C59 !important;
        font-weight: 700 !important;
    }
    .section-header {
        font-size: 19px;
        margin-top: 15px;
        margin-bottom: 8px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 4px;
    }
    .sub-text {
        font-size: 13px;
        color: #475569;
        margin-bottom: 12px;
    }
    .btn-calcular {
        background-color: #f59e0b;
        color: #000000;
        text-align: center;
        font-weight: 700;
        padding: 12px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 16px;
    }
    .card-costo-total {
        background-color: #0F2C59;
        color: #ffffff;
        border-radius: 10px;
        padding: 12px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        font-size: 18px;
        margin-top: 10px;
        margin-bottom: 25px;
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FUNCIONES DE CACHÉ (Evita recargas lentas de la base de datos)
# -----------------------------------------------------------------------------
@st.cache_data
def obtener_catalogo_base():
    return pd.DataFrame([
        {"id": 1, "categoria": "Fuentes de calcio", "nombre": "Carbonato de Calcio", "precio_soles_kg": 2.00, "pct": 15.0},
        {"id": 2, "nombre": "Cal Agrícola", "categoria": "Fuentes de calcio", "precio_soles_kg": 1.50, "pct": 10.0},
        {"id": 3, "categoria": "Fuentes de fósforo", "nombre": "Fosfato Dicálcico", "precio_soles_kg": 4.20, "pct": 10.0},
        {"id": 4, "categoria": "Fuentes de magnesio", "nombre": "Óxido de Magnesio", "precio_soles_kg": 3.80, "pct": 5.0},
        {"id": 5, "categoria": "Fuentes de sodio", "nombre": "Sal Común", "precio_soles_kg": 1.20, "pct": 15.0},
        {"id": 6, "categoria": "Microminerales", "nombre": "Premezcla Mineral Trace", "precio_soles_kg": 8.50, "pct": 5.0},
        {"id": 7, "categoria": "Endurecedores y aglutinantes", "nombre": "Melaza de Caña", "precio_soles_kg": 2.50, "pct": 35.0},
        {"id": 8, "categoria": "Endurecedores y aglutinantes", "nombre": "Urea Agrícola", "precio_soles_kg": 3.50, "pct": 15.0},
    ])

# Estado de navegación
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "1. Inicio"

# Inicialización de catálogo en la sesión
if 'catalogo_ingredientes' not in st.session_state:
    st.session_state.catalogo_ingredientes = obtener_catalogo_base()

# Encabezado visual tipo SmartPhone
st.markdown("<div class='phone-notch'></div>", unsafe_allow_html=True)

# Cargar logo en memoria
logo_path = "Logo_NUTRIBLOCK.jpg"
if os.path.exists(logo_path):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo_path, use_container_width=True)
else:
    st.markdown("""
        <div style='text-align: center; font-size: 24px; font-weight: 800; color: #0F2C59;'>
            🧊 NUTRIBLOCK
        </div>
        <div style='text-align: center; font-size: 11px; color: #2e7d32; font-weight: 600; margin-bottom: 15px;'>
            TUS INSUMOS, TUS COSTOS, MEJORES DECISIONES
        </div>
    """, unsafe_allow_html=True)

# =============================================================================
# MÓDULO 1: INICIO
# =============================================================================
if st.session_state.pagina_actual == "1. Inicio":
    tab_app, tab_cat, tab_info = st.tabs(["📲 Formular", "📦 Insumos", "🛡️ Alertas"])

    with tab_app:
        st.markdown("<div class='section-header'>1. Datos del animal</div>", unsafe_allow_html=True)
        categoria_animal = st.selectbox(
            "Categoría",
            options=["Vacas lecheras en lactación", "Vacas secas", "Vaquillonas / Crecimiento"],
            index=0
        )
        col_peso, col_leche = st.columns(2)
        with col_peso:
            peso_vivo = st.number_input("Peso vivo (kg)", min_value=50.0, value=450.0, step=10.0)
        with col_leche:
            leche_diaria = st.number_input("Leche (litros/día)", min_value=0.0, value=18.0, step=1.0)

        st.markdown("---")

        st.markdown("<div class='section-header'>2. Características del bloque</div>", unsafe_allow_html=True)
        peso_fabricar = st.number_input("Peso total que desea fabricar (kg)", min_value=0.1, value=50.0, step=5.0)
        num_animales = st.number_input("Número de animales en el lote (Unidades)", min_value=1, value=10, step=1)

        st.markdown("---")

        st.markdown("<div class='section-header'>3. Seleccionar ingredientes</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-text'>El productor selecciona los ingredientes que consigue en su localidad.</div>", unsafe_allow_html=True)

        df_ing = st.session_state.catalogo_ingredientes
        categorias = [
            "Fuentes de calcio",
            "Fuentes de fósforo",
            "Fuentes de magnesio",
            "Fuentes de sodio",
            "Microminerales",
            "Endurecedores y aglutinantes"
        ]

        ingredientes_seleccionados = []
        for cat in categorias:
            opciones_cat = df_ing[df_ing["categoria"] == cat]["nombre"].tolist()
            if opciones_cat:
                sel = st.multiselect(
                    f"{cat}",
                    options=opciones_cat,
                    default=opciones_cat[:1]
                )
                ingredientes_seleccionados.extend(sel)

        st.markdown("---")
        st.markdown("### 📊 Resultado de la Formulación")

        if not ingredientes_seleccionados:
            st.warning("⚠️ Seleccione al menos un ingrediente por categoría.")
        else:
            df_filtrado = df_ing[df_ing["nombre"].isin(ingredientes_seleccionados)].copy()
            suma_pct_base = df_filtrado["pct"].sum()
            df_filtrado["pct_ajustado"] = (df_filtrado["pct"] / suma_pct_base) * 100.0
            
            filas = []
            costo_total = 0.0

            for _, row in df_filtrado.iterrows():
                pct = row["pct_ajustado"]
                precio = row["precio_soles_kg"]
                kg = (peso_fabricar * pct) / 100.0
                costo_parcial = kg * precio
                costo_total += costo_parcial
                
                filas.append({
                    "Insumo": row["nombre"],
                    "% Inclusión": round(pct, 1),
                    "Cantidad (kg)": round(kg, 2),
                    "Costo (S/)": round(costo_parcial, 2)
                })

            df_resultado = pd.DataFrame(filas)
            st.dataframe(df_resultado, use_container_width=True, hide_index=True)

            st.session_state['ultima_receta'] = {
                "categoria": categoria_animal,
                "peso_lote": peso_fabricar,
                "animales": num_animales,
                "costo_total": costo_total,
                "detalle": df_resultado
            }

            kg_por_animal = peso_fabricar / num_animales if num_animales > 0 else 0
            st.caption(f"💡 Rendimiento estimado: **{kg_por_animal:.2f} kg** de bloque disponibles por animal.")

            st.markdown("<div class='btn-calcular'>Calcular lote</div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class='card-costo-total'>
                    <span>Costo Total</span>
                    <span>S/ {costo_total:.2f}</span>
                </div>
            """, unsafe_allow_html=True)

    with tab_cat:
        st.caption("Administración del Catálogo de Insumos y Precios")
        df_edit = st.data_editor(
            st.session_state.catalogo_ingredientes,
            hide_index=True,
            column_config={
                "precio_soles_kg": st.column_config.NumberColumn("S/ / kg", format="S/ %.2f"),
                "pct": st.column_config.NumberColumn("Inclusión base (%)", format="%.1f%%")
            },
            use_container_width=True
        )
        st.session_state.catalogo_ingredientes = df_edit

    with tab_info:
        st.caption("Directrices de Ganadería de Precisión")
        st.info("Un bloque nutricional mineral complementa la dieta pero no la sustituye.")

# =============================================================================
# MÓDULO 2: MIS RECETAS
# =============================================================================
elif st.session_state.pagina_actual == "2. Mis Recetas":
    st.markdown("<div class='section-header'>📂 Mis Recetas e Informes</div>", unsafe_allow_html=True)

    if 'ultima_receta' in st.session_state:
        receta_data = st.session_state['ultima_receta']
        st.success(f"Receta activa: **{receta_data['categoria']}** ({receta_data['peso_lote']} kg)")
        st.dataframe(receta_data['detalle'], use_container_width=True, hide_index=True)
        
        try:
            output_excel = io.BytesIO()
            with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                df_resumen = pd.DataFrame([
                    {"Parámetro": "Categoría Animal", "Valor": receta_data['categoria']},
                    {"Parámetro": "Peso Total del Lote (kg)", "Valor": receta_data['peso_lote']},
                    {"Parámetro": "Número de Animales", "Valor": receta_data['animales']},
                    {"Parámetro": "Costo Total Estimado (S/)", "Valor": round(receta_data['costo_total'], 2)}
                ])
                df_resumen.to_excel(writer, sheet_name='Resumen_Lote', index=False)
                receta_data['detalle'].to_excel(writer, sheet_name='Detalle_Ingredientes', index=False)
            output_excel.seek(0)
            
            st.download_button(
                label="📥 Descargar Receta en Excel (.xlsx)",
                data=output_excel,
                file_name=f"Receta_NUTRIBLOCK_{receta_data['peso_lote']}kg.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception:
            csv_data = receta_data['detalle'].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Receta en CSV",
                data=csv_data,
                file_name=f"Receta_NUTRIBLOCK_{receta_data['peso_lote']}kg.csv",
                mime="text/csv"
            )
    else:
        st.info("💡 Aún no has realizado ningún cálculo.")

# =============================================================================
# MÓDULO 3: GUÍA NUTRIBLOCK
# =============================================================================
elif st.session_state.pagina_actual == "3. Guía NUTRIBLOCK":
    st.markdown("<div class='section-header'>📖 Guía Técnica de Elaboración</div>", unsafe_allow_html=True)
    st.markdown("""
    #### 1. Preparación y Pesado
    * Pese cada ingrediente seco exacto.
    * Homogenice primero todos los minerales secos durante 3 a 5 minutos.
    #### 2. Mezcla de Aglutinantes
    * Caliente la melaza e incorpore la urea.
    * Vierta la mezcla líquida sobre la harina mineral y amase.
    #### 3. Compactación en Molde
    * Apisone fuertemente en capas de 5 cm.
    #### 4. Curado y Secado
    * Deje secar a la sombra durante **3 a 5 días**.
    """)

# =============================================================================
# NAVEGACIÓN INFERIOR
# =============================================================================
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("📲 Inicio", use_container_width=True):
        st.session_state.pagina_actual = "1. Inicio"
        st.rerun()
with c2:
    if st.button("📂 Mis Recetas", use_container_width=True):
        st.session_state.pagina_actual = "2. Mis Recetas"
        st.rerun()
with c3:
    if st.button("📖 Guía", use_container_width=True):
        st.session_state.pagina_actual = "3. Guía NUTRIBLOCK"
        st.rerun()
