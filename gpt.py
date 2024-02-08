from openai import OpenAI

client = OpenAI(api_key='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') 

messages = [ {"role": "system", "content": 
            "You are an intelligent assistant."} ] 

print("This is your assistant, how can I help you today? When you are done, enter 'exit' to quit the program.")
while True: 
    message = input("User : ") 

    if message == 'exit':
        exit()
    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages) 
    reply = chat.choices[0].message.content 
    print(f"Bot: {reply}") 
    messages.append({"role": "assistant", "content": reply}) 
