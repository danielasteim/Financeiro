class ContaBancaria:
    # Lista para armazenar todas as contas bancárias
    contas = []
    id_counter = 1  # Contador para gerar IDs únicos

    def __init__(self, banco, agencia, numero_conta, titular):
        """Inicializa uma nova conta bancária."""
        self.id_conta = ContaBancaria.id_counter
        ContaBancaria.id_counter += 1
        self.banco = banco
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.titular = titular
        self.saldo = 0.0  # Saldo inicial
        ContaBancaria.contas.append(self)

    @classmethod
    def nova_conta(cls, banco, agencia, numero_conta, titular):
        """Cria e adiciona uma nova conta bancária."""
        nova = cls(banco, agencia, numero_conta, titular)
        print(f"Conta criada com sucesso: {nova}")
        return nova

    @classmethod
    def editar_conta(cls, id_conta, banco=None, agencia=None, numero_conta=None, titular=None):
        """Edita uma conta bancária existente."""
        for conta in cls.contas:
            if conta.id_conta == id_conta:
                if banco:
                    conta.banco = banco
                if agencia:
                    conta.agencia = agencia
                if numero_conta:
                    conta.numero_conta = numero_conta
                if titular:
                    conta.titular = titular
                print(f"Conta bancária atualizada: {conta}")
                return conta
        print(f"Conta bancária com ID {id_conta} não encontrada.")
        return None

    @classmethod
    def remover_conta(cls, id_conta):
        """Remove uma conta bancária existente."""
        for conta in cls.contas:
            if conta.id_conta == id_conta:
                cls.contas.remove(conta)
                print(f"Conta bancária removida: {conta}")
                return conta
        print(f"Conta bancária com ID {id_conta} não encontrada.")
        return None

    @classmethod
    def listar_contas(cls):
        """Lista todas as contas bancárias existentes."""
        if not cls.contas:
            print("Nenhuma conta bancária encontrada.")
        for conta in cls.contas:
            print(conta)

    def depositar(self, valor):
        """Realiza um depósito na conta bancária."""
        if valor > 0:
            self.saldo += valor
            print(f"Depósito de R${valor:.2f} realizado na conta {self.numero_conta}. Saldo atual: R${self.saldo:.2f}")
        else:
            print("Valor de depósito inválido.")

    def sacar(self, valor):
        """Realiza um saque da conta bancária."""
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            print(f"Saque de R${valor:.2f} realizado da conta {self.numero_conta}. Saldo atual: R${self.saldo:.2f}")
        elif valor > self.saldo:
            print(f"Saldo insuficiente para saque de R${valor:.2f}. Saldo atual: R${self.saldo:.2f}")
        else:
            print("Valor de saque inválido.")

    def __repr__(self):
        """Representação textual de uma conta bancária."""
        return f"Conta(ID: {self.id_conta}, Banco: {self.banco}, Agência: {self.agencia}, Número: {self.numero_conta}, Titular: {self.titular}, Saldo: R${self.saldo:.2f})"


# Exemplo de uso
if __name__ == "__main__":
    # Criar novas contas bancárias
    conta1 = ContaBancaria.nova_conta("Banco do Brasil", "1234", "987654", "João Silva")
    conta2 = ContaBancaria.nova_conta("Caixa Econômica", "5678", "123456", "Maria Oliveira")

    # Listar todas as contas
    print("\nListando contas bancárias:")
    ContaBancaria.listar_contas()

    # Editar uma conta bancária
    print("\nEditando conta bancária:")
    ContaBancaria.editar_conta(1, banco="Itaú", titular="João Souza")

    # Depositar em uma conta
    print("\nDepositando em conta:")
    conta1.depositar(500.00)

    # Sacar de uma conta
    print("\nRealizando saque:")
    conta1.sacar(200.00)

    # Listar novamente
    print("\nListando contas após alterações:")
    ContaBancaria.listar_contas()

    # Remover uma conta bancária
    print("\nRemovendo conta bancária:")
    ContaBancaria.remover_conta(2)

    # Listar novamente
    print("\nListando contas após remoção:")
    ContaBancaria.listar_contas()
