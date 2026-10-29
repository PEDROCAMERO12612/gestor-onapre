import streamlit as st
import pandas as pd
import io

# -----------------------------------------------------------------------------
# 1. Configuración de la Página para Adaptabilidad y Diseño Responsivo
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gestor ONAPRE - Instructivo N° 06",
    page_icon="📊",
    layout="wide",  # Permite que la aplicación aproveche todo el ancho de la pantalla
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para optimizar la adaptabilidad y legibilidad
st.markdown("""
    <style>
    /* Estilos para contenedores de tarjetas responsivas */
    .metric-card {
        background-color: #1e222d;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2e3440;
        margin-bottom: 10px;
    }
    /* Adaptabilidad de tablas */
    .stDataFrame {
        width: 100% !important;
    }
    /* Estilos de botones responsivos */
    div.stButton > button {
        width: 100%;
        border-radius: 6px;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Encabezado Principal Institucional
# -----------------------------------------------------------------------------
st.title("SISTEMA DE GESTIÓN - INSTRUCTIVO NRO 6 - OFICINA DE PLANIFICACIÓN DEL EJÉRCITO BOLIVARIANO")
st.caption("Herramienta simplificada para la carga, validación y cálculo automático de reportes mensuales para la ONAPRE.")

# -----------------------------------------------------------------------------
# 3. Panel Lateral (Sidebar) Responsivo: Parámetros del Órgano
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("1. Parámetros del Órgano")
    codigo_presupuestario = st.text_input("Código Presupuestario", value="00150")
    denominacion_organo = st.text_input("Denominación del Órgano", value="Ministerio del Poder Popular para la Defensa / Ejército Bolivariano")
    mes_reporte = st.selectbox(
        "Mes de Reporte",
        ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    )
    ano_fiscal = st.number_input("Año Fiscal", min_value=2020, max_value=2035, value=2026, step=1)

# Inicializar estados de la sesión para almacenamiento temporal de tablas
if "obras" not in st.session_state:
    st.session_state.obras = []

if "financiero" not in st.session_state:
    st.session_state.financiero = []

if "fisico" not in st.session_state:
    st.session_state.fisico = []

# -----------------------------------------------------------------------------
# 4. Cuerpo Principal con Pestañas Responsivas
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🏗️ Formulario 0601 (Obras)",
    "💰 Formulario 0602 (Financiero)",
    "📈 Formulario 0603 (Físico)",
    "📋 Resumen y Consolidado"
])

# -----------------------------------------------------------------------------
# PESTAÑA 1: Formulario 0601 (Obras)
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Registro de Ejecución Financiera de Obras")
    
    # Filas con columnas adaptables (utilizan distribución flex de Streamlit)
    col1, col2 = st.columns([1, 2])
    with col1:
        accion_esp_obra = st.text_input("Acción Específica (Obra)", value="Ej. 01")
    with col2:
        denominacion_obra = st.text_input("Denominación de la Obra", placeholder="Nombre detallado de la obra...")

    col3, col4 = st.columns(2)
    with col3:
        monto_prog_obra = st.number_input("Monto Programado del Mes (V1)", min_value=0.0, format="%.2f")
    with col4:
        monto_ejec_obra = st.number_input("Monto Causado / Ejecutado del Mes (V2)", min_value=0.0, format="%.2f")

    if st.button("Agregar Obra al Reporte", key="btn_obra"):
        if denominacion_obra.strip() != "":
            st.session_state.obras.append({
                "Acción Específica": accion_esp_obra,
                "Denominación de la Obra": denominacion_obra,
                "Programado (Bs.)": monto_prog_obra,
                "Ejecutado (Bs.)": monto_ejec_obra
            })
            st.success(f"Obra '{denominacion_obra}' agregada correctamente.")
        else:
            st.warning("Por favor ingrese la denominación de la obra.")

    if st.session_state.obras:
        st.write("---")
        st.subheader("Obras Registradas")
        df_obras = pd.DataFrame(st.session_state.obras)
        st.dataframe(df_obras, use_container_width=True)

# -----------------------------------------------------------------------------
# PESTAÑA 2: Formulario 0602 (Financiero)
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Ejecución Financiera Presupuestaria por Partidas")
    
    col_fin1, col_fin2 = st.columns([1, 2])
    with col_fin1:
        partida = st.text_input("Partida Presupuestaria", value="4.01.00.00.00")
    with col_fin2:
        denominacion_partida = st.text_input("Denominación de la Partida", value="Gastos de Personal")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        monto_ley = st.number_input("Presupuesto Ley (Bs.)", min_value=0.0, format="%.2f")
    with col_m2:
        modificaciones = st.number_input("Modificaciones (Bs.)", format="%.2f")
    with col_m3:
        monto_compromiso = st.number_input("Compromisos (Bs.)", min_value=0.0, format="%.2f")

    col_m4, col_m5 = st.columns(2)
    with col_m4:
        monto_causado = st.number_input("Monto Causado (Bs.)", min_value=0.0, format="%.2f")
    with col_m5:
        monto_pagado = st.number_input("Monto Pagado (Bs.)", min_value=0.0, format="%.2f")

    if st.button("Guardar Registro Financiero", key="btn_fin"):
        st.session_state.financiero.append({
            "Partida": partida,
            "Denominación": denominacion_partida,
            "Presupuesto Ley": monto_ley,
            "Modificaciones": modificaciones,
            "Presupuesto Modificado": monto_ley + modificaciones,
            "Compromiso": monto_compromiso,
            "Causado": monto_causado,
            "Pagado": monto_pagado
        })
        st.success(f"Partida {partida} registrada exitosamente.")

    if st.session_state.financiero:
        st.write("---")
        df_fin = pd.DataFrame(st.session_state.financiero)
        st.dataframe(df_fin, use_container_width=True)

# -----------------------------------------------------------------------------
# PESTAÑA 3: Formulario 0603 (Físico)
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Control de Ejecución Física y Metas")
    
    col_fis1, col_fis2 = st.columns([1, 2])
    with col_fis1:
        unidad_medida = st.text_input("Unidad de Medida", value="Informe / Inspección")
    with col_fis2:
        meta_nombre = st.text_input("Denominación de la Meta", placeholder="Descripción de la meta física...")

    col_fm1, col_fm2 = st.columns(2)
    with col_fm1:
        meta_prog = st.number_input("Meta Programada del Mes", min_value=0.0, format="%.2f")
    with col_fm2:
        meta_ejec = st.number_input("Meta Ejecutada del Mes", min_value=0.0, format="%.2f")

    if st.button("Guardar Registro Físico", key="btn_fis"):
        cumplimiento = (meta_ejec / meta_prog * 100) if meta_prog > 0 else 0.0
        st.session_state.fisico.append({
            "Unidad de Medida": unidad_medida,
            "Denominación de la Meta": meta_nombre,
            "Meta Programada": meta_prog,
            "Meta Ejecutada": meta_ejec,
            "% Cumplimiento": f"{cumplimiento:.2f}%"
        })
        st.success("Registro de meta física guardado.")

    if st.session_state.fisico:
        st.write("---")
        df_fis = pd.DataFrame(st.session_state.fisico)
        st.dataframe(df_fis, use_container_width=True)

# -----------------------------------------------------------------------------
# PESTAÑA 4: Resumen y Consolidado
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Resumen Consolidado del Reporte ONAPRE N° 06")
    
    st.markdown(f"""
    **Órgano:** {denominacion_organo}  
    **Código Presupuestario:** `{codigo_presupuestario}` | **Período:** {mes_reporte} {ano_fiscal}
    """)
    st.write("---")

    # Muestra de tablas consolidadas limpias (omitiendo filas de cero)
    if st.session_state.obras:
        st.markdown("##### 🏗️ Obras Ejecutadas (Formulario 0601)")
        df_o = pd.DataFrame(st.session_state.obras)
        df_o_clean = df_o[(df_o["Programado (Bs.)"] > 0) | (df_o["Ejecutado (Bs.)"] > 0)]
        st.dataframe(df_o_clean, use_container_width=True)

    if st.session_state.financiero:
        st.markdown("##### 💰 Ejecución Financiera (Formulario 0602)")
        df_f = pd.DataFrame(st.session_state.financiero)
        df_f_clean = df_f[(df_f["Causado"] > 0) | (df_f["Presupuesto Ley"] > 0)]
        st.dataframe(df_f_clean, use_container_width=True)

    if st.session_state.fisico:
        st.markdown("##### 📈 Ejecución Física (Formulario 0603)")
        df_ph = pd.DataFrame(st.session_state.fisico)
        st.dataframe(df_ph, use_container_width=True)

    # Generación y descarga de archivo Excel consolidado
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if st.session_state.obras:
            pd.DataFrame(st.session_state.obras).to_excel(writer, sheet_name='Formulario_0601', index=False)
        if st.session_state.financiero:
            pd.DataFrame(st.session_state.financiero).to_excel(writer, sheet_name='Formulario_0602', index=False)
        if st.session_state.fisico:
            pd.DataFrame(st.session_state.fisico).to_excel(writer, sheet_name='Formulario_0603', index=False)
    
    excel_data = output.getvalue()
    
    st.download_button(
        label="📥 Descargar Reporte Consolidado (Excel)",
        data=excel_data,
        file_name=f"ONAPRE_Instructivo6_{codigo_presupuestario}_{mes_reporte}_{ano_fiscal}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
