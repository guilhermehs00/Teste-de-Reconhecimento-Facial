import torch
import shutil
from facenet_pytorch import InceptionResnetV1
from torchvision import transforms
import numpy as np
from PIL import Image
import os
from sklearn.neighbors import NearestNeighbors

# Carregar o modelo pré-treinado
model = InceptionResnetV1(pretrained='vggface2').eval()

# Função para extrair vetor descritor
def extrair_vetor_descritor(imagem):
    try:
        img = Image.open(imagem).convert('RGB')
    except Exception as e:
        print(f"Erro ao abrir a imagem: {e}")
        return None

    transform = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        vetor_descritor = model(img_tensor).numpy().flatten()
    return vetor_descritor

# Carregar conjunto de dados de celebridades e criar banco de dados
diretorio_celebridades = "Pessoas"
descritores = []
nomes = []

# Iterar sobre as subpastas no diretório das celebridades
for pasta in os.listdir(diretorio_celebridades):
    subpasta_path = os.path.join(diretorio_celebridades, pasta)
    if os.path.isdir(subpasta_path):
        for arquivo in os.listdir(subpasta_path):
            if arquivo.endswith(".jpg") or arquivo.endswith(".png"):
                nome_celebridade = pasta
                caminho_imagem = os.path.join(subpasta_path, arquivo)
                vetor_descritor = extrair_vetor_descritor(caminho_imagem)
                if vetor_descritor is not None:
                    descritores.append(vetor_descritor)
                    nomes.append(nome_celebridade)

# Ajustar o modelo Nearest Neighbors
knn = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(descritores)

# Função para incluir uma nova pessoa no banco de dados
def incluir_pessoa(nome, imagem):
    vetor_descritor = extrair_vetor_descritor(imagem)
    if vetor_descritor is None:
        print("Erro ao extrair o vetor descritor da nova pessoa.")
        return
    
    descritores.append(vetor_descritor)
    nomes.append(nome)
    knn.fit(descritores, nomes)

    # Criar uma pasta com o nome da pessoa, se não existir
    pasta_pessoa = os.path.join(diretorio_celebridades, nome)
    if not os.path.exists(pasta_pessoa):
        os.makedirs(pasta_pessoa)

    # Copiar a imagem para a pasta da pessoa
    caminho_imagem_destino = os.path.join(pasta_pessoa, os.path.basename(imagem))
    shutil.copyfile(imagem, caminho_imagem_destino)

# Função para realizar o reconhecimento facial e exibir resultados
def reconhecimento_facial_com_imagem(imagem):
    vetor_descritor_desconhecido = extrair_vetor_descritor(imagem)
    if vetor_descritor_desconhecido is None:
        print("Erro ao extrair o vetor descritor da imagem de teste.")
        return None, None, None, None, None
    
    distancia, indice = knn.kneighbors([vetor_descritor_desconhecido], n_neighbors=1)
    nome_identificado = nomes[indice[0][0]]
    score_similaridade = 1 / (1 + distancia[0][0])

    # Definir um limiar de similaridade (ajuste conforme necessário)
    limiar_similaridade = 0.5

    if score_similaridade < limiar_similaridade:
        novo_identificado = True
    else:
        novo_identificado = False

    # Encontrar uma imagem da pessoa identificada na pasta correspondente
    pasta_identificada = os.path.join(diretorio_celebridades, nome_identificado)
    arquivos_imagem = [os.path.join(pasta_identificada, f) for f in os.listdir(pasta_identificada) if f.endswith((".jpg", ".png"))]
    img_identificada = Image.open(arquivos_imagem[0])

    img_teste = Image.open(imagem)

    return nome_identificado, score_similaridade, novo_identificado, img_teste, img_identificada