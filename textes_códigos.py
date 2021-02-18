# import locale

# # locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


# valor_em_dolar_formatado = locale.currency(5454512.4593681, grouping=True)
# print(valor_em_dolar_formatado)

# class Calculadora:
#     def somar(self, x, y):
#         return x+y
    
#     def dividir(self, x, y):
#         return x / y 


# if __name__ == "__main__":
#     calc = Calculadora()

#     print(calc.somar(50, 60))


# from collections import Counter, defaultdict, OrderedDict, namedtuple


# lista = [2, 4, 4, 5, 5, 6, 4, 3, 2, 2, 2, 5, 3, 3, 5, 4, 3, 2, 2, 2, 4]

# dicio = dict(Counter(lista))
# dicio_2 = {2:3, 3:5, 5:7}
# print(dicio_2)
# print(type(dicio))

# dicio = defaultdict(lambda: 'Padrão')

# dicio['Curso'] = 'Python 3'
# dicio['Formato'] = 'On-line'
# print(dicio)

# print(dicio['Escola'])
# print(dicio['Curso'])

# dicio1 = {'a': 1, 'b': 2}
# dicio2 = {'b': 2, 'a': 1}

# print(dicio1 == dicio2)  # True

# odict1 = OrderedDict({'a': 1, 'b': 2})
# odict2 = OrderedDict({'b': 2, 'a': 1})

# print(odict1 == odict2)  # False

# # cachorro = namedtuple('cachorro', 'idade raca nome')
# # cachorro = namedtuple('cachorro', 'idade, raca, nome')
# cachorro = namedtuple('cachorro', ['idade', 'raca', 'nome'])

# ray = cachorro(idade=10, raca='husk', nome='ray')

# print(ray.idade)
# print(ray.raca)
# print(ray.nome)
# print()
# print(ray[0])
# print(ray[1])
# print(ray[2])
# print('INDEX', ray.index('husk'))


# idade = 33
# calcado = '33'
# print('TESTE IGUALDADE')
# print(idade == calcado)  # False

# from send2trash import send2trash

# send2trash('teste_send.txt')

# def delay():
#     # iterador = iter(lista)
#     # yield next(iterador)
#     lista = ['0.9s1', '0.6s2', '0.3s3', '0.9s4', '0.6s5', '0.3s6']
#     for i in lista[::-1]:
#         yield i

import datetime
year = datetime.timezone.Y
   
    


if __name__ == "__main__":
    # print(next(delay()))
    # print(next(delay()))
    # print(next(delay()))
    # print(next(delay()))
    # print(next(delay()))
    # print(next(delay()))
    # a = delay()
    # print(next(a))
    # print('oi')
    # print(next(a))
    # print('oi')
    # print(next(a))
    # print('oi')
    # print(next(a))
    print(year)
    
    