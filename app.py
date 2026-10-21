import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Gestor ONAPRE - Instructivo N° 06", layout="wide")

st.title("Sistema de Gestión - Instructivo N° 06 (ONAPRE)")

# Estilos CSS específicos para ocultar elementos de Streamlit al imprimir y mostrar el formato oficial
st.markdown("""
<style>
@media print {
    /* Ocultar la barra lateral, botones y menús de Streamlit al imprimir */
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

# Pestañas principales
tab1, tab2, tab3, tab4 = st.tabs([
    "🏗️ Formulario 0601 (Obras)",
    "💰 Formulario 0602 (Financiero)",
    "📈 Formulario 0603 (Físico)",
    "📋 Resumen y Consolidado"
])

with tab1:
    st.subheader("Formulario 0601: Ejecución Mensual de las Obras Contenidas en el Proyecto")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        sipes_ae = st.text_input("Código SIPES de la Acción Específica", key="0601_sipes")
        den_obra = st.text_input("Denominación de la Obra", key="0601_obra")
    with col2:
        prog_mes = st.number_input("Programado Mes (Bs.)", min_value=0.0, key="0601_p_mes")
        caus_mes = st.number_input("Causado Mes (Bs.)", min_value=0.0, key="0601_c_mes")
        prog_acum = st.number_input("Programado Acumulado (Bs.)", min_value=0.0, key="0601_p_acum")
        caus_acum = st.number_input("Causado Acumulado (Bs.)", min_value=0.0, key="0601_c_acum")
    
    var_abs_acum = caus_acum - prog_acum
    var_rel_acum = (var_abs_acum / prog_acum * 100) if prog_acum > 0 else 0.0
    
    st.info(f"**Variación Absoluta Acumulada:** Bs. {var_abs_acum:,.2f} | **Variación Relativa Acumulada:** {var_rel_acum:.2f}%")

with tab2:
    st.subheader("Formulario 0602: Ejecución Financiera Mensual por Partidas de Egresos")
    st.markdown("Visualización de partidas, genéricas, específicas y subespecíficas (SIGECOF)")
    st.text_area("Explicación de Desviaciones (Obligatorio si lo ejecutado difiere de lo programado)", key="desviacion_0602")

with tab3:
    st.subheader("Formulario 0603: Ejecución Física Mensual de los Proyectos")
    unidad_medida = st.text_input("Unidad Física de Medida", key="0603_UM")
    meta_prog = st.number_input("Meta Programada Acumulada", min_value=0.0, key="0603_m_prog")
    meta_ejec = st.number_input("Meta Ejecutada Acumulada", min_value=0.0, key="0603_m_ejec")

with tab4:
    st.subheader("Resumen e Impresión del Instructivo N° 06")
    st.markdown("---")
    
    # HTML del Formulario Oficial ONAPRE estructurado para la vista y exportación PDF
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
                <tr>
                    <td style="text-align: left; border: 1px solid #000; padding: 4px;">Construcción de Sede Principal</td>
                    <td style="border: 1px solid #000; padding: 4px;">0,00</td>
                    <td style="border: 1px solid #000; padding: 4px;">0,00</td>
                    <td style="border: 1px solid #000; padding: 4px;">0,00</td>
                    <td style="border: 1px solid #000; padding: 4px;">0,00</td>
                    <td style="border: 1px solid #000; padding: 4px;">0,00</td>
                    <td style="border: 1px solid #000; padding: 4px;">0,00</td>
                    <td style="border: 1px solid #000; padding: 4px;">0,00</td>
                    <td style="border: 1px solid #000; padding: 4px;">0,00%</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Para exportar al formato exacto:** Presiona **Ctrl + P** en tu navegador, selecciona la orientación **Horizontal (Landscape)** y guarda como PDF.")
