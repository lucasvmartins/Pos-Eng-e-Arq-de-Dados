import csv
from cryptography.fernet import Fernet

# ==============================
# Função para gerar e salvar chave
# ==============================
def gerar_chave(arquivo_chave="chave.key"):
    chave = Fernet.generate_key()
    with open(arquivo_chave, "wb") as f:
        f.write(chave)
    print(f"Chave gerada e salva em {arquivo_chave}")

# ==============================
# Função para carregar a chave
# ==============================
def carregar_chave(arquivo_chave="chave.key"):
    with open(arquivo_chave, "rb") as f:
        return f.read()

# ==============================
# Criptografar CSV
# ==============================
def criptografar_csv(arquivo_csv, arquivo_saida, chave):
    fernet = Fernet(chave)

    with open(arquivo_csv, newline='', encoding="utf-8") as csvfile:
        leitor = list(csv.reader(csvfile))

    # Mantém a primeira linha (cabeçalho) sem alteração
    cabecalho = leitor[0]
    linhas = leitor[1:]

    linhas_cripto = []
    for linha in linhas:
        nova_linha = [linha[0]]  # mantém a primeira coluna sem criptografia
        for valor in linha[1:]:
            valor_bytes = valor.encode("utf-8")
            valor_cripto = fernet.encrypt(valor_bytes).decode("utf-8")
            nova_linha.append(valor_cripto)
        linhas_cripto.append(nova_linha)

    # Salva no novo CSV
    with open(arquivo_saida, "w", newline='', encoding="utf-8") as csvfile:
        escritor = csv.writer(csvfile)
        escritor.writerow(cabecalho)
        escritor.writerows(linhas_cripto)

    print(f"Arquivo criptografado salvo em {arquivo_saida}")

# ==============================
# Descriptografar CSV
# ==============================
def descriptografar_csv(arquivo_csv, arquivo_saida, chave):
    fernet = Fernet(chave)

    with open(arquivo_csv, newline='', encoding="utf-8") as csvfile:
        leitor = list(csv.reader(csvfile))

    cabecalho = leitor[0]
    linhas = leitor[1:]

    linhas_decripto = []
    for linha in linhas:
        nova_linha = [linha[0]]  # mantém a primeira coluna sem alteração
        for valor in linha[1:]:
            valor_bytes = valor.encode("utf-8")
            valor_decripto = fernet.decrypt(valor_bytes).decode("utf-8")
            nova_linha.append(valor_decripto)
        linhas_decripto.append(nova_linha)

    with open(arquivo_saida, "w", newline='', encoding="utf-8") as csvfile:
        escritor = csv.writer(csvfile)
        escritor.writerow(cabecalho)
        escritor.writerows(linhas_decripto)

    print(f"Arquivo descriptografado salvo em {arquivo_saida}")


# ==============================
# Exemplo de uso
# ==============================

i = 1
op = 4
while i == 1:
    # Gera chave apenas uma vez
    print("1- Gerar senha")
    print("2- Criptografar arquivo")
    print("3- Decriptografar arquivo")
    print("0- Sair")
    while op not in [1, 2, 3, 0]:
        op = int(input("Escolha uma opção correta: "))
    

    if op == 1:
        gerar_chave()
        chave = carregar_chave()
    elif op == 2:
        criptografar_csv("dados.csv", "dados_criptografados.csv", chave)
    elif op == 3:
        descriptografar_csv("dados_criptografados.csv", "dados_decriptografados.csv", chave)
    else:
        i = 0
        print("Até a próxima!")
    op = 4

