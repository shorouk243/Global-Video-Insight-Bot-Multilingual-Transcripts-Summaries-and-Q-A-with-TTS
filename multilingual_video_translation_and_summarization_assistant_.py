# -*- coding: utf-8 -*-
"""Multilingual Video Translation and Summarization Assistant .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YDzEdKexfg4A1L385sRJQJsMshw6TZoS
"""

!pip install pydub

!pip install yt-dlp

!yt-dlp -f mp4 https://www.youtube.com/watch?v=i5Q02YX2VTw -o video.mp4

from IPython.display import HTML
from base64 import b64encode

# Open the video file
video_path = 'video.mp4'

# Encode the video to base64
mp4 = open(video_path, 'rb').read()
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()

# Display the video
HTML("""
<video width=500 controls>
      <source src="%s" type="video/mp4">
</video>
""" % data_url)

!apt-get install -y ffmpeg

!ffmpeg -i video.mp4 -q:a 0 -map a audio.wav

!pip install ffmpeg-python

!ffmpeg -i audio.wav audio.mp3

from IPython.display import Audio

# Play the converted MP3 file
Audio('audio.mp3')

from pydub import AudioSegment

# Step 2: Extract Audio from Video
audio_path = "/content/audio.wav"
video = AudioSegment.from_file(video_path, "mp4")
video.export(audio_path, format="wav")

# Ensure the audio is in the correct format (16kHz sample rate for the model)
audio = AudioSegment.from_wav(audio_path)
audio = audio.set_frame_rate(16000)
audio.export("/content/processed_audio.wav", format="wav")

from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio
import torch
from pydub import AudioSegment
from pathlib import Path
# from GPTranslate import Book

# Step 1: Extract Audio from Video
audio_path = "audio.wav"
video = AudioSegment.from_file("video.mp4", "mp4")
video.export(audio_path, format="wav")

# Ensure the audio is in the correct format (16kHz sample rate for the model)
audio = AudioSegment.from_wav(audio_path)
audio = audio.set_frame_rate(16000)
audio.export("processed_audio.wav", format="wav")

# Load Whisper model and processor for transcription
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")

# Function to split audio into smaller chunks
def split_audio(audio_tensor, sample_rate, chunk_size=30):
    chunk_length = int(chunk_size * sample_rate)
    num_chunks = audio_tensor.shape[1] // chunk_length + 1
    chunks = [audio_tensor[:, i * chunk_length:(i + 1) * chunk_length] for i in range(num_chunks)]
    return chunks

# Process audio file
audio_tensor, sample_rate = torchaudio.load("processed_audio.wav", normalize=True)

# Split the audio into chunks
audio_chunks = split_audio(audio_tensor, sample_rate, chunk_size=30)

