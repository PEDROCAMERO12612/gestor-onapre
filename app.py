import io
import pandas as pd
import streamlit as st
import openpyxl

# Configuración inicial de la página web
st.set_page_config(
    page_title="Asistente ONAPRE Instructivo N° 06", page_icon="📊", layout="wide"
)

st.title("📊 Asistente de Ejecución Físico-Financiera (Instructivo N° 06)")
st.markdown(
    "Generación de reportes bajo los formatos oficiales y presupuestarios de la"
    " ONAPRE."
)

# Inicializar memoria de sesión
if "obras" not in st.session_state:
  st.session_state.obras = []

# Pestañas principales
tab1, tab2, tab3 = st.tabs(
    [
        "⚙️ Parámetros del Órgano",
        "🏗️ Formulario 0601 (Obras y Partidas)",
        "📑 Resumen y Consolidado",
    ]
)

# --- PESTAÑA 1: PARÁMETROS ---
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
        "Año Fiscal", min_value=2024, max_value=2030, value=2026, key="input_anio"
    )

  st.success(
      f"Parámetros configurados para: {denominacion_organo} ({mes_reporte}"
      f" {anio_fiscal})"
  )

# --- PESTAÑA 2: FORMULARIO (OBRAS / PARTIDAS) ---
with tab2:
  st.subheader("Registro de Asignación y Ejecución Financiera")
  st.markdown(
      "Ingrese la asignación anual aprobada, junto con lo programado y"
      " ejecutado en el mes."
  )

  col_a, col_b = st.columns(2)
  with col_a:
    accion_especifica = st.text_input(
        "Acción Específica / Código", placeholder="Ej. 01", key="form_accion"
    )
    monto_asignado_anual = st.number_input(
        "Asignación Presupuestaria Anual (Bs.)",
        min_value=0.0,
        format="%.2f",
        key="form_anual",
    )
    monto_prog_mes = st.number_input(
        "Programado del Mes (V1)", min_value=0.0, format="%.2f", key="form_prog"
    )
  with col_b:
    denominacion_obra = st.text_input(
        "Denominación de la Obra / Partida",
        placeholder="Nombre de la obra...",
        key="form_obra_nombre",
    )
    monto_caus_mes = st.number_input(
        "Causado / Ejecutado del Mes (V2)",
        min_value=0.0,
        format="%.2f",
        key="form_caus",
    )

  if st.button("➕ Registrar Partida al Reporte", type="primary"):
    if denominacion_obra and accion_especifica:
      variacion = monto_prog_mes - monto_caus_mes
      st.session_state.obras.append({
          "sipes": "01",
          "ppto": "01",
          "accion": accion_especifica,
          "denominacion": denominacion_obra,
          "asignado_anual": monto_asignado_anual,
          "prog_mes": monto_prog_mes,
          "caus_mes": monto_caus_mes,
          "var_abs": variacion,
      })
      st.success(f"¡Registro '{denominacion_obra}' agregado con éxito!")
    else:
      st.warning(
          "Por favor, complete al menos la Acción Específica y la Denominación."
      )

  if len(st.session_state.obras) > 0:
    st.markdown("---")
    st.markdown("### Registros Cargados:")
    st.dataframe(pd.DataFrame(st.session_state.obras), use_container_width=True)

# --- PESTAÑA 3: RESUMEN Y CONSOLIDADO OFICIAL ---
with tab3:
  st.subheader(
      f"Resumen y Consolidado Oficial ONAPRE ({mes_reporte} {anio_fiscal})"
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

    # Generación del reporte con openpyxl integrando la asignación anual
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Instructivo_06"

    # Cabeceras institucionales
    ws["A1"] = f"(1) CÓDIGO PRESUPUESTARIO DEL ÓRGANO: {codigo_presupuestario}"
    ws["A2"] = f"DENOMINACIÓN DEL ÓRGANO: {denominacion_organo}"
    ws["A3"] = f"MES: {mes_reporte.upper()} {anio_fiscal}"
    ws["F1"] = "FECHA: ___/___/______"

    ws["A5"] = (
        "EJECUCIÓN FINANCIERA MENSUAL DE LAS OBRAS CONTENIDAS EN EL PROYECTO"
        " (En Bolívares)"
    )

    # Cabeceras de la tabla oficial
    ws.cell(row=8, column=1, value="SIPES")
    ws.cell(row=8, column=2, value="Ppto.")
    ws.cell(row=8, column=3, value="Acción y Denominación")
    ws.cell(row=8, column=4, value="Asignación Anual")
    ws.cell(row=8, column=5, value="Programado Mes")
    ws.cell(row=8, column=6, value="Causado Mes")
    ws.cell(row=8, column=7, value="Variación Absoluta")

    # Inserción de filas de datos
    start_row = 9
    for i, obra in enumerate(st.session_state.obras):
      r = start_row + i
      ws.cell(row=r, column=1, value=obra["sipes"])
      ws.cell(row=r, column=2, value=obra["ppto"])
      ws.cell(
          row=r, column=3, value=f"{obra['accion']} - {obra['denominacion']}"
      )
      ws.cell(row=r, column=4, value=obra["asignado_anual"])
      ws.cell(row=r, column=5, value=obra["prog_mes"])
      ws.cell(row=r, column=6, value=obra["caus_mes"])
      ws.cell(row=r, column=7, value=obra["var_abs"])

    # Justificación al pie
    pie_row = start_row + len(st.session_state.obras) + 2
    ws.cell(row=pie_row, column=1, value="JUSTIFICACIÓN DE LAS DESVIACIONES:")
    ws.cell(row=pie_row + 1, column=1, value=justificacion)

    output = io.BytesIO()
    wb.save(output)
    excel_data = output.getvalue()

    # Botón de descarga oficial
    st.download_button(
        label="📥 Descargar Reporte Oficial (Formato ONAPRE)",
        data=excel_data,
        file_name=(
            f"Instructivo_06_Oficial_{denominacion_organo}_{mes_reporte}_{anio_fiscal}.xlsx"
        ),
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )

    if st.button("🗑️ Limpiar Registros"):
      st.session_state.obras = []
      st.session_state["justificacion_texto"] = ""
      st.rerun()
  else:
    st.info(
        "Aún no hay registros cargados. Vaya a la pestaña 'Formulario 0601'"
        " para comenzar."
    )
