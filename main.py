import analisadores

while True: 
    texto = input("Escolha os números > ")
    resultado, erros = analisadores.principal('<Apenas números são aceitos>', texto)

    if erros:print(erros.resultado_erro())
    else:print(resultado)