"""Unit tests for the EmotionDetection package."""
import unittest
from unittest import mock

import requests

from EmotionDetection.emotion_detection import URL, emotion_detector


def _service_reachable():
    """Return True if the Watson NLP endpoint answers (only inside the IBM lab)."""
    try:
        requests.post(URL, json={}, timeout=5)
        return True
    except requests.RequestException:
        return False


@unittest.skipUnless(_service_reachable(), "Watson NLP service not reachable")
class TestEmotionDetection(unittest.TestCase):
    """Live tests against the Watson NLP service."""

    def test_emotion_detector(self):
        """Each statement should produce the expected dominant emotion."""
        cases = {
            "I am glad this happened": "joy",
            "I am really mad about this": "anger",
            "I feel disgusted just hearing about this": "disgust",
            "I am so sad about this": "sadness",
            "I am really afraid that this will happen": "fear",
        }
        for statement, expected in cases.items():
            with self.subTest(statement=statement):
                self.assertEqual(emotion_detector(statement)["dominant_emotion"], expected)


class TestEmotionDetectionOffline(unittest.TestCase):
    """Tests of the formatting and error handling, with the service mocked out."""

    @mock.patch("EmotionDetection.emotion_detection.requests.post")
    def test_formats_scores_and_picks_dominant(self, mock_post):
        """Scores are extracted and the highest one is the dominant emotion."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "emotionPredictions": [{"emotion": {
                "anger": 0.01, "disgust": 0.02, "fear": 0.03, "joy": 0.9, "sadness": 0.04,
            }}]
        }
        result = emotion_detector("I love this")
        self.assertEqual(result["joy"], 0.9)
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_blank_input_returns_none(self):
        """Blank input gives all None values without calling the service."""
        for text in ("", "   "):
            result = emotion_detector(text)
            self.assertTrue(all(value is None for value in result.values()))

    @mock.patch("EmotionDetection.emotion_detection.requests.post")
    def test_status_400_returns_none(self, mock_post):
        """A 400 response from the service gives all None values."""
        mock_post.return_value.status_code = 400
        result = emotion_detector("???")
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
