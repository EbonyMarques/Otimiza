from domain.main import *

#results guide
#[0] - Constants([cp.Parameter(), cp.Parameter(), cp.Parameter()])
#[1] - Variables([cp.Variable(), cp.Variable(), cp.Variable()])
#[2] - Strigs(["x1","x2","x3"])

names = ["investimento", "espaço", "quantidade mínima de produto", "quantidade máxima de produto"]
messages = ["<!> Comecemos setando a função objetivo.",
            ">>> Para cada produto considerado, entre com seu custo e, por fim, com o montante disponível para investimento: ",
            "<!> Ótimo. Agora, tratemos das restrições!",
            ">>> Para cada produto considerado, entre com sua área e, por fim, com a área total disponível: ",
            "<!> Caso deseje adicionar restrição(ões) de quantidade(s) mínima(s), entre com aquele(s) produto(s) que terá(ão). Por exemplo: x1,x3,...\n<!> Caso não deseje, apenas tecle enter para continuar: ", 
            "<!> Caso deseje adicionar restrição(ões) de quantidade(s) máxima(s), entre com aquele(s) produto(s) que terá(ão). Por exemplo: x1,x3,...\n<!> Caso não deseje, apenas tecle enter para continuar: ",
            ">>> Entre com a quantidade mínima do produto ",
            ">>> Entre com a quantidade máxima do produto ",
            ">>> Para cada produto considerado, entre com seu lucro: ",
            "<?> Entre com 'e' para editar o problema originalmente definido ou com qualquer outra tecla para voltar ao menu...",
            ">>> "]
errors = ["<!> Este produto não existe: "]

def menu():
    print("*-*"*15 + "\n")
    print("<!> Bem-vindo ao Maximizer!\n<?> O que você deseja fazer?\n\n<1> Definir novo problema...\n<2> Sair.")
    while True:
        result = decisor()
        if result == 0:
            print("<!> Opção inválida!")
            continue
        elif result == 1:
            print("\n" + "*-*"*15 + "\n")
            action = new_problem()
            if action == 0:
                menu()
                break
        elif result == 2:
            print("\n<!> Obrigado por usar!")
            print("*-*"*15)
            break
        else:
            print("<!> Tente novamente!")
            continue

def decisor():
    action = input("\n"+messages[-1])
    if action == "1":
        return 1
    elif action == "2":
        return 2
    else:
        return 0
    
def new_problem():
    results = []
    constraints = []
    string_answers = []

    print("<!> Definamos um novo problema!")
    # Definição da função objetivo
    string_answers.append(
        objective(messages, results)
    )

    print(messages[2])

    # Definição da restrição de investimento
    string_answers.append(
        basic_constraint(messages[1], names[0], results, constraints, "<=")
    )

    #Definição da restrição de espaço
    string_answers.append(
        basic_constraint(messages[3], names[1], results, constraints, "<=")
    )

    #Definição da restrição de valores positivos ">=0"
    for i in range(len(results[0])):
        constraints.append(results[1][i] >= 0)
        string_answers.append(results[2][i]+" >= 0")

    #Definição da restrição de quantidades mínimas
    constraint = value_constraint([messages[4], messages[6], messages[-1]], errors, names[2], results, constraints, ">=")
    if (constraint):
        string_answers.append(constraint)

    #Definição da restrição de quantidades máximas
    constraint = value_constraint([messages[5], messages[7], messages[-1]], errors, names[3], results, constraints, "<=")
    if (constraint):
        string_answers.append(constraint)

    #Construção da função Objetivo c1*x1+c2*x2+...+cn*xn
    objetivo = results[0][0]*results[1][0]
    for i in range(1,len(results[0])):
        objetivo += results[0][i]*results[1][i]

    #Construção e resolução do problema de maximização, utilizando a biblioteca solver
    problema = cp.Problem(cp.Maximize(objetivo), constraints)
    #problema.solve(solver=cp.CPLEX)
    problema.solve()

    print("*-*"*15)
    print("Função objetivo do problema: z = %s."%(string_answers[0]))

    print("\n<!> Há", len(constraints), "restrições.\n")

    for i in range(len(string_answers)):
        if i == 0:
            continue
        else:
            print(string_answers[i])

    print()

    try:
        print("<!> Esta é a solução ótima para o problema originalmente definido:\n<!> %d = "%(int(problema.value)), end="")
        newStr_constraints = write_result(list(map(lambda x: x.value,results[1])),string_answers)
        print(newStr_constraints+'\n')
    except:
        print("<!> Não há solução ótima para o problema originalmente definido!")

    try:
        newInvConstraint = new_investiments_problem(string_answers, results, "d")
        constraints2 = constraints
        constraints2[0] = newInvConstraint[0]
        problema = cp.Problem(cp.Maximize(objetivo), constraints2)
        #problema.solve(solver=cp.CPLEX)
        problema.solve()

        print("<!> Há solução ótima para um problema com o dobro do investimento (%.1f):\n<!> %d = "%(newInvConstraint[1], int(problema.value)),end="")
        newStr_constraints = write_result(list(map(lambda x: x.value,results[1])),string_answers)
        print(newStr_constraints+'\n')
    except:
        pass

    try:
        newInvConstraint = new_investiments_problem(string_answers, results, "h")
        constraints3 = constraints
        constraints3[0] = newInvConstraint[0]
        problema = cp.Problem(cp.Maximize(objetivo), constraints3)
        #problema.solve(solver=cp.CPLEX)
        problema.solve()

        print("<!> Também há solução ótima para um problema com a metade do investimento (%.1f):\n<!> %d = "%(newInvConstraint[1], int(problema.value)),end="")
        newStr_constraints = write_result(list(map(lambda x: x.value,results[1])),string_answers)
        print(newStr_constraints+'\n')
    except:
        pass

    print(messages[9])
    action = input(messages[-1])
    print()

    if action.lower() == "e":
        print("<?> O que você deseja fazer?:\n\n<1> Editar função objetivo...\n<2> Editar restrição de Investimento...\n<3> Editar restrição de Espaço...\n<4> Editar restrição de Quantidade mínima...\n<5> Editar restrição de Quantidade máxima...\n<6> Voltar ao menu...\n\n")
        valor = input(messages[-1])
    else:
        return 0

    # if valor === 1:
    # elif valor === 2:
    # elif valor === 3:
    # elif valor === 4:
    # elif valor === 5:
    # elif valor === 6:
    #     continue
    # elif valor === 7:
    #     print("Até logo.")
    #     break