# Function to transcribe each chunk
def transcribe_chunk(audio_chunk):
    input_features = processor(audio_chunk.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    return processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

# Transcribe each chunk and combine the results
full_transcription = ""
for chunk in audio_chunks:
    transcription = transcribe_chunk(chunk)
    full_transcription += transcription + " "

print("Full Transcription:", full_transcription)

from transformers import pipeline
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torchaudio

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Summarize the transcription
def summarize_text(text):
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Path to the audio file
file_path = "/content/processed_audio.wav"


# Summarize the transcription
summary = summarize_text(full_transcription)
print("Summary:", summary)

from googletrans import Translator
import torch

# Initialize the Translator
translator = Translator()

# Function to translate text to a specified language
def translate_text(text, dest_language):
    translation = translator.translate(text, dest=dest_language)
    return translation.text

# Translate the full transcription, summary, and questions
translated_transcription_ar = translate_text(full_transcription, 'ar')
translated_summary_ar = translate_text(summary, 'ar')

print("Translated Transcription (AR):", translated_transcription_ar)
print("Translated Summary (AR):", translated_summary_ar)

# You can repeat this for other languages (e.g., German and Russian) as needed.
translated_transcription_de = translate_text(full_transcription, 'de')
translated_summary_de = translate_text(summary, 'de')

translated_transcription_ru = translate_text(full_transcription, 'ru')
translated_summary_ru = translate_text(summary, 'ru')

print("Translated Transcription (DE):", translated_transcription_de)
print("Translated Summary (DE):", translated_summary_de)

print("Translated Transcription (RU):", translated_transcription_ru)
print("Translated Summary (RU):", translated_summary_ru)

from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer, pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import torchaudio
from pydub import AudioSegment
import soundfile as sf
import torch
from datasets import load_dataset
from IPython.display import Audio
from googletrans import Translator

# Initialize the translator
translator = Translator()

# Step 5: Question Answering
qa_model_name = "deepset/roberta-base-squad2"
qa_pipeline = pipeline("question-answering", model=qa_model_name, tokenizer=qa_model_name)

full_transcription = "I had some tantrums of saying, I can't do this, this is too hard. When I was a kid and comparing myself to everyone else and saying, I can't do it, I'll never be able to do that. My parents always sat me down and said, look Nick, yes, there are things that you can't do, but don't say, I can't do it. Ask yourself, how can I do it? You know, there's ways around it. You can get from one side of the mountain to another. but you don't just have to walk over it. Maybe you can go underneath it or around it. There's always ways in achieving the same goal. The way that I've achieved in my life doesn't always look the same for everyone else. But the key to that success was I believed in myself. If someone else could do something, then I could try and work out how. It starts with believing in yourself."

# Translate the full transcription to Arabic
full_transcription_ar = translator.translate(full_transcription, src='en', dest='ar').text
print("Full Transcription in Arabic:", full_transcription_ar)

def answer_question(question, context):
    # Translate the question from Arabic to English
    question_en = translator.translate(question, src='ar', dest='en').text

    # Answer the question
    QA_input = {'question': question_en, 'context': context}
    answer_en = qa_pipeline(QA_input)['answer']

    # Translate the answer back to Arabic
    answer_ar = translator.translate(answer_en, src='en', dest='ar').text
    return answer_ar

# Assuming you have a text-to-speech pipeline similar to what you used before
synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")

def generate_speech(text, speaker_embedding):
    speech = synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})
    return speech

# Get user input for multiple questions in Arabic
questions = []
print("Enter your questions in Arabic (type 'done' when finished):")
while True:
    question = input("Question: ")
    if question.lower() == 'done':
        break
    questions.append(question)

# Load speaker embeddings for Arabic TTS (you might need to replace this with an Arabic speaker embedding)
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

# Answer each question and generate speech in Arabic
for i, question in enumerate(questions):
    print(f"Processing Question {i+1}: {question}")

    # Answer the user's question in Arabic
    answer_ar = answer_question(question, full_transcription)
    print(f"Answer {i+1} in Arabic: {answer_ar}")

    # Generate Arabic speech from the answer
    speech = generate_speech(answer_ar, speaker_embedding)

    # Save and play the synthesized Arabic speech
    output_speech_path = f"/content/speech_ar_{i+1}.wav"
    sf.write(output_speech_path, speech["audio"], samplerate=speech["sampling_rate"])

    # Play the saved audio file
    display(Audio(output_speech_path))

print("All questions processed.")

!pip install gTTS

from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer, pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import torchaudio
from pydub import AudioSegment
import soundfile as sf
import torch
from datasets import load_dataset
from IPython.display import Audio
from googletrans import Translator
from gtts import gTTS

# Initialize the translator
translator = Translator()

# Step 5: Question Answering
qa_model_name = "deepset/roberta-base-squad2"
qa_pipeline = pipeline("question-answering", model=qa_model_name, tokenizer=qa_model_name)

full_transcription = "I had some tantrums of saying, I can't do this, this is too hard. When I was a kid and comparing myself to everyone else and saying, I can't do it, I'll never be able to do that. My parents always sat me down and said, look Nick, yes, there are things that you can't do, but don't say, I can't do it. Ask yourself, how can I do it? You know, there's ways around it. You can get from one side of the mountain to another. but you don't just have to walk over it. Maybe you can go underneath it or around it. There's always ways in achieving the same goal. The way that I've achieved in my life doesn't always look the same for everyone else. But the key to that success was I believed in myself. If someone else could do something, then I could try and work out how. It starts with believing in yourself."

# Translate the full transcription to Arabic
full_transcription_ar = translator.translate(full_transcription, src='en', dest='ar').text
print("Full Transcription in Arabic:", full_transcription_ar)

