class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_actual = None
        self.indice_token = 0
        self.codigo_python = "" 
        self.mesaje = ""

    def analizar(self):
        self.mensaje = ""
        self.codigo_python = ""
        try:
            self.token_actual = self.tokens[self.indice_token]
            if self.token_actual[0] == 'TIPO_DE_DATO':
                self.declaracion_variable()
            elif self.token_actual[0] == 'PALABRA_RESERVADA':
                if self.token_actual[1] == 'UwU-if':
                    self.sentencia_if()
                elif self.token_actual[1] == 'UwU-def':
                    self.declaracion_funcion()
                elif self.token_actual[1] == 'UwU-for':
                    self.declaracion_for()
               
            resto_codigo = " ".join(token[1] for token in self.tokens[self.indice_token:])
            self.codigo_python += resto_codigo + "\n"
            self.mensaje = "La cadena de entrada es válida."
        except SyntaxError as e:
            self.mensaje = f"Error de sintaxis: {e}"
        
        print(self.mensaje)
        return self.codigo_python, self.mensaje
    

    def coincidir(self, tipo_token):
        if self.token_actual and self.token_actual[0] == tipo_token:
            self.consumir_token()
        else:
            raise SyntaxError(f"Token inesperado: {self.token_actual}")

    def consumir_token(self):
        self.indice_token += 1
        if self.indice_token < len(self.tokens):
            self.token_actual = self.tokens[self.indice_token]
        else:
            self.token_actual = None

    def declaracion_variable(self):
        tipo_dato = self.token_actual[1]
        identificador = self.tokens[self.indice_token + 1][1]  # Capturamos el identificador
        valor = self.tokens[self.indice_token + 3][1]  # Capturamos el valor de la asignación

        self.coincidir('TIPO_DE_DATO')
        self.coincidir('IDENTIFICADOR')
        self.coincidir('ASIGNACION')

        # Traducción de la declaración de variable
        if tipo_dato == 'UwU-int':
            self.coincidir('ENTERO')
            self.codigo_python += f"{identificador} = {valor}\n"  # int en Python es implícito
        elif tipo_dato == 'UwU-float':
            self.coincidir('FLOTANTE')
            self.codigo_python += f"{identificador} = float({valor})\n"
        elif tipo_dato == 'UwU-var':
            self.coincidir('CADENA')
            self.codigo_python += f"{identificador} = {valor}\n"  # var en Python no es necesario
        else:
            raise SyntaxError("Tipo de dato no válido")

        
    def declaracion_funcion(self):
        # Asume que la palabra reservada ya ha sido validada como 'UwU-def'
        nombre_funcion = self.tokens[self.indice_token + 1][1]  # Capturamos el nombre de la función
        # Capturamos el contenido de la función
        contenido = self.tokens[self.indice_token + 5][1]  # Capturamos el contenido de la función

        # Validamos y consumimos los tokens necesarios para la sintaxis de la función
        self.coincidir('PALABRA_RESERVADA')  # 'UwU-def'
        self.coincidir('IDENTIFICADOR')      # nombre de la función
        self.coincidir('PARENTESIS_IZQ')     # '('
        self.coincidir('PARENTESIS_DER')     # ')'
        self.coincidir('DOS_PUNTOS')         # ':'
        self.coincidir('CONTENIDO')          # contenido (print)

        # Traducción de la declaración de función a Python
        self.codigo_python += f"def {nombre_funcion}(): {contenido}\n"
        print(f'contenido en parser: {self.codigo_python}')


    def sentencia_if(self):
        # Capturar la condición del if.
        numero1 = self.tokens[self.indice_token + 1][1]
        operador = self.tokens[self.indice_token + 2][1]
        numero2 = self.tokens[self.indice_token + 3][1]
        contenido_if = self.tokens[self.indice_token + 5][1]
        
        self.coincidir('PALABRA_RESERVADA')  # 'UwU-if'
        self.coincidir('ENTERO')              # Primer número de la condición
        self.coincidir('SIMBOLOS')            # Operador de comparación
        self.coincidir('ENTERO')              # Segundo número de la condición
        self.coincidir('DOS_PUNTOS')          # ':'
        self.coincidir('CONTENIDO')           # Cuerpo del if
    
        self.codigo_python += f"if {numero1} {operador} {numero2}: {contenido_if}\n"
    
        # Revisar si hay un else.
        if self.token_actual and self.token_actual[0] == 'PALABRA_RESERVADA' and self.token_actual[1] == 'UwU-else':
            self.consumir_token()
            self.coincidir('DOS_PUNTOS')
            contenido_else = self.tokens[self.indice_token][1] 
            self.coincidir('CONTENIDO')

            self.codigo_python += "else: " + contenido_else + "\n"

    def declaracion_for(self):
        self.coincidir('PALABRA_RESERVADA')  # 'UwU-for'
        identificador = self.tokens[self.indice_token + 0][1]  # Capturamos el identificador
        rango_final = self.tokens[self.indice_token + 2][1]  # Capturamos el final del rango
        contenido = self.tokens[self.indice_token + 4][1]

        self.coincidir('IDENTIFICADOR')      # Identificador de la variable del for
        self.coincidir('RANGO')              # 'UwU-range'
        self.coincidir('ENTERO')             # Final del rango
        self.coincidir('DOS_PUNTOS')         # ';'
        self.coincidir('CONTENIDO')          # Contenido del for

        # Traducción a Python
        self.codigo_python += f"for {identificador} in range({rango_final}): {contenido}\n"


    def expresion(self):
        self.coincidir('IDENTIFICADOR')
        self.coincidir('SIMBOLOS')
        if self.token_actual[0] == 'IDENTIFICADOR' or self.token_actual[0] == 'CADENA' or self.token_actual[0] == 'ENTERO':
            self.consumir_token()
        else:
            raise SyntaxError("Se esperaba un identificador o una cadena en la expresión")
