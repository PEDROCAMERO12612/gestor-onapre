import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Gestor ONAPRE - Instructivo N° 06", layout="wide")

st.title("Sistema de Gestión - Instructivo N° 06 (ONAPRE)")

# Configuración dinámica de Unidad y Datos Generales
with st.sidebar:
    st.header("⚙️ Datos de la Unidad u Órgano")
    
    codigo_organo = st.text_input("Código del Órgano", value="008", key="cod_org")
    denom_organo = st.text_input("Denominación del Órgano", value="MINISTERIO DEL PODER POPULAR PARA LA DEFENSA", key="den_org")
    unidad_ejecutora = st.text_input("Unidad Ejecutora / Responsable", value="53 BRIGADA DE INFANTERÍA DE SELVA", key="uni_eje")
    mes_reporte = st.text_input("Mes de Reporte", value="JULIO", key="mes_rep")
    fecha_reporte = st.text_input("Fecha de Emisión", value="31/07/2026", key="fec_rep")
    
    st.markdown("---")
    st.info("💡 **Impresión Unificada:** En la pestaña 'Resumen', usa el botón de descarga para guardar los 4 formatos en horizontal.")

# Botón de reinicio principal
col_tit, col_btn = st.columns([4, 1])
with col_btn:
    if st.button("🔄 Reiniciar / Borrar Datos", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown("---")

# Declaración de pestañas principales (4 Formatos Oficiales + Resumen)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 1. Ejecución Financiera",
    "💰 2. Financiera por Partidas",
    "📈 3. Ejecución Física Proyectos",
    "📋 4. Cuadro Anexo Física",
    "🖨️ Resumen y Exportación PDF"
])

# ==========================================
# PESTAÑA 1: EJECUCIÓN FINANCIERA (PROYECTOS)
# ==========================================
with tab1:
    st.subheader("Formulario 1: Ejecución Financiera Mensual de Proyectos / Acciones Centralizadas")
    st.markdown("Cargue su archivo Excel o edite la tabla:")

    archivo_fin = st.file_uploader("📂 Cargar Excel (Ejecución Financiera Proyectos)", type=["xlsx"], key="up_fin")

    if "df_financiera" not in st.session_state:
        st.session_state.df_financiera = pd.DataFrame(columns=[
            "SIPES", "Ppto.", "Denominación", "Prog. Mensual", "Prog. Acumulado",
            "Ejec. Mensual Comprometido", "Ejec. Mensual Causado",
            "Ejec. Acumulado Comprometido", "Ejec. Acumulado Causado", "Unidad Responsable"
        ])

    if archivo_fin is not None:
        try:
            st.session_state.df_financiera = pd.read_excel(archivo_fin)
            st.success("✅ Datos financieros cargados con éxito.")
        except Exception as e:
            st.error(f"❌ Error al leer archivo: {e}")

    st.session_state.df_financiera = st.data_editor(
        st.session_state.df_financiera, 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_financiera"
    )

# ==========================================
# PESTAÑA 2: FINANCIERA POR PARTIDAS DE EGRESOS
# ==========================================
with tab2:
    st.subheader("Formulario 2: Ejecución Financiera Mensual por Partidas de Egresos")
    st.markdown("Cargue un archivo de Excel con su distribución de partidas:")

    archivo_partidas = st.file_uploader("📂 Cargar Excel (Ejecución por Partidas)", type=["xlsx"], key="up_part")

    # Inicializamos vacío para que no cargue datos inventados por defecto
    if "df_partidas" not in st.session_state:
        st.session_state.df_partidas = pd.DataFrame(columns=[
            "Partida", "Genérica", "Específica", "Sub-Esp", "Conc", 
            "Denominación", "Crédito Anual", "Prog. Mes", "Comp. Mes", 
            "Caus. Mes", "Prog. Acum.", "Comp. Acum.", "Caus. Acum."
        ])

    if archivo_partidas is not None:
        try:
            df_temp = pd.read_excel(archivo_partidas, header=None)
            columnas_esperadas = [
                "Partida", "Genérica", "Específica", "Sub-Esp", "Conc", 
                "Denominación", "Crédito Anual", "Prog. Mes", "Comp. Mes", 
                "Caus. Mes", "Prog. Acum.", "Comp. Acum.", "Caus. Acum."
            ]
            if len(df_temp.columns) >= len(columnas_esperadas):
                df_temp = df_temp.iloc[:, :len(columnas_esperadas)]
                df_temp.columns = columnas_esperadas
                st.session_state.df_partidas = df_temp
            else:
                st.session_state.df_partidas = pd.read_excel(archivo_partidas)
            st.success("✅ Partidas cargadas con éxito desde su archivo.")
        except Exception as e:
            st.error(f"❌ Error al leer archivo: {e}")

    st.session_state.df_partidas = st.data_editor(
        st.session_state.df_partidas, 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_partidas"
    )

