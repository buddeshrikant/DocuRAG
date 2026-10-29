import os
from groq import Groq

# Connect to Groq using the API key from your terminal
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Send a tiny test message
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Groq connection successful."
        }
    ],
)

# Display the model's reply
print(response.choices[0].message.content)