#################################################################
# Basicamente começar com um loop infinito, sempre pedindo por  #
# comandos do usuário (retorno da função menuPrincipal)         #
# ###############################################################
# bibliotecas para a remoção dos arquivos (no OS) e pegar o tempo
import os
from datetime import datetime


def pedirDinheiro():
    return float(input("Digite um valor em reais: "))

def retornoHist(cpf):
    # sempre vai retornar o historico do cpf pedido
    lista_historico = []
    hist_user = lerHist(cpf)
    for linhas in hist_user:
        lista_historico.append(linhas.split(" "))
    hist_user.close()
    return lista_historico

def checarCPF():
    # numero de cpf é chamado muitas vezes no programa
    # por isso, é melhor criar uma função
    while True:
        cpf = input("Agora digite seu CPF: ")
        if cpf == "" or int(cpf) <= 0:
            print("Digite um valor válido para seu CPF")
        else:
            break
    return cpf

def checarConta(cpf):
    # maneira de checar se arquivo existe, logo, também checa o cpf
    # retorna True se arquivo existe
    return os.path.isfile("usuarios/%s.txt" % cpf)


def checarSenha(arquivo):
    # senha também importante checar
    tentativas = 0
    itens = arquivo.readlines()
    senha_user = itens[3].strip("\n")
    # usuario tem 3 tentativas para acertar a senha
    while tentativas < 3:
        # comparo a senha digitada com o que foi registrado no arquivo
        senha_dig = input("Por favor digite sua senha: ")
        if senha_user == senha_dig:
            return True
        else:
            print("Tente novamente")
            tentativas += 1
    else:
        print("3 tentativas foram estouradas")



def operacaoDebito(cpf):
        # aqui é feita a operação para debito
        # é apenas lido e convertido o ultimo termo da lista
        # que sempre será o valor total
        arquivo_user = lerArq(cpf)
        valores_hist = retornoHist(cpf)
        itens = arquivo_user.readlines()
        # variaveis definidas a partir do ultimo termo e ultima lista da lista
        valor_total = float(valores_hist[-1][-1])
        valor_pedido = pedirDinheiro()
        hist_user = modificarHist(cpf)
        if itens[2].strip("\n") == "salario" or itens[2] == "salário":
            # taxa de 5%
            taxa_deb = valor_pedido * 0.05
            novo_total = valor_total - (valor_pedido * 1.05) # taxas
            if novo_total < 0:
                print("Contas salário não podem ter saldo negativo")
            else:
                hist_user.write("%s %s %s %s %s\n" % (pegarTempo(), "-", valor_pedido, taxa_deb, novo_total))
                print("Débito realizado com sucesso! ")

        elif itens[2].strip("\n") == "comum":
            # taxa de 3%
            taxa_deb = valor_pedido * 0.03
            novo_total = valor_total - (valor_pedido * 1.03)
            if novo_total < -500:
                print("Contas comum não podem ter saldo negativo menor que R$ 500")
            else:
                hist_user.write("%s %s %s %s %s\n" % (pegarTempo(), "-", valor_pedido, taxa_deb, novo_total))
                print("Débito realizado com sucesso! ")

        elif itens[2].strip("\n") == "plus":
            # taxa de 1%
            taxa_deb = valor_pedido * 0.01
            novo_total = valor_total - (valor_pedido * 1.01)
            if novo_total < -5000:
                print("Contas plus não podem ter saldo negativo menor que R$ 5000")
            else:
                hist_user.write("%s %s %s %s %s\n" % (pegarTempo(), "-", valor_pedido, taxa_deb, novo_total))
                print("Débito realizado com sucesso! ")

        else:
            print("Sua conta foi criada incorretamente")


        arquivo_user.close()
        hist_user.close()


def operacaoDeposito(cpf):
    valores_hist = retornoHist(cpf)
    # mesmo processo que no debito
    valor_total = float(valores_hist[-1][-1])
    valor_pedido = pedirDinheiro()
    hist_user = modificarHist(cpf)
    novo_total = valor_pedido + valor_total
    taxa = 0
    hist_user.write("%s %s %s %s %s\n" % (pegarTempo(), "+", valor_pedido, taxa, novo_total))
    print("Deposito realizado com sucesso! ")



def operacaoSaldo(cpf):
    # Saldo apenas mostra(print) qual o valor total da conta
    valores_hist = retornoHist(cpf)
    valor_total = float(valores_hist[-1][-1])
    print("O seu saldo na conta é R$", valor_total)
    if valor_total < 0:
        print("Lembre-se de pagar suas contas :D")

def operacaoExtrato(cpf):
    valores_hist = retornoHist(cpf)
    arquivo_user = lerArq(cpf)
    itens = arquivo_user.readlines()
    print("")
    print("Nome: {}CPF: {}Conta: {}" .format(itens[1], itens[0], itens[2]))
    for listas in valores_hist:
        print("Data: {} {} {} {:^12.2f} {} {:5.2f} {} {:>12.2f} ".format(listas[0], listas[1], listas[2], float(listas[3]),"Tarifa:", float(listas[4]),"Saldo:", float(listas[5])))

# funcoes que retornam o arquivo para a conta para o cliente nos modos
# escrita, modificação e leitura, podem haver problemas de permissões em sistemas
# como gnu/linux, não testado em mac

def escreverArq(cpf):
    return open("usuarios/%s.txt" % cpf, "w")

def modificarArq(cpf):
    return open("usuarios/%s.txt" % cpf, "a")

def lerArq(cpf):
    return open("usuarios/%s.txt" % cpf, "r")
# funcoes para leitura, escrita e alteração de historicos
def escreverHist(cpf):
    return open("historico/historico_%s.txt" % cpf, "w")

def modificarHist(cpf):
    return open("historico/historico_%s.txt" % cpf, "a")

def lerHist(cpf):
    return open("historico/historico_%s.txt" % cpf, "r")
# funcao para retornar o tempo
def pegarTempo():
    return datetime.now().strftime('%Y-%m-%d %H:%M')

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
    historico_user = escreverHist(cpf_usuario)
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
    valor_total = valor_inicial
    # A partir de agora, vou apenas trabalhar com essa ordem de itens
    arquivo_user.write("%s\n%s\n%s\n%s\n" % (cpf_usuario, nome_usuario, tipo_conta, senha_usuario))
    if valor_inicial == "0":
        historico_user.write("%s %s %s 0 %s\n" % (pegarTempo(), "", valor_inicial, valor_total)) # Valor inicial nulo como primeiro "débito"
    else:
        historico_user.write("%s %s %s 0 %s\n" % (pegarTempo(), "+", valor_inicial, valor_total))

    arquivo_user.close()
    historico_user.close()
    print("Parabéns! Sua conta foi criada com sucesso.")



def apagarCliente():
    pergunta = input("Deseja mesmo deletar sua conta? ")
    if pergunta == "sim" or pergunta == "Sim" or pergunta == "SIM":
        cpf_usuario = checarCPF()
        # funcao os remove apaga o arquivo
        if checarConta(cpf_usuario):
            os.remove("usuarios/%s.txt" % cpf_usuario)
            os.remove("historico/historico_%s.txt" % cpf_usuario)
            print("Sua conta foi deletada com sucesso")
        else:
            print("Sua conta não existe ou foi digitada incorretamente")
    else:
        # qualquer erro de digitação será desconsiderado para evitar acidentes
        # usuario será jogado para o menu principal
        print("Sua conta NÂO foi deletada ")


def contaDebito():
    cpf_usuario = checarCPF()
    if checarConta(cpf_usuario):
        arquivo_user = lerArq(cpf_usuario);
        if checarSenha(arquivo_user):
            arquivo_user.close()
            operacaoDebito(cpf_usuario);
    else:
        print("Sua conta não existe ou não foi digitada corretamente")

def contaDeposito():
    cpf_usuario = checarCPF()
    if checarConta(cpf_usuario):
        operacaoDeposito(cpf_usuario);
    else:
        print("Sua conta não existe ou não foi digitada corretamente")


def contaSaldo():
    cpf_usuario = checarCPF()
    if checarConta(cpf_usuario):
        arquivo_user = lerArq(cpf_usuario);
        if checarSenha(arquivo_user):
            arquivo_user.close()
            operacaoSaldo(cpf_usuario);
    else:
        print("Sua conta não existe ou não foi digitada corretamente")

def contaExtrato():
    cpf_usuario = checarCPF()
    if checarConta(cpf_usuario):
        arquivo_user = lerArq(cpf_usuario);
        if checarSenha(arquivo_user):
            arquivo_user.close()
            operacaoExtrato(cpf_usuario);
    else:
        print("Sua conta não existe ou não foi digitada corretamente")


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
