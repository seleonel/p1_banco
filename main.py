#################################################################
# Basicamente começar com um loop infinito, sempre pedindo por  #
# comandos do usuário (retorno da função menuPrincipal)         #
# ###############################################################
# bibliotecas para a remoção dos arquivos (no OS), procurar num "dicionario" determinadas
# expressões e letras, e datetime para pegar o tempo
import os
import re
from datetime import datetime

def pedirDinheiro():
    while True:
        # O comando try é essencialmente usado para orientação de objetos, mas é muito útil
        # quando utilizado com error handling
        # Um bloco é "experimentado/tentado", e se algum erro ocorrer, o programa não sai com o system exit
        try:
            valor_positivo = input("Digite um valor em reais: ")
            # basicamente procuro por alguma letra até o usuário digitar apenas números
            if re.search('[a-zA-Z]', valor_positivo):
                print("Digite um valor válido")
            elif valor_positivo in "!-=*&¨$#@|}{[]´":
                print("Digite um valor válido")
            elif float(valor_positivo) <= 0:
                # valores negativos podem afetar as operações
                # também não posso receber zero para depósitos ou débitos
                print("Digite um valor válido")
            else:
                return float(valor_positivo)
        except ValueError as ex:
            print("Valor válido não inserido, o valor inserido não pode ser convertido")

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
    # comando interessante para "error handling", caso haja um erro, except retornará
    # o valor 0, jogando o usuario direto para o menu
    try:
        tentativas = 0
        while tentativas < 3:
            cpf = input("Agora digite seu CPF: ")
            if cpf == ""  or re.search('[a-zA-Z]', cpf):
                print("Digite um valor válido para seu CPF")
            elif int(cpf) < 0:
                print("Digite um valor válido para seu CPF")
            else:
                return int(cpf)
            tentativas += 1
        else:
            # aqui forço o exception
            return int(cpf)
    except ValueError:
        print("O CPF não foi digitado corretamente")
        return 0

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
        # salvo no histórico o débito com os valores corrigidos para cada tipo de conta
        # é verificado o tipo de conta do usuario
        if itens[2].strip("\n") == "salario" or itens[2].strip("\n") == "salário":
            # taxa de 5%
            taxa_deb = valor_pedido * 0.05
            novo_total = valor_total - (valor_pedido * 1.05) # taxas
            if novo_total < 0:
                print("Contas salário não podem ter saldo negativo")
            else:
                hist_user.write("%s %s %s %s %s\n" % (pegarTempo(), "-", valor_pedido, taxa_deb, novo_total))
                print("Débito realizado com sucesso! ")
                print("")
                print("")

        elif itens[2].strip("\n") == "comum":
            # taxa de 3%
            taxa_deb = valor_pedido * 0.03
            novo_total = valor_total - (valor_pedido * 1.03)
            if novo_total < -500:
                print("Contas comum não podem ter saldo negativo menor que R$ 500")
            else:
                hist_user.write("%s %s %s %s %s\n" % (pegarTempo(), "-", valor_pedido, taxa_deb, novo_total))
                print("Débito realizado com sucesso! ")
                print("")
                print("")

        elif itens[2].strip("\n") == "plus":
            # taxa de 1%
            taxa_deb = valor_pedido * 0.01
            novo_total = valor_total - (valor_pedido * 1.01)
            if novo_total < -5000:
                print("Contas plus não podem ter saldo negativo menor que R$ 5000")
            else:
                hist_user.write("%s %s %s %s %s\n" % (pegarTempo(), "-", valor_pedido, taxa_deb, novo_total))
                print("Débito realizado com sucesso! ")
                print("")
                print("")

        else:
            # caso extremo, caso algo tenha sido registrado incorretamente
            # muito difícil ocorrer, mas caso hajam injeções nos arquivos
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
    taxa = 0 # não há taxa, mas para manter a organização, imprimo como 0
    hist_user.write("%s %s %s %s %s\n" % (pegarTempo(), "+", valor_pedido, taxa, novo_total))
    print("Deposito realizado com sucesso! ")
    print("")
    print("")



def operacaoSaldo(cpf):
    # Saldo apenas mostra(print) qual o valor total da conta
    valores_hist = retornoHist(cpf)
    valor_total = float(valores_hist[-1][-1]) # não é preciso converter
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
             ******************************************
             *  Digite a operação desejada:           *
             ******************************************

    """)
    tentativas = 0
    while tentativas < 5:
        escolha_user = input()
        # sempre chechando se o usuário tenta digitar letras
        # entretanto, é falho para símbolos como "-"
        if escolha_user == ""  or re.search('[a-zA-Z]', escolha_user):
            print("Digite uma opção válida")
        else:
            return int(escolha_user)
        tentativas += 1
    else:
        print("Limite de 5 tentativas atingido")
        return 0

def novoCliente():
    # série de loops para checar potenciais e intencionais erros e bugs de input, nem todos foram filtrados,
    # mas a maioria deles foram neutralizados
    nome_usuario = input("Digite seu nome: ")
    cpf_usuario = checarCPF();
    if cpf_usuario == 0:
        print("Você será levado para o menu")
        return 0
    # criado um arquivo unico para cada usuario
    # caso haja falha num arquivo, nem todos os dados seriam perdidos
    arquivo_user = escreverArq(cpf_usuario)
    historico_user = escreverHist(cpf_usuario)
    tentativas = 0
    # 3 tentativas para cada item, resetando o contador quando o loop é finalizado
    # novamente, retorno pro menu, caso algum valor não tenha sido corretamente providenciado
    while tentativas < 3:
        tipo_conta = input("Digite o tipo de sua conta (salário, comum ou plus?): ")
        if tipo_conta == "salário" or tipo_conta == "salario" or tipo_conta == "comum" or tipo_conta == "plus":
            break
        else:
            print("Por favor, digite corretamente o tipo de sua conta")
        tentativas += 1
    else:
        print("Você será levado para o menu")
        return 0
    tentativas = 0
    while tentativas < 3:
        valor_inicial = input("Digite um valor inicial para sua conta: ")
        if valor_inicial == "" or re.search("[a-zA-Z]", valor_inicial):
            print("Digite um valor inicial válido")
        elif float(valor_inicial) < 0:
            print("Digite um valor inicial válido")
        else:
            break
        tentativas += 1
    else:
        print("Você será levado para o menu")
        return 0
    tentativas = 0
    while tentativas < 3:
        senha_usuario = input("Agora digite sua senha para finalizar a sua criação de conta: ")
        if senha_usuario == "":
            # acredito que letras sejam aceitas na senha
            print("Por favor, digite uma senha válida")
        else:
            break
        tentativas += 1
    else:
        print("Você será levado para o menu")
        return 0

    valor_total = valor_inicial
    # A partir de agora, vou apenas trabalhar com essa ordem de itens
    # dados não "mutáveis" criam o perfil do usuário
    arquivo_user.write("%s\n%s\n%s\n%s\n" % (cpf_usuario, nome_usuario, tipo_conta, senha_usuario))
    # enquanto o valor inicial é gravado no histórico
    if valor_inicial == "0":
        historico_user.write("%s %s %s 0 %s\n" % (pegarTempo(), "", valor_inicial, valor_total)) # Valor inicial nulo como primeiro "débito"
    else:
        historico_user.write("%s %s %s 0 %s\n" % (pegarTempo(), "+", valor_inicial, valor_total))
    # sempre importante fechar os arquivos
    arquivo_user.close()
    historico_user.close()

    print("Parabéns! Sua conta foi criada com sucesso.")
    print("")
    print("")



def apagarCliente():
    # para apagar o cliente é necessário ter o cpf
    # adicionei uma pergunta para confirmar o desejo do usuário
    try:
        pergunta = input("Deseja mesmo deletar sua conta? ")
        if pergunta == "sim" or pergunta == "Sim" or pergunta == "SIM":
            cpf_usuario = checarCPF()
            # funcao os remove apaga o arquivo
            if checarConta(cpf_usuario):
                # funcao remove da biblioteca os apaga diretamente os arquivos
                # entretanto preciso checar se existem antes para evitar erros
                os.remove("usuarios/%s.txt" % cpf_usuario)
                os.remove("historico/historico_%s.txt" % cpf_usuario)
                print("Sua conta foi deletada com sucesso")
                print("")
                print("")
            else:
                print("Sua conta não existe ou foi digitada incorretamente")
                print("")
                print("")
        else:
            # qualquer erro de digitação será desconsiderado para evitar acidentes
            # usuario será jogado para o menu principal
            print("Sua conta NÂO foi deletada ")
    # caso dê erros de permissão, conta não será apagada
    except IOError:
            print("Sua conta não foi deletada por motivos técnicos, por favor consulte um técnico")
            return 0

def contaDebito():
    # para débito é preciso checar se a conta existe, e se a senha está correta
    cpf_usuario = checarCPF()
    if checarConta(cpf_usuario):
        arquivo_user = lerArq(cpf_usuario);
        if checarSenha(arquivo_user):
            arquivo_user.close()
            operacaoDebito(cpf_usuario);
    else:
        # mensagem de erro padrão para caso seja digitado algo incorreto
        print("Sua conta não existe ou não foi digitada corretamente")

def contaDeposito():
    # só CPF é checado para deposito
    cpf_usuario = checarCPF()
    if checarConta(cpf_usuario):
        operacaoDeposito(cpf_usuario);
    else:
        print("Sua conta não existe ou não foi digitada corretamente")


def contaSaldo():
    # saldo apenas cpf e senha são pedidos
    cpf_usuario = checarCPF()
    if checarConta(cpf_usuario):
        arquivo_user = lerArq(cpf_usuario);
        if checarSenha(arquivo_user):
            arquivo_user.close()
            operacaoSaldo(cpf_usuario);
    else:
        print("Sua conta não existe ou não foi digitada corretamente")

def contaExtrato():
    # extrato precisa de senha e cpf
    cpf_usuario = checarCPF()
    if checarConta(cpf_usuario):
        arquivo_user = lerArq(cpf_usuario);
        if checarSenha(arquivo_user):
            arquivo_user.close()
            operacaoExtrato(cpf_usuario);
    else:
        print("Sua conta não existe ou não foi digitada corretamente")


while True:
    # menu principal simples, que servirá de fallback caso algum erro ocorra
    # no caso de erros, valores nulos serão retornados
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
        # qualquer valor inválido + 0 sairá do programa por segurança
        break

print("Operação finalizada com sucesso! ")
print("")
print("")
