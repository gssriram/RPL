import gradio as gr
import time
from transformers import pipeline
from gtts import gTTS

# Initialize the chatbot model
pipe = pipeline("text-generation", model="sriramgs/RPL_gpt2_new")
asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")
global bot_message
# Create a Gradio interface
with gr.Blocks() as demo:

    chatbot = gr.Chatbot(avatar_images=("human.png", "bot.png"), value=[[None, "Welcome to the Indore-Ekk Number Superstore family! We're thrilled to have you on board. \n How can I assist you today?"]])
    with gr.Row(label="Voice Input and Output"):
        with gr.Column(variant="panel"):
            audio_file = gr.Audio(label='Voice based Input',source="microphone",type="filepath",optional=True)
        with gr.Column(variant="panel"):
            play_audio = gr.Audio(label='Output Audio', autoplay=True)
    audio_out = gr.Textbox(visible=False)

    with gr.Row(label="Voice Input and Output"):
        with gr.Column(label='Text Based Input', variant="panel"):
            msg = gr.Textbox(placeholder="Ask me your doubts")
        with gr.Column(variant="panel"):
          with gr.Row():
            clear = gr.Button("Clear the Chatbot Conversation")

    def text_to_speech(text):
      var = gTTS(text = text,lang = 'en')
      var.save('eng.mp3')
      return gr.Audio.update(value='eng.mp3')

    def user(user_message, history):
        global query
        global fck
        query = user_message
        fck = model_response(query)
        print(user_message,fck)
        return '', history + [[user_message, None]],gr.Textbox.update(value=fck)

    def model_response(query):
        global a
        a = pipe("Q: " + str(query))
        a = a[0]['generated_text'].split('\n')[1][3:]
        return a

    def bot(history):
      global bot_message
      bot_message = model_response(query)
      history[-1][1] = ""
      for character in fck:
          history[-1][1] += character
          time.sleep(0.05)
          yield history


    def speech_to_text(audio_file,history):
      if audio_file == None:
        return "", history + [[None, None]]
      else:
        global query
        global fck
        text = asr(audio_file)["text"]
        query = text
        fck = model_response(query)
        print(text)
        return None, history + [[text, None]],gr.Textbox.update(value=fck)
        #return text

    audio_file.stop_recording(speech_to_text, [audio_file,chatbot], [audio_file,chatbot,audio_out], queue=False, show_progress=False).then(bot, chatbot, chatbot)

    msg.submit(user, [msg, chatbot], [msg, chatbot,audio_out], queue=False).then(
        bot, chatbot, chatbot
    )

    clear.click(lambda: None, None, chatbot, queue=False)
    audio_out.change(text_to_speech,inputs=[audio_out], outputs=play_audio)

demo.queue()
demo.launch(debug=True)
