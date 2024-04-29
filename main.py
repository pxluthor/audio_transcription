import streamlit as st
import whisper
import os

st.title("Audio APP")

audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"], key="audio_uploader")

model = whisper.load_model("base")
st.text("Whisper Model Loaded")

if st.sidebar.button("TRANSCREVER"):
    if audio_file is not None:
        st.sidebar.success("Transcrevendo áudio...")
        try:
            # Salvar o arquivo temporário
            with open("temp_audio.mp3", "wb") as f:
                f.write(audio_file.read())
            # Passar o caminho do arquivo temporário para o Whisper
            transcription = model.transcribe("temp_audio.mp3")
            st.sidebar.success("Transcrição completada!")
            st.markdown(transcription["text"])
            # Remover o arquivo temporário após o uso
            os.remove("temp_audio.mp3")
        except RuntimeError as e:
            st.sidebar.error(f"Erro ao transcrever áudio: {e}")
    else:
        st.sidebar.error("Por favor, carregue um áudio")

st.sidebar.header("Reproduzir áudio")        
st.sidebar.audio(audio_file)

