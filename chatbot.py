import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("AI: Configuration error. API key is missing.")
    exit()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

conversation = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. Give clear and simple answers."
    }
]

print("\n🤖 AI CHATBOT")
print("Type your message and press Enter.")
print("Type 'exit' to close the chatbot.\n")

while True:

    user_message = input("You: ").strip()

    if not user_message:
        continue

    if user_message.lower() == "exit":
        print("AI: Goodbye! 👋")
        break

    conversation.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=conversation
        )

        ai_message = response.choices[0].message.content

        print(f"AI: {ai_message}\n")

        conversation.append({
            "role": "assistant",
            "content": ai_message
        })

    except Exception:
        print("AI: Sorry, I couldn't respond right now. Please try again.\n")
        conversation.pop()