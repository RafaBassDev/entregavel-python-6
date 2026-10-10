"""Sprint 6 - Sistema de loja com programacao orientada a objetos."""

from abc import ABC, abstractmethod
import math


# 1. Classe abstrata: representa qualquer produto da loja.
class Produto(ABC):
    """Classe mae com os dados e as regras comuns dos produtos."""

    def __init__(self, nome, preco):
        """Cria um produto e valida nome e preco."""
        self.nome = nome
        self.preco = preco

    @property
    def nome(self):
        """Consulta o nome do produto."""
        return self._nome

    @nome.setter
    def nome(self, valor):
        """Impede que o produto tenha um nome vazio."""
        if not isinstance(valor, str) or valor.strip() == "":
            raise ValueError("O nome do produto nao pode ser vazio.")
        self._nome = valor.strip()

    @property
    def preco(self):
        """Consulta o preco do produto."""
        return self._preco

    @preco.setter
    def preco(self, valor):
        """Aceita apenas precos numericos, finitos e nao negativos."""
        if type(valor) not in (int, float) or not math.isfinite(valor) or valor < 0:
            raise ValueError("O preco deve ser um numero maior ou igual a zero.")
        self._preco = valor

    @abstractmethod
    def calcular_preco_final(self):
        """Cada tipo de produto deve calcular o proprio preco final."""
        pass

    def __str__(self):
        """Mostra uma descricao simples para o usuario."""
        return f"{self.nome} | Preco final: R$ {self.calcular_preco_final():.2f}"

    def __repr__(self):
        """Mostra uma representacao util durante o desenvolvimento."""
        return f"Produto(nome={self.nome!r}, preco={self.preco!r})"

    def __lt__(self, outro):
        """Permite ordenar produtos por preco final com sorted()."""
        if not isinstance(outro, Produto):
            return NotImplemented
        return self.calcular_preco_final() < outro.calcular_preco_final()


# 2. Classe filha: adiciona o frete ao preco.
class ProdutoFisico(Produto):
    """Produto entregue fisicamente, com custo de frete."""

    def __init__(self, nome, preco, frete):
        """Reaproveita os dados da classe mae e define o frete."""
        super().__init__(nome, preco)
        self.frete = frete

    @property
    def frete(self):
        """Consulta o valor do frete."""
        return self._frete

    @frete.setter
    def frete(self, valor):
        """Impede fretes invalidos."""
        if type(valor) not in (int, float) or not math.isfinite(valor) or valor < 0:
            raise ValueError("O frete deve ser um numero maior ou igual a zero.")
        self._frete = valor

    def calcular_preco_final(self):
        """Soma o frete ao preco do produto."""
        return self.preco + self.frete

    def __str__(self):
        """Apresenta o produto fisico e seu frete."""
        return f"{super().__str__()} | Frete: R$ {self.frete:.2f}"

    def __repr__(self):
        """Representacao tecnica de um produto fisico."""
        return f"ProdutoFisico({self.nome!r}, {self.preco!r}, {self.frete!r})"


# 3. Outra classe filha: aplica um desconto ao preco.
class ProdutoDigital(Produto):
    """Produto entregue digitalmente, com desconto percentual."""

    def __init__(self, nome, preco, desconto):
        """Reaproveita os dados da classe mae e define o desconto."""
        super().__init__(nome, preco)
        self.desconto = desconto

    @property
    def desconto(self):
        """Consulta a porcentagem de desconto."""
        return self._desconto

    @desconto.setter
    def desconto(self, valor):
        """Aceita descontos entre 0 e 100 por cento."""
        if (type(valor) not in (int, float)
                or not math.isfinite(valor)
                or valor < 0 or valor > 100):
            raise ValueError("O desconto deve estar entre 0 e 100.")
        self._desconto = valor

    def calcular_preco_final(self):
        """Desconta uma porcentagem do preco original."""
        return self.preco * (1 - self.desconto / 100)

    def __str__(self):
        """Apresenta o produto digital e seu desconto."""
        return f"{super().__str__()} | Desconto: {self.desconto}%"

    def __repr__(self):
        """Representacao tecnica de um produto digital."""
        return f"ProdutoDigital({self.nome!r}, {self.preco!r}, {self.desconto!r})"


