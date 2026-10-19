import streamlit as st
import pandas as pd

# Configuración inicial de las pestañas que ya tienes definidas
tab1, tab2, tab3, tab4 = st.tabs([
    "🏗️ Formulario 0601 (Obras)",
    "💰 Formulario 0602 (Financiero)",
    "📈 Formulario 0603 (Físico)",
    "📋 Resumen y Consolidado"
])

with tab1:
    st.subheader("Formulario 0601: Ejecución Mensual de las Obras Contenidas en el Proyecto")
    st.markdown("---")
    
    # Ejemplo de campos para el formulario 0601 exigidos por la ONAPRE
    col1, col2 = st.columns(2)
    with col1:
        sipes_ae = st.text_input("Código SIPES de la Acción Específica", key="0601_sipes")
        den_obra = st.text_input("Denominación de la Obra", key="0601_obra")
    with col2:
        prog_mes = st.number_input("Programado Mes (Bs.)", min_value=0.0, key="0601_p_mes")
        caus_mes = st.number_input("Causado Mes (Bs.)", min_value=0.0, key="0601_c_mes")
        prog_acum = st.number_input("Programado Acumulado (Bs.)", min_value=0.0, key="0601_p_acum")
        caus_acum = st.number_input("Causado Acumulado (Bs.)", min_value=0.0, key="0601_c_acum")
    
    # Cálculo automático de Variación Absoluta y Relativa (Fórmulas ONAPRE)
    var_abs_acum = caus_acum - prog_acum
    var_rel_acum = (var_abs_acum / prog_acum * 100) if prog_acum > 0 else 0.0
    
    st.info(f"**Variación Absoluta Acumulada:** Bs. {var_abs_acum:,.2f} | **Variación Relativa Acumulada:** {var_rel_acum:.2f}%")

with tab2:
    st.subheader("Formulario 0602: Ejecución Financiera Mensual por Partidas de Egresos")
    st.markdown("Visualización de partidas, genéricas, específicas y subespecíficas (SIGECOF)")
    
    # Simulación de tabla con las columnas del instructivo
    data_ejemplo = pd.DataFrame({
        "Partida": ["401", "402"],
        "Genérica": ["01", "03"],
        "Específica": ["01", "00"],
        "Denominación": ["Gastos de Personal", "Materiales y Suministros"],
        "Comprometido Prog. Acum.": [100000.0, 50000.0],
        "Comprometido Ejec. Acum.": [95000.0, 50000.0]
    })
    st.dataframe(data_ejemplo, use_container_width=True)
    
    # Campo obligatorio para justificar desviaciones según nota del instructivo
    st.text_area("Explicación de Desviaciones (Obligatorio si lo ejecutado difiere de lo programado)", key="desviacion_0602")

with tab3:
    st.subheader("Formulario 0603: Ejecución Física Mensual de los Proyectos")
    st.markdown("Control de metas físicas programadas vs. ejecutadas.")
    unidad_medida = st.text_input("Unidad Física de Medida (Ej. Metros, Kilómetros, Talleres)", key="0603_UM")
    meta_prog = st.number_input("Meta Programada Acumulada", min_value=0.0, key="0603_m_prog")
    meta_ejec = st.number_input("Meta Ejecutada Acumulada", min_value=0.0, key="0603_m_ejec")

with tab4:
    st.subheader("Resumen e Impresión del Instructivo N° 06")
    st.success("Los datos están listos para la validación y consolidación exigida dentro de los primeros 5 días del mes.")
    
    if st.button("🖨️ Generar Vista de Impresión / Reporte Oficial"):
        st.balloons()
        st.warning("Para exportar formalmente, presiona Ctrl + P en tu navegador y selecciona 'Guardar como PDF' con orientación horizontal.")
