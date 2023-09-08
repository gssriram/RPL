# Use a pipeline as a high-level helper
import gradio as gr
import time
from transformers import pipeline

pipe = pipeline("text-generation", model="sriramgs/rpl_gpt2")

with gr.Blocks() as demo:

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask me your doubts")
    clear = gr.Button("Clear")

    def user(user_message, history):
        global query
        query = user_message
        return "", history + [[user_message, None]]

    def model_response(query):
        a = pipe("Q: " + str(query))
        a = a[0]['generated_text'].split('\n')[1][3:]
        return a

    def bot(history):
        bot_message = model_response(query)
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            time.sleep(0.05)
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch(debug = True)