import streamlit as st
from PIL import Image
from bkgremoval import remove_background
from watermark import watermark
import tempfile
import os

st.set_page_config(page_title="Procesamiento de Imágenes", page_icon="🖼️")

st.sidebar.title("Herramientas")
st.sidebar.success("Selecciona una herramienta.")

st.title("Eliminación de Fondo en Imágenes")
st.write("Sube una imagen y elimina el fondo automáticamente.")

uploaded_file = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen original", width=True)

    st.info("Aquí aparecerá la imagen sin fondo después del procesamiento.")

    col_eliminarfondo, col_marcadeagua, col_ambos = st.columns(3)

    with col_eliminarfondo:
        eliminarfondo = st.button("Eliminar Fondo")
    with col_marcadeagua:
        marcadeagua = st.button("Agrega Marca de Agua")
    with col_ambos:
        ambos = st.button("Elimina Fondo y Agrega Marca de Agua")
    
    # Slider for logo transparency
    alpha_value = st.sidebar.slider(
        "Transparencia de la marca de agua (0 = invisible, 255 = opaco)", 
        min_value=0, max_value=255, value=128
    )

    if eliminarfondo or marcadeagua or ambos:
        input_filename = uploaded_file.name
        name, ext = os.path.splitext(input_filename)
        output_filename = f"{name}_fondo.png"

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as input_tmp:
            image.save(input_tmp.name)
            input_path = input_tmp.name

        # Remove background
        removed_image = None
        if eliminarfondo or ambos:
            removed_image = remove_background(input_path)

        # Show and download background-removed image
        if eliminarfondo and removed_image is not None:
            st.image(removed_image, caption="Imagen sin fondo", width=True)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as out_tmp:
                removed_image.save(out_tmp.name)
                with open(out_tmp.name, "rb") as file:
                    st.download_button(
                        label="Descargar imagen sin fondo",
                        data=file,
                        file_name=output_filename,
                        mime="image/png"
                    )
                os.remove(out_tmp.name)

        # Show and download watermark only (no background removal)
        if marcadeagua:
            watermarked_image = watermark(image, alpha_value=alpha_value)
            st.image(watermarked_image, caption="Imagen con Marca de Agua", width=True)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as wm_tmp:
                watermarked_image.save(wm_tmp.name)
                with open(wm_tmp.name, "rb") as file:
                    st.download_button(
                        label="Descargar imagen con marca de agua",
                        data=file,
                        file_name=f"{name}_marca.png",
                        mime="image/png"
                    )
                os.remove(wm_tmp.name)

        # Show and download background-removed + watermark
        if ambos and removed_image is not None:
            watermarked_image = watermark(removed_image, alpha_value=alpha_value)
            st.image(watermarked_image, caption="Imagen sin fondo y con Marca de Agua", width=True)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as wm_tmp:
                watermarked_image.save(wm_tmp.name)
                with open(wm_tmp.name, "rb") as file:
                    st.download_button(
                        label="Descargar imagen sin fondo y con marca de agua",
                        data=file,
                        file_name=f"{name}_fondo_marca.png",
                        mime="image/png"
                    )
                os.remove(wm_tmp.name)

        # Clean up temp file
        os.remove(input_path)

else:
    st.write("Por favor, sube una imagen para comenzar.")