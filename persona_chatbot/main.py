from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import gradio as gr

model_name = "af1tang/personaGPT"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

persona = [
    "I am a licensed therapist who listens with empathy.",
    "I provide emotional support and thoughtful responses.",
    "My goal is to help users reflect and heal."
]
persona_string = "\n".join([f"<|persona|> {p}" for p in persona])

def generate_reply(user_input, history):
    prompt = persona_string
    for message in history:
        prompt += f"\n<|user|> {message['user']}\n<|bot|> {message['bot']}"
    prompt += f"\n<|user|> {user_input}\n<|bot|>"

    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    output_ids = model.generate(
        input_ids,
        max_length=input_ids.shape[1] + 100,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.92,
        temperature=0.7,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3,
        eos_token_id=tokenizer.eos_token_id
    )
    bot_reply = tokenizer.decode(output_ids[0], skip_special_tokens=True).split("<|bot|>")[-1].strip().split("<|user|>")[0].strip()
    history.append({"user": user_input, "bot": bot_reply})
    return bot_reply, history

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Talk to a Therapist (Persona Chatbot)")
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(label="Your message", placeholder="How are you feeling today?")
    clear = gr.Button("Clear Chat")
    state = gr.State([])

    def user_message(user_input, history):
        reply, updated_history = generate_reply(user_input, history)
        messages = []
        for h in updated_history:
            messages.append({"role": "user", "content": h["user"]})
            messages.append({"role": "assistant", "content": h["bot"]})
        return messages, updated_history

    msg.submit(user_message, [msg, state], [chatbot, state])
    clear.click(lambda: ([], []), None, [chatbot, state])

demo.launch(share=True)