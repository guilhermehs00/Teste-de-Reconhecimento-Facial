import customtkinter as ctk
import base64
import threading
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import Reconhecimento_Facial as rf
from screeninfo import get_monitors

# Função para carregar imagem de teste e iniciar reconhecimento facial
def carregar_imagem_e_reconhecer():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("Arquivos de imagem", "*.jpg *.png")])
    if caminho_imagem:
        # Função a ser executada em uma thread separada
        def reconhecer_thread():
            nome_identificado, score_similaridade, novo_identificado, img_teste, img_identificada = rf.reconhecimento_facial_com_imagem(caminho_imagem)

            # Atualizar a interface gráfica com os resultados
            tela.after(0, lambda: atualizar_interface(nome_identificado, score_similaridade, novo_identificado, img_teste, img_identificada, caminho_imagem))

        # Inicia uma nova thread para o reconhecimento facial
        threading.Thread(target=reconhecer_thread).start()

# Função para atualizar a interface gráfica com os resultados do reconhecimento facial
def atualizar_interface(nome_identificado, score_similaridade, novo_identificado, img_teste, img_identificada, caminho_imagem):
    if novo_identificado:
        nome_novo = simpledialog.askstring("Pessoa não reconhecida", "Digite o nome da pessoa que será cadastrada:")
        if nome_novo:
            # Codificar a imagem em Base64
            with open(caminho_imagem, "rb") as img_file:
                imagem_bytes = img_file.read()
                imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8')
            rf.incluir_pessoa(nome_novo, imagem_base64)
            resultado = f"Pessoa não reconhecida!\nFoi adicionada ao banco de dados como {nome_novo}."
            img_identificada = Image.open("Imag2.png")  # Mostrar imagem padrão
        else:
            messagebox.showwarning("Nome não fornecido", f"Nenhum nome foi fornecido. \n A pessoa não foi cadastrada!")
            resultado = f"Pessoa não reconhecida.\n Cadastro cancelado!"
            img_identificada = Image.open("Imag2.png")  # Mostrar imagem padrão
    else:
        resultado = f"Pessoa identificada: {nome_identificado}\nScore de similaridade: {score_similaridade:.2f}"
    
    label_resultado.configure(text=resultado)
    mostrar_imagem(img_teste, label_imagem_teste, max_width=400, max_height=400)
    mostrar_imagem(img_identificada, label_imagem_identificada, max_width=400, max_height=400)


# Função para mostrar imagem na interface
def mostrar_imagem(img, label, max_width=400, max_height=400):
    # Redimensionar a imagem se necessário
    width, height = img.size
    if width > max_width or height > max_height:
        img.thumbnail((max_width, max_height), Image.LANCZOS)  
    
    img_ctk = ImageTk.PhotoImage(img)
    label.configure(image=img_ctk)
    label.image = img_ctk  # Manter referência para evitar coleta de lixo

# Interface gráfica
tela = ctk.CTk()
tela.title("Reconhecimento Facial")

# Obtém as dimensões da tela
monitor_info = get_monitors()[0]
largura_tela = monitor_info.width
altura_tela = monitor_info.height

# Define a geometria da janela para as dimensões da tela
tela.geometry(f"{largura_tela}x{altura_tela}")
tela.config(bg="#042747")

# Frame centralizado na tela com tamanho 500x500
frame_1 = ctk.CTkFrame(tela, width=950, height=650, fg_color="#042747")
frame_1.pack(anchor="center", pady=20)
frame_1.pack_propagate(False)  # Desativa a propagação de tamanho

frame_imagem = ctk.CTkFrame(frame_1, width=800, height=400, bg_color="white", fg_color="white")
frame_imagem.grid(row=0, column=0, padx=5, pady=5)

label_resultado = ctk.CTkLabel(frame_1, text="", text_color="white", font=("Arial", 20, "bold"))
label_resultado.grid(row=1, column=0, padx=5, pady=5)

botao_carregar = ctk.CTkButton(frame_1, text="Carregar Imagem de Teste", font=("Arial", 20, "bold"), bg_color="#042747", fg_color="green", command=carregar_imagem_e_reconhecer)
botao_carregar.grid(row=2, column=0, pady=10)

label_titulo_test = ctk.CTkLabel(frame_imagem, text="Imagem de teste", text_color="black", font=("Arial", 20, "bold"))
label_titulo_test.grid(row=0, column=0, padx=5, pady=5)

label_imagem_teste = ctk.CTkLabel(frame_imagem, width=400, height=400, text="")
label_imagem_teste.grid(row=1, column=0, padx=5, pady=5)
Imagem_1 = Image.open("Imag1.png")
mostrar_imagem(Imagem_1, label_imagem_teste, max_width=400, max_height=400)

label_titulo_ident = ctk.CTkLabel(frame_imagem, text="Imagem da Pessoa Identificada", text_color="black", font=("Arial", 20, "bold"))
label_titulo_ident.grid(row=0, column=1, padx=5, pady=5)

label_imagem_identificada = ctk.CTkLabel(frame_imagem, width=400, height=400, text="")
label_imagem_identificada.grid(row=1, column=1, padx=5, pady=5)
Imagem_2 = Image.open("Imag2.png")
mostrar_imagem(Imagem_2, label_imagem_identificada, max_width=400, max_height=400)

tela.mainloop()
