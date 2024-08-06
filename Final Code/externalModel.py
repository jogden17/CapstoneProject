import os

os.environ["GROQ_API_KEY"] = "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"

from groq import Groq

def textGen(text):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": ("Edit the following text in the style of a newspaper article, make sure to remove all "
                            + "political bias and repetitive information. Do not add any additional information to "
                            + "what you are provided and do not include any irrelevant information. The total "
                            + "length should be about 2 paragraphs. Do not include any title or additional text to your"
                            + " edited version:" + text),
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.3,
    )

    result = chat_completion.choices[0].message.content

    print(result)
    return result
