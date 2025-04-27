class Plano:

    planos = []
    id_counter = 1

    def __init__(self, nome, preco, duracao):
        """Inicializa um novo plano."""
        self.id_plano = Plano.id_counter
        Plano.id_counter += 1
        self.nome = nome
        self.preco = preco
        self.duracao = duracao
        Plano.planos.append(self)

    @classmethod
    def novo_plano(cls, nome, preco, duracao):
        novo = cls(nome, preco, duracao)
        #print(f"Plano criado com sucesso: {novo}")
        return novo

    @classmethod
    def editar_plano(cls, id_plano, nome=None, preco=None, duracao=None):
        for plano in cls.planos:
            if plano.id_plano == id_plano:
                if nome:
                    plano.nome = nome
                if preco:
                    plano.preco = preco
                if duracao:
                    plano.duracao = duracao
                print(f"Plano atualizado: {plano}")
                return plano
        print(f"Plano com ID {id_plano} não encontrado.")
        return None

    @classmethod
    def remover_plano(cls, id_plano):
        for plano in cls.planos:
            if plano.id_plano == id_plano:
                cls.planos.remove(plano)
                print(f"Plano removido: {plano}")
                return plano
        print(f"Plano com ID {id_plano} não encontrado.")
        return None

    @classmethod
    def listar_planos(cls):
        if not cls.planos:
            print("Nenhum plano encontrado.")
        for plano in cls.planos:
            print(plano)

    def __repr__(self): #representa um plano em string 
        return f"Plano(ID: {self.id_plano}, Nome: {self.nome}, Preço: {self.preco}, Duração: {self.duracao} dias)"


if __name__ == "__main__":
    while True:
        print("\nMenu de Planos:")
        print("1 - Adicionar plano")
        print("2 - Editar plano")
        print("3 - Remover plano")
        print("4 - Listar planos")
        print("5 - Sair")
        
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Por favor, insira um número válido.")
            continue

        if opcao == 1: # Adicionar plano
            nome = input("Digite o nome do plano: ")
            try:
                preco = float(input("Digite o preço do plano: "))
                duracao = int(input("Digite a duração do plano (em dias): "))
            except ValueError:
                print("Por favor, insira valores válidos para preço e duração.")
                continue

            Plano.novo_plano(nome, preco, duracao)
            print("Plano adicionado com sucesso!")

        elif opcao == 2: # Editar plano
            try:
                id_plano = int(input("Digite o ID do plano que deseja editar: "))
            except ValueError:
                print("Por favor, insira um ID válido.")
                continue

            nome = input("Digite o novo nome (ou pressione Enter para não alterar): ")
            try:
                preco = input("Digite o novo preço (ou pressione Enter para não alterar): ")
                preco = float(preco) if preco else None
                duracao = input("Digite a nova duração (ou pressione Enter para não alterar): ")
                duracao = int(duracao) if duracao else None
            except ValueError:
                print("Por favor, insira valores válidos para preço e duração.")
                continue

            Plano.editar_plano(id_plano, nome or None, preco, duracao)

        elif opcao == 3: # Remover plano
            try:
                id_plano = int(input("Digite o ID do plano que deseja remover: "))
            except ValueError:
                print("Por favor, insira um ID válido.")
                continue

            Plano.remover_plano(id_plano)

        elif opcao == 4: # Listar planos
            print("\nPlanos disponíveis:")
            Plano.listar_planos()

        elif opcao == 5: # Sair
            print("Encerrando")
            break

        else:
            print("Opção inválida. Tente novamente.")
