# INÍCIO DA CRIAÇÃO DAS CONSTANTES

    #Vão ser o range dos números da calculadora
CONSTANTES = '0123456789'
#FIM DA CRIAÇÃO DAS CONSTANTES
# --------------------------------#
# INÍCIO DA CRIAÇÃO DOS TOKENS
OP_INT = 'OP_INT'
OP_FLOAT = 'OP_FLOAT'
OP_MAIS = 'OP_ADD'
OP_MENOS = 'OP_SUB'
OP_MUL = 'OP_MUL'
OP_DIV = 'OP_DIV'
OP_PAREN_ESQ = 'PAREN_ESQ'
OP_PAREN_DIR = 'PAREN_DIR'
# FIM DA CRIAÇÃO DOS TOKENS
# INÍCIO TRATAMENTO DE ERROS


# Área da parte semântica
class Error:
    def __init__(self,inicio, fim, tipo_erro, descricao):
        #inicializando as varáveis pro tratamento
        self.inicio = inicio
        self.fim = fim
        self.tipo_erro = tipo_erro
        self.descricao = descricao
    def resultado_erro(self):
        #se ocorrer um erro, irá informa o tipo do erro e uma breve descrição
        resultado = f'{self.tipo_erro}: {self.descricao}'
        #informar a linnha e qual arquivo deu erro  
        resultado += f' <-- Erro {self.inicio.arq_nome}, linha: {self.inicio.linha + 1}'
        return resultado

class CaracterInvalido(Error):
    def __init__(self, inicio, fim,descricao):
        super().__init__(inicio, fim,'Caracter Inválido', descricao)
#FIM TRATAMENTO DE ERROS

class Posicao:
    def __init__(self, index, linha, coluna, arq_nome, arq_texto):
        self.index = index
        self.linha = linha
        self.coluna = coluna
        self.arq_nome = arq_nome
        self.arq_texto = arq_texto
    def analisa_prox_caractere(self, char_atual):
        self.index += 1
        self.coluna += 1
        
        if char_atual == '\n':
            self.linha += 1
            self.coluna = 0
        
        return self
    
    # Cópia das posições pra informar o dos erros(não consegui consertar)
    def copia_pos(self):
        return Posicao(self.index, self.linha, self.coluna, self.arq_nome, self.arq_texto)

#A classes que vai informa as informações do dados colocado no terminal
class Token:
    def __init__(self, tipo_, valor=None):
        self.tipo = tipo_
        self.valor = valor
    def __repr__(self):
        if self.valor: return f'{self.tipo}: {self.valor}'
        return f'{self.tipo}'

# Classe do Analisador léxico
class analisadorLexico:
    def __init__(self, arq_nome, arq_texto):
        self.arq_nome = arq_nome
        self.arq_texto = arq_texto
        self.pos = Posicao(-1, 0, -1, arq_nome, arq_texto)
        self.char_atual = None
        self.analisa_prox_caractere()
    
    def analisa_prox_caractere(self):
        self.pos.analisa_prox_caractere(self.char_atual)
        self.char_atual = self.arq_texto[self.pos.index] if self.pos.index < len(self.arq_texto) else None

    #Criação da função para identificar o dados posto no terminal
    #Junto de condições para identificar os operadores e parênteses
    def criar_tokens(self):
        tokens = []

        while self.char_atual != None:
            if self.char_atual in ' \t':
                self.analisa_prox_caractere()
            elif self.char_atual in CONSTANTES:
                tokens.append(self.criar_numero())
            elif self.char_atual == '+':
                tokens.append(Token(OP_MAIS))
                self.analisa_prox_caractere()
            elif self.char_atual == '-':
                tokens.append(Token(OP_MENOS))
                self.analisa_prox_caractere()
            elif self.char_atual == '*':
                tokens.append(Token(OP_MUL))
                self.analisa_prox_caractere()
            elif self.char_atual == '/':
                tokens.append(Token(OP_DIV))
                self.analisa_prox_caractere()
            elif self.char_atual == '(':
                tokens.append(Token(OP_PAREN_ESQ))
                self.analisa_prox_caractere()
            elif self.char_atual == ')':
                tokens.append(Token(OP_PAREN_DIR))
                self.analisa_prox_caractere()
            else:
                inicio = self.pos.copia_pos()
                char = self.char_atual
                self.analisa_prox_caractere()
                return [], CaracterInvalido(inicio, self.pos, "'" + char + "'")
    
        return tokens, None

    #Aqui realzia o tratamento dos números, diferenciando de FLOAT e INT
    def criar_numero(self):
        num_str = ''
        ponto_count = 0

        while self.char_atual != None and self.char_atual in CONSTANTES + '.':
            if self.char_atual =='.':
                if ponto_count == 1: break
                ponto_count += 1
                num_str += '.'
            else: 
                num_str += self.char_atual
            self.analisa_prox_caractere()
        if ponto_count == 0:
            return Token(OP_INT, int(num_str))
        else:
            return Token(OP_FLOAT, float(num_str))

def principal(arq_nome,arq_texto):
    lexico = analisadorLexico(arq_nome,arq_texto)
    tokens, erros = lexico.criar_tokens()

    return tokens, erros