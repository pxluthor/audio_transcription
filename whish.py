import whisper
import streamlit as st
from tempfile import NamedTemporaryFile
import os

st.title("🔉 Aplicativo de transcrição automática de áudio e vídeo 🔉")
st.info('✨ Arquivos de áudio - WAV, MP3, MP4, OGG, WMA, AAC, FLAC, FLV | vídeo - MP4')

audio_file = st.file_uploader("Upload de Áudio ou Vídeo", type=["wav", "mp3", "ogg", "wma", "aac", "flac", "mp4", "flv"])

if audio_file is not None:
    model = whisper.load_model('medium') 
    # Playing audio file
    st.header("Play áudio:")
    st.audio(audio_file)

    if st.button("TRANSCREVER"):
        with st.spinner("Processando Audio... 💫"):
            with NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
                temp.write(audio_file.read())
                temp.close()  # Fechar o arquivo temporário antes de reabri-lo
                st.success("Realizando a transcrição")
                transcription = model.transcribe(temp.name, fp16=False)
                st.success("Transcrição Completada")


                with st.expander("Visualizar texto"):
                    
                 
                    st.markdown(transcription['text'])
                    st.markdown("---")

                    
                       
                with st.expander("Visualizar Descrição"):
                    for segment in transcription['segments']:
                        st.markdown(f"**Tempo:** {segment['start']} - {segment['end']}")
                        st.markdown(f"- {segment['text']}")
                
                    


                # Salvar a transcrição em um arquivo de texto
                file_path = os.path.join('audio_transcription/arquivos', 'transcript.txt')
                with open("transcript.txt", "w") as f:
                    f.write(transcription["text"])

                # Fornecer um botão de download para a transcrição
                st.download_button("Download Texto", transcription["text"])
                
            
