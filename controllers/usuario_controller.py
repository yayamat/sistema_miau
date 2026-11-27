import os
from datetime import datetime

from models.aluno_model import *
from controllers.aluno_controller import carregar_alunos
from utils.validacoes import *

# Caminho a partir da pasta do projeto.
# Assim funciona mesmo se o terminal estiver em outra pasta.
PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO = os.path.join(PASTA, "database", "usuarios.txt")


def salvar_usuario(usuario):

    with open(ARQUIVO, "a", encoding="utf-8") as arquivo:

        linha = (
            f"{usuario['nome']};"
            f"{usuario['email']};"
            f"{usuario['senha']};"
            f"{usuario['perfil']}\n"
        )

        arquivo.write(linha)


def gravar_todos(usuarios):

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:

        for usuario in usuarios:

            linha = (
                f"{usuario['nome']};"
                f"{usuario['email']};"
                f"{usuario['senha']};"
                f"{usuario['perfil']}\n"
            )

            arquivo.write(linha)


def carregar_usuarios():

    usuarios = []

    try:

        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:

            for linha in arquivo:

                dados = linha.strip().split(";")

                usuario = {
                    "nome": dados[0],
                    "email": dados[1],
                    "senha": dados[2],
                    "perfil": dados[3]
                }

                usuarios.append(usuario)

    except FileNotFoundError:
        print("Arquivo usuarios.txt não encontrado.")

    except IndexError:
        print("Erro: linha com formato errado em usuarios.txt.")

    return usuarios


def fazer_login(email, senha):

    usuarios = carregar_usuarios()

    for usuario in usuarios:

        if usuario["email"] == email.strip() and usuario["senha"] == senha.strip():
            return usuario

    return None


def listar_usuarios():

    usuarios = carregar_usuarios()

    if len(usuarios) == 0:
        print("Nenhum usuário cadastrado.")
        return

    for usuario in usuarios:

        print("\n----------------------")
        print("Nome:", usuario["nome"])
        print("E-mail:", usuario["email"])
        print("Perfil:", usuario["perfil"])


def atualizar_usuario(email):

    usuarios = carregar_usuarios()

    encontrado = False

    for usuario in usuarios:

        if usuario["email"].lower() == email.strip().lower():

            novo_nome = input("Novo nome: ")

            while validar_nome(novo_nome) == False:
                print("Nome inválido.")
                novo_nome = input("Novo nome: ")

            nova_senha = input("Nova senha: ")

            while nova_senha.strip() == "":
                print("A senha não pode ficar em branco.")
                nova_senha = input("Nova senha: ")

            usuario["nome"] = novo_nome
            usuario["senha"] = nova_senha

            encontrado = True

    if not encontrado:
        print("Usuário não encontrado.")
        return

    gravar_todos(usuarios)

    print("Usuário atualizado.")


def excluir_usuario(email):

    usuarios = carregar_usuarios()

    novos = []

    for usuario in usuarios:

        if usuario["email"] != email:
            novos.append(usuario)

    if len(novos) == len(usuarios):
        print("Usuário não encontrado.")
        return

    gravar_todos(novos)

    print("Usuário excluído.")


def gerar_relatorio():

    usuarios = carregar_usuarios()
    alunos = carregar_alunos()

    total_perfis = {"professor": 0, "aee": 0, "gestor": 0}

    for usuario in usuarios:
        perfil = usuario["perfil"].strip().lower()
        if perfil in total_perfis:
            total_perfis[perfil] += 1

    total_apoio = {
        "ACOMPANHAMENTO AEE": 0,
        "EM OBSERVACAO": 0,
        "SEM NECESSIDADE": 0
    }

    for aluno in alunos:

        apoio = verificar_apoio(
            aluno["laudo"],
            aluno["dificuldade"]
        )

        if apoio in total_apoio:
            total_apoio[apoio] += 1

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    texto = "===== RELATÓRIO MIAU =====\n"
    texto += f"Data: {data}\n\n"

    texto += "USUÁRIOS\n"
    texto += f"Professores: {total_perfis['professor']}\n"
    texto += f"Professores AEE: {total_perfis['aee']}\n"
    texto += f"Gestores: {total_perfis['gestor']}\n\n"

    texto += "ALUNOS\n"
    texto += f"Total: {len(alunos)}\n"

    for apoio in total_apoio:
        texto += f"{apoio}: {total_apoio[apoio]}\n"

    print("\n" + texto)

    try:

        pasta_relatorios = os.path.join(PASTA, "relatorios")
        os.makedirs(pasta_relatorios, exist_ok=True)

        nome_arquivo = os.path.join(
            pasta_relatorios,
            "relatorio_" + datetime.now().strftime("%Y-%m-%d_%H-%M") + ".txt"
        )

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

        print("Relatório salvo em:", nome_arquivo)

    except OSError:
        print("Não foi possível salvar o relatório.")