import torch
from facenet_pytorch import InceptionResnetV1
from torchvision import transforms
import numpy as np
from PIL import Image
from sklearn.neighbors import NearestNeighbors
import firebase_admin
from firebase_admin import credentials, firestore
import base64
from io import BytesIO
import threading

# Variáveis globais
model = None
db = None
pessoas_ref = None
descritores = []
nomes = []
knn = None
dados_carregados = False

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

# Função para carregar dados do Firebase em uma thread separada
def carregar_dados():
    global model, db, pessoas_ref, descritores, nomes, knn, dados_carregados

    # Carregar o modelo pré-treinado
    model = InceptionResnetV1(pretrained='vggface2').eval()
    # Inicializar o aplicativo do Firebase
    cred = credentials.Certificate("D:/Users/User/Documents/Reconhecimento_Facial_Firebase_AdminSDK.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    pessoas_ref = db.collection('Pessoas')

    pessoas = list(pessoas_ref.stream())
    # Verificar se existem documentos na coleção
    if pessoas:
        # Itera sobre documentos da coleção no BD
        for doc in pessoas:
            nome_celebridade = doc.id
            print(nome_celebridade)  # Printar o nome do documento
            imagem_base64 = doc.to_dict().get('ImagemBase64')
            if imagem_base64:
                # Decodifica a imagem Base64 para obter os dados binários da imagem
                dados_imagem = base64.b64decode(imagem_base64)
                vetor_descritor = extrair_vetor_descritor(BytesIO(dados_imagem))
                if vetor_descritor is not None:
                    descritores.append(vetor_descritor)
                    nomes.append(nome_celebridade)

        # Ajustar o modelo Nearest Neighbors apenas se houver descritores
        if descritores:
            knn = NearestNeighbors(n_neighbors=1, algorithm='auto')
            knn.fit(descritores, nomes)
    else:
        print("A coleção 'Pessoas' está vazia ou não existe.")
    
    dados_carregados = True

# Iniciar a thread para carregar dados
thread_carregar_dados = threading.Thread(target=carregar_dados)
thread_carregar_dados.start()

# Função para incluir uma nova pessoa no banco de dados
def incluir_pessoa(nome, imagem_base64):
    global knn  # Referenciar a variável global knn
    vetor_descritor = extrair_vetor_descritor(BytesIO(base64.b64decode(imagem_base64)))
    if vetor_descritor is None:
        print("Erro ao extrair o vetor descritor da nova pessoa.")
        return
    
    # Adicionar o vetor descritor e o nome da pessoa às listas locais
    descritores.append(vetor_descritor)
    nomes.append(nome)

    # Inicializar knn se ainda não estiver definido
    if knn is None:
        knn = NearestNeighbors(n_neighbors=1, algorithm='auto')

    knn.fit(descritores, nomes)

    # Criar um documento com o nome da pessoa
    doc_pessoa = pessoas_ref.document(nome)
    doc_pessoa.set({
        'ImagemBase64': imagem_base64
    })

# Função para realizar o reconhecimento facial e exibir resultados
def reconhecimento_facial_com_imagem(imagem):
    global knn  # Referenciar a variável global knn
    
    # Certifique-se de que os dados foram carregados
    if not dados_carregados:
        print("Dados ainda não foram carregados. Por favor, aguarde.")
        return None, None, False, None, None

    vetor_descritor_desconhecido = extrair_vetor_descritor(imagem)
    if vetor_descritor_desconhecido is None:
        return "", None, None, None, None
    
    if not knn or not descritores:
        # Se não há descritores ou knn não está definido, considerar a pessoa como não identificada
        return None, None, True, Image.open(imagem), None

    distancia, indice = knn.kneighbors([vetor_descritor_desconhecido], n_neighbors=1)
    nome_identificado = nomes[indice[0][0]]
    score_similaridade = 1 / (1 + distancia[0][0])

    # Definir um limiar de similaridade (ajuste conforme necessário)
    limiar_similaridade = 0.51

    if score_similaridade < limiar_similaridade:
        novo_identificado = True
    else:
        novo_identificado = False

    # Encontrar uma imagem da pessoa identificada na pasta correspondente
    doc_identificado = pessoas_ref.document(nome_identificado).get()
    dados = doc_identificado.to_dict()
    imagem_base64 = dados.get('ImagemBase64')
    imagem_bytes = base64.b64decode(imagem_base64)
    img_identificada = Image.open(BytesIO(imagem_bytes))

    img_teste = Image.open(imagem)

    return nome_identificado, score_similaridade, novo_identificado, img_teste, img_identificada
