
Descrição Detalhada do Projeto: Reconhecimento Facial
Objetivo:

Este projeto tem como objetivo desenvolver um sistema de reconhecimento facial que utilize uma interface gráfica para carregar imagens de teste e comparar com um banco de dados de pessoas previamente cadastradas. O sistema exibe o resultado do reconhecimento, incluindo o nome da pessoa identificada, a pontuação de similaridade e a imagem da pessoa na interface.

Funcionalidades:

Carregar imagem de teste a partir do computador do usuário;
Comparar a imagem de teste com o banco de dados de pessoas cadastradas;
Identificar a pessoa mais similar na imagem de teste;
Exibir o nome da pessoa identificada, a pontuação de similaridade e a imagem da pessoa na interface;
Cadastrar novas pessoas no banco de dados, incluindo imagem e nome.
Tecnologias Utilizadas:

Python: Linguagem de programação principal;
tkinter: Biblioteca para criação de interfaces gráficas;
customtkinter: Biblioteca para criação de interfaces gráficas com tema personalizado;
facenet_pytorch: Biblioteca para reconhecimento facial com modelo InceptionResnetV1;
torchvision: Biblioteca para operações de pré-processamento de imagens;
numpy: Biblioteca para computação numérica;
PIL: Biblioteca para manipulação de imagens;
sklearn.neighbors: Biblioteca para algoritmos de K Nearest Neighbors;
firebase-admin: Biblioteca para integração com o Firebase;
Arquitetura do Sistema:

O sistema é composto por dois arquivos principais:

UI.py: Implementa a interface gráfica do usuário, utilizando a biblioteca customtkinter. As funções principais incluem:
carregar_imagem_e_reconhecer(): Carrega a imagem de teste, inicia o reconhecimento facial em uma thread separada e atualiza a interface com os resultados.
atualizar_interface(): Atualiza a interface com os resultados do reconhecimento facial, incluindo nome da pessoa identificada, pontuação de similaridade, imagens e mensagens.
mostrar_imagem(): Mostra a imagem na interface gráfica.
Reconhecimento_Facial.py: Implementa as funções de reconhecimento facial, utilizando o modelo InceptionResnetV1 e a biblioteca firebase-admin para interagir com o banco de dados Firebase. As funções principais incluem:
extrair_vetor_descritor(): Extrai o vetor descritor da imagem de teste.
incluir_pessoa(): Inclui uma nova pessoa no banco de dados Firebase, armazenando a imagem Base64 e o nome.
reconhecimento_facial_com_imagem(): Realiza o reconhecimento facial na imagem de teste, retornando o nome da pessoa identificada, a pontuação de similaridade, a imagem da pessoa identificada e a imagem de teste.
Banco de Dados:

O banco de dados utiliza o Firebase Firestore para armazenar as imagens e os nomes das pessoas cadastradas. Cada documento na coleção "Pessoas" representa uma pessoa e possui o seguinte campo:

ImagemBase64: Imagem da pessoa codificada em Base64;

Fluxo de Execução:

O usuário inicia a aplicação;
A interface gráfica é exibida, permitindo que o usuário carregue uma imagem de teste;
Ao carregar a imagem, a função carregar_imagem_e_reconhecer() é chamada:
A função abre a imagem de teste;
Extrai o vetor descritor da imagem de teste;
Chama a função reconhecimento_facial_com_imagem() para realizar o reconhecimento facial;
Atualiza a interface gráfica com os resultados do reconhecimento.
A função reconhecimento_facial_com_imagem():
Extrai o vetor descritor da imagem de teste;
Utiliza o algoritmo K Nearest Neighbors para comparar o vetor descritor da imagem de teste com os vetores descritores das pessoas cadastradas no banco de dados;
Retorna o nome da pessoa mais similar, a pontuação de similaridade, a imagem da pessoa identificada e a imagem de teste.
A função atualizar_interface() atualiza a interface gráfica com os resultados do reconhecimento:
Exibe o nome da pessoa identificada, a pontuação de similaridade e as imagens;
Se a pessoa não for identificada, permite que o usuário cadastre a pessoa no banco de dados.
Considerações Adicionais:

O sistema utiliza um modelo de reconhecimento facial pré-treinado, o InceptionResnetV1. A performance do reconhecimento pode variar de acordo com a qualidade da imagem e a quantidade de pessoas cadastradas no banco de dados
