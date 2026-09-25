import io
import pandas as pd
import streamlit as st

# Configuración inicial de la página web
st.set_page_config(
    page_title="Asistente ONAPRE Instructivo N° 06", page_icon="📊", layout="wide"
)

st.title("📊 Asistente de Ejecución Físico-Financiera (Instructivo N° 06)")
st.markdown(
    "Herramienta simplificada para la carga, validación y cálculo automático"
    " de informes mensuales para la ONAPRE."
)

# Inicializar memoria de sesión para las obras y campos
if "obras" not in st.session_state:
  st.session_state.obras = []

# Pestañas principales de la aplicación
tab1, tab2, tab3 = st.tabs(
    [
        "⚙️ Parámetros del Órgano",
        "🏗️ Formulario 0601 (Obras)",
        "📑 Resumen y Consolidado",
    ]
)

# --- PESTAÑA 1: PARÁMETROS DEL ÓRGANO ---
with tab1:
  st.subheader("Parámetros del Órgano")

  col1, col2 = st.columns(2)
  with col1:
    codigo_presupuestario = st.text_input(
        "Código Presupuestario", value="29884", key="input_cod"
    )
    mes_reporte = st.selectbox(
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
        index=7,
        key="input_mes",
    )
  with col2:
    denominacion_organo = st.text_input(
        "Denominación del Órgano / Ente Ejecutor",
        value="MINISTERIO BRIGADA DE CARIBES",
        key="input_den",
    )
    anio_fiscal = st.number_input(
        "Año Fiscal",
        min_value=2024,
        max_value=2030,
        value=2026,
        key="input_anio",
    )

  st.success(
      f"Parámetros configurados para: {denominacion_organo} ({mes_reporte}"
      f" {anio_fiscal})"
  )

# --- PESTAÑA 2: FORMULARIO 0601 (OBRAS) ---
with tab2:
  st.subheader("Registro de Ejecución Financiera de Obras")
  st.markdown(
      "Ingrese los datos de la obra y haga clic en 'Registrar Obra'."
  )

  col_a, col_b = st.columns(2)
  with col_a:
    accion_especifica = st.text_input(
        "Acción Específica", placeholder="Ej. 01", key="form_accion"
    )
    monto_programado = st.number_input(
        "Monto Programado del Mes (V1)",
        min_value=0.0,
        format="%.2f",
        key="form_prog",
    )
  with col_b:
    denominacion_obra = st.text_input(
        "Denominación de la Obra",
        placeholder="Nombre de la obra...",
        key="form_obra_nombre",
    )
    monto_causado = st.number_input(
        "Monto Causado / Ejecutado del Mes (V2)",
        min_value=0.0,
        format="%.2f",
        key="form_caus",
    )

  if st.button("➕ Registrar Obra al Reporte", type="primary"):
    if denominacion_obra and accion_especifica:
      diferencia = monto_programado - monto_causado
      st.session_state.obras.append({
          "Acción Específica": accion_especifica,
          "Denominación de la Obra": denominacion_obra,
          "Programado Mes (V1)": monto_programado,
          "Causado Mes (V2)": monto_causado,
          "Diferencia": diferencia,
      })
      st.success(f"¡Obra '{denominacion_obra}' agregada exitosamente!")
    else:
      st.warning(
          "Por favor, complete al menos la Acción Específica y la Denominación"
          " de la Obra."
      )

  # Mostrar lista previa de obras cargadas en esta misma pestaña para control visual
  if len(st.session_state.obras) > 0:
    st.markdown("---")
    st.markdown("### Obras Registradas Hasta el Momento:")
    st.dataframe(pd.DataFrame(st.session_state.obras), use_container_width=True)

# --- PESTAÑA 3: RESUMEN Y CONSOLIDADO ---
with tab3:
  st.subheader(
      f"Resumen y Consolidado para la ONAPRE ({mes_reporte} {anio_fiscal})"
  )

  if len(st.session_state.obras) > 0:
    df_obras = pd.DataFrame(st.session_state.obras)
    st.dataframe(df_obras, use_container_width=True)

    st.markdown("### 📋 Justificación de Desviaciones")
    justificacion = st.text_area(
        "Redacte aquí las causas de las variaciones:",
        value=st.session_state.get("justificacion_texto", ""),
        key="input_justificacion",
    )
    st.session_state["justificacion_texto"] = justificacion

    # Generar archivo Excel estructurado bajo el formato oficial Instructivo N° 06
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      df_export = df_obras.copy()
      df_export.columns = [
          "Acción Específica",
          "Denominación de la Obra / Proyecto",
          "Programado Mes (V1)",
          "Causado Mes (V2)",
          "Variación / Diferencia",
      ]
      df_export.to_excel(
          writer, sheet_name="Instructivo_06", index=False, startrow=6
      )

      sheet = writer.sheets["Instructivo_06"]
      sheet["A1"] = "REPÚBLICA BOLIVARIANA DE VENEZUELA"
      sheet["A2"] = "MINISTERIO DEL PODER POPULAR PARA LA DEFENSA"
      sheet["A3"] = (
          "EJÉRCITO BOLIVARIANO — OFICINA DE PLANIFICACIÓN Y PRESUPUESTO"
      )
      sheet["A4"] = (
          f"INFORME DE EJECUCIÓN FÍSICO-FINANCIERA (INSTRUCTIVO N° 06) -"
          f" PERÍODO: {mes_reporte.upper()} {anio_fiscal}"
      )
      sheet["A5"] = (
          f"ÓRGANO / ENTE: {denominacion_organo} | CÓDIGO: {codigo_presupuestario}"
      )

      fila_pie = len(df_export) + 9
      sheet.cell(
          row=fila_pie, column=1, value="JUSTIFICACIÓN DE LAS DESVIACIONES:"
      )
      sheet.cell(row=fila_pie + 1, column=1, value=justificacion)

    excel_data = output.getvalue()

    # Botón oficial de descarga directa a la computadora
    st.download_button(
        label="📥 Descargar Consolidado Oficial (Instructivo N° 06)",
        data=excel_data,
        file_name=(
            f"Instructivo_06_ONAPRE_{denominacion_organo}_{mes_reporte}_{anio_fiscal}.xlsx"
        ),
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )

    if st.button("🗑️ Limpiar Todos los Registros"):
      st.session_state.obras = []
      st.session_state["justificacion_texto"] = ""
      st.rerun()
  else:
    st.info(
        "Aún no hay obras cargadas. Vaya a la pestaña 'Formulario 0601"
        " (Obras)' para registrar al menos una obra."
    )
