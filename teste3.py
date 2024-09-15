import requests
import json
import speech_recognition as sr
import pyttsx3

# Configuração do pyttsx3
alexa = pyttsx3.init()
alexa.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_MARIA_11.0')
alexa.setProperty('volume', 1.0)
alexa.setProperty('rate', 160)

# Função para obter resposta do modelo
def obter_resposta(pergunta):
    url = "http://localhost:11434/api/generate"
    input_json = {
        "model": "llama3.1",
        "prompt": "responda sucintamente em português em poucas palavras em um parágrafo: " + pergunta
    }
    response = requests.post(url, json=input_json)
    linhas = response.text.strip().split('\n')
    valores_response = [json.loads(linha).get('response') for linha in linhas]
    return ''.join(valores_response)

# Função para reconhecimento de fala e cálculo
def reconhecer_e_calcular():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as mic:
        reconhecedor.adjust_for_ambient_noise(mic, duration=2)
        print("O que deseja calcular?")
        alexa.say("O que deseja calcular?")
        alexa.runAndWait()
        audio = reconhecedor.listen(mic)
        print("Aguarde...")
        texto = reconhecedor.recognize_google(audio, language='pt')
        print(texto)
        conta = texto.split()
        resultado = None
        try:
            if conta[1] == '/' and float(conta[2]) != 0:
                resultado = float(conta[0]) / float(conta[2])
            elif conta[1] == '+':
                resultado = float(conta[0]) + float(conta[2])
            elif conta[1] == '-':
                resultado = float(conta[0]) - float(conta[2])
            elif conta[1] == 'x':
                resultado = float(conta[0]) * float(conta[2])
        except:
            print("Ops, não consegui entender.")
            alexa.say("Ops, não consegui entender.")
            alexa.runAndWait()
        if resultado is not None:
            print(resultado)
            alexa.say("O resultado é " + str(resultado))
            alexa.runAndWait()

# Loop infinito
while True:
    pergunta = input("O que deseja saber? ")
    print("Aguarde...carregando...")
    resposta = obter_resposta(pergunta)
    print(resposta)
    reconhecer_e_calcular()
