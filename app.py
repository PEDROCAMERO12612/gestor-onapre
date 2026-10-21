Import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Gestor ONAPRE - Instructivo N° 06", layout="wide")

st.title("Sistema de Gestión - Instructivo N° 06 (ONAPRE)")

# Declaración de pestañas principales
tab1, tab2, tab3, tab4 = st.tabs([
    "🏗️ Formulario 0601 (Obras)",
    "💰 Formulario 0602 (Financiero / Distribución)",
    "📈 Formulario 0603 (Físico)",
    "📋 Resumen y Consolidado"
])

with tab1:
    st.subheader("Formulario 0601: Carga y Ejecución Mensual de Obras")
    st.markdown("Ingrese o edite la distribución de obras. Para borrar una fila equivocada, selecciónela en la tabla y presione la tecla **Supr** o **Backspace**.")

    if "df_obras" not in st.session_state:
        st.session_state.df_obras = pd.DataFrame([
            {
                "Denominación de la Obra": "Construcción de Sede Principal",
                "Prog. Mes": 10000.0,
                "Comp. Mes": 9500.0,
                "Caus. Mes": 9000.0,
                "Prog. Acum.": 50000.0,
                "Comp. Acum.": 48000.0,
                "Caus. Acum.": 45000.0
            }
        ])

    st.session_state.df_obras = st.data_editor(
        st.session_state.df_obras, 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_obras"
    )

with tab2:
    st.subheader("Formulario 0602: Distribución Presupuestaria y Ejecución Financiera (SIGECOF)")
    st.markdown("""
    Cargue o edite las partidas presupuestarias anuales (Créditos, Programado y Ejecutado) correspondientes a su unidad ejecutora.  
    *💡 **Nota:** Puede agregar nuevas filas al final o borrar filas haciendo clic en el selector de fila y presionando `Supr`.*
    """)

    if "df_partidas" not in st.session_state:
        st.session_state.df_partidas = pd.DataFrame([
            {
                "Partida": "4.02", "Genérica": "01", "Específica": "01", "Sub-Esp": "00", "Conc": "200",
                "Denominación": "Alimentos y bebidas para personas", 
                "Crédito Anual (Bs.)": 40266.0,
                "Prog. Mes": 5000.0, "Comp. Mes": 4000.0, "Caus. Mes": 4000.0,
                "Prog. Acum.": 20000.0, "Comp. Acum.": 18000.0, "Caus. Acum.": 18000.0
            },
            {
                "Partida": "4.03", "Genérica": "09", "Específica": "01", "Sub-Esp": "00", "Conc": "200",
                "Denominación": "Viáticos y pasajes dentro del país", 
                "Crédito Anual (Bs.)": 12437.0,
                "Prog. Mes": 2000.0, "Comp. Mes": 1500.0, "Caus. Mes": 1500.0,
                "Prog. Acum.": 6000.0, "Comp. Acum.": 5500.0, "Caus. Acum.": 5500.0
            }
        ])

    st.session_state.df_partidas = st.data_editor(
        st.session_state.df_partidas,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_partidas"
    )

    st.markdown("---")
    st.text_area(
        "Explicación de las desviaciones financieras (Obligatorio si lo ejecutado difiere de lo programado)", 
        key="desviacion_0602"
    )

with tab3:
    st.subheader("Formulario 0603: Ejecución Física Mensual")
    unidad_medida = st.text_input("Unidad Física de Medida", key="0603_UM", value="Metros / Actividades / Unidades")
    st.markdown("Detalle la meta física programada y ejecutada del período.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Programada Mes", value=10.0, key="fis_prog_mes")
    with col2:
        st.number_input("Ejecutada Mes", value=8.0, key="fis_ejec_mes")
    with col3:
        st.number_input("Acumulada Ejecutada", value=35.0, key="fis_ejec_acum")

