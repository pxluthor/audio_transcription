import streamlit as st
import whisper
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="LESTE_TRANSCRIPTION", page_icon="musical_note",layout="wide")

# CSS
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

bg = """
<style> [data-testid="stAppViewContainer"]{
background: rgb(6,36,39);
}
</style>
"""
st.markdown(bg, unsafe_allow_html=True)

st.title("🔉 Aplicativo de transcrição automática de áudio e vídeo 🔉")
st.info('✨ Arquivos de áudio - WAV, MP3, MP4, OGG, WMA, AAC, FLAC, FLV | video - MP4')

# Upload audio file with streamlit
audio_file = st.file_uploader("Upload Audio ou video", type=["wav","mp3","ogg","wma","aac","flac","mp4","flv"])

if audio_file is not None:
    # Importing model -- base(74M parameter)
    model = whisper.load_model("base")
    st.info("Whisper model loaded")

    # Playing audio file
    st.header("Play áudio:")
    st.audio(audio_file)

    # Generating transcript
    if st.button("TRANSCREVER"):
        with st.spinner("Processando áudio... 💫"):
            with NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
                temp.write(audio_file.read())
                temp.close()  # Fechar o arquivo temporário antes de reabri-lo
                st.success("Realizando a transcrição")
                transcription = model.transcribe(temp.name, fp16=True)
                st.success("Transcrição Completada")
                st.markdown(transcription["text"])
                st.code(transcription["text"])

                # Salvar a transcrição em um arquivo de texto
                with open("transcript.txt", "w") as f:
                    f.write(transcription["text"])
               

                # Fornecer um botão de download para a transcrição
                st.download_button("Download Transcript", transcription["text"])
            
