# Global Video Insight Bot: Multilingual Transcripts, Summaries, and Q&A with TTS

## Project Overview

The **Global Video Insight Bot** is a comprehensive system that processes video and audio content to generate multilingual transcripts, summaries, and answers to user-generated questions. Additionally, it provides text-to-speech (TTS) outputs in multiple languages, enhancing accessibility and user interaction.

## Key Features

- **Transcription**: Convert spoken content from video or audio files into text using state-of-the-art models.
- **Summarization**: Generate concise summaries of the transcribed content.
- **Question Answering**: Answer questions related to the content based on the generated transcripts.
- **Multilingual Support**: Translate transcripts, summaries, and answers into multiple languages.
- **Text-to-Speech**: Convert translated text into speech for a fully immersive experience.

## Benefits

1. **Enhanced Accessibility**:
   - The system provides transcription, translation, and TTS features, making audio and video content accessible to users with hearing or visual impairments, or those who prefer different languages.

2. **Multilingual Interaction**:
   - Users can interact with the system in their preferred language, making it easier to understand and engage with content. This is particularly useful in global, multilingual settings.

3. **Time Efficiency**:
   - By summarizing long videos or audio files, the system saves users time by providing quick insights without needing to consume the entire content.

4. **Improved User Experience**:
   - The combination of Q&A and TTS allows users to interact with the content in a more dynamic way, asking questions and receiving spoken answers, which can be beneficial in educational, professional, or entertainment contexts.

5. **Content Versatility**:
   - The system can handle various content types (educational videos, podcasts, lectures, etc.), making it versatile for different use cases, such as learning, research, content creation, and more.

6. **Scalability**:
   - The project can be scaled to handle large volumes of content, making it suitable for organizations, educational institutions, or media companies that need to process and distribute content to diverse audiences.

## Models and Libraries Used

### 1. **Transcription: `openai/whisper`**
   - **Purpose**: Converts spoken language from audio or video content into text.
   - **Details**: The `openai/whisper` model is known for its high accuracy and capability to handle diverse accents and background noise, making it ideal for transcription tasks across different languages.

### 2. **Summarization: `facebook/bart-large-cnn`**
   - **Purpose**: Generates concise summaries of long transcripts.
   - **Details**: `facebook/bart-large-cnn` is a transformer-based model pre-trained on CNN/DailyMail news articles. It is designed for abstractive summarization, which means it can produce summaries that capture the essence of the text while being syntactically coherent.

### 3. **Question Answering: `deepset/roberta-base-squad2`**
   - **Purpose**: Provides answers to questions based on the context of the transcripts.
   - **Details**: This model is fine-tuned on the SQuAD 2.0 dataset, which contains questions posed on a set of Wikipedia articles. The model is robust in understanding context and providing accurate, context-aware answers.

### 4. **Translation: `googletrans`**
   - **Purpose**: Translates transcripts, summaries, and answers into various languages.
   - **Details**: `googletrans` is a Python library that provides access to Google Translate's API, allowing for quick and accurate translation across numerous languages.

### 5. **Text-to-Speech: `gTTS`**
   - **Purpose**: Converts translated text into speech.
   - **Details**: `gTTS` (Google Text-to-Speech) is a Python library and CLI tool to interface with Google Translate’s text-to-speech API. It is used to generate spoken versions of the text in multiple languages, offering users an auditory experience.

## System Workflow

1. **Input**: The user uploads a video or audio file.
2. **Language Selection**: The user selects a preferred language for the output.
3. **Transcription**: The `openai/whisper` model transcribes the audio content into text.
4. **Summarization**: The `facebook/bart-large-cnn` model generates a summary of the transcribed text.
5. **Question Answering**: The user can input questions, and the `deepset/roberta-base-squad2` model provides answers based on the transcript.
6. **Translation**: The `googletrans` library translates the transcript, summary, and Q&A content into the selected language.
7. **Text-to-Speech**: The `gTTS` library converts the translated text into speech, providing audio output in the selected language.
8. **Output**: The system outputs the full transcription, summary, and Q&A in both text and audio formats.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/Global-Video-Insight-Bot.git
    cd Global-Video-Insight-Bot
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    ```bash
    python app.py
    ```

## Usage

1. **Upload** an audio or video file.
2. **Select** the output language.
3. **Enter** any questions (optional).
4. **Submit** the form to receive the transcription, summary, Q&A, and corresponding speech outputs.

## Example Chart

![System Workflow](https://via.placeholder.com/800x400.png?text=System+Workflow+Diagram)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
