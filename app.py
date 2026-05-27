import streamlit as st
import pandas as pd
import database as db

# Configuración de página
st.set_page_config(page_title="Vigilancia Montebello", layout="wide")
db.inicializar_db()

st.title("🛡️ Sistema de Gestión - Vigilancia Montebello")
st.write("Control de aportes mensuales, morosidad y actualización de base de datos.")
st.markdown("---")

# --- MENÚ LATERAL ---
menu = ["📊 Dashboard", "👥 Residentes (CRUD)", "💰 Registrar Pagos"]
opcion = st.sidebar.selectbox("Seleccione una opción", menu)

# --- VISTA 1: DASHBOARD ---
if opcion == "📊 Dashboard":
    st.subheader("Indicadores Clave de Rendimiento (KPIs)")
    
    raw_data = db.obtener_matriz_pagos()
    if raw_data:
        df = pd.DataFrame(raw_data, columns=["ID", "Nombre", "Lote", "Mes", "Año", "Monto", "Estado"])
        
        # Métricas
        total_recaudado = df["Monto"].sum()
        total_residentes = len(db.obtener_residentes())
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Recaudado Histórico", f"S/ {total_recaudado:,.2f}")
        col2.metric("Total Residentes Registrados", total_residentes)
        col3.metric("Cuota Estándar", "S/ 30.00")
        
        st.markdown("---")
        st.subheader("📋 Matriz General de Control")
        
        # Filtro de búsqueda veloz
        busqueda = st.text_input("🔍 Buscar por Nombre o Lote:")
        if busqueda:
            df = df[df["Nombre"].str.contains(busqueda, case=False) | df["Lote"].str.contains(busqueda, case=False)]
            
        st.dataframe(df.dropna(subset=["Mes"]), use_container_width=True)
    else:
        st.info("No hay datos registrados aún. Vaya a la sección de Residentes.")

# --- VISTA 2: CRUD DE RESIDENTES ---
elif opcion == "👥 Residentes (CRUD)":
    st.subheader("Administración del Padrón de Residentes")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("### Agregar Residente")
        nuevo_nombre = st.text_input("Nombre Completo (Apellidos y Nombres):")
        nuevo_lote = st.text_input("Número de Lote / Casa (Ej: 210):")
        if st.button("Guardar Registro"):
            if nuevo_nombre and nuevo_lote:
                exito = db.registrar_residente(nuevo_nombre, nuevo_lote)
                if exito:
                    st.success("Residente añadido correctamente.")
                    st.rerun()
                else:
                    st.error("El número de lote ya se encuentra asignado.")
            else:
                st.warning("Complete todos los campos.")
                
    with c2:
        st.markdown("### Residentes Activos")
        lista = db.obtener_residentes()
        if lista:
            df_res = pd.DataFrame(lista, columns=["ID", "Nombre", "Lote"])
            st.dataframe(df_res, use_container_width=True)
            
            st.markdown("### Acciones Rápidas (Editar / Eliminar)")
            id_sel = st.number_input("Ingrese ID del residente a modificar:", min_value=1, step=1)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                nom_mod = st.text_input("Nuevo Nombre:")
                lot_mod = st.text_input("Nuevo Lote:")
                if st.button("📝 Aplicar Cambios"):
                    db.actualizar_residente(id_sel, nom_mod, lot_mod)
                    st.success("Datos actualizados.")
                    st.rerun()
            with col_b2:
                st.write("Zona de Peligro:")
                if st.button("❌ Eliminar Permanentemente"):
                    db.eliminar_residente(id_sel)
                    st.warning("Registro borrado.")
                    st.rerun()

# --- VISTA 3: REGISTRO DE PAGOS ---
elif opcion == "💰 Registrar Pagos":
    st.subheader("Carga de Aportaciones Mensuales")
    
    residentes = db.obtener_residentes()
    if residentes:
        dict_res = {f"{r[1]} (Lote {r[2]})": r[0] for r in residentes}
        seleccionado = st.selectbox("Seleccione el Residente:", list(dict_res.keys()))
        residente_id = dict_res[seleccionado]
        
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            mes = st.selectbox("Mes correspondencia:", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"])
            anio = st.selectbox("Año:", ["2024", "2025", "2026"])
        with col_p2:
            monto = st.number_input("Monto Recaudado (S/):", min_value=0.0, value=30.0, step=5.0)
        with col_p3:
            estado = st.selectbox("Estado del Pago:", ["Pagado", "Parcial", "Deuda"])
            
        if st.button("💾 Grabar Estado de Pago"):
            db.registrar_o_actualizar_pago(residente_id, mes, anio, monto, estado)
            st.success(f"Pago registrado con éxito para {seleccionado}.")
    else:
        st.error("Debe registrar al menos un residente antes de procesar pagos.")
