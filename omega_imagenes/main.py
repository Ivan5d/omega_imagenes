import streamlit as st

st.set_page_config(
    page_title="Herramientas de Diseño de Omega",
    page_icon="assets/favicon_omega.png",
)

st.write("## Bienvenido a las herramientas de diseño de Omega.")

st.sidebar.success("Selecciona una herramienta.")

st.markdown(
    """
    Esta es una App de Streamlit que se creó específicamente como herramienta especializadas
    para solucionar tareas de diseño relacionadas a Omega para evitar usar software de terceros.
    
    ### ¿Cómo funciona?
    - Este programa corre remotamente en una computadora externa, por lo que debe asegurarse que 
    dicha computadora esté encendida y conectada a internet.
    - Si necesita ayuda, ve alguna falla o cree que se podría mejorar algo,
    por favor contacte a Ivan Diaz al correo de contabilidad@resistenciasomega.com.mx Este proyecto 
    está en el repositorio de Ivan5d en GitHub y está en constante mejora. 
"""
)

# Botón para ir a la página de Eliminación de Fondos
if st.button("Ir a Eliminación de Fondos y Marca de Agua 🖼️"):
    st.switch_page("pages/1_backgroundremoval.py")

