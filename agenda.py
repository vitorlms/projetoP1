import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(i, texto, cor) :
  if cor == 'A':
    print(RED, str(i), texto + BOLD)
    return RESET
  elif cor == 'B':
    cor = YELLOW
  elif cor == 'C':
    cor = BLUE
  elif cor == 'D':
    cor = GREEN
  print(cor, str(i), texto)
  
  return RESET

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '':
    return False

  ################ COMPLETAR
  novaAtividade = ''
  if extras[0] != '':
    novaAtividade += extras[0] + ' '
  if extras[1] != '':
    novaAtividade += extras[1] + ' '
  if extras[2] != '':
    novaAtividade += extras[2] + ' '
    
  novaAtividade += descricao
  
  if extras[3] != '':
    novaAtividade += extras[3] + ' '
  if extras[4] != '':
    novaAtividade += extras[4]

  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):

  ################ COMPLETAR
  if len(pri) == 3:
    if pri[0] == '(' and pri[2] == ')':
      if pri[1] >= 'A' and pri[1] <= 'Z':
        return True
  
  return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    ################ COMPLETAR
    hora = horaMin[:2]
    minuto = horaMin[2:]

    if hora < '00' or hora > '23':
      print('Formato de hora inválido')
      return False
    elif minuto < '00' or minuto > '59':
      print('Formato de minuto inválido')
      return False
    return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data):
  if len(data) != 8 or not soDigitos(data):
    return False
  ################ COMPLETAR
  dia = data[:2]
  mes = data[2:4]
  ano = data[4:]

  if mes == '01' or mes == '03' or mes == '05' or mes == '07' or mes == '08' or mes == '10' or mes == '12':
    if dia < '01' or dia > '31':
      print('Formato de data inválida')
    else:
      return True
  elif mes == '02':
    if dia < '01' or dia > '29':
      print('Formato de data inválida')
    else:
      return True
  elif mes == '04' or mes == '06' or mes == '09' or mes == '11':
    if dia < '01' or dia > '30':
      print('Formato de data inválida')
    else:
      return True
  else:
    print('Mês inválido')
  return False

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):

  ################ COMPLETAR
  if len(proj) >= 2:
    if proj[0] == '+':
      return True

  return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):

  ################ COMPLETAR
  if len(cont) >= 2:
    if cont[0] == '@':
      return True

  return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []
  
  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras
    
    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    ################ COMPLETAR
    for info in tokens:
      if dataValida(info):
        data = info
      elif horaValida(info):
        hora = info
      elif prioridadeValida(info):
        pri = info
      elif contextoValido(info):
        contexto = info
      elif projetoValido(info):
        projeto = info
      else:
        desc += info + ' '
        
    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():

  ################ COMPLETAR
  fp = open(TODO_FILE, 'r')
  itens = organizar(fp)
  fp.close()
  
  ordenarPorPrioridade(itens)
  ordenarPorDataHora(itens)

  f = open(TODO_FILE, 'r')
  todoList = organizar(f)
  f.close()
  
  for item in itens:
    i = 0
    while i < len(todoList):
      if item == todoList[i]:
        printarItem(i, item)
      i += 1
    
  return
  
def printar(itens):
  for item in itens:
    print(item)  

def printarItem(i, item):
  if item[1][0] != '':
    data = item[1][0][:2] + '/' + item[1][0][2:4] + '/' + item[1][0][4:]
  else:
    data = ''
  if item[1][1] != '':
    hora = item[1][1][:2] + 'h' + item[1][1][2:] + 'min'
  else:
    hora = ''
  if item[1][2] != '':
    pri = item[1][2]
    cor = pri[1]
  else:
    pri = ''
    cor = RESET
  if item[1][3] != '':
    contexto = item[1][3]
  else:
    contexto = ''
  if item[1][4] != '':
    projeto = item[1][4]
  else:
    projeto = ''
    
  texto = data + ' ' + hora + ' ' + pri + ' ' + item[0] + ' ' + contexto + ' ' + projeto
  
  return printCores(i, texto, cor)

