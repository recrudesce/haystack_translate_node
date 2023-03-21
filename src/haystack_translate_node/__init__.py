from haystack.nodes.base import BaseComponent
import requests
import uuid
from typing import Optional


class TranslateQuery(BaseComponent):
    def __init__(
        self,
        api_key: str = "",
        base_lang: Optional[str] = "en",
        location: Optional[str] = "uksouth",
        azure_translate_endpoint: Optional[
            str
        ] = "https://api.cognitive.microsofttranslator.com/",
    ):
        super().__init__()
        self.api_key = api_key
        self.location = location
        self.azure_translate_endpoint = azure_translate_endpoint
        self.base_lang = base_lang

        self.headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Ocp-Apim-Subscription-Region": self.location,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }
        self.params = {"api-version": "3.0"}
        self.detect_url = azure_translate_endpoint + "/detect"
        self.translate_path = "/translate"

    outgoing_edges = 1

    def run(self, query: str, **kwargs):
        body = [{"text": query}]
        detect_request = requests.post(
            self.detect_url, params=self.params, headers=self.headers, json=body
        )
        detect_response = detect_request.json()

        src_lng = detect_response[0]["language"]

        translate_params = "?from=" + src_lng + "&to=" + self.base_lang
        body = [{"text": query}]

        translate_url = (
            self.azure_translate_endpoint + self.translate_path + translate_params
        )
        translate_request = requests.post(
            translate_url, params=self.params, headers=self.headers, json=body
        )

        translate_response = translate_request.json()
        output = {
            "in_lang": [detect_response[0]["language"]],
            "in_query": query,
            "query": translate_response[0]["translations"][0]["text"],
        }
        return output, "output_1"

    def run_batch(self, query: str, **kwargs):
        return


class TranslateAnswer(BaseComponent):
    def __init__(
        self,
        api_key: str = "",
        base_lang: Optional[str] = "en",
        location: Optional[str] = "uksouth",
        azure_translate_endpoint: Optional[
            str
        ] = "https://api.cognitive.microsofttranslator.com/",
    ):
        super().__init__()
        self.azure_translate_endpoint = azure_translate_endpoint
        self.api_key = api_key
        self.location = location
        self.base_lang = base_lang

        self.headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Ocp-Apim-Subscription-Region": self.location,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }
        self.params = {"api-version": "3.0"}
        self.translate_path = "/translate"

    outgoing_edges = 1

    def run(self, in_lang: list, results: list, **kwargs):
        translate_params = "?from=" + self.base_lang + "&to=" + in_lang[0]
        body = [{"text": results[0]}]

        translate_url = (
            self.azure_translate_endpoint + self.translate_path + translate_params
        )

        translate_request = requests.post(
            translate_url, params=self.params, headers=self.headers, json=body
        )

        translate_response = translate_request.json()
        output = {
            "out_answer": translate_response[0]["translations"][0]["text"],
        }
        return output, "output_1"

    def run_batch(self, in_lang: list, results: list, **kwargs):
        return
