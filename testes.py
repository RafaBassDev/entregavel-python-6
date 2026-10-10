"""Testes simples da Sprint 6, usando assert e try/except."""

from sistema_loja import Produto, ProdutoFisico, ProdutoDigital, Carrinho


# 1. Criacao e calculo de preco dos produtos.
mouse = ProdutoFisico("Mouse", 50, 10)
curso = ProdutoDigital("Curso Python", 200, 10)
assert mouse.calcular_preco_final() == 60
assert curso.calcular_preco_final() == 180

# 2. Heranca, polimorfismo e representacao.
assert isinstance(mouse, Produto)
assert isinstance(curso, Produto)
assert "Mouse" in str(mouse)
assert "ProdutoDigital" in repr(curso)
assert sorted([mouse, curso])[0] is mouse

# 3. Carrinho com composicao.
carrinho = Carrinho("Ana")
carrinho.adicionar_produto(mouse)
carrinho.adicionar_produto(curso)
assert carrinho.calcular_total() == 240
assert len(carrinho.produtos) == 2

# 4. Setters bloqueiam alteracoes invalidas.
try:
    mouse.preco = -100
    raise AssertionError("Deveria recusar preco negativo.")
except ValueError:
    assert mouse.preco == 50

try:
    curso.desconto = 101
    raise AssertionError("Deveria recusar desconto acima de 100.")
except ValueError:
    assert curso.desconto == 10

try:
    carrinho.adicionar_produto("Texto")
    raise AssertionError("Deveria recusar objetos que nao sao produtos.")
except TypeError:
    assert len(carrinho.produtos) == 2

try:
    Produto("Generico", 10)
    raise AssertionError("Deveria impedir instanciar a classe abstrata.")
except TypeError:
    pass

print("Todos os testes da Sprint 6 passaram!")
