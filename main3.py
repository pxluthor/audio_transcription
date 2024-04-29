import streamlit as st
import subprocess
import os
from io import BytesIO

st.title('TRANSCRIPTION APP')
extensions = ['json', 'srt', 'txt', 'vtt', 'tsv']

# Upload the audio file
audio_file = st.file_uploader('Upload Audio', type=['wav', 'mp3', 'mp4a'])

# Verify if a file is uploaded
if audio_file is not None:

    st.header("Play áudio:")
    st.audio(audio_file)

    nome_original = os.path.splitext(audio_file.name)[0]
    # Save the uploaded file to BytesIO
    audio_bytes = BytesIO(audio_file.read())

# Button to start transcription
if st.button('Transcribe Audio') and audio_file:
    with st.spinner("Processando Audio... 💫"):
        # Remove files with specified extensions
        for ext in extensions:
            for filename in os.listdir("arquivos"):
                if filename.endswith(f".{ext}"):
                    filepath = os.path.join("arquivos", filename)
                    os.remove(filepath)

        # Command to be executed
        command = ["whisper", "-", "--model", "medium", "--language", "pt"]

        # Execute the command
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(input=audio_bytes.getvalue())

        # Save output to BytesIO
        output_bytes = BytesIO(out)

        # Move the generated transcription files to BytesIO
        generated_files = {}
        for ext in extensions:
            generated_file_name = f"{nome_original}.{ext}"
            generated_files[ext] = BytesIO()
            generated_files[ext].write(output_bytes.getvalue())

        # Display download buttons for the transcribed files
        for ext in extensions:
            if ext in generated_files:
                with st.expander(f"Arquivo {ext.upper()}"):
                    st.markdown(f"**Download {nome_original}.{ext}:**")
                    st.download_button(label=f"Download {ext.upper()}", data=generated_files[ext].getvalue(), file_name=f"{nome_original}.{ext}", mime=None)
                    generated_files[ext].seek(0)
                    st.text_area(f"Conteúdo do arquivo {ext.upper()}", value=generated_files[ext].read().decode('utf-8'), height=200)
