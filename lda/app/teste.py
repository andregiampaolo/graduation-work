import random

matriz_topicos_palavra = [
    ['farmaceutico','medicamento','producao','farmaceutica','lavagem'],
    ['informatica','sistema','equipamento','elaboracao','testar'],
    ['condominio','copeiro','porteiro','copar','pastar','suco'],
    ['pessoal','admissao','departamento','folhar','ferir'],
    ['coordenador','pedagogicas','acompanhamento','corpo','educacao'],
    ['administrativo','auxiliar','atendimento','cliente','controlo'],
    ['projetista','desenvolvimento','dar','mover','desenvolver'],
    ['contramestre','sanitarias','etc','eletricas','hidraulicas'],
    ['despacho','fiscalizar','pessoa','dner','movimentacao'],
    ['institucional','relacoes','estrar','rodoviaria','pronasci'],
    ['paciente','exame','saude','prescricao','medicar'],
    ['obrar','construcao','seguranca','engenheiro','trabalhar'],
    ['educacao','professorar','aula','ensinar','professor'],
    ['manutencao','juridico','tecnico','advogar','preventivo'],
    ['saude','tecnico','enfermagem','paciente','enfermeiro'],
    ['obrar','execucao','sanitario','pavimentacao','sistema'],
    ['producao','comunicacao','educacao','marketing','publicar'],
    ['limpeza','gerar','servicos','limpar','conservacao'],
    ['grafica','exercicios','prescricao','saude','orientacao'],
    ['tubulacoes','instalacoes','hidraulico','bombeiro','fazer'],
]

tamanho_lista = len(matriz_topicos_palavra) - 1

index = 0
for lista_palavras in matriz_topicos_palavra:
    numero_lista = random.randint(0,tamanho_lista)
    if numero_lista == index:
        numero_lista = random.randint(0,index-1)

    numero_palavra_intrusa = random.randint(0,4)

    # palavra adicionada

    # adicionando a palavra 
    lista_palavras.append(matriz_topicos_palavra[numero_lista][numero_palavra_intrusa])
    # mistrando as palavras da lista
    random.shuffle(lista_palavras)

    print(lista_palavras)
    print('Palavra adicionada: ', matriz_topicos_palavra[numero_lista][numero_palavra_intrusa])
    print()

    index = index + 1
    



