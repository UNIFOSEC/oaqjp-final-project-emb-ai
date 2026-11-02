"""Emotion detection using the embeddable Watson NLP EmotionPredict service."""
import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network"
    "/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")
TIMEOUT_SECONDS = 10


def _empty_result():
    """Return the result used for invalid input: every field set to None."""
    result = {emotion: None for emotion in EMOTIONS}
    result["dominant_emotion"] = None
    return result


def emotion_detector(text_to_analyse):
    """Detect emotions in text using Watson NLP.

    Returns a dict with a score for anger, disgust, fear, joy and sadness,
    plus the name of the highest-scoring emotion under 'dominant_emotion'.
    If the service answers with status 400 (for example, blank input),
    every value in the dict is None.
    Network failures and other HTTP errors raise requests.RequestException.
    """
    payload = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(URL, json=payload, headers=HEADERS, timeout=TIMEOUT_SECONDS)

    if response.status_code == 400:
        return _empty_result()
    response.raise_for_status()

    scores = response.json()["emotionPredictions"][0]["emotion"]
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(EMOTIONS, key=result.get)
    return result
