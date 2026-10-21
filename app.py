with tab4:
    st.subheader("Resumen e Impresión del Instructivo N° 06")
    st.markdown("---")
    
    # Recoger los datos del editor de la pestaña 1
    df_actual = st.session_state.df_obras
    
    filas_html = ""
    tot_p_mes, tot_c_mes, tot_ca_mes = 0, 0, 0
    tot_p_acum, tot_c_acum, tot_ca_acum = 0, 0, 0
    
    for index, row in df_actual.iterrows():
        p_mes = float(row["Prog. Mes"])
        co_mes = float(row["Comp. Mes"])
        ca_mes = float(row["Caus. Mes"])
        p_acum = float(row["Prog. Acum."])
        co_acum = float(row["Comp. Acum."])
        ca_acum = float(row["Caus. Acum."])
        
        # Fórmulas de Variación Oficial ONAPRE
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
                <td style="text-align: left; border: 1px solid #000; padding: 4px;">{row["Denominación de la Obra"]}</td>
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

    # Renderizado seguro por partes en Streamlit
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

    # Tabla con los datos dinámicos
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
    st.info("💡 **Listo:** Ahora el formato se renderizará correctamente en HTML con los datos que cargaste en la primera pestaña.")