def answer_question(question, context):
    # Translate the question from Arabic to English
    question_en = translator.translate(question, src='ar', dest='en').text

    # Answer the question
    QA_input = {'question': question_en, 'context': context}
    answer_en = qa_pipeline(QA_input)['answer']

    # Translate the answer back to Arabic
    answer_ar = translator.translate(answer_en, src='en', dest='ar').text
    return answer_ar

# Define the generate_speech function using gTTS as an alternative
def generate_speech(text, lang='ar'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        output_speech_path = "/content/speech.wav"
        tts.save(output_speech_path)
        return output_speech_path
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

# Get user input for multiple questions in Arabic
questions = []
print("Enter your questions in Arabic (type 'done' when finished):")
while True:
    question = input("Question: ")
    if question.lower() == 'done':
        break
    questions.append(question)

# Answer each question and generate speech in Arabic
for i, question in enumerate(questions):
    print(f"Processing Question {i+1}: {question}")

    # Answer the user's question in Arabic
    answer_ar = answer_question(question, full_transcription)
    print(f"Answer {i+1} in Arabic: {answer_ar}")

    # Generate Arabic speech from the answer
    output_speech_path = generate_speech(answer_ar, lang='ar')

    if output_speech_path:
        # Play the saved audio file
        display(Audio(output_speech_path))
    else:
        print(f"Failed to generate speech for question {i+1}")

print("All questions processed.")

!pip install googletrans

!pip install datasets

from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import torch # Import the torch library
summary= " When I was a kid, I was comparing myself to everyone else and saying, I can't do it, I'll never be able to do that. The way that I've achieved in my life doesn't always look the same for everyone else. But the key to that success was I believed in myself."

synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

# You can replace this embedding with your own as well.

speech = synthesiser(summary, forward_params={"speaker_embeddings": speaker_embedding})

sf.write("speech.wav", speech["audio"], samplerate=speech["sampling_rate"])

from IPython.display import Audio

# Play the saved audio file
Audio("/content/speech.wav")

from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer, pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import torchaudio
from pydub import AudioSegment
import soundfile as sf
import torch
from datasets import load_dataset
from IPython.display import Audio

# Step 5: Question Answering
qa_model_name = "deepset/roberta-base-squad2"
qa_pipeline = pipeline("question-answering", model=qa_model_name, tokenizer=qa_model_name)

full_transcription=  "I had some tantrums of saying, I can't do this, this is too hard. When I was a kid and comparing myself to everyone else and saying, I can't do it, I'll never be able to do that. My parents always sat me down and said, look Nick, yes, there are things that you can't do, but don't say, I can't do it. Ask yourself, how can I do it? You know, there's ways around it. You can get from one side of the mountain to another.  but you don't just have to walk over it. Maybe you can go underneath it or around it. There's always ways in achieving the same goal. The way that I've achieved in my life doesn't always look the same for everyone else. But the key to that success was I believed in myself. If someone else could do something, then I could try and work out how. It starts with believing in yourself."

def answer_question(question, context):
    QA_input = {'question': question, 'context': context}
    answer = qa_pipeline(QA_input)
    return answer['answer']

# Assuming you have a text-to-speech pipeline similar to what you used before
synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")
def generate_speech(text, speaker_embedding): # Define the generate_speech function
    speech = synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})
    return speech

# Get user input for multiple questions
questions = []
print("Enter your questions (type 'done' when finished):")
while True:
    question = input("Question: ")
    if question.lower() == 'done':
        break
    questions.append(question)

# Answer each question and generate speech
for i, question in enumerate(questions):
    print(f"Processing Question {i+1}: {question}")

    # Answer the user's question based on the summary
    answer = answer_question(question, full_transcription)
    print(f"Answer {i+1}: {answer}")

    # Generate speech from the answer
    speech = generate_speech(answer, speaker_embedding) # Now you can call generate_speech

    # Save and play the synthesized speechgreat
    output_speech_path = f"/content/speech_{i+1}.wav"
    sf.write(output_speech_path, speech["audio"], samplerate=speech["sampling_rate"])

    # Play the saved audio file
    display(Audio(output_speech_path))

print("All questions processed.")

from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer, pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import torchaudio
from pydub import AudioSegment
import soundfile as sf
import torch
from datasets import load_dataset
from IPython.display import Audio

# Step 1: Extract Audio from Video
video_path = "/content/video.mp4"  # Update with your video file path
audio_path = "/content/audio.wav"

# Convert video to audio
video = AudioSegment.from_file(video_path, "mp4")
video.export(audio_path, format="wav")

# Ensure the audio is in the correct format (16kHz sample rate for the model)
audio = AudioSegment.from_wav(audio_path)
audio = audio.set_frame_rate(16000)
processed_audio_path = "/content/processed_audio.wav"
audio.export(processed_audio_path, format="wav")

# Step 2: Load pre-trained model and tokenizer for transcription
model_name = "facebook/wav2vec2-base-960h"
model = Wav2Vec2ForCTC.from_pretrained(model_name)
tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)

# Function to transcribe audio and format text
def transcribe_audio(file_path):
    audio_input, sample_rate = torchaudio.load(file_path, normalize=True)
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        audio_input = resampler(audio_input)
    inputs = tokenizer(audio_input.squeeze().numpy(), return_tensors="pt", padding="longest")
    with torch.no_grad():
        logits = model(input_values=inputs.input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]

    # Convert transcription to normal case
    normal_case_text = transcription.capitalize()
    return normal_case_text

# Step 3: Summarize the transcription
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    summary = summarizer(text, max_length=300, min_length=100, do_sample=False)  # Adjusted lengths
    return summary[0]['summary_text']

# Step 4: Synthesize speech from summary
synthesiser = pipeline("text-to-speech", model="microsoft/speecht5_tts")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

def generate_speech(text, embedding):
    speech = synthesiser(text, forward_params={"speaker_embeddings": embedding})
    return speech

# Step 5: Question Answering
qa_model_name = "deepset/roberta-base-squad2"
qa_pipeline = pipeline("question-answering", model=qa_model_name, tokenizer=qa_model_name)

def answer_question(question, context):
    QA_input = {'question': question, 'context': context}
    answer = qa_pipeline(QA_input)
    return answer['answer']

# Get user input for multiple questions
questions = []
print("Enter your questions (type 'done' when finished):")
while True:
    question = input("Question: ")
    if question.lower() == 'done':
        break
    questions.append(question)

# Process and transcribe audio
transcription = transcribe_audio(processed_audio_path)
print("Transcription:", transcription)

# Summarize the transcription
summary = summarize_text(transcription)
print("Summary:", summary)

# Answer each question and generate speech
for i, question in enumerate(questions):
    print(f"Processing Question {i+1}: {question}")

    # Answer the user's question based on the summary
    answer = answer_question(question, summary)
    print(f"Answer {i+1}: {answer}")

    # Generate speech from the answer
    speech = generate_speech(answer, speaker_embedding)

    # Save and play the synthesized speech
    output_speech_path = f"/content/speech_{i+1}.wav"
    sf.write(output_speech_path, speech["audio"], samplerate=speech["sampling_rate"])

    # Play the saved audio file
    display(Audio(output_speech_path))

print("All questions processed.")

from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import torchaudio
from pydub import AudioSegment
import soundfile as sf
import torch
from datasets import load_dataset
from IPython.display import Audio
from googletrans import Translator
from gtts import gTTS

# Initialize the translator
translator = Translator()

# Load Whisper model and processor for transcription
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")

# Function to split audio into smaller chunks
def split_audio(audio_tensor, sample_rate, chunk_size=30):
    chunk_length = int(chunk_size * sample_rate)
    num_chunks = audio_tensor.shape[1] // chunk_length + 1
    chunks = [audio_tensor[:, i * chunk_length:(i + 1) * chunk_length] for i in range(num_chunks)]
    return chunks

# Process audio file
audio_tensor, sample_rate = torchaudio.load("processed_audio.wav", normalize=True)

# Split the audio into chunks
audio_chunks = split_audio(audio_tensor, sample_rate, chunk_size=30)

