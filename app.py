import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Gestor ONAPRE - Instructivo N° 06",
    page_icon="📊",
    layout="wide",
)

# Título principal
st.title("📊 Asistente de Ejecución Físico-Financiera (Instructivo N° 06)")
st.markdown(
    "Herramienta simplificada para la carga, validación y cálculo automático de"
    " reportes mensuales para la ONAPRE."
)

# MÓDULO 1: Configuración Institucional
st.sidebar.header("1. Parámetros del Órgano")
codigo_organo = st.sidebar.text_input("Código Presupuestario", "00150")
denominacion_organo = st.sidebar.text_input(
    "Denominación del Órgano", "Ministerio / Ente Ejecutor"
)
mes_reporte = st.sidebar.selectbox(
    "Mes de Reporte",
    [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ],
)
anio_reporte = st.sidebar.number_input("Año Fiscal", value=2026, step=1)

# Pestañas principales de navegación
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🏗️ Formulario 0601 (Obras)",
        "💰 Formulario 0602 (Financiero)",
        "📈 Formulario 0603 (Físico)",
        "📑 Resumen y Consolidado",
    ]
)

# Inicializar estados en memoria
if "obras_data" not in st.session_state:
  st.session_state.obras_data = pd.DataFrame(
      columns=[
          "Acción Específica",
          "Nombre de la Obra",
          "Prog_Mes",
          "Ejec_Comprometido",
          "Ejec_Causado",
      ]
  )

if "financiero_data" not in st.session_state:
  st.session_state.financiero_data = pd.DataFrame(
      columns=[
          "Proyecto/Acción",
          "Partida",
          "Programado_Mes",
          "Comprometido_Mes",
          "Causado_Mes",
      ]
  )

# MÓDULO 2: Formulario 0601 (Obras)
with tab1:
  st.subheader("Registro de Ejecución Financiera de Obras")
  with st.form("form_obra"):
    col1, col2 = st.columns(2)
    with col1:
      accion_esp = st.text_input("Acción Específica", placeholder="Ej. 01")
      nombre_obra = st.text_input("Denominación de la Obra")
    with col2:
      prog_mes = st.number_input(
          "Monto Programado del Mes (V1)", min_value=0.0, format="%.2f"
      )
      ejec_causado = st.number_input(
          "Monto Causado / Ejecutado del Mes (V2)",
          min_value=0.0,
          format="%.2f",
      )

    submitted_obra = st.form_submit_button("Agregar Obra al Reporte")
    if submitted_obra and nombre_obra:
      nueva_fila = pd.DataFrame(
          [[accion_esp, nombre_obra, prog_mes, 0.0, ejec_causado]],
          columns=[
              "Acción Específica",
              "Nombre de la Obra",
              "Prog_Mes",
              "Ejec_Comprometido",
              "Ejec_Causado",
          ],
      )
      st.session_state.obras_data = pd.concat(
          [st.session_state.obras_data, nueva_fila], ignore_index=True
      )
      st.success("¡Obra agregada con éxito!")

  if not st.session_state.obras_data.empty:
    st.markdown("### Listado de Obras Cargadas")
    df_temp = st.session_state.obras_data.copy()
    df_temp["Variación Absoluta (VA)"] = (
        df_temp["Ejec_Causado"] - df_temp["Prog_Mes"]
    )
    df_temp["Variación Relativa (%)"] = (
        df_temp["Variación Absoluta (VA)"] / df_temp["Prog_Mes"].replace(0, 1)
    ) * 100
    st.dataframe(df_temp, use_container_width=True)

# MÓDULO 3: Formulario 0602 (Ejecución Financiera por Partidas)
with tab2:
  st.subheader("Ejecución Financiera por Partidas Presupuestarias")
  with st.form("form_financiero"):
    c1, c2, c3 = st.columns(3)
    with c1:
      proy_accion = st.text_input("Proyecto o Acción Centralizada")
    with c2:
      partida = st.text_input("Partida Presupuestaria", placeholder="Ej. 4.01")
    with c3:
      prog_fin = st.number_input(
          "Programado Financiero", min_value=0.0, format="%.2f"
      )

    c4, c5 = st.columns(2)
    with c4:
      comp_fin = st.number_input("Comprometido Mes", min_value=0.0, format="%.2f")
    with c5:
      caus_fin = st.number_input("Causado Mes", min_value=0.0, format="%.2f")

    submitted_fin = st.form_submit_button("Guardar Partida")
    if submitted_fin and partida:
      nueva_fin = pd.DataFrame(
          [[proy_accion, partida, prog_fin, comp_fin, caus_fin]],
          columns=[
              "Proyecto/Acción",
              "Partida",
              "Programado_Mes",
              "Comprometido_Mes",
              "Causado_Mes",
          ],
      )
      st.session_state.financiero_data = pd.concat(
          [st.session_state.financiero_data, nueva_fin], ignore_index=True
      )
      st.success("¡Partida registrada con éxito!")

  if not st.session_state.financiero_data.empty:
    st.markdown("### Consolidado Financiero del Mes")
    df_f_temp = st.session_state.financiero_data.copy()
    df_f_temp["Diferencia (Prog - Causado)"] = (
        df_f_temp["Programado_Mes"] - df_f_temp["Causado_Mes"]
    )
    st.dataframe(df_f_temp, use_container_width=True)

# MÓDULO 4: Formulario 0603 & Resumen Consolidado
with tab3:
  st.subheader("Ejecución Física de Metas")
  meta_nombre = st.text_input("Descripción de la Meta Física")
  unidad_medida = st.text_input("Unidad de Medida")
  col_m1, col_m2 = st.columns(2)
  with col_m1:
    meta_prog = st.number_input("Cantidad Programada (Mes)", min_value=0.0)
  with col_m2:
    meta_ejec = st.number_input("Cantidad Ejecutada (Mes)", min_value=0.0)

  if meta_prog > 0:
    eficacia = (meta_ejec / meta_prog) * 100
    st.metric(
        label="Índice de Eficacia Física del Periodo", value=f"{eficacia:.2f}%"
    )

with tab4:
  st.subheader("Resumen y Consolidado para la ONAPRE")
  st.info(
      f"Órgano: **{denominacion_organo}** (Código: {codigo_organo}) | Periodo:"
      f" **{mes_reporte} {anio_reporte}**"
  )
  st.markdown("### 📋 Justificación de Desviaciones")
  st.text_area(
      "Redacte aquí las causas de las variaciones:", placeholder="Explique..."
  )

  if st.button("📥 Generar Consolidado Descargable"):
    st.success("¡Datos consolidados correctamente!")