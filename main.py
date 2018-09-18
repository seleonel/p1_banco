#################################################################
# Basicamente começar com um loop infinito, sempre pedindo por  #
# comandos do usuário (retorno da função menuPrincipal)         #
# ###############################################################
# biblioteca os para a remoção do arquivo
import os

def checarCPF():
    # numero de cpf é checado inumeras vezes
    while True:
        cpf = input("Agora digite seu CPF: ")
        if cpf == "" or int(cpf) <= 0:
            print("Digite um valor válido para seu CPF")
        else:
            break
    return cpf


# funcao que retorna o arquivo para a conta para o cliente
def escreverArq(cpf):
    return open("usuarios/%s.txt" % cpf, "w")


def menuPrincipal():
    # 3 aspas funciona como strings de multilinhas, aqui posso "desenhar" um menu mais
    # bonito, retorno uma int de qualquer forma
    print("""
             ******************************************
             *          Banco QuemPoupaTem            *
             ******************************************
             * 1 - Novo Cliente                       *
             * 2 - Apaga Cliente                      *
             * 3 - Debita                             *
             * 4 - Deposita                           *
             * 5 - Saldo                              *
             * 6 - Extrato                            *
             *                                        *
             * 0 - Sair                               *
             ****************************************** """)
    return int(input("""
             *  Digite a operação desejada:           *
             ******************************************
    """))



def novoCliente():
    # série de loops para checar potenciais e intencionais erros e bugs de input, nem todos foram filtrados,
    # mas a maioria deles foram neutralizados
    nome_usuario = input("Digite seu nome: ")
    cpf_usuario = checarCPF();
    # criado um arquivo unico para cada usuario
    # caso haja falha num arquivo, nem todos os dados seriam perdidos
    arquivo_user = escreverArq(cpf_usuario)

    while True:
        tipo_conta = input("Digite o tipo de sua conta (salário, comum ou plus?): ")
        if tipo_conta == "salário" or tipo_conta == "salario" or tipo_conta == "comum" or tipo_conta == "plus":
            break
        else:
            print("Por favor, digite corretamente o tipo de sua conta")
    while True:
        valor_inicial = input("Digite um valor inicial para sua conta: ")
        if valor_inicial == "":
            print("Digite um valor inicial válido")
        elif float(valor_inicial) < 0:
            print("Digite um valor inicial válido")
        else:
            break
    while True:
        senha_usuario = input("Agora digite sua senha para finalizar a sua criação de conta: ")
        if senha_usuario == "":
            print("Por favor, digite uma senha válida")
        else:
            break
    # A partir de agora, vou apenas trabalhar com essa ordem,

    arquivo_user.write("%s\n%s\n%s\n%s\n%s\n" % (cpf_usuario, nome_usuario, tipo_conta, valor_inicial, senha_usuario))
    arquivo_user.close()
    print("Parabéns! Sua conta foi criada com sucesso.")



def apagarCliente():
    pergunta = input("Deseja mesmo deletar sua conta? ")
    if pergunta == "sim" or pergunta == "Sim" or pergunta == "SIM":
        cpf_usuario = checarCPF()
        # funcao os remove apaga o arquivo
        os.remove("usuarios/%s.txt" % cpf_usuario)
        print("Sua conta foi deletada com sucesso")
    else:
        # qualquer erro de digitação será desconsiderado para evitar acidentes
        # usuario será jogado para o menu principal
        print("Sua conta NÂO foi deletada ")


def contaDebito():
    cpf_usuario = checarCPF()

def contaDeposito():
    cpf_usuario = checarCPF()

def contaSaldo():
    cpf_usuario = checarCPF()

def contaExtrato():
    cpf_usuario = checarCPF()


while True:
    itens_menu = menuPrincipal();

    if itens_menu == 1:
        novoCliente();
    elif itens_menu == 2:
        apagarCliente();
    elif itens_menu == 3:
        contaDebito();
    elif itens_menu == 4:
        contaDeposito();
    elif itens_menu == 5:
        contaSaldo();
    elif itens_menu == 6:
        contaExtrato();
    else:
        break

print("Operação finalizada com sucesso! ")
