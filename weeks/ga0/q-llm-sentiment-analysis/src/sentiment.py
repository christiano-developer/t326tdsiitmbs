import httpx

# Exact test text (note the DOUBLE space between "qZMGqx7" and "XJHhTji3")
TEXT = "U8jxE atNpVd TsBW qZMGqx7  XJHhTji3 D9cZtLdOsqCgM"

response = httpx.post(
    "https://api.openai.com/v1/chat/completions",
    headers={
        "Authorization": "Bearer dummy-api-key",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Analyze the sentiment of the user's text. "
                    "Classify it as exactly one of: GOOD, BAD, or NEUTRAL. "
                    "Reply with only that one word."
                ),
            },
            {"role": "user", "content": TEXT},
        ],
    },
)
response.raise_for_status()
print(response.json()["choices"][0]["message"]["content"])
