import gradio as gr
import time
from transformers import pipeline

# Initialize the chatbot model
pipe = pipeline("text-generation", model="sriramgs/RPL_gpt2_new")
asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Create a Gradio interface
with gr.Blocks() as demo:
    play_audio = gr.Button("Play the Chatbot response")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask me your doubts")
    audio_file = [gr.Audio(source="microphone",type="filepath",optional=True),]
    record_audio = gr.Button("Convert into Text")
    clear = gr.Button("Clear the Chatbot Conversation")

    def text_to_speech():
      pass

    def user(user_message, history):
        global query
        query = user_message
        return "", history + [[user_message, None]]

    def model_response(query):
        global a
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

    def speech_to_text(mic=None, file=None):
      if mic is not None:
          audio = mic
      elif file is not None:
          audio = file
      else:
          return "You must either provide a mic recording or a file"
      text = asr(audio)["text"]
      return text

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

    clear.click(lambda: None, None, chatbot, queue=False)
    record_audio.click(speech_to_text,inputs=audio_file,outputs=msg)
    play_audio.click(text_to_speech)

demo.queue()
demo.launch(debug=True)
