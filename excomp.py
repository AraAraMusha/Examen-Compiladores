import ply.lex as lex
import tkinter as tk
from tkinter import scrolledtext

class Lexer:
    tokens = [
        'DELIMITADOR',
        'OPERADOR',
        'PALABRA_RESERVADA',
        'ENTERO',
        'IDENTIFICADOR',
        'PUNTO',  # Token para el punto "."
    ]

    t_ignore = ' \t'
    contador_lineas = 1
    token_count = {}  # Diccionario para contar los tokens

    reserved = {
        'for': 'FOR',
        'do': 'DO',
        'public': 'PUBLIC',
        'static': 'STATIC',
        'const': 'CONST',
        'main': 'MAIN',
        'class': 'CLASS',
        'int': 'INT',  # Agregado int como palabra reservada
        'programa': 'PROGRAMA',  # Agregado 'programa' como palabra reservada
        'read':'READ',
        'end': 'END',
        'printf': 'PRINTF',
    }

    tokens += reserved.values()

    @staticmethod
    def t_DELIMITADOR(t):
        r'[{}();]'
        return t

    @staticmethod
    def t_OPERADOR(t):
        r'[-+*/=<>]'
        return t

    @staticmethod
    def t_ENTERO(t):
        r'-?\b\d+\b'
        return t

    @staticmethod
    def t_IDENTIFICADOR(t):
        r'\b[a-zA-Z0-9]+\b'  #  cualquier combinación de letras
        if t.value == 'suma':
            t.type = 'IDENTIFICADOR'  # Marcar 'suma' como un identificador
        else:
            t.type = 'PALABRA_RESERVADA' if t.value in Lexer.reserved else 'IDENTIFICADOR'
        # Contador de tokens
        Lexer.token_count.setdefault(t.type, 0)
        Lexer.token_count[t.type] += 1
        return t

    @staticmethod
    def t_PUNTO(t):
        r'\.'
        return t

    @staticmethod
    def t_PALABRA_RESERVADA(t):
        r'for|do|public|static|const|main|class|programa|read|printf|end'  # Agregado 'programa' como palabra reservada
        t.type = Lexer.reserved.get(t.value, 'PALABRA_RESERVADA')
        return t

    @staticmethod
    def t_newline(t):
        r'\n+'
        Lexer.contador_lineas += t.value.count('\n')
        t.lexer.lineno += t.value.count('\n')

    @staticmethod
    def t_eof(t):
        t.lexer.lineno += t.value.count('\n')
        return None

    @staticmethod
    def t_error(t):
        print(f"Error léxico: Carácter inesperado '{t.value[0]}' en la línea {Lexer.contador_lineas}")
        t.lexer.skip(1)

    @staticmethod
    def build():
        return lex.lex(module=Lexer())


lexer = Lexer.build()

def analizar_lexico(entrada):
    lexer.lineno = 1  # Reiniciar el contador de líneas
    lexer.input(entrada)
    tokens = []
    errores = []
    token_count = {}  # Diccionario para contar los tokens

    for tok in lexer:
        if tok.type != 'UNKNOWN':
            tokens.append((tok.type, tok.value, tok.lineno))
            # Contador de tokens
            token_count.setdefault(tok.type, 0)
            token_count[tok.type] += 1
        elif tok.type == 'UNKNOWN':
            errores.append((f"Error léxico: Token no reconocido '{tok.value}'", tok.lineno))

    mostrar_resultados(tokens, errores)
    mostrar_conteo(token_count)

    return tokens, errores

def analizar_button_click():
    entrada_text = entrada.get("1.0", tk.END)
    tokens, errores = analizar_lexico(entrada_text)

def mostrar_resultados(tokens, errores):
    resultado_text = ""
    for token in tokens:
        resultado_text += f"{token[0]}: {token[1]} (Línea {token[2]})\n"

    resultado_textbox.config(state=tk.NORMAL)
    resultado_textbox.delete('1.0', tk.END)
    resultado_textbox.insert(tk.END, resultado_text)
    resultado_textbox.config(state=tk.DISABLED)

def mostrar_conteo(token_count):
    conteo_text = "Conteo de tokens:\n"
    for token_type, count in token_count.items():
        conteo_text += f"{token_type}: {count}\n"

    conteo_textbox.config(state=tk.NORMAL)
    conteo_textbox.delete('1.0', tk.END)
    conteo_textbox.insert(tk.END, conteo_text)
    conteo_textbox.config(state=tk.DISABLED)

ventana = tk.Tk()
ventana.title("Analizador Léxico")

etiqueta = tk.Label(ventana, text="Ingrese la expresión:")
entrada = scrolledtext.ScrolledText(ventana, height=10, width=100) 
analizar_button = tk.Button(ventana, text="Analizar", command=analizar_button_click)

resultado_textbox = scrolledtext.ScrolledText(ventana, height=10, width=20)
resultado_textbox.config(state=tk.DISABLED)

conteo_textbox = scrolledtext.ScrolledText(ventana, height=10, width=20)
conteo_textbox.config(state=tk.DISABLED)

etiqueta.pack(pady=10)
entrada.pack(pady=10)
analizar_button.pack(pady=10)
resultado_textbox.pack(side='right', padx=10, pady=10, fill='both', expand=True)
conteo_textbox.pack(side='right', padx=10, pady=10, fill='both', expand=True)

ventana.mainloop()
