import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestor ONAPRE - Instructivo N° 06", layout="wide")

st.title("Sistema de Gestión - Instructivo N° 06 (ONAPRE)")

# Estilos CSS para el formato oficial e impresión
st.markdown("""
<style>
@media print {
    [data-testid="stSidebar"], .stButton, header, footer {
        display: none !important;
    }
    @page {
        size: letter landscape;
        margin: 0.5cm;
    }
    body {
        background: #fff !important;
    }
}
.formato-onapre {
    border: 2px solid #000;
    padding: 15px;
    background: #fff;
    font-family: Arial, sans-serif;
    color: #000;
    margin-bottom: 20px;
}
.tabla-onapre th, .tabla-onapre td {
    border: 1px solid #000 !important;
    text-align: center;
    vertical-align: middle;
    font-size: 10px;
    padding: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# Declaración de pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "🏗️ Formulario 0601 (Obras)",
    "💰 Formulario 0602 (Financiero)",
    "📈 Formulario 0603 (Físico)",
    "📋 Resumen y Consolidado"
])

with tab1:
    st.subheader("Formulario 0601: Carga y Ejecución Mensual de Obras")
    st.markdown("Ingrese o edite la distribución y los montos ejecutados directamente en la tabla inferior:")

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
    st.subheader("Formulario 0602: Ejecución Financiera Mensual por Partidas")
    st.markdown("Control de partidas, genéricas, específicas y subespecíficas (SIGECOF)")
    st.text_area("Explicación de Desviaciones (Obligatorio si lo ejecutado difiere de lo programado)", key="desviacion_0602")

with tab3:
    st.subheader("Formulario 0603: Ejecución Física Mensual")
    unidad_medida = st.text_input("Unidad Física de Medida", key="0603_UM")

with tab4:
    st.subheader("Resumen e Impresión del Instructivo N° 06")
    st.markdown("---")
    
    df_actual = st.session_state.df_obras
    
    filas_html = ""
    tot_p_mes, tot_c_mes, tot_ca_mes = 0, 0, 0
    tot_p_acum, tot_c_acum, tot_ca_acum = 0, 0, 0
    
    for index, row in df_actual.iterrows():
        # Validar si el nombre de la obra está vacío o es nulo para omitir filas vacías
        nombre_obra = row["Denominación de la Obra"]
        if not nombre_obra or pd.isna(nombre_obra) or str(nombre_obra).strip() == "None":
            continue
            
        # Función auxiliar segura para convertir valores a float evitando errores por celdas vacías
        def limpiar_val(val):
            try:
                return float(val) if val is not None and not pd.isna(val) else 0.0
            except:
                return 0.0

        p_mes = limpiar_val(row["Prog. Mes"])
        co_mes = limpiar_val(row["Comp. Mes"])
        ca_mes = limpiar_val(row["Caus. Mes"])
        p_acum = limpiar_val(row["Prog. Acum."])
        co_acum = limpiar_val(row["Comp. Acum."])
        ca_acum = limpiar_val(row["Caus. Acum."])
        
        # Fórmulas Oficiales ONAPRE
        var_abs = ca_acum - p_acum
        var_rel = (var_abs / p_acum * 100) if p_acum > 0 else 0.0
        
        tot_p_mes += p_mes
        tot_c_mes += co_mes
        tot_ca_mes += ca_mes
        tot_p_acum += p_acum
        tot_c_acum += co_acum
        tot_ca_acum += ca_acum
        
        filas_html += f"""
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

    st.markdown("""
    <div class="formato-onapre">
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
        
        <div style="border: 1px solid #000; padding: 6px; font-size: 10px; margin-bottom: 10px; background-color: #f8f9fa;">
            <div><strong>(1) CÓDIGO PRESUPUESTARIO DEL ÓRGANO:</strong> ______________ &nbsp;&nbsp;&nbsp; <strong>DENOMINACIÓN:</strong> ________________________________</div>
            <div style="margin-top: 4px;"><strong>(2) PROYECTO:</strong> ________________________________________________________________________________</div>
        </div>
    """, unsafe_allow_html=True)

    tabla_completa = f"""
        <table class="table table-bordered tabla-onapre" style="width: 100%; border-collapse: collapse;">
            <thead style="background-color: #e2e8f0;">
                <tr>
                    <th rowspan="2" style="width: 25%; border: 1px solid #000; padding: 4px;">(9) DENOMINACIÓN DE LA OBRA</th>
                    <th colspan="3" style="border: 1px solid #000; padding: 4px;">(10) MES</th>
                    <th colspan="3" style="border: 1px solid #000; padding: 4px;">(11) ACUMULADO</th>
                    <th colspan="2" style="border: 1px solid #000; padding: 4px;">(12-13) VARIACIÓN ACUMULADA</th>
                </tr>
                <tr>
                    <th style="border: 1px solid #000; padding: 4px;">PROGRAMADO</th>
                    <th style="border: 1px solid #000; padding: 4px;">COMPROMETIDO</th>
                    <th style="border: 1px solid #000; padding: 4px;">CAUSADO</th>
                    <th style="border: 1px solid #000; padding: 4px;">PROGRAMADO</th>
                    <th style="border: 1px solid #000; padding: 4px;">COMPROMETIDO</th>
                    <th style="border: 1px solid #000; padding: 4px;">CAUSADO</th>
                    <th style="border: 1px solid #000; padding: 4px;">ABSOLUTA</th>
                    <th style="border: 1px solid #000; padding: 4px;">%</th>
                </tr>
            </thead>
            <tbody>
                {filas_html}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f1f5f9;">
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
    
    st.markdown(tabla_completa, unsafe_allow_html=True)
    st.info("💡 **Listo:** Las filas vacías o nulas se ignoran automáticamente para evitar errores. Presiona **Ctrl + P** para exportarlo como PDF.")
