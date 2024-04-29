import streamlit as st
import whisper
import os

st.title("🔉 Aplicativo de transcrição automática de áudio e vídeo 🔉")
st.info('✨ Arquivos de áudio - WAV, MP3, MP4, OGG, WMA, AAC, FLAC, FLV | vídeo - MP4')

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
            with st.expander("Visualizar texto"):
                st.markdown(transcription["text"])
                st.code(transcription["text"])

            with st.expander("Visualizar Descrição"):
                    for segment in transcription['segments']:
                        st.markdown(f"**Tempo:** {segment['start']} - {segment['end']}")
                        st.markdown(f"- {segment['text']}")
            # Remover o arquivo temporário após o uso
            os.remove("temp_audio.mp3")
        except RuntimeError as e:
            st.sidebar.error(f"Erro ao transcrever áudio: {e}")
    else:
        st.sidebar.error("Por favor, carregue um áudio")

st.sidebar.header("Reproduzir áudio")        
st.sidebar.audio(audio_file)

