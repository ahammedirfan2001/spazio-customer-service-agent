from agent import client, MODEL_NAME

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": "Say hello to Spazio Restaurant in one sentence."
        }
    ]
)

print(response.choices[0].message.content)