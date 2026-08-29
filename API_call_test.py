import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    temperature=0.2,
    system="You are a financial risk analyst. Only state facts grounded in the provided text.",
    messages=[{"role": "user", "content": "What is a liquidity risk?"}]
)
print(message.content[0].text)
print(f"Stop reason: {message.stop_reason}")