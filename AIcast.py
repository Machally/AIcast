from pathlib import Path                    # modulo para manipular path de arquivo
import os                                   # modulo os para leitura de arquivo .env (apikeys)
import re                                   # modulo para manipulacao de caracteres
from dotenv import load_dotenv              # modulo para carregar variaveis de ambiente
import time                                 # modulo para temporizacoes
import google.generativeai as genai         # API da google gemini
from openai import OpenAI                   # API da Open AI (usamos o text-to-speech na aplicacao)
import undetected_chromedriver as uc        # modulo para tornar o chromedriver nao detectavel como bot
from selenium.webdriver.common.by import By # modulo para automacao do navegador Chrome 
import pygame                               # modulo para stream de audio

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY2')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

client = OpenAI()

url = "https://pi.ai/talk"
browser = uc.Chrome()
browser.get(url)

print(browser.command_executor._url)
print(browser.session_id)

def play_mp3(file_path):
    # Inicializa o mixer de música do pygame d
    pygame.mixer.init()
    
    # Carrega o arquivo de música
    pygame.mixer.music.load(file_path)
    
    # Toca a música
    pygame.mixer.music.play()
    
    # Espera a música terminar ou pode adicionar uma lógica para parar a música com um evento
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def clean_responses(text):
    # Remove textos entre **
    clean_response = re.sub(r"\*\*.*?\*\*", "", text)
    # Elimina todas as instâncias de \n
    clean_response = re.sub(r"\n", " ", clean_response)
    return clean_response
        
def main():
    assistente_falante = False
    ligar_microfone = True

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    if ligar_microfone:
        import speech_recognition as sr  # pip install SpeechRecognition
        r = sr.Recognizer()
        mic = sr.Microphone(device_index=2)

    msg = """Iremos fazer um podcast. Você será o apresentador do podcast. Em seguida fará
        alguns comentários sobre a resposta que receber, e então uma fará uma nova pergunta, 
        aguardando receber uma nova resposta como input de texto. No total devem ser 5 perguntas.
        É importante que seja um conversa casual, dando respostas diretas. Não fique dizendo coisas como:
        "Claro Pi", "Obrigado pela resposta", e também não gere rótulos para as falas, como **Host**, **Pi**. 
        Não agradeça pelas respostas. O nosso primeira tema será: "A geração de vídeo a partir de comandos textuais por IA: 
        O Modelo Sora da Open AI e seus impactos na humanidade".
        Faça uma apresentação do podcast chamado "AItalks", se apresente como a inteligência artificial 'Gemini', 
        explique para seu convidado a dinâmica do podcast (você faz a pergunta, o convidado responde de forma direta). 
        Introduza seu convidado, o Pi, inteligência artificial da empresa 'Inflection AI'. 
        Faça a primeira pergunta, e NÃO gere as respostas para as perguntas, faça uma nova pergunta APENAS quando receber 
        a resposta anterior como input, uma de cada vez.
        NÃO GERE seções como **Apresentação**, **Introdução**, **Primeira Pergunta**... preciso que seja plain text.
        Ao receber todas as respostas, no final, você deve agradecer ao convidado, e se despedir."""
         
    response = chat.send_message(msg)
    clean_response = clean_responses(response.text)
    print("Gemini:", clean_response, "\n")
    
    msg = "Vamos conversar em português, ok? " + clean_response
           
    browser.find_element('xpath', '//*[@id="__next"]/main/div/div/div[3]/div[1]/div[4]/div/div/textarea').send_keys(msg)
    time.sleep(2) 
    browser.find_element('xpath', '//*[@id="__next"]/main/div/div/div[3]/div[1]/div[4]/div/button').click()
    browser.find_element('xpath', '//*[@id="__next"]/main/div/div/div[3]/div[2]/div[2]/div/div[2]/button').click()
    browser.find_element('xpath', '//*[@id="__next"]/main/div/div/div[3]/div[2]/div[2]/div/div[1]/button[1]').click()
    time.sleep(1)
    
    while True:
        if ligar_microfone:
            with mic as fonte:
                r.adjust_for_ambient_noise(fonte)
                print("Fale alguma coisa (ou diga 'desligar')")
                audio = r.listen(fonte)
                print("Enviando para reconhecimento")
                try:
                    texto = r.recognize_google(audio, language="pt-BR")
                    print("Pi: {}".format(texto))
                except Exception as e:
                    print("Não entendi o que você disse. Erro", e)
                    texto = ""
        else:
            texto = input("Escreva sua mensagem (ou #sair): ")

        if texto.lower() == "desligar":
            break

        response = chat.send_message(texto)
        clean_response = clean_responses(response.text)
        print("Gemini:", clean_response, "\n")

        browser.find_element('xpath', '//*[@id="__next"]/main/div/div/div[3]/div[1]/div[4]/div/div/textarea').send_keys(clean_response)
        time.sleep(2) 
        browser.find_element('xpath', '//*[@id="__next"]/main/div/div/div[3]/div[1]/div[4]/div/button').click()
        
        if assistente_falante:
            speech_file_path = Path(__file__).parent / "speech.mp3"        
            with client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice="alloy",
                input=response.text,
            ) as response:
                response.stream_to_file(speech_file_path)
            
            play_mp3('speech.mp3')

    print("Encerrando Chat")

if __name__ == '__main__':
    main()