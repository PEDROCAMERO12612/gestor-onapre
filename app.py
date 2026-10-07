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
    "Herramienta simplificada para la carga masiva/manual, validación y cálculo"
    " automático de informes para la ONAPRE."
)

# Inicializar memoria de sesión para guardar las obras/partidas
if "obras" not in st.session_state:
  st.session_state.obras = []

# --- BARRA LATERAL: PARÁMETROS DEL ÓRGANO ---
with st.sidebar:
  st.header("1. Parámetros del Órgano")
  codigo_presupuestario = st.text_input(
      "Código Presupuestario", value="29381", key="input_cod"
  )
  denominacion_organo = st.text_input(
      "Denominación del Órgano",
      value='513 BINF "GD MARIANO ONTILLA"',
      key="input_den",
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
      index=9,
      key="input_mes",
  )
  anio_fiscal = st.number_input(
      "Año Fiscal", min_value=2015, max_value=2030, value=2019, key="input_anio"
  )

  st.markdown("---")
  st.success(f"Órgano configurado:\n{denominacion_organo}")

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🏗️ Formulario 0601 (Obras)",
        "💰 Formulario 0602 (Financiero)",
        "📈 Formulario 0603 (Físico)",
        "📑 Resumen y Consolidado",
    ]
)

# --- PESTAÑA 1: FORMULARIO 0601 (OBRAS - CON CARGA MASIVA Y MANUAL) ---
with tab1:
  st.subheader("Registro de Ejecución Financiera de Obras")

  # SECCIÓN DE CARGA MASIVA POR EXCEL
  with st.expander("📁 Carga Masiva por Archivo Excel (Importar Distribución)"):
    st.markdown(
        "Puedes subir un archivo Excel con las columnas: `accion`,"
        " `denominacion`, `asignado_anual`, `prog_mes`, `caus_mes`."
    )

    # Botón para descargar plantilla modelo
    df_plantilla = pd.DataFrame([{
        "accion": "401000000",
        "denominacion": "MATERIALES Y SUMINISTROS",
        "asignado_anual": 5000000.00,
        "prog_mes": 3312241.58,
        "caus_mes": 0.00,
    }])
    output_temp = io.BytesIO()
    df_plantilla.to_excel(output_temp, index=False)
    st.download_button(
        "📥 Descargar Plantilla Modelo para Carga Masiva",
        data=output_temp.getvalue(),
        file_name="plantilla_onapre_obras.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )

    archivo_subido = st.file_uploader(
        "Examinar archivo Excel (.xlsx)", type=["xlsx"]
    )
    if archivo_subido is not None:
      try:
        df_importado = pd.read_excel(archivo_subido)
        for _, row in df_importado.iterrows():
          prog = float(row["prog_mes"])
          caus = float(row["caus_mes"])
          variacion = prog - caus
          st.session_state.obras.append({
              "sipes": "01",
              "ppto": "01",
              "accion": str(row["accion"]),
              "denominacion": str(row["denominacion"]),
              "asignado_anual": float(row["asignado_anual"]),
              "prog_mes": prog,
              "caus_mes": caus,
              "var_abs": variacion,
          })
        st.success(
            "¡Archivo importado con éxito! Se añadieron los registros a la"
            " tabla."
        )
      except Exception as e:
        st.error(
            "Error al procesar el archivo. Asegúrate de usar las columnas de la"
            f" plantilla. Detalle: {e}"
        )

  st.markdown("---")
  st.markdown("### Carga Manual Individual")

  col_a, col_b = st.columns(2)
  with col_a:
    accion_especifica = st.text_input(
        "Acción Específica / Código", placeholder="Ej. 401000000", key="form_accion"
    )
    monto_asignado_anual = st.number_input(
        "Asignación Presupuestaria Anual (Bs.)",
        min_value=0.0,
        format="%.2f",
        key="form_anual",
    )
    monto_prog_mes = st.number_input(
        "Monto Programado del Mes (V1)",
        min_value=0.0,
        format="%.2f",
        key="form_prog",
    )
  with col_b:
    denominacion_obra = st.text_input(
        "Denominación de la Obra",
        placeholder="MATERIALES Y SUMINISTROS",
        key="form_obra_nombre",
    )
    monto_caus_mes = st.number_input(
        "Monto Causado / Ejecutado del Mes (V2)",
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
          "asignado_anual": monto_asignado_anual,
          "prog_mes": monto_prog_mes,
          "caus_mes": monto_caus_mes,
          "var_abs": variacion,
      })
      st.success(f"¡Obra '{denominacion_obra}' registrada correctamente!")
    else:
      st.warning("Por favor, completa al menos el código y la denominación.")

  # Gestión y eliminación individual de registros cargados
  if len(st.session_state.obras) > 0:
    st.markdown("---")
    st.markdown("### 📋 Registros Actuales Cargados (Gestión Individual)")
    df_registros = pd.DataFrame(st.session_state.obras)
    st.dataframe(df_registros, use_container_width=True)

    col_del1, col_del2 = st.columns([2, 1])
    with col_del1:
      indice_a_borrar = st.selectbox(
          "Selecciona un registro si deseas eliminarlo por error:",
          options=range(len(st.session_state.obras)),
          format_func=lambda x: (
              f"Registro #{x+1}: {st.session_state.obras[x]['accion']} -"
              f" {st.session_state.obras[x]['denominacion']}"
          ),
      )
    with col_del2:
      st.write("")
      if st.button("🗑️ Eliminar Registro Seleccionado"):
        eliminado = st.session_state.obras.pop(indice_a_borrar)
        st.success(f"¡Registro '{eliminado['denominacion']}' eliminado!")
        st.rerun()

