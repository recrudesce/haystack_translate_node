# haystack_translate_node
An Azure Translation node for Haystack - you will need this configured in your Azure subscription: https://learn.microsoft.com/en-us/azure/cognitive-services/translator/translator-overview

Include in your pipeline as follows:

```python
from translate import TranslateAnswer, TranslateQuery

translate_query = TranslateQuery(api_key="<yourapikey>", location="<yourazureregion>", azure_translate_endpoint="<yourazureendpoint>", base_lang="en")
translate_answer = TranslateAnswer(api_key="<yourapikey>", location="<yourazureregion>", azure_translate_endpoint="<yourazureendpoint>", base_lang="en")

pipel = Pipeline()
pipel.add_node(component=translate_query, name="TranslateQuery", inputs=["Query"])
pipel.add_node(component=retriever, name="Retriever", inputs=["TranslateQuery"])
pipel.add_node(component=prompt_node, name="prompt_node", inputs=["Retriever"])
pipel.add_node(component=translate_answer, name="TranslateAnswer", inputs=["prompt_node"])
```

`location`, `azure_translate_endpoint`, and `base_lang` are optional, and will default to `uksouth`, `https://api.cognitive.microsofttranslator.com/`, and `en` respectively.

 - TranslateQuery will determine the language of the query, and assign it to the `in_lang` JSON value.
 - TranslateQuery will take the original query, in any language, and assign it to the `in_query` JSON value.
 - TranslateQuery will overwrite the original `query` JSON value with the translated English value

 - You can then query your `base_lang` corpus using the `query` value as normal using a standard Haystack Retriever node, which will place your results in `results`.

 - TranslateAnswer translate the `base_lang` result stored in `results` back to the language stored in `in_lang` and subsequently store it in the `out_answer` JSON value.