# ==========================================
# PESTAÑA 3: EJECUCIÓN FÍSICA PROYECTOS
# ==========================================
with tab3:
    st.subheader("Formulario 3: Ejecución Física Mensual de los Proyectos del Órgano")
    st.markdown("Detalle metas físicas programadas y ejecutadas:")

    archivo_fis = st.file_uploader("📂 Cargar Excel (Ejecución Física)", type=["xlsx"], key="up_fis")

    if "df_fisica_proyectos" not in st.session_state:
        st.session_state.df_fisica_proyectos = pd.DataFrame(columns=[
            "SIPES", "Ppto.", "Denominación", "Unidad de Medida", 
            "Meta Prog. Mensual", "Meta Prog. Acumulado", 
            "Meta Ejec. Mensual", "Meta Ejec. Acumulado", "Unidad Responsable"
        ])

    if archivo_fis is not None:
        try:
            st.session_state.df_fisica_proyectos = pd.read_excel(archivo_fis)
            st.success("✅ Datos de ejecución física cargados con éxito.")
        except Exception as e:
            st.error(f"❌ Error al leer archivo: {e}")

    st.session_state.df_fisica_proyectos = st.data_editor(
        st.session_state.df_fisica_proyectos, 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_fisica_proyectos"
    )

# ==========================================
# PESTAÑA 4: CUADRO ANEXO FÍSICO
# ==========================================
with tab4:
    st.subheader("Formulario 4: Cuadro Anexo de Ejecución Física (Unidad Ejecutora Local)")
    st.markdown("Desglose operativo de actividades y misiones:")

    archivo_cua = st.file_uploader("📂 Cargar Excel (Cuadro Anexo)", type=["xlsx"], key="up_cua")

    if "df_cuadro_anexo" not in st.session_state:
        st.session_state.df_cuadro_anexo = pd.DataFrame(columns=[
            "Unidad", "N°", "Operación / Actividad"
        ])

    if archivo_cua is not None:
        try:
            st.session_state.df_cuadro_anexo = pd.read_excel(archivo_cua)
            st.success("✅ Cuadro anexo cargado con éxito.")
        except Exception as e:
            st.error(f"❌ Error al leer archivo: {e}")

    st.session_state.df_cuadro_anexo = st.data_editor(
        st.session_state.df_cuadro_anexo, 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_cuadro_anexo"
    )