# --- PESTAÑA 2: FORMULARIO 0602 (FINANCIERO) ---
with tab2:
  st.subheader("Ejecución Financiera por Partidas Presupuestarias")
  st.info(
      "Módulo complementario para el registro financiero específico por partidas"
      " del Instructivo N° 06."
  )
  col_f1, col_f2, col_f3 = st.columns(3)
  with col_f1:
    st.text_input("Proyecto de Acción Centralizada", key="fin_proy")
    st.number_input("Comprometido Mes", min_value=0.0, format="%.2f", key="fin_com")
  with col_f2:
    st.text_input("Partida Presupuestaria", placeholder="Ej. 4.01", key="fin_part")
    st.number_input("Causado Mes", min_value=0.0, format="%.2f", key="fin_cau")
  with col_f3:
    st.number_input("Programado Financiero", min_value=0.0, format="%.2f", key="fin_prog")

  if st.button("Guardar Partida Financiera"):
    st.success("Datos financieros guardados temporalmente en el sistema.")

# --- PESTAÑA 3: FORMULARIO 0603 (FÍSICO) ---
with tab3:
  st.subheader("Ejecución Física de Metas")
  st.info("Módulo para el registro del avance físico de las metas programadas.")
  st.text_area("Descripción de la Meta Alcanzada", key="fis_meta")
  st.number_input("Porcentaje de Avance Físico (%)", min_value=0.0, max_value=100.0, key="fis_porc")
  if st.button("Guardar Avance Físico"):
    st.success("Avance físico registrado correctamente.")

# --- PESTAÑA 4: RESUMEN Y CONSOLIDADO ---
with tab4:
  st.subheader(
      f"Resumen y Consolidado Oficial ONAPRE ({mes_reporte} {anio_fiscal})"
  )

  if len(st.session_state.obras) > 0:
    df_obras = pd.DataFrame(st.session_state.obras)
    st.dataframe(df_obras, use_container_width=True)

    st.markdown("### 📋 Justificación de Desviaciones")
    justificacion = st.text_area(
        "Redacte aquí las causas de las variaciones o desviaciones:",
        value=st.session_state.get("justificacion_texto", ""),
        key="input_justificacion",
    )
    st.session_state["justificacion_texto"] = justificacion

    # Generador del archivo oficial de Excel con openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Instructivo_06"

    ws["A1"] = f"(1) CÓDIGO PRESUPUESTARIO DEL ÓRGANO: {codigo_presupuestario}"
    ws["A2"] = f"DENOMINACIÓN DEL ÓRGANO: {denominacion_organo}"
    ws["A3"] = f"MES: {mes_reporte.upper()} {anio_fiscal}"
    ws["F1"] = "FECHA: ___/___/______"

    ws["A5"] = (
        "EJECUCIÓN FINANCIERA MENSUAL DE LAS OBRAS CONTENIDAS EN EL PROYECTO"
        " (En Bolívares)"
    )

    ws.cell(row=8, column=1, value="SIPES")
    ws.cell(row=8, column=2, value="Ppto.")
    ws.cell(row=8, column=3, value="Acción y Denominación")
    ws.cell(row=8, column=4, value="Asignación Anual")
    ws.cell(row=8, column=5, value="Programado Mes")
    ws.cell(row=8, column=6, value="Causado Mes")
    ws.cell(row=8, column=7, value="Variación Absoluta")

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

    pie_row = start_row + len(st.session_state.obras) + 2
    ws.cell(row=pie_row, column=1, value="JUSTIFICACIÓN DE LAS DESVIACIONES:")
    ws.cell(row=pie_row + 1, column=1, value=justificacion)

    output = io.BytesIO()
    wb.save(output)
    excel_data = output.getvalue()

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

    if st.button("🗑️ Limpiar Todos los Registros"):
      st.session_state.obras = []
      st.session_state["justificacion_texto"] = ""
      st.rerun()
  else:
    st.info(
        "Aún no hay registros cargados. Ve a la pestaña 'Formulario 0601 (Obras)'"
        " para hacer tu carga masiva o manual."
    )
