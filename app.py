 import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.title("Conversión de Texto a Audio")

# Imagen de portada (asegúrate de tener 'caperucita.png' en tu carpeta)
image = Image.open('caperucita.png')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

# Crear carpeta temporal si no existe
try:
    os.mkdir("temp")
except:
    pass

# Texto base
st.subheader("Una pequeña Fábula: Caperucita Roja")
st.write(
    "Había una vez una niña muy dulce y amable que siempre vestía una capa roja, "
    "por lo que todos la llamaban Caperucita Roja. Un día, su madre le pidió que llevara "
    "una cesta con comida a casa de su abuela, que vivía al otro lado del bosque.\n\n"
    "En el camino, Caperucita se encontró con un lobo astuto que, al saber a dónde iba, "
    "corrió por un atajo, llegó antes que ella y se hizo pasar por la abuela. "
    "Cuando Caperucita llegó, notó que su 'abuela' se veía muy extraña.\n\n"
    "—¡Abuelita! ¡Qué ojos tan grandes tienes! —Para verte mejor, querida.\n"
    "—¡Abuelita! ¡Qué orejas tan grandes tienes! —Para oírte mejor.\n"
    "—¡Abuelita! ¡Qué boca tan grande tienes! —¡Para comerte mejor!\n\n"
    "Y entonces, el lobo saltó de la cama para atraparla. Por suerte, un leñador que pasaba por ahí "
    "oyó los gritos, entró en la casa y rescató a Caperucita y a su abuela del vientre del lobo. "
    "Desde ese día, Caperucita prometió no hablar con extraños en el bosque."
)

# Área para ingresar texto personalizado
st.markdown("¿Quieres escucharlo? Copia el texto a continuación:")
text = st.text_area("Ingrese el texto a escuchar:")

# Selección de idioma
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English")
)

lg = 'es' if option_lang == "Español" else 'en'

def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

# Botón para convertir
if st.button("Convertir a Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    # Descargar el archivo de audio
    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='Archivo'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="Archivo de Audio"), unsafe_allow_html=True)

# Eliminar archivos antiguos
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
