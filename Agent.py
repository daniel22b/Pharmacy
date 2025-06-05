import PySimpleGUI as sg
import pandas as pd
from openai import OpenAI
from dekorator import count_agent_usage
client = OpenAI(api_key="")

def query_gpt_and_find_medicine(symptoms, df, conversation_history):
    prompt = f"""
The user writes symptoms in Polish: "{symptoms}".

You are a professional and empathetic medical AI assistant speaking only in Polish.  
Your tone is calm, respectful, and clear — like a trusted doctor.

- Use previous conversation history to avoid repeating questions.
- Based on the symptoms so far, identify up to 3 possible causes.
- Recommend the most appropriate medicine from the list below, explaining briefly why.
- If information is incomplete, ask user for more details in a natural way.
- Encourage user to provide additional symptoms for a better diagnosis.
- Avoid generic or repetitive questions.
- Respond in about 80 words, only in Polish.

Medicine list:
{df['ID,DRUG,ON_RECEPT,NO_PACKAGES_AVAILABLE,DATE,RECEPT_ID,PRICE'].to_string(index=False)}
"""

    messages = conversation_history.copy()  
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=200,
        temperature=0.5
    )
    return response.choices[0].message.content


@count_agent_usage
def agent_ai():
    try:
        df = pd.read_excel("drugs.xlsx")
    except FileNotFoundError:
        sg.popup_error("Nie znaleziono pliku drugs.xlsx")
        return

    layout = [
        [sg.Multiline("Dzień dobry! Jestem agentem AI. Opisz proszę swoje objawy, a postaram się dobrać odpowiedni lek.\n", size=(60, 15), key="-CHAT-", disabled=True)],
        [sg.InputText(key="-INPUT-", size=(50, 1)), sg.Button("Wyślij"), sg.Button("Zamknij")]
    ]
    window = sg.Window("Asystent AI", layout)

    conversation_history = [
        {"role": "assistant", "content": "Dzień dobry! Jestem agentem AI. Opisz proszę swoje objawy, a postaram się dobrać odpowiedni lek."}
    ]

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Zamknij"):
            break

        if event == "Wyślij":
            user_msg = values["-INPUT-"].strip()
            if not user_msg:
                continue

            conversation_history.append({"role": "user", "content": user_msg})
            current_chat = window["-CHAT-"].get()
            window["-CHAT-"].update(f"{current_chat}\nTy: {user_msg}\n")
            window["-INPUT-"].update("")
            window.refresh()

            try:
                response = query_gpt_and_find_medicine(user_msg, df, conversation_history)
                conversation_history.append({"role": "assistant", "content": response.strip()})

                current_chat = window["-CHAT-"].get()
                window["-CHAT-"].update(f"{current_chat}\nAgent: {response.strip()}\n")  # <-- tutaj dodano \n przed Agent
            except Exception as e:
                current_chat = window["-CHAT-"].get()
                window["-CHAT-"].update(f"{current_chat}\nAgent: Wystąpił błąd: {str(e)}\n")

    window.close()