def ordenarPorDataHora(itens):
  ################ COMPLETAR
  i = 0
  while i < len(itens) - 1:
    if itens[i][1][2] == itens[i+1][1][2]: #mesma prioridade
      if itens[i][1][0] == '' and itens[i][1][1] == '':
        trocarPosicao(i, itens)
      elif (itens [i][1][0] == itens[i+1][1][0]) and (itens[i][1][1] != itens[i+1][1][1]): #mesma data, com horas diferentes
        if itens[i][1][1] > itens[i+1][1][1] and itens[i+1][1][1] != '':
          trocarPosicao(i, itens)
          i = 0
      else:
        if inverterData(itens[i]) > inverterData(itens[i+1]) and itens[i+1][1][0] != '':
          trocarPosicao(i, itens)
          i = 0
    i += 1
  return itens

def trocarPosicao(i, itens):
  aux = itens[i]
  itens[i] = itens[i+1]
  itens[i+1] = aux
  return

def inverterData(item):
  return item[1][0][4:] + item[1][0][2:4] + item[1][0][:2]

def ordenarPorPrioridade(itens):

  ################ COMPLETAR
  i, ordem = 0, 90
  while i < len(itens):
    if itens[i][1][2] == '':
      itens.insert(0, itens.pop(i))
    i += 1

  while ordem >= 65:
    i = 0
    while i < len(itens):
      if itens[i][1][2] != '':
        if itens[i][1][2][1] == chr(ordem):
          itens.insert(0, itens.pop(i))
      i += 1
    ordem -= 1
  
  return itens

def fazer(num):

  ################ COMPLETAR
  done = remover(num)
  
  fp = open(ARCHIVE_FILE, 'a')
  fp.write(done)
  fp.close()
  
  return 

def remover(num):

  ################ COMPLETAR
  fp = open(TODO_FILE, 'r')
  todo = fp.readlines()
  fp.close()

  item = todo[int(num)]
  
  fp = open(TODO_FILE, 'w')
  for l in todo:
    if l != item:
      fp.write(l)
  fp.close()
  
  return item

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, pri):

  ################ COMPLETAR
  fp = open(TODO_FILE, 'r')
  todo = fp.readlines()
  fp.close()
  
  pri = '(' + pri + ')'
  
  item = todo[int(num)]
  tokens = item.split()
  
  fp = open(TODO_FILE, 'w')
  for l in todo:
    if l == item:      
      if dataValida(tokens[0]):
        if horaValida(tokens[1]):
          if prioridadeValida(tokens[2]):
            tokens[2] = pri
          else:
            tokens.insert(2, pri)
        else:
          if prioridadeValida(tokens[1]):
            tokens[1] = pri
          else:
            tokens.insert(1, pri)
      elif horaValida(tokens[0]):
        if prioridadeValida(tokens[1]):
          tokens[1] = pri
        else:
          tokens.insert(1, pri)
      elif prioridadeValida(tokens[0]):
        tokens[0] = pri
      else:
        tokens.insert(0, pri)
        
      i, itemPrioritario = 0, ''
      while i < len(tokens):
        itemPrioritario += tokens[i] + ' '
        i += 1
        
      fp.write(itemPrioritario + '\n')
        
    else:
      fp.write(l)
      
  fp.close()
  
  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if len(comandos) == 1:
    print('Não há entrada de comandos.')
    
  elif comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
    
  elif comandos[1] == LISTAR:
    return listar()
    ################ COMPLETAR

  elif comandos[1] == REMOVER:
    if len(comandos) != 3:
      return 'Erro, parâmetros incorretos'
    elif not soDigitos(comandos[2]):
      return 'Erro, parâmetros incorretos'
    return remover(comandos[2])

    ################ COMPLETAR    

  elif comandos[1] == FAZER:
    if len(comandos) != 3:
      return 'Erro, parâmetros incorretos'
    elif not soDigitos(comandos[2]):
      return 'Erro, parâmetros incorretos'
    return fazer(comandos[2])

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    if len(comandos) != 4:
      return 'Erro, parâmetros incorretos'
    elif not soDigitos(comandos[2]) or comandos[3] < 'A' or comandos[3] > 'Z':
      return 'Erro, parâmetros incorretos'
    return priorizar(comandos[2], comandos[3])

    ################ COMPLETAR

  else :
    print("Comando inválido.")
      
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)


