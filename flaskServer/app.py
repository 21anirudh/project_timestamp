from flask import Flask, request, jsonify
from pytube import YouTube
import whisper
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

app = Flask(__name__)

def extract_topics(transcript):
    sentences = transcript.split('.')
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = vectorizer.fit_transform(sentences)

    # Perform NMF topic modeling
    num_topics = 5  # Adjust the number of topics as needed
    nmf = NMF(n_components=num_topics, random_state=1)
    nmf.fit(tfidf)
    
    # Get the top words for each topic
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        topic_words = [feature_names[i] for i in topic.argsort()[:-6:-1]]
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

        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="en", verbose=True)
        transcript = result["text"] if result else None

        if not transcript:
            return jsonify({"error": "Failed to transcribe the audio."}), 500

        # Check if the topic is present in the transcript
        timestamp = None
        for entry in result["entries"]:
            if topic.lower() in entry["text"].lower():
                timestamp = entry["start_time"]
                break

        return jsonify({"timestamp": timestamp})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
