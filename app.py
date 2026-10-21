import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Gestor ONAPRE - Instructivo N° 06", layout="wide")

st.title("Sistema de Gestión - Instructivo N° 06 (ONAPRE)")

# Botón de reinicio directo en la parte superior principal
col_tit, col_btn = st.columns([4, 1])
with col_btn:
    if st.button("🔄 Reiniciar / Borrar Datos", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown("---")

# Declaración de las 4 pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. Ejecución Financiera",
    "📈 2. Ejecución Física Proyectos",
    "📋 3. Cuadro Anexo Ejecución Física",
    "🖨️ Resumen y Exportación PDF"
])

# ==========================================
# PESTAÑA 1: EJECUCIÓN FINANCIERA
# ==========================================
with tab1:
    st.subheader("Formulario 1: Ejecución Financiera Mensual de Proyectos / Acciones Centralizadas")
    st.markdown("Cargue un archivo Excel con su data o edite directamente en la tabla:")

    archivo_fin = st.file_uploader("📂 Cargar Excel (Ejecución Financiera)", type=["xlsx"], key="up_fin")

    if "df_financiera" not in st.session_state:
        st.session_state.df_financiera = pd.DataFrame([
            {
                "SIPES": "07815", "Ppto.": 29884, 
                "Denominación": '12 BRIGADA DE CARIBES "G/J. ALMIDIEN RAMON MORENO ACOSTA"', 
                "Prog. Mensual": 2655226.00, "Prog. Acumulado": 15931356.00,
                "Ejec. Mensual Comprometido": 0.00, "Ejec. Mensual Causado": 0.00,
                "Ejec. Acumulado Comprometido": 0.00, "Ejec. Acumulado Causado": 0.00,
                "Unidad Responsable": "12 BRIGADA CARIBES"
            }
        ])

    if archivo_fin is not None:
        try:
            st.session_state.df_financiera = pd.read_excel(archivo_fin)
            st.success("✅ Datos financieros cargados exitosamente desde el archivo.")
        except Exception as e:
            st.error(f"❌ Error al leer el archivo: {e}")

    st.session_state.df_financiera = st.data_editor(
        st.session_state.df_financiera, 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_financiera"
    )

# ==========================================
# PESTAÑA 2: EJECUCIÓN FÍSICA PROYECTOS
# ==========================================
with tab2:
    st.subheader("Formulario 2: Ejecución Física Mensual de los Proyectos del Órgano")
    st.markdown("Cargue un archivo Excel o modifique las metas físicas del período:")

    archivo_fis = st.file_uploader("📂 Cargar Excel (Ejecución Física Proyectos)", type=["xlsx"], key="up_fis")

    if "df_fisica_proyectos" not in st.session_state:
        st.session_state.df_fisica_proyectos = pd.DataFrame([
            {
                "SIPES": "07815", "Ppto.": 29884, 
                "Denominación": '12 BRIGADA DE CARIBES "G/J. ALMIDIEN RAMON MORENO ACOSTA"', 
                "Unidad de Medida": "OPERACIONES MILITARES", 
                "Meta Prog. Mensual": 3.0, "Meta Prog. Acumulado": 3.0,
                "Meta Ejec. Mensual": 3.0, "Meta Ejec. Acumulado": 3.0,
                "Unidad Responsable": "12 BRIGADA CARIBES"
            }
        ])

    if archivo_fis is not None:
        try:
            st.session_state.df_fisica_proyectos = pd.read_excel(archivo_fis)
            st.success("✅ Datos de ejecución física cargados exitosamente.")
        except Exception as e:
            st.error(f"❌ Error al leer el archivo: {e}")

    st.session_state.df_fisica_proyectos = st.data_editor(
        st.session_state.df_fisica_proyectos, 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_fisica_proyectos"
    )

