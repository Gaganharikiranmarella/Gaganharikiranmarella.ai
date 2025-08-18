from ai_client import call_ai
import re

def remove_emojis(text):
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

class XEROAssistant:
    def __init__(self):
        self.system_prompt = (
            "You are XERO (pronounced as 'zero'), a highly intelligent, concise, and friendly personal AI assistant. "
            "You help the user with any task, provide clear, emoji-free answers, and are their trusted digital companion."
        )
        self.chat_history = []

    def ask(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})
        response = call_ai(self.chat_history, system_prompt=self.system_prompt)
        response = remove_emojis(response)
        self.chat_history.append({"role": "assistant", "content": response})
        return response
