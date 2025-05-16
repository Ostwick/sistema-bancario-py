import textwrap

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas
[q] Sair

=> """

# Dados iniciais
usuarios = []
contas = []

AGENCIA_PADRAO = "0001"
LIMITE_SAQUES_DIARIO = 3
LIMITE_SAQUE = 500.0

# --------------------- USUÁRIO ---------------------

def criar_usuario():
    tipo = input("Tipo de cliente [PF/PJ]: ").strip().upper()
    if tipo not in ["PF", "PJ"]:
        print("Tipo inválido.")
        return

    documento = input("Informe o CPF/CNPJ (somente números): ").strip()
    if filtrar_usuario(documento):
        print("Usuário já existe!")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nº - bairro - cidade/UF): ")

    usuario = {
        "tipo": tipo,
        "documento": documento,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "contas": []
    }

    usuarios.append(usuario)
    print("Usuário criado com sucesso!")

def filtrar_usuario(documento):
    return next((u for u in usuarios if u["documento"] == documento), None)

# --------------------- CONTA ---------------------

def criar_conta():
    documento = input("Informe o CPF/CNPJ do titular: ").strip()
    usuario = filtrar_usuario(documento)

    if not usuario:
        print("Usuário não encontrado.")
        return

    numero = len(contas) + 1

    conta = {
        "agencia": AGENCIA_PADRAO,
        "numero": numero,
        "saldo": 0.0,
        "historico": [],
        "limite_saque": LIMITE_SAQUE,
        "numero_saques": 0,
        "limite_saques_diario": LIMITE_SAQUES_DIARIO,
        "documento_cliente": documento
    }

    contas.append(conta)
    usuario["contas"].append(numero)

    print(f"Conta {numero} criada com sucesso!")

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    for conta in contas:
        usuario = filtrar_usuario(conta["documento_cliente"])
        print("=" * 30)
        print(f"Agência: {conta['agencia']}")
        print(f"C/C: {conta['numero']}")
        print(f"Titular: {usuario['nome']}")
        print("=" * 30)

def selecionar_conta():
    documento = input("Informe seu CPF/CNPJ: ").strip()
    usuario = filtrar_usuario(documento)

    if not usuario:
        print("Usuário não encontrado.")
        return None

    if not usuario["contas"]:
        print("Este usuário não possui contas.")
        return None

    print("Contas disponíveis:")
    for numero in usuario["contas"]:
        print(f"- Conta número: {numero}")

    try:
        numero = int(input("Informe o número da conta: "))
        conta = next((c for c in contas if c["numero"] == numero and c["documento_cliente"] == documento), None)
        if not conta:
            print("Conta não encontrada.")
        return conta
    except ValueError:
        print("Entrada inválida.")
        return None

# --------------------- OPERAÇÕES ---------------------

def depositar():
    conta = selecionar_conta()
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("Valor inválido.")
        return

    if valor <= 0:
        print("Valor deve ser positivo.")
        return

    conta["saldo"] += valor
    conta["historico"].append({"tipo": "Depósito", "valor": valor})
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")

def sacar():
    conta = selecionar_conta()
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("Valor inválido.")
        return

    if valor <= 0:
        print("Valor deve ser positivo.")
        return

    if valor > conta["saldo"]:
        print("Saldo insuficiente.")
    elif valor > conta["limite_saque"]:
        print("Valor excede o limite de saque.")
    elif conta["numero_saques"] >= conta["limite_saques_diario"]:
        print("Número de saques diários excedido.")
    else:
        conta["saldo"] -= valor
        conta["numero_saques"] += 1
        conta["historico"].append({"tipo": "Saque", "valor": valor})
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")

def exibir_extrato():
    conta = selecionar_conta()
    if not conta:
        return

    print("\n========== EXTRATO ==========")
    if not conta["historico"]:
        print("Não foram realizadas movimentações.")
    else:
        for item in conta["historico"]:
            print(f"{item['tipo']}: R$ {item['valor']:.2f}")
    print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")
    print("==============================")

# ===================== LAÇO PRINCIPAL =====================

def main():
    while True:
        opcao = input(menu()).strip().lower()

        if opcao == "d":
            depositar()
        elif opcao == "s":
            sacar()
        elif opcao == "e":
            exibir_extrato()
        elif opcao == "nu":
            criar_usuario()
        elif opcao == "nc":
            criar_conta()
        elif opcao == "lc":
            listar_contas()
        elif opcao == "q":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