# ==========================================
# PESTAÑA 3: CUADRO ANEXO EJECUCIÓN FÍSICA
# ==========================================
with tab3:
    st.subheader("Formulario 3: Cuadro Anexo de la Ejecución Física (Unidad Ejecutora Local)")
    st.markdown("Cargue un archivo Excel o desglose el listado de operaciones y actividades:")

    archivo_cua = st.file_uploader("📂 Cargar Excel (Cuadro Anexo)", type=["xlsx"], key="up_cua")

    if "df_cuadro_anexo" not in st.session_state:
        st.session_state.df_cuadro_anexo = pd.DataFrame([
            {
                "Unidad": '12 BRIGADA DE CARIBES "G/J. ALMIDIEN RAMON MORENO ACOSTA"',
                "N°": 2,
                "Operación / Actividad": "PLANIFICACION Y SUPERVISION DE LAS ACTIVIDADES CIVICO-MILITARES EFECTUADAS POR LAS UNIDADES ADSCRITAS A ESTA UNIDAD SUPERIOR"
            },
            {
                "Unidad": '12 BRIGADA DE CARIBES "G/J. ALMIDIEN RAMON MORENO ACOSTA"',
                "N°": 1,
                "Operación / Actividad": "MANTENIMIENTO DE EQUIPOS E INSTALACIONES"
            },
            {
                "Unidad": '12 BRIGADA DE CARIBES "G/J. ALMIDIEN RAMON MORENO ACOSTA"',
                "N°": 1,
                "Operación / Actividad": "SEGURIDAD Y RESGUARDO DE INSTALACIONES Y EQUIPOS DE LA UNIDAD"
            },
            {
                "Unidad": '12 BRIGADA DE CARIBES "G/J. ALMIDIEN RAMON MORENO ACOSTA"',
                "N°": 2,
                "Operación / Actividad": "DESPLIEGUE Y CONDUCCION DE LA OPERACION MILITAR ESCUDO BOLIVARIANO 2026."
            }
        ])

    if archivo_cua is not None:
        try:
            st.session_state.df_cuadro_anexo = pd.read_excel(archivo_cua)
            st.success("✅ Cuadro anexo cargado exitosamente.")
        except Exception as e:
            st.error(f"❌ Error al leer el archivo: {e}")

    st.session_state.df_cuadro_anexo = st.data_editor(
        st.session_state.df_cuadro_anexo, 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_cuadro_anexo"
    )

