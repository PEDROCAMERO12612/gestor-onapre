import io
import pandas as pd
import streamlit as st
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# Configuración inicial de la página web
st.set_page_config(
    page_title="Asistente ONAPRE Instructivo N° 06", page_icon="📊", layout="wide"
)

st.title("📊 Asistente de Ejecución Físico-Financiera (Instructivo N° 06)")
st.markdown(
    "Herramienta de generación de reportes bajo los formatos oficiales de la"
    " ONAPRE."
)

# Inicializar memoria de sesión
if "obras" not in st.session_state:
  st.session_state.obras = []

# Pestañas principales
tab1, tab2, tab3 = st.tabs(
    [
        "⚙️ Parámetros del Órgano",
        "🏗️ Formulario 0601 (Obras)",
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

# --- PESTAÑA 2: FORMULARIO (OBRAS) ---
with tab2:
  st.subheader("Registro de Ejecución Financiera de Obras")

  col_a, col_b = st.columns(2)
  with col_a:
    accion_especifica = st.text_input(
        "Acción Específica / Código", placeholder="Ej. 01", key="form_accion"
    )
    monto_prog_mes = st.number_input(
        "Programado Mes (V1)", min_value=0.0, format="%.2f", key="form_prog"
    )
  with col_b:
    denominacion_obra = st.text_input(
        "Denominación de la Obra",
        placeholder="Nombre de la obra...",
        key="form_obra_nombre",
    )
    monto_caus_mes = st.number_input(
        "Causado / Ejecutado Mes (V2)",
        min_value=0.0,
        format="%.2f",
        key="form_caus",
    )

  if st.button("➕ Registrar Obra al Reporte", type="primary"):
    if denominacion_obra and accion_especifica:
      variacion = monto_prog_mes - monto_caus_mes
      st.session_state.obras.append({
          "sipes": "01",
          "ppto": "01",
          "accion": accion_especifica,
          "denominacion": denominacion_obra,
          "prog_mes": monto_prog_mes,
          "prog_acum": monto_prog_mes,  # Estimado base
          "caus_mes": monto_caus_mes,
          "caus_acum": monto_caus_mes,  # Estimado base
          "var_abs": variacion,
      })
      st.success(f"¡Obra '{denominacion_obra}' agregada exitosamente!")
    else:
      st.warning(
          "Por favor, complete al menos la Acción Específica y la Denominación"
          " de la Obra."
      )

  if len(st.session_state.obras) > 0:
    st.markdown("---")
    st.markdown("### Obras Registradas:")
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

    # Generación de Excel con diseño exacto del Instructivo N° 06
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      wb = writer.book
      ws = wb.active
      ws.title = "Instructivo_06"

      # Estilos institucionales
      font_title = Font(name="Arial", size=10, bold=True)
      font_bold = Font(name="Arial", size=9, bold=True)
      font_normal = Font(name="Arial", size=9)
      align_center = Alignment(
          horizontal="center", vertical="center", wrap_text=True
      )
      align_left = Alignment(horizontal="left", vertical="center")
      align_right = Alignment(horizontal="right", vertical="center")

      thin_border = Border(
          left=Side(style="thin", color="000000"),
          right=Side(style="thin", color="000000"),
          top=Side(style="thin", color="000000"),
          bottom=Side(style="thin", color="000000"),
      )

      # 1. Encabezado institucional superior
      ws["A1"] = f"(1) CÓDIGO PRESUPUESTARIO DEL ÓRGANO: {codigo_presupuestario}"
      ws["A2"] = f"DENOMINACIÓN DEL ÓRGANO: {denominacion_organo}"
      ws["A3"] = f"MES: {mes_reporte.upper()} {anio_fiscal}"
      ws["H1"] = "FECHA: ___/___/______"

      for r in range(1, 4):
        ws.merge_cells(
            start_row=r, start_column=1, end_row=r, end_column=4
        )  # Ajuste de cabecera
        ws.cell(row=r, column=1).font = font_title

      # Título principal del formato
      ws.merge_cells("A5:I5")
      ws["A5"] = (
          "EJECUCIÓN FINANCIERA MENSUAL DE LAS OBRAS CONTENIDAS EN EL PROYECTO"
          " (En Bolívares)"
      )
      ws["A5"].font = Font(name="Arial", size=11, bold=True)
      ws["A5"].alignment = align_center

      # 2. Cabeceras de la Tabla Oficial (Estructura de celdas múltiples)
      # Fila 7 y 8 para cabeceras combinadas
      headers_row7 = [
          "CÓDIGO (3)",
          "",
          "(4)\nACCIÓN ESPECÍFICA",
          "EJECUTADO",
          "",
          "",
          "",
          "VARIACIÓN ACUMULADA",
          "",
      ]
      ws.append([])  # Fila 6 vacía de separación
      ws.append([
          "SIPES",
          "Ppto.",
          "Denominación",
          "PROGRAMADO\nMES",
          "COMPROMETIDO\nMES",
          "CAUSADO\nMES",
          "PROGRAMADO\nACUMULADO",
          "COMPROMETIDO\nACUMULADO",
          "CAUSADO\nACUMULADO",
          "(7) ABSOLUTA",
          "(8) %",
      ])

      # Aplicar formato de cabecera a la tabla
      # Inserción de datos reales desde session_state
      row_start = 9
      for i, obra in enumerate(st.session_state.obras):
        row_num = row_start + i
        ws.append([
            obra["sipes"],
            obra["ppto"],
            obra["accion"] + " - " + obra["denominacion"],
            obra["prog_mes"],
            obra["prog_mes"],  # Comprometido mes simulado
            obra["caus_mes"],
            obra["prog_acum"],
            obra["prog_acum"],
            obra["caus_acum"],
            obra["var_abs"],
            (
                (obra["var_abs"] / obra["prog_mes"] * 100)
                if obra["prog_mes"] > 0
                else 0.0
            ),
        ])

      # Sección de justificación al pie
      last_row = row_start + len(st.session_state.obras) + 2
      ws.cell(
          row=last_row, column=1, value="JUSTIFICACIÓN DE LAS DESVIACIONES:"
      ).font = font_bold
      ws.cell(row=last_row + 1, column=1, value=justificacion).font = (
          font_normal
      )

    excel_data = output.getvalue()

    # Botón de descarga con el formato oficial
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
        "Aún no hay obras cargadas. Vaya a la pestaña 'Formulario 0601"
        " (Obras)' para comenzar."
    )