# Function to transcribe each chunk
def transcribe_chunk(audio_chunk):
    input_features = processor(audio_chunk.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    return processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

# Transcribe each chunk and combine the results
full_transcription = ""
for chunk in audio_chunks:
    transcription = transcribe_chunk(chunk)
    full_transcription += transcription + " "

print("Full Transcription:", full_transcription)

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Summarize the transcription
def summarize_text(text):
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Summarize the transcription
summary = summarize_text(full_transcription)
print("Summary:", summary)

# Step 5: Question Answering
qa_model_name = "deepset/roberta-base-squad2"
qa_pipeline = pipeline("question-answering", model=qa_model_name, tokenizer=qa_model_name)

def answer_question(question, context):
    QA_input = {'question': question, 'context': context}
    answer = qa_pipeline(QA_input)
    return answer['answer']

# Define the generate_speech function using gTTS
def generate_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        output_speech_path = f"/content/speech_{lang}.wav"
        tts.save(output_speech_path)
        return output_speech_path
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

# Define languages
languages = {
    'en': 'English',
    'ar': 'Arabic',
    'de': 'German',
    'ko': 'Korean',
    'hi': 'Hindi'
}

# Process, translate, and generate speech for transcription and summary
for lang_code, lang_name in languages.items():
    print(f"\nProcessing for {lang_name}:")

    # Translate full transcription
    translated_transcription = translator.translate(full_transcription, src='en', dest=lang_code).text
    print(f"Full Transcription in {lang_name}: {translated_transcription}")

    # Generate speech for full transcription
    transcription_speech_path = generate_speech(translated_transcription, lang_code)
    if transcription_speech_path:
        print(f"Playing Full Transcription Speech in {lang_name}:")
        display(Audio(transcription_speech_path))

    # Translate summary
    translated_summary = translator.translate(summary, src='en', dest=lang_code).text
    print(f"Summary in {lang_name}: {translated_summary}")

    # Generate speech for summary
    summary_speech_path = generate_speech(translated_summary, lang_code)
    if summary_speech_path:
        print(f"Playing Summary Speech in {lang_name}:")
        display(Audio(summary_speech_path))


# Get user input for multiple questions
questions = []
print("Enter your questions (type 'done' when finished):")
while True:
    question = input("Question: ")
    if question.lower() == 'done':
        break
    questions.append(question)

# Process and translate, then generate speech
for lang_code, lang_name in languages.items():
    print(f"\nProcessing for {lang_name}:")

    # Translate transcription and summary
    translated_transcription = translator.translate(full_transcription, src='en', dest=lang_code).text
    translated_summary = translator.translate(summary, src='en', dest=lang_code).text
    print(f"Full Transcription in {lang_name}: {translated_transcription}")
    print(f"Summary in {lang_name}: {translated_summary}")

    # Answer each question in the selected language
    for i, question in enumerate(questions):
        # Translate the question to English for QA model
        question_en = translator.translate(question, src=lang_code, dest='en').text

        # Answer the question based on the English context
        answer_en = answer_question(question_en, full_transcription)

        # Translate the answer back to the selected language
        answer = translator.translate(answer_en, src='en', dest=lang_code).text

        print(f"Question {i+1} in {lang_name}: {question}")
        print(f"Answer {i+1} in {lang_name}: {answer}")

        # Generate speech from the answer in the selected language
        output_speech_path = generate_speech(answer, lang=lang_code)

        if output_speech_path:
            # Play the saved audio file
            display(Audio(output_speech_path))
        else:
            print(f"Failed to generate speech for question {i+1} in {lang_name}")

print("All questions processed.")

import gradio as gr
from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline
import torchaudio
from pydub import AudioSegment
import soundfile as sf
from googletrans import Translator
from langdetect import detect

# Initialize components
translator = Translator()
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
qa_model_name = "deepset/roberta-base-squad2"
qa_pipeline = pipeline("question-answering", model=qa_model_name, tokenizer=qa_model_name)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
synthesiser = pipeline("text-to-speech", model="microsoft/speecht5_tts")

# Define language codes
languages = {
    'ar': 'Arabic',
    'de': 'German',
    'ko': 'Korean',
    'hi': 'Hindi',
    'en': 'English'
}

def detect_and_translate(text, target_lang='en'):
    detected_lang = detect(text)
    if detected_lang != target_lang:
        translated_text = translator.translate(text, src=detected_lang, dest=target_lang).text
        return translated_text, detected_lang
    return text, detected_lang

def translate_back(text, target_lang):
    return translator.translate(text, src='en', dest=target_lang).text

def generate_speech(text, lang_code):
    try:
        speech = synthesiser(text, lang=lang_code)
        output_speech_path = f"{lang_code}_speech.wav"
        sf.write(output_speech_path, speech[0]["array"], samplerate=speech[0]["sampling_rate"])
        return output_speech_path
    except Exception as e:
        print(f"Error in generating speech: {e}")
        return None

def process_audio(file_path):
    try:
        # Ensure audio is in correct format
        audio = AudioSegment.from_wav(file_path)
        audio = audio.set_frame_rate(16000)
        audio.export("processed_audio.wav", format="wav")

        # Transcribe audio
        audio_tensor, sample_rate = torchaudio.load("processed_audio.wav", normalize=True)
        input_features = processor(audio_tensor.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt").input_features
        predicted_ids = model.generate(input_features)
        full_transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        # Summarize transcription
        summary = summarizer(full_transcription, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

        return full_transcription, summary
    except Exception as e:
        print(f"Error in processing audio: {e}")
        return None, None

def handle_text(language_code, text, question=None):
    try:
        translated_text, detected_lang = detect_and_translate(text, target_lang='en')
        if question:
            translated_question = translator.translate(question, src=detected_lang, dest='en').text
            answer = qa_pipeline({'question': translated_question, 'context': translated_text})['answer']
            translated_answer = translate_back(answer, detected_lang)
            answer_speech_path = generate_speech(translated_answer, language_code)
        else:
            translated_answer = None
            answer_speech_path = None

        transcription_speech_path = generate_speech(translated_text, language_code)
        summary = summarizer(translated_text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        summary_speech_path = generate_speech(summary, language_code)

        return {
            "full_transcription": translated_text,
            "summary": summary,
            "answer": translated_answer,
            "transcription_speech": transcription_speech_path,
            "summary_speech": summary_speech_path,
            "answer_speech": answer_speech_path
        }
    except Exception as e:
        print(f"Error in handling text: {e}")
        return None

def gradio_interface(audio_file, language_code, question=None):
    try:
        # Process audio
        full_transcription, summary = process_audio(audio_file.name)

        if not full_transcription:
            return "Error in processing audio", None, None, None, None, None

        # Handle text
        result = handle_text(language_code, full_transcription, question)

        if not result:
            return "Error in handling text", None, None, None, None, None

        return (
            result["full_transcription"],
            result["summary"],
            result["answer"],
            result["transcription_speech"],
            result["summary_speech"],
            result["answer_speech"]
        )
    except Exception as e:
        print(f"Error in Gradio interface: {e}")
        return "Error occurred", None, None, None, None, None

# Gradio interface
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Audio(type="filepath", label="Upload Audio/Video"),  # Remove 'source' argument
        gr.Dropdown(choices=list(languages.keys()), label="Select Language"),
        gr.Textbox(label="Question (optional)")
    ],
    outputs=[
        gr.Textbox(label="Full Transcription"),
        gr.Textbox(label="Summary"),
        gr.Textbox(label="Answer (if question provided)"),
        gr.Audio(label="Transcription Speech"),
        gr.Audio(label="Summary Speech"),
        gr.Audio(label="Answer Speech (if question provided)")
    ],
    title="Multilingual Audio Processing",
    description="Upload an audio file, select a language, and optionally enter a question. The system will transcribe the audio, summarize it, and generate text-to-speech outputs in the selected language."
)
iface.launch()

!pip uninstall httpx

!pip install httpx==0.13.3

!pip install --upgrade googletrans

import httpx
import googletrans
import gradio

print(f"httpx version: {httpx.__version__}")
print(f"googletrans version: {googletrans.__version__}")
print(f"Gradio version: {gradio.__version__}")

!pip install --upgrade googletrans httpx httpcore

!pip uninstall httpx

!pip uninstall gradio
!pip install gradio==4.41.0

!pip install --upgrade httpx

!pip install googletrans

!pip install googletrans==4.0.0-rc1

!pip install transformers
from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline, AutoModelForQuestionAnswering, AutoTokenizer

!pip install gtts

!pip install googletrans

!pip install langdetect