# ==========================================
# PESTAÑA 5: RESUMEN Y EXPORTACIÓN UNIFICADA
# ==========================================
with tab5:
    st.subheader("Resumen Consolidado e Impresión Completa")
    st.markdown("---")

    def limpiar_val(val):
        try:
            return float(val) if val is not None and not pd.isna(val) else 0.0
        except:
            return 0.0

    c_org = st.session_state.get("cod_org", "008")
    d_org = st.session_state.get("den_org", "MINISTERIO DEL PODER POPULAR PARA LA DEFENSA")
    u_eje = st.session_state.get("uni_eje", "UNIDAD EJECUTORA")
    m_rep = st.session_state.get("mes_rep", "JULIO")
    f_rep = st.session_state.get("fec_rep", "31/07/2026")

    # HTML FIRMAS UNIFICADAS
    html_firmas = """
    <div style="display: flex; justify-content: space-between; margin-top: 30px; font-size: 8px; text-align: center;">
        <div>_________________________________<br><strong>PROGRAMADOR</strong></div>
        <div>_________________________________<br><strong>ADMINISTRADOR</strong></div>
        <div>_________________________________<br><strong>COMANDANTE</strong></div>
    </div>
    """

    # 1. FORMATO 1: FINANCIERA PROYECTOS
    df_fin = st.session_state.df_financiera
    filas_fin_html = ""
    t_pm, t_pa, t_cm, t_cam, t_ca, t_caa = 0, 0, 0, 0, 0, 0

    for _, row in df_fin.iterrows():
        denom = row.get("Denominación", "")
        if not denom or str(denom).strip() in ["None", ""]: continue
        
        pm = limpiar_val(row.get("Prog. Mensual", 0))
        pa = limpiar_val(row.get("Prog. Acumulado", 0))
        cm = limpiar_val(row.get("Ejec. Mensual Comprometido", 0))
        cam = limpiar_val(row.get("Ejec. Mensual Causado", 0))
        ca = limpiar_val(row.get("Ejec. Acumulado Comprometido", 0))
        caa = limpiar_val(row.get("Ejec. Acumulado Causado", 0))
        
        v_comp = ((cm - pm) / pm * 100) if pm > 0 else -100.0
        v_caus = ((cam - pm) / pm * 100) if pm > 0 else -100.0

        t_pm += pm; t_pa += pa; t_cm += cm; t_cam += cam; t_ca += ca; t_caa += caa

        filas_fin_html += f"""
            <tr>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("SIPES", "")}</td>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("Ppto.", "")}</td>
                <td style="text-align: left; border: 1px solid #000; padding: 4px;">{denom}</td>
                <td style="border: 1px solid #000; padding: 4px;">{pm:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{pa:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{cm:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{cam:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{ca:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{caa:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{v_comp:.0f}%</td>
                <td style="border: 1px solid #000; padding: 4px;">{v_caus:.0f}%</td>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("Unidad Responsable", u_eje)}</td>
            </tr>
        """

    html_f1 = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 8px; font-size: 9px;">
            <div><strong>CÓDIGO DEL ÓRGANO:</strong> {c_org}<br><strong>DENOMINACIÓN DEL ÓRGANO:</strong> {d_org}<br><strong>MES:</strong> {m_rep}</div>
            <div><strong>FECHA:</strong> {f_rep}</div>
        </div>
        <h5 style="text-align: center; font-weight: bold; font-size: 11px; margin-bottom: 5px;">EJECUCIÓN FINANCIERA MENSUAL DE LOS PROYECTOS / ACCIONES CENTRALIZADAS DEL ÓRGANO</h5>
        <p style="text-align: center; font-size: 8px; margin-bottom: 8px;">(En Bolívares)</p>
        
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 8px;">
            <thead style="background-color: #e2e8f0;">
                <tr>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">SIPES</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">Ppto.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px; width: 20%;">Denominación</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Programado</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Ejecutado Mensual</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Ejecutado Acumulado</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Variación Mes</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">Unidad Responsable</th>
                </tr>
                <tr>
                    <th style="border: 1px solid #000; padding: 3px;">Mensual</th>
                    <th style="border: 1px solid #000; padding: 3px;">Acumulado</th>
                    <th style="border: 1px solid #000; padding: 3px;">Compromiso</th>
                    <th style="border: 1px solid #000; padding: 3px;">Causado</th>
                    <th style="border: 1px solid #000; padding: 3px;">Compromiso</th>
                    <th style="border: 1px solid #000; padding: 3px;">Causado</th>
                    <th style="border: 1px solid #000; padding: 3px;">% Comp.</th>
                    <th style="border: 1px solid #000; padding: 3px;">% Caus.</th>
                </tr>
            </thead>
            <tbody>
                {filas_fin_html}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f1f5f9;">
                    <td colspan="3" style="border: 1px solid #000; padding: 4px; text-align: right;">TOTAL.....</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_pm:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_pa:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_cm:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_cam:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_ca:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_caa:,.2f}</td>
                    <td colspan="3" style="border: 1px solid #000; padding: 4px;"></td>
                </tr>
            </tfoot>
        </table>
        {html_firmas}
    """

    # 2. FORMATO 2: FINANCIERA POR PARTIDAS DE EGRESOS
    df_part = st.session_state.df_partidas
    filas_part_html = ""
    tot_cred, tot_pm_p, tot_cm_p, tot_cam_p, tot_pa_p, tot_ca_p, tot_caa_p = 0, 0, 0, 0, 0, 0, 0

    for _, row in df_part.iterrows():
        den = row.get("Denominación", "")
        if not den or str(den).strip() in ["None", ""]: continue

        cred = limpiar_val(row.get("Crédito Anual", 0))
        p_m = limpiar_val(row.get("Prog. Mes", 0))
        c_m = limpiar_val(row.get("Comp. Mes", 0))
        ca_m = limpiar_val(row.get("Caus. Mes", 0))
        p_a = limpiar_val(row.get("Prog. Acum.", 0))
        c_a = limpiar_val(row.get("Comp. Acum.", 0))
        ca_a = limpiar_val(row.get("Caus. Acum.", 0))

        var_abs = ca_a - p_a
        var_rel = ((var_abs) / p_a * 100) if p_a > 0 else 0.0

        tot_cred += cred; tot_pm_p += p_m; tot_cm_p += c_m; tot_cam_p += ca_m
        tot_pa_p += p_a; tot_ca_p += c_a; tot_caa_p += ca_a

        filas_part_html += f"""
            <tr>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px;">{row.get("Partida", "")}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px;">{row.get("Genérica", "")}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px;">{row.get("Específica", "")}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px;">{row.get("Sub-Esp", "")}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px;">{row.get("Conc", "")}</td>
                <td style="text-align: left; border: 1px solid #000; padding: 3px; font-size: 7px; width: 20%;">{den}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px; white-space: nowrap;">{cred:,.2f}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px; white-space: nowrap;">{p_m:,.2f}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px; white-space: nowrap;">{c_m:,.2f}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px; white-space: nowrap;">{ca_m:,.2f}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px; white-space: nowrap;">{p_a:,.2f}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px; white-space: nowrap;">{c_a:,.2f}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px; white-space: nowrap;">{ca_a:,.2f}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px; white-space: nowrap;">{var_abs:,.2f}</td>
                <td style="border: 1px solid #000; padding: 3px; font-size: 7px; white-space: nowrap;">{var_rel:.1f}%</td>
            </tr>
        """

    tot_v_abs = tot_caa_p - tot_pa_p
    tot_v_rel = (tot_v_abs / tot_pa_p * 100) if tot_pa_p > 0 else 0.0

    html_f2 = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 8px; font-size: 9px;">
            <div><strong>CÓDIGO DEL ÓRGANO:</strong> {c_org}<br><strong>DENOMINACIÓN DEL ÓRGANO:</strong> {d_org}<br><strong>MES:</strong> {m_rep}</div>
            <div><strong>FECHA:</strong> {f_rep}</div>
        </div>
        <h5 style="text-align: center; font-weight: bold; font-size: 11px; margin-bottom: 5px;">EJECUCIÓN FINANCIERA MENSUAL DE LOS PROYECTOS / ACCIONES CENTRALIZADAS DEL ÓRGANO, POR PARTIDAS DE EGRESOS</h5>
        <p style="text-align: center; font-size: 8px; margin-bottom: 8px;">(En Bolívares)</p>
        
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 8px;">
            <thead style="background-color: #e2e8f0;">
                <tr>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">PART.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">GEN.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">ESP.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">SUB.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">CONC.</th>
                    <th rowspan="2" style="width: 22%; border: 1px solid #000; padding: 3px;">DENOMINACIÓN</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">CRÉDITO ANUAL</th>
                    <th colspan="3" style="border: 1px solid #000; padding: 3px;">EJECUCIÓN MENSUAL</th>
                    <th colspan="3" style="border: 1px solid #000; padding: 3px;">EJECUCIÓN ACUMULADA</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">VARIACIÓN ACUMULADA</th>
                </tr>
                <tr>
                    <th style="border: 1px solid #000; padding: 3px;">PROG.</th>
                    <th style="border: 1px solid #000; padding: 3px;">COMP.</th>
                    <th style="border: 1px solid #000; padding: 3px;">CAUS.</th>
                    <th style="border: 1px solid #000; padding: 3px;">PROG.</th>
                    <th style="border: 1px solid #000; padding: 3px;">COMP.</th>
                    <th style="border: 1px solid #000; padding: 3px;">CAUS.</th>
                    <th style="border: 1px solid #000; padding: 3px;">ABSOLUTA</th>
                    <th style="border: 1px solid #000; padding: 3px;">%</th>
                </tr>
            </thead>
            <tbody>
                {filas_part_html}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f1f5f9;">
                    <td colspan="6" style="border: 1px solid #000; padding: 4px; text-align: right;">TOTAL PRESUPUESTO:</td>
                    <td style="border: 1px solid #000; padding: 4px; white-space: nowrap;">{tot_cred:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px; white-space: nowrap;">{tot_pm_p:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px; white-space: nowrap;">{tot_cm_p:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px; white-space: nowrap;">{tot_cam_p:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px; white-space: nowrap;">{tot_pa_p:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px; white-space: nowrap;">{tot_ca_p:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px; white-space: nowrap;">{tot_caa_p:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px; white-space: nowrap;">{tot_v_abs:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px; white-space: nowrap;">{tot_v_rel:.1f}%</td>
                </tr>
            </tfoot>
        </table>
        {html_firmas}
    """

    # 3. FORMATO 3: EJECUCIÓN FÍSICA PROYECTOS
    df_fis = st.session_state.df_fisica_proyectos
    filas_fis_html = ""
    tot_f_pm, tot_f_pa, tot_f_em, tot_f_ea = 0, 0, 0, 0

    for _, row in df_fis.iterrows():
        denom = row.get("Denominación", "")
        if not denom or str(denom).strip() in ["None", ""]: continue
        
        pm = limpiar_val(row.get("Meta Prog. Mensual", 0))
        pa = limpiar_val(row.get("Meta Prog. Acumulado", 0))
        em = limpiar_val(row.get("Meta Ejec. Mensual", 0))
        ea = limpiar_val(row.get("Meta Ejec. Acumulado", 0))

        tot_f_pm += pm; tot_f_pa += pa; tot_f_em += em; tot_f_ea += ea

        filas_fis_html += f"""
            <tr>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("SIPES", "")}</td>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("Ppto.", "")}</td>
                <td style="text-align: left; border: 1px solid #000; padding: 4px;">{denom}</td>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("Unidad de Medida", "")}</td>
                <td style="border: 1px solid #000; padding: 4px;">{pm:,.0f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{pa:,.0f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{em:,.0f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{ea:,.0f}</td>
                <td style="border: 1px solid #000; padding: 4px;">0</td>
                <td style="border: 1px solid #000; padding: 4px;">100%</td>
                <td style="border: 1px solid #000; padding: 4px;">0</td>
                <td style="border: 1px solid #000; padding: 4px;">100%</td>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("Unidad Responsable", u_eje)}</td>
            </tr>
        """

    html_f3 = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 8px; font-size: 9px;">
            <div><strong>CÓDIGO DEL ÓRGANO:</strong> {c_org}<br><strong>DENOMINACIÓN DEL ÓRGANO:</strong> {d_org}<br><strong>MES:</strong> {m_rep}</div>
            <div><strong>FECHA:</strong> {f_rep}</div>
        </div>
        <h5 style="text-align: center; font-weight: bold; font-size: 11px; margin-bottom: 5px;">EJECUCIÓN FÍSICA MENSUAL DE LOS PROYECTOS DEL ÓRGANO</h5>
        
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 8px;">
            <thead style="background-color: #e2e8f0;">
                <tr>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">SIPES</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">Ppto.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px; width: 18%;">Denominación</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">Unidad de Medida</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Meta Programada</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Meta Ejecutada</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Variación Mes</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Variación Acumulada</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">Unidad Responsable</th>
                </tr>
                <tr>
                    <th style="border: 1px solid #000; padding: 3px;">Mensual</th>
                    <th style="border: 1px solid #000; padding: 3px;">Acumulada</th>
                    <th style="border: 1px solid #000; padding: 3px;">Mensual</th>
                    <th style="border: 1px solid #000; padding: 3px;">Acumulada</th>
                    <th style="border: 1px solid #000; padding: 3px;">Absoluta</th>
                    <th style="border: 1px solid #000; padding: 3px;">Relativa %</th>
                    <th style="border: 1px solid #000; padding: 3px;">Absoluta</th>
                    <th style="border: 1px solid #000; padding: 3px;">Relativa %</th>
                </tr>
            </thead>
            <tbody>
                {filas_fis_html}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f1f5f9;">
                    <td colspan="4" style="border: 1px solid #000; padding: 4px; text-align: right;">TOTAL.....</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_f_pm:,.0f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_f_pa:,.0f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_f_em:,.0f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_f_ea:,.0f}</td>
                    <td colspan="5" style="border: 1px solid #000; padding: 4px;"></td>
                </tr>
            </tfoot>
        </table>
        {html_firmas}
    """

    # 4. FORMATO 4: CUADRO ANEXO FÍSICO
    df_cuad = st.session_state.df_cuadro_anexo
    filas_cuad_html = ""
    tot_n = 0

    for _, row in df_cuad.iterrows():
        op = row.get("Operación / Actividad", "")
        if not op or str(op).strip() in ["None", ""]: continue
        n = int(row.get("N°", 0))
        tot_n += n

        filas_cuad_html += f"""
            <tr>
                <td style="border: 1px solid #000; padding: 6px; text-align: center;">{n}</td>
                <td style="border: 1px solid #000; padding: 6px; text-align: left;">{op}</td>
            </tr>
        """

    html_f4 = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 8px; font-size: 9px;">
            <div><strong>UNIDAD:</strong> {u_eje}</div>
            <div><strong>MES:</strong> {m_rep}</div>
        </div>
        <h5 style="text-align: center; font-weight: bold; font-size: 11px; margin-bottom: 10px;">CUADRO ANEXO DE LA EJECUCIÓN FÍSICA DE LA UNIDAD EJECUTORA LOCAL</h5>
        
        <table style="width: 100%; border-collapse: collapse; font-size: 9px;">
            <thead style="background-color: #e2e8f0; text-align: center;">
                <tr>
                    <th style="border: 1px solid #000; padding: 5px; width: 10%;">N°</th>
                    <th style="border: 1px solid #000; padding: 5px; width: 90%;">OPERACIÓN / ACTIVIDAD</th>
                </tr>
            </thead>
            <tbody>
                {filas_cuad_html}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f1f5f9;">
                    <td style="border: 1px solid #000; padding: 5px; text-align: center;">{tot_n}</td>
                    <td style="border: 1px solid #000; padding: 5px; text-align: left;">TOTAL</td>
                </tr>
            </tfoot>
        </table>
        {html_firmas}
    """

    # Estructura HTML consolidada unificada con clases y saltos de página estrictos
    html_consolidado = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @media print {{
                @page {{
                    size: letter landscape !important;
                    margin: 0.5cm !important;
                }}
                body {{
                    background: #fff !important;
                    -webkit-print-color-adjust: exact;
                }}
                .hoja-formato {{
                    page-break-before: always !important;
                    page-break-after: always !important;
                    break-before: page !important;
                    break-after: page !important;
                    display: block !important;
                }}
                .hoja-formato:first-of-type {{
                    page-break-before: avoid !important;
                    break-before: avoid !important;
                }}
            }}
            .hoja-formato {{
                border: 2px solid #000;
                padding: 15px;
                background: #fff;
                font-family: Arial, sans-serif;
                color: #000;
                margin-bottom: 40px;
                box-sizing: border-box;
                width: 100%;
            }}
        </style>
    </head>
    <body>
        <div class="hoja-formato">{html_f1}</div>
        <div class="hoja-formato">{html_f2}</div>
        <div class="hoja-formato">{html_f3}</div>
        <div class="hoja-formato">{html_f4}</div>
    </body>
    </html>
    """

    st.info("💡 **Método infalible para el PDF horizontal:** Haz clic en el botón de abajo para **Descargar el Documento Completo**, ábrelo en tu navegador y presiona **Ctrl + P** para guardar tus 4 páginas independientes perfectamente adaptadas.")

    st.download_button(
        label="📥 Descargar / Guardar Documento Completo (HTML para Impresión)",
        data=html_consolidado,
        file_name="Instructivo_ONAPRE_06_Consolidado.html",
        mime="text/html",
        type="primary"
    )

    st.markdown("### Vista Previa en Pantalla")
    components.html(html_consolidado, height=900, scrolling=True)
