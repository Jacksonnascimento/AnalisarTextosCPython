import tkinter as tk
from tkinter import simpledialog
from googletrans import Translator
from textblob import TextBlob
import pyodbc


def entradaTexto():
    # Solicita a entrada do usuário
    texto = simpledialog.askstring("Entrada", "Por favor, informe seu texto:")
    if texto:
        textoEmIngles = traducao_para_ingles(texto)
        resultadoSubjetividade, resultadoPolaridade, polaridade, subjetividade = analise_sentimentos(textoEmIngles)
        resultadoAnalise = "Subjetividade: " + resultadoSubjetividade + "\n" + "Polaridade: " +  resultadoPolaridade
        label_result.config(text=f"{resultadoAnalise}")
        logNoBancoDados(texto, textoEmIngles, resultadoAnalise, polaridade, subjetividade)
        return texto
    return None
def logNoBancoDados(textoorignal, textoEmIngles, resultadoAnalise, polaridade, subjetividade):
    server = 'localhost'
    database = 'ANALISE_TEXTO_SENTIMENTOS'
    username = 'sa'
    password = '87519023'

    conn_str = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=' + server + ';'
                                 'DATABASE=' + database + ';'
                                                          'UID=' + username + ';'
                                                                              'PWD=' + password
    )
    try:
        conexao = pyodbc.connect(conn_str)
        cursor = conexao.cursor()
        cursor.execute('''
                        INSERT INTO RESULTADO_ANALISE (
                                RA_TEXTO_INPUT,
                                RA_TEXTO_INGLES,
                                RA_RESULTADO_ANALISE,
                                RA_POLARIDADE,
                                RA_SUBJETIVIDADE)                       
                                VALUES (?, ?, ?, ?, ?)''',
                       (textoorignal, textoEmIngles, resultadoAnalise, polaridade, subjetividade))
        conexao.commit()
        cursor.close()
        conexao.close()
        print("Operação realizada com sucesso!")
    except pyodbc.Error as e:
        print(f"Erro: {e}")

def traducao_para_ingles(text):
    translator = Translator()
    translation = translator.translate(text, src='pt', dest='en')
    return translation.text

def analise_sentimentos(texto):


    blob = TextBlob(texto)

    # Analisar o sentimento
    sentimento = blob.sentiment

    # Interpretar o sentimento
    polaridade = sentimento.polarity
    subjetividade = sentimento.subjectivity

    # Determinar a interpretação do sentimento
    if polaridade > 0:
        if polaridade >= 0.5:
            resultadoPolaridade = "Expressa um sentimento muito positivo."
        else:
            resultadoPolaridade = "Expressa um sentimento positivo moderado."
    elif polaridade < 0:
        if polaridade <= -0.5:
            resultadoPolaridade = "Expressa um sentimento muito negativo."
        else:
            resultadoPolaridade = "Expressa um sentimento negativo moderado."
    else:
        resultadoPolaridade = "Neutro."

    if subjetividade >= 0.75:
        resultadoSubjetividade = "Altamente subjetivo."
    elif subjetividade >= 0.5:
        resultadoSubjetividade = "Subjetivo."
    else:
        resultadoSubjetividade = "Objetivo."

    return resultadoSubjetividade, resultadoPolaridade, polaridade, subjetividade

# Cria a janela principal
root = tk.Tk()
root.geometry("300x200")  # Define o tamanho da janela
root.title("Analise")

# Cria um botão que chama a função entradaTexto
btn_ask = tk.Button(root, text="Clique para inserir", command=entradaTexto)
btn_ask.pack(pady=20)

# Cria um label para mostrar o resultado
label_result = tk.Label(root, text="")
label_result.pack(pady=20)

# Executa o loop principal da janela
root.mainloop()


