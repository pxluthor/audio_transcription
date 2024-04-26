import streamlit as st 
import subprocess
import os

st.title('TRANSCRIPTION APP')
extensions = ['json', 'srt', 'txt', 'vtt', 'tsv']

# Create a directory to save uploaded files if it doesn't exist
#if not os.path.exists("arquivos"):
#    os.makedirs("arquivos")

# Upload the audio file
audio_file = st.file_uploader('Upload Audio', type=['wav', 'mp3', 'mp4a'])

# Verify if a file is uploaded
if audio_file is not None:
    nome_original = os.path.splitext(audio_file.name)[0]
    # Save the uploaded file to disk with the original name
    audio_path = os.path.join("arquivos", audio_file.name)
    with open(audio_path, "wb") as f:
        f.write(audio_file.getbuffer())

# Button to start transcription
if st.button('Transcribe Audio') and audio_file:

    # Remove files with specified extensions
    for ext in extensions:
        for filename in os.listdir("arquivos"):
            if filename.endswith(f".{ext}"):
                filepath = os.path.join("arquivos", filename)
                os.remove(filepath)

    # Command to be executed
    command = ["whisper", audio_path, "--model", "medium", "--language", "pt"]

    # Execute the command
    subprocess.run(command)

    # Remove the audio file after transcription
    os.remove(audio_path)

    # Move the generated transcription files to the 'arquivos' directory
    for ext in extensions:
        generated_file = f"{nome_original}.{ext}"
        generated_file_path = os.path.join(os.getcwd(), generated_file)
        if os.path.exists(generated_file_path):
            os.rename(generated_file_path, os.path.join("arquivos", generated_file))

    # Display download buttons for the transcribed files
    for ext in extensions:
        generated_file = f"{nome_original}.{ext}"
        generated_file_path = os.path.join("arquivos", generated_file)
        if os.path.exists(generated_file_path):
            with st.expander(f"Arquivo {ext.upper()}"):
                st.markdown(f"**Download {generated_file}:**")
                with open(generated_file_path, 'rb') as file:
                    st.download_button(label=f"Download {ext.upper()}", data=file, file_name=generated_file, mime=None)
                with open(generated_file_path, 'r', encoding='utf-8') as file:
                    st.text_area(f"Conteúdo do arquivo {ext.upper()}", value=file.read(), height=200)        

