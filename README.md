# haystack_translate_node
An Azure Translation node for Haystack

Include in your pipeline as follows

```python
from translate import TranslateAnswer, TranslateQuery

translate_query = TranslateQuery(api_key="<yourapikey>", location="<yourazureregion>", azure_translate_endpoint="<yourazureendpoint>")
translate_answer = TranslateAnswer(api_key="<yourapikey>", location="<yourazureregion>", azure_translate_endpoint="<yourazureendpoint>")

pipel = Pipeline()
pipel.add_node(component=translate_query, name="TranslateQuery", inputs=["Query"])
pipel.add_node(component=retriever, name="Retriever", inputs=["TranslateQuery"])
pipel.add_node(component=prompt_node, name="prompt_node", inputs=["Retriever"])
pipel.add_node(component=translate_answer, name="TranslateAnswer", inputs=["prompt_node"])
```

 - TranslateQuery will determine the language of the query, and assign it to the `in_lang` JSON value.
 - TranslateQuery will take the original query, in any language, and assign it to the `in_query` JSON value.
 - TranslateQuery will overwrite the original `query` JSON value with the translated English value

 - You can then query your English corpus using the `query` value as normal using a standard Haystack Retriever node, which will place your results in `results`.

 - TranslateAnswer translate the English result stored in `results` back to the language stored in `in_lang` and subsequently store it in the `out_answer` JSON value.


**TODO:**
 - Work out how to allow you to set your "base" language.  I.e. if your corpus is in French, no use translating the query into English is there :P
