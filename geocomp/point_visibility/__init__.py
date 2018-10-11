
'''Algoritmos para o problema da visibilidade de um ponto:

Dado várias arestas e um ponto, descobrir quais arestas são visíveis
pelo ponto.

Algoritmos disponiveis:
- Usando ABBB

'''

from . import point_visibility

# cada entrada deve ter:
#  [ 'nome-do-modulo', 'nome-da-funcao', 'nome do algoritmo' ]
children = (
    ('point_visibility', 'point_visibility_with_points', 'Visibilidade de ponto\n(com ABBB)'),
)

__all__ = [a[0] for a in children]
