import streamlit as st

# Diccionario de opciones dependientes
dependencias = {
    "Carrera 1": ["Materia 1", "Materia 2", "Materia 3"],
    "Carrera 2": ["Materia 4", "Materia 5", "Materia 6"],
    "Carrera 3": ["Materia 7", "Materia 8", "Materia 9"]
}

st.title("Test frontend Calendario Automático")

# Campo de entrada para email
email = st.text_input("Email")

# Primera lista desplegable
categoria = st.selectbox("Categoría:", list(dependencias.keys()))

# Segunda lista con selección múltiple (según categoría seleccionada)
if categoria:
    opciones = st.multiselect("Opciones:", dependencias[categoria])

    # Mostrar resultados
    st.markdown("---")
    st.subheader("Resumen")
    st.write(f"📧 Email: {email}")
    st.write(f"Carrera: {categoria}")
    st.write(f"Materias: {', '.join(opciones) if opciones else 'Ninguna'}")