# ==========================================
# PESTAÑA 4: RESUMEN Y EXPORTACIÓN UNIFICADA PDF
# ==========================================
with tab4:
    st.subheader("Resumen Consolidado e Impresión del Instructivo N° 06")
    st.markdown("---")
    st.info("💡 **Instrucción de PDF:** Presiona **Ctrl + P** en tu teclado para exportar los tres formatos oficiales en un solo documento organizado.")

    def limpiar_val(val):
        try:
            return float(val) if val is not None and not pd.isna(val) else 0.0
        except:
            return 0.0

    # 1. RENDERIZAR FORMATO 1 (FINANCIERA)
    df_fin = st.session_state.df_financiera
    filas_fin_html = ""
    t_prog_m, t_prog_a, t_comp_m, t_caus_m, t_comp_a, t_caus_a = 0, 0, 0, 0, 0, 0

    for _, row in df_fin.iterrows():
        denom = row.get("Denominación", "")
        if not denom or str(denom).strip() in ["None", ""]: continue
        
        p_m = limpiar_val(row.get("Prog. Mensual", 0))
        p_a = limpiar_val(row.get("Prog. Acumulado", 0))
        c_m = limpiar_val(row.get("Ejec. Mensual Comprometido", 0))
        ca_m = limpiar_val(row.get("Ejec. Mensual Causado", 0))
        c_a = limpiar_val(row.get("Ejec. Acumulado Comprometido", 0))
        ca_a = limpiar_val(row.get("Ejec. Acumulado Causado", 0))
        
        v_comp_mes = ((c_m - p_m) / p_m * 100) if p_m > 0 else -100.0
        v_caus_mes = ((ca_m - p_m) / p_m * 100) if p_m > 0 else -100.0

        t_prog_m += p_m; t_prog_a += p_a; t_comp_m += c_m; t_caus_m += ca_m; t_comp_a += c_a; t_caus_a += ca_a

        filas_fin_html += f"""
            <tr>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("SIPES", "")}</td>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("Ppto.", "")}</td>
                <td style="text-align: left; border: 1px solid #000; padding: 4px;">{denom}</td>
                <td style="border: 1px solid #000; padding: 4px;">{p_m:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{p_a:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{c_m:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{ca_m:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{c_a:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{ca_a:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{v_comp_mes:.0f}%</td>
                <td style="border: 1px solid #000; padding: 4px;">{v_caus_mes:.0f}%</td>
                <td style="border: 1px solid #000; padding: 4px;">{row.get("Unidad Responsable", "")}</td>
            </tr>
        """

    html_f1 = f"""
    <div style="border: 2px solid #000; padding: 12px; background: #fff; font-family: Arial, sans-serif; color: #000; margin-bottom: 30px; page-break-after: always;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 8px; font-size: 9px;">
            <div><strong>CÓDIGO DEL ÓRGANO:</strong> 008<br><strong>DENOMINACIÓN DEL ÓRGANO:</strong> MINISTERIO DEL PODER POPULAR PARA LA DEFENSA<br><strong>MES:</strong> JULIO</div>
            <div><strong>FECHA:</strong> 31/07/2026</div>
        </div>
        <h5 style="text-align: center; font-weight: bold; font-size: 11px; margin-bottom: 5px;">EJECUCIÓN FINANCIERA MENSUAL DE LOS PROYECTOS/ACCIONES CENTRALIZADAS DEL ÓRGANO</h5>
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
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">Unidad Responsable de la Ejecución</th>
                </tr>
                <tr>
                    <th style="border: 1px solid #000; padding: 3px;">Mensual</th>
                    <th style="border: 1px solid #000; padding: 3px;">Acumulado</th>
                    <th style="border: 1px solid #000; padding: 3px;">Compromiso</th>
                    <th style="border: 1px solid #000; padding: 3px;">Causado</th>
                    <th style="border: 1px solid #000; padding: 3px;">Compromiso</th>
                    <th style="border: 1px solid #000; padding: 3px;">Causado</th>
                    <th style="border: 1px solid #000; padding: 3px;">% Compromiso</th>
                    <th style="border: 1px solid #000; padding: 3px;">% Causado</th>
                </tr>
            </thead>
            <tbody>
                {filas_fin_html}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f1f5f9;">
                    <td colspan="3" style="border: 1px solid #000; padding: 4px; text-align: right;">TOTAL.....</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_prog_m:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_prog_a:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_comp_m:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_caus_m:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_comp_a:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_caus_a:,.2f}</td>
                    <td colspan="3" style="border: 1px solid #000; padding: 4px;"></td>
                </tr>
            </tfoot>
        </table>

        <!-- Firmas con solo los cargos -->
        <div style="display: flex; justify-content: space-between; margin-top: 25px; font-size: 8px; text-align: center;">
            <div>_________________________________<br><strong>PROGRAMADOR</strong></div>
            <div>_________________________________<br><strong>ADMINISTRADOR</strong></div>
            <div>_________________________________<br><strong>COMANDANTE</strong></div>
        </div>
    </div>
    """

    # 2. RENDERIZAR FORMATO 2 (FÍSICA PROYECTOS)
    df_fis = st.session_state.df_fisica_proyectos
    filas_fis_html = ""
    t_pm, t_pa, t_em, t_ea = 0, 0, 0, 0

    for _, row in df_fis.iterrows():
        denom = row.get("Denominación", "")
        if not denom or str(denom).strip() in ["None", ""]: continue
        
        pm = limpiar_val(row.get("Meta Prog. Mensual", 0))
        pa = limpiar_val(row.get("Meta Prog. Acumulado", 0))
        em = limpiar_val(row.get("Meta Ejec. Mensual", 0))
        ea = limpiar_val(row.get("Meta Ejec. Acumulado", 0))

        t_pm += pm; t_pa += pa; t_em += em; t_ea += ea

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
                <td style="border: 1px solid #000; padding: 4px;">{row.get("Unidad Responsable", "")}</td>
            </tr>
        """

    html_f2 = f"""
    <div style="border: 2px solid #000; padding: 12px; background: #fff; font-family: Arial, sans-serif; color: #000; margin-bottom: 30px; page-break-after: always;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 8px; font-size: 9px;">
            <div><strong>CÓDIGO DEL ÓRGANO:</strong> 008<br><strong>DENOMINACIÓN DEL ÓRGANO:</strong> MINISTERIO DEL PODER POPULAR PARA LA DEFENSA<br><strong>MES:</strong> JULIO</div>
            <div><strong>FECHA:</strong> 31/07/2026</div>
        </div>
        <h5 style="text-align: center; font-weight: bold; font-size: 11px; margin-bottom: 5px;">EJECUCIÓN FÍSICA MENSUAL DE LOS PROYECTOS DEL ÓRGANO</h5>
        
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 8px;">
            <thead style="background-color: #e2e8f0;">
                <tr>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">SIPES</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">Ppto.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px; width: 18%;">Denominación</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">Unidad de Medida</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Meta del Proyecto Programada</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Meta del Proyecto Ejecutada</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Variación Mes</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 3px;">Variación Acumulada</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 3px;">Unidad Responsable de la Ejecución</th>
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
                    <td style="border: 1px solid #000; padding: 4px;">{t_pm:,.0f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_pa:,.0f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_em:,.0f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{t_ea:,.0f}</td>
                    <td colspan="5" style="border: 1px solid #000; padding: 4px;"></td>
                </tr>
            </tfoot>
        </table>

        <!-- Firmas con solo los cargos -->
        <div style="display: flex; justify-content: space-between; margin-top: 25px; font-size: 8px; text-align: center;">
            <div>_________________________________<br><strong>PROGRAMADOR</strong></div>
            <div>_________________________________<br><strong>ADMINISTRADOR</strong></div>
            <div>_________________________________<br><strong>COMANDANTE</strong></div>
        </div>
    </div>
    """

    # 3. RENDERIZAR FORMATO 3 (CUADRO ANEXO FÍSICA)
    df_cuadro = st.session_state.df_cuadro_anexo
    filas_cuadro_html = ""
    total_n = 0

    for _, row in df_cuadro.iterrows():
        op = row.get("Operación / Actividad", "")
        if not op or str(op).strip() in ["None", ""]: continue
        n = int(row.get("N°", 0))
        total_n += n

        filas_cuadro_html += f"""
            <tr>
                <td style="border: 1px solid #000; padding: 6px; text-align: center;">{n}</td>
                <td style="border: 1px solid #000; padding: 6px; text-align: left;">{op}</td>
            </tr>
        """

    html_f3 = f"""
    <div style="border: 2px solid #000; padding: 12px; background: #fff; font-family: Arial, sans-serif; color: #000; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 8px; font-size: 9px;">
            <div><strong>UNIDAD:</strong> 12 BRIGADA DE CARIBES "G/J. ALMIDIEN RAMON MORENO ACOSTA"</div>
            <div><strong>MES:</strong> JULIO</div>
        </div>
        <h5 style="text-align: center; font-weight: bold; font-size: 11px; margin-bottom: 10px;">CUADRO ANEXO DE LA EJECUCION FISICA DE LA UNIDAD EJECUTORA LOCAL</h5>
        
        <table style="width: 100%; border-collapse: collapse; font-size: 9px;">
            <thead style="background-color: #e2e8f0; text-align: center;">
                <tr>
                    <th style="border: 1px solid #000; padding: 5px; width: 10%;">N°</th>
                    <th style="border: 1px solid #000; padding: 5px; width: 90%;">OPERACIÓN</th>
                </tr>
            </thead>
            <tbody>
                {filas_cuadro_html}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f1f5f9;">
                    <td style="border: 1px solid #000; padding: 5px; text-align: center;">{total_n}</td>
                    <td style="border: 1px solid #000; padding: 5px; text-align: left;">TOTAL</td>
                </tr>
            </tfoot>
        </table>

        <!-- Firmas con solo los cargos -->
        <div style="display: flex; justify-content: space-between; margin-top: 25px; font-size: 8px; text-align: center;">
            <div>_________________________________<br><strong>PROGRAMADOR</strong></div>
            <div>_________________________________<br><strong>ADMINISTRADOR</strong></div>
            <div>_________________________________<br><strong>COMANDANTE</strong></div>
        </div>
    </div>
    """

    # Bloque consolidado unificado para PDF
    html_consolidado_total = f"""
    <html>
    <head>
        <style>
            @media print {{
                @page {{ size: letter landscape; margin: 0.5cm; }}
                body {{ background: #fff !important; }}
            }}
        </style>
    </head>
    <body>
        {html_f1}
        {html_f2}
        {html_f3}
    </body>
    </html>
    """

    st.markdown("### Vista Consolidada de los 3 Formatos Oficiales")
    components.html(html_consolidado_total, height=850, scrolling=True)
