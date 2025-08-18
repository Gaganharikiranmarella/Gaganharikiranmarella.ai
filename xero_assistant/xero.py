from ai_client import call_ai

class XEROAssistant:
    def __init__(self):
        self.system_prompt = (
            "You are XERO (pronounced as 'zero'), a highly intelligent, concise, and friendly personal AI assistant. "
            "You help the user with any task, provide clear answers, and are their trusted digital companion."
        )
        self.chat_history = []

    def ask(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})
        response = call_ai(self.chat_history, system_prompt=self.system_prompt)
        self.chat_history.append({"role": "assistant", "content": response})
        return response
