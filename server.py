"""Flask web server for the Emotion Detection application."""
from flask import Flask, render_template, request
import requests

from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emot_detector():
    """Analyze the 'textToAnalyze' query parameter and return a formatted response."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    try:
        result = emotion_detector(text_to_analyze)
    except requests.RequestException:
        return "The emotion detection service is unavailable. Please try again later.", 503

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    return (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


@app.route("/")
def render_index_page():
    """Render the main application page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