with tab4:
    st.subheader("Resumen e Impresión del Instructivo N° 06")
    st.markdown("---")
    
    def limpiar_val(val):
        try:
            return float(val) if val is not None and not pd.isna(val) else 0.0
        except:
            return 0.0

    # ==========================
    # 1. DATOS FORMULARIO 0601
    # ==========================
    df_obras = st.session_state.df_obras
    filas_obras_html = ""
    tot_p_mes, tot_c_mes, tot_ca_mes = 0, 0, 0
    tot_p_acum, tot_c_acum, tot_ca_acum = 0, 0, 0
    
    for index, row in df_obras.iterrows():
        nombre_obra = row.get("Denominación de la Obra", "")
        if not nombre_obra or pd.isna(nombre_obra) or str(nombre_obra).strip() in ["None", ""]:
            continue
            
        p_mes = limpiar_val(row.get("Prog. Mes", 0))
        co_mes = limpiar_val(row.get("Comp. Mes", 0))
        ca_mes = limpiar_val(row.get("Caus. Mes", 0))
        p_acum = limpiar_val(row.get("Prog. Acum.", 0))
        co_acum = limpiar_val(row.get("Comp. Acum.", 0))
        ca_acum = limpiar_val(row.get("Caus. Acum.", 0))
        
        var_abs = ca_acum - p_acum
        var_rel = (var_abs / p_acum * 100) if p_acum > 0 else 0.0
        
        tot_p_mes += p_mes
        tot_c_mes += co_mes
        tot_ca_mes += ca_mes
        tot_p_acum += p_acum
        tot_c_acum += co_acum
        tot_ca_acum += ca_acum
        
        filas_obras_html += f"""
            <tr>
                <td style="text-align: left; border: 1px solid #000; padding: 4px;">{nombre_obra}</td>
                <td style="border: 1px solid #000; padding: 4px;">{p_mes:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{co_mes:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{ca_mes:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{p_acum:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{co_acum:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{ca_acum:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{var_abs:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px;">{var_rel:.2f}%</td>
            </tr>
        """

    tot_var_abs_acum = tot_ca_acum - tot_p_acum
    tot_var_rel_acum = (tot_var_abs_acum / tot_p_acum * 100) if tot_p_acum > 0 else 0.0

    html_0601 = f"""
    <div style="border: 2px solid #000; padding: 15px; background: #fff; font-family: Arial, sans-serif; color: #000; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 8px; margin-bottom: 10px;">
            <div>
                <strong style="font-size: 11px;">REPÚBLICA BOLIVARIANA DE VENEZUELA</strong><br>
                <small style="font-size: 9px;">MINISTERIO DEL PODER POPULAR DE ECONOMÍA Y FINANZAS</small><br>
                <small style="font-size: 9px;">OFICINA NACIONAL DE PRESUPUESTO (ONAPRE)</small>
            </div>
            <div style="text-align: right;">
                <span style="border: 1px solid #000; padding: 4px 8px; font-weight: bold; font-size: 11px;">Formulario: 0601</span>
            </div>
        </div>
        
        <h5 style="text-align: center; font-weight: bold; font-size: 12px; margin-bottom: 2px;">EJECUCIÓN MENSUAL DE LAS OBRAS CONTENIDAS EN EL PROYECTO</h5>
        <p style="text-align: center; font-size: 9px; margin-bottom: 10px;">(En Bolívares)</p>
        
        <table style="width: 100%; border-collapse: collapse; text-align: center;">
            <thead style="background-color: #e2e8f0;">
                <tr>
                    <th rowspan="2" style="width: 25%; border: 1px solid #000; padding: 4px; font-size: 10px;">(9) DENOMINACIÓN DE LA OBRA</th>
                    <th colspan="3" style="border: 1px solid #000; padding: 4px; font-size: 10px;">(10) MES</th>
                    <th colspan="3" style="border: 1px solid #000; padding: 4px; font-size: 10px;">(11) ACUMULADO</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 4px; font-size: 10px;">(12-13) VARIACIÓN ACUMULADA</th>
                </tr>
                <tr>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">PROGRAMADO</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">COMPROMETIDO</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">CAUSADO</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">PROGRAMADO</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">COMPROMETIDO</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">CAUSADO</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">ABSOLUTA</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">%</th>
                </tr>
            </thead>
            <tbody>
                {filas_obras_html}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f1f5f9; font-size: 10px;">
                    <td style="border: 1px solid #000; padding: 4px;">(14) TOTAL OBRAS</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_p_mes:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_c_mes:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_ca_mes:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_p_acum:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_c_acum:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_ca_acum:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_var_abs_acum:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_var_rel_acum:.2f}%</td>
                </tr>
            </tfoot>
        </table>
    </div>
    """

    st.markdown("### Formato Oficial: 0601 (Obras)")
    components.html(html_0601, height=350, scrolling=True)

    # ==========================
    # 2. DATOS FORMULARIO 0602
    # ==========================
    df_partidas = st.session_state.df_partidas
    filas_partidas_html = ""
    tot_credito, tot_p_mes_f, tot_co_mes_f, tot_ca_mes_f = 0, 0, 0, 0
    tot_p_acum_f, tot_co_acum_f, tot_ca_acum_f = 0, 0, 0

    for index, row in df_partidas.iterrows():
        denominacion = row.get("Denominación", "")
        if not denominacion or pd.isna(denominacion) or str(denominacion).strip() in ["None", ""]:
            continue
            
        partida = row.get("Partida", "")
        generica = row.get("Genérica", "")
        especifica = row.get("Específica", "")
        sesp = row.get("Sub-Esp", "")
        conc = row.get("Conc", "")
        
        credito = limpiar_val(row.get("Crédito Anual (Bs.)", 0))
        p_mes_f = limpiar_val(row.get("Prog. Mes", 0))
        co_mes_f = limpiar_val(row.get("Comp. Mes", 0))
        ca_mes_f = limpiar_val(row.get("Caus. Mes", 0))
        p_acum_f = limpiar_val(row.get("Prog. Acum.", 0))
        co_acum_f = limpiar_val(row.get("Comp. Acum.", 0))
        ca_acum_f = limpiar_val(row.get("Caus. Acum.", 0))
        
        var_abs_f = ca_acum_f - p_acum_f
        var_rel_f = (var_abs_f / p_acum_f * 100) if p_acum_f > 0 else 0.0
        
        tot_credito += credito
        tot_p_mes_f += p_mes_f
        tot_co_mes_f += co_mes_f
        tot_ca_mes_f += ca_mes_f
        tot_p_acum_f += p_acum_f
        tot_co_acum_f += co_acum_f
        tot_ca_acum_f += ca_acum_f
        
        filas_partidas_html += f"""
            <tr>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{partida}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{generica}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{especifica}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{sesp}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{conc}</td>
                <td style="text-align: left; border: 1px solid #000; padding: 4px; font-size: 10px;">{denominacion}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{credito:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{p_mes_f:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{co_mes_f:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{ca_mes_f:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{p_acum_f:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{co_acum_f:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{ca_acum_f:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{var_abs_f:,.2f}</td>
                <td style="border: 1px solid #000; padding: 4px; font-size: 10px;">{var_rel_f:.2f}%</td>
            </tr>
        """

    tot_var_abs_f = tot_ca_acum_f - tot_p_acum_f
    tot_var_rel_f = (tot_var_abs_f / tot_p_acum_f * 100) if tot_p_acum_f > 0 else 0.0

    html_0602 = f"""
    <div style="border: 2px solid #000; padding: 15px; background: #fff; font-family: Arial, sans-serif; color: #000; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 8px; margin-bottom: 10px;">
            <div>
                <strong style="font-size: 11px;">REPÚBLICA BOLIVARIANA DE VENEZUELA</strong><br>
                <small style="font-size: 9px;">MINISTERIO DEL PODER POPULAR DE ECONOMÍA Y FINANZAS</small><br>
                <small style="font-size: 9px;">OFICINA NACIONAL DE PRESUPUESTO (ONAPRE)</small>
            </div>
            <div style="text-align: right;">
                <span style="border: 1px solid #000; padding: 4px 8px; font-weight: bold; font-size: 11px;">Formulario: 0602</span>
            </div>
        </div>
        
        <h5 style="text-align: center; font-weight: bold; font-size: 12px; margin-bottom: 2px;">EJECUCIÓN FINANCIERA MENSUAL POR PARTIDAS DE EGRESOS</h5>
        <p style="text-align: center; font-size: 9px; margin-bottom: 10px;">(En Bolívares)</p>
        
        <table style="width: 100%; border-collapse: collapse; text-align: center;">
            <thead style="background-color: #e2e8f0;">
                <tr>
                    <th rowspan="2" style="border: 1px solid #000; padding: 4px; font-size: 10px;">PART.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 4px; font-size: 10px;">GEN.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 4px; font-size: 10px;">ESP.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 4px; font-size: 10px;">SESP.</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 4px; font-size: 10px;">CONC.</th>
                    <th rowspan="2" style="width: 20%; border: 1px solid #000; padding: 4px; font-size: 10px;">DENOMINACIÓN</th>
                    <th rowspan="2" style="border: 1px solid #000; padding: 4px; font-size: 10px;">CRÉDITO PRESUPUESTARIO</th>
                    <th colspan="3" style="border: 1px solid #000; padding: 4px; font-size: 10px;">MES</th>
                    <th colspan="3" style="border: 1px solid #000; padding: 4px; font-size: 10px;">ACUMULADO</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 4px; font-size: 10px;">VARIACIÓN ACUMULADA</th>
                </tr>
                <tr>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">PROG.</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">COMP.</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">CAUS.</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">PROG.</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">COMP.</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">CAUS.</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">ABSOLUTA</th>
                    <th style="border: 1px solid #000; padding: 4px; font-size: 10px;">%</th>
                </tr>
            </thead>
            <tbody>
                {filas_partidas_html}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f1f5f9; font-size: 10px;">
                    <td colspan="6" style="border: 1px solid #000; padding: 4px; text-align: right;">TOTAL PRESUPUESTO:</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_credito:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_p_mes_f:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_co_mes_f:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_ca_mes_f:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_p_acum_f:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_co_acum_f:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_ca_acum_f:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_var_abs_f:,.2f}</td>
                    <td style="border: 1px solid #000; padding: 4px;">{tot_var_rel_f:.2f}%</td>
                </tr>
            </tfoot>
        </table>
    </div>
    """

    st.markdown("### Formato Oficial: 0602 (Financiero por Partidas)")
    components.html(html_0602, height=400, scrolling=True)

    desv = st.session_state.get("desviacion_0602", "")
    if desv:
        st.markdown(f"""
        <div style="border: 1px solid #000; padding: 10px; background: #fff; color: #000; margin-top: 10px;">
            <strong>Explicación de Desviaciones (Formulario 0602):</strong>
            <p style="font-size: 10px; margin-top: 5px;">{desv}</p>
        </div>
        """, unsafe_allow_html=True)
