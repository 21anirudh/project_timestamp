from flask import Flask, request, jsonify
from pytube import YouTube
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi as ypa

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(text)
    processed_tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(processed_tokens)

def extract_topics(transcript):
    data = pd.DataFrame({"text": [transcript]})
    data["processed_text"] = data["text"].apply(preprocess)

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(data["processed_text"])
    lda = LatentDirichletAllocation(n_components=5)
    lda.fit(tfidf)

    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for idx, topic in enumerate(lda.components_):
        print(f"Topic {idx + 1}:")
        topic_words_idx = topic.argsort()[-5:][::-1]
        topic_words = [feature_names[i] for i in topic_words_idx]
        topics.append(topic_words)

    return topics

@app.route("/", methods=["GET"])
def index():
    return "Pheu! chal gaya"

@app.route("/extract_timestamp", methods=["POST"])
def extract_timestamp():
    data = request.json
    video_url = data["video_url"]
    topic = data["topic"]

    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_path = audio_stream.download(output_path="temp", filename="temp_audio.mp3")

        if not audio_path:
            return jsonify({"error": "Failed to download the audio."}), 500

        # Get transcript using youtube_transcript_api
        transcript_list = ypa.list_transcripts(yt.video_id)
        transcript = None
        for entry in transcript_list:
            if entry.language_code == 'en':
                transcript = entry.fetch()
                break

        if not transcript:
            return jsonify({"error": "Failed to retrieve the transcript."}), 500

        timestamp = None
        for segment in transcript:
            if topic.lower() in segment["text"].lower():
                timestamp = segment["start"]
                break

        return jsonify({"timestamp": timestamp})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
