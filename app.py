import os
import openai
import gradio as gr

#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
openai.api_key = "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"

start_sequence = "\nShakespeare:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation in the style of William Shakespeare.\n\nShakespeare: Hello, I'm the best person to talk to. Nobody talks better than me. What can I do for you today?\nHuman:"

#def openai_create(prompt):

#    response = openai.Completion.create(
#    model="text-davinci-003",
#    prompt=prompt,
#    temperature=0.9,
#    max_tokens=150,
#    top_p=1,
#    frequency_penalty=0,
#    presence_penalty=0.6,
#    stop=[" Human:", " AI:"]
#    )

#    return response.choices[0].text


def openai_create(prompt):

    # Get user input
    user_input = prompt.split("Human:")[-1].strip()

    # Concatenate user input with existing prompt
    new_prompt = prompt + f"\nShakespeare: {user_input} respond as William Shakespeare."

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=new_prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    return response.choices[0].text



def chatgpt_clone(input, history):
    history = history or []
    # Append the user input to the conversation history
    history.append(('Human:', input))
    # Concatenate the history to form the new prompt
    prompt = restart_sequence.join(["".join(i) for i in history])
    # Generate response from OpenAI
    response = openai_create(prompt)
    # Append the response to the conversation history
    history.append(('Shakespeare:', response))
    # Return the updated history
    return history, history


block = gr.Blocks()


with block:
    gr.Markdown("""<h1><center>SaulGPT</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

# block.launch(debug = True)
block.launch(share=True)