# 4. Composicao: o carrinho contem objetos Produto.
class Carrinho:
    """Guarda os produtos escolhidos por um cliente."""

    def __init__(self, cliente):
        """Cria um carrinho vazio associado ao nome do cliente."""
        self.cliente = cliente
        self._produtos = []

    @property
    def cliente(self):
        """Consulta o nome do cliente."""
        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        """Nao permite nomes de cliente vazios."""
        if not isinstance(valor, str) or valor.strip() == "":
            raise ValueError("O nome do cliente nao pode ser vazio.")
        self._cliente = valor.strip()

    @property
    def produtos(self):
        """Devolve uma copia imutavel da lista de produtos."""
        return tuple(self._produtos)

    def adicionar_produto(self, produto):
        """Aceita apenas objetos da classe Produto ou de suas filhas."""
        if not isinstance(produto, Produto):
            raise TypeError("O carrinho aceita apenas produtos.")
        self._produtos.append(produto)

    def calcular_total(self):
        """Soma os precos finais dos produtos cadastrados."""
        total = 0
        for produto in self._produtos:
            total += produto.calcular_preco_final()
        return total

    def __str__(self):
        """Apresenta a quantidade de itens e o total do carrinho."""
        return (f"Carrinho de {self.cliente} | "
                f"{len(self._produtos)} produtos | "
                f"Total: R$ {self.calcular_total():.2f}")

    def __repr__(self):
        """Representacao tecnica do carrinho."""
        return f"Carrinho(cliente={self.cliente!r}, itens={len(self._produtos)})"


def demonstrar_sistema():
    """Cria objetos, demonstra polimorfismo e testa erros comuns."""
    # 5. Dez objetos Produto (5 fisicos e 5 digitais).
    produtos = [
        ProdutoFisico("Notebook", 2500, 50),
        ProdutoFisico("Mouse", 45.90, 15),
        ProdutoFisico("Teclado", 120, 20),
        ProdutoFisico("Monitor", 900, 40),
        ProdutoFisico("Fone de ouvido", 150, 12),
        ProdutoDigital("Curso Python", 200, 10),
        ProdutoDigital("E-book de Logica", 50, 20),
        ProdutoDigital("Curso Git", 150, 15),
        ProdutoDigital("Template de Portfolio", 80, 25),
        ProdutoDigital("Apostila HTML", 30, 5),
    ]

    carrinho = Carrinho("Ana")  # 11º objeto: composicao.

    print("========== SISTEMA DE LOJA - SPRINT 6 ==========")
    print(f"Produtos criados: {len(produtos)}")
    print("\nProdutos e precos finais (polimorfismo):")
    for produto in produtos:
        # O mesmo metodo tem resultados diferentes em cada classe filha.
        print(produto)
        carrinho.adicionar_produto(produto)

    print("\nProdutos ordenados por preco final (__lt__):")
    for produto in sorted(produtos):
        print(f"{produto.nome}: R$ {produto.calcular_preco_final():.2f}")

    print("\nResumo do carrinho (composicao):")
    print(carrinho)
    print(f"Exemplo de __repr__: {repr(produtos[0])}")

    # 6. Tratamento de excecoes: dados que nao devem ser aceitos.
    print("\nTestes de validacao com try/except:")
    try:
        ProdutoFisico("Produto incorreto", -10, 5)
    except ValueError as erro:
        print(f"Preco invalido: {erro}")

    try:
        ProdutoDigital("Curso incorreto", 100, 120)
    except ValueError as erro:
        print(f"Desconto invalido: {erro}")

    try:
        produtos[0].preco = -50
    except ValueError as erro:
        print(f"Alteracao bloqueada: {erro}")

    try:
        carrinho.adicionar_produto("Nao sou um produto")
    except TypeError as erro:
        print(f"Item invalido: {erro}")

    try:
        Produto("Generico", 10)
    except TypeError:
        print("Classe abstrata: nao pode criar um Produto diretamente.")

    print(f"\nPreco preservado do Notebook: R$ {produtos[0].preco:.2f}")
    print("===============================================")


if __name__ == "__main__":
    demonstrar_sistema()
