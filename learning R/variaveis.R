###############################
###   OBJETOS (VARIaVEIS)   ###
###############################

m <- 4 * 7
# ou
m = 4 * 7

print(m)   # bem parecido com python
m

# Nao usar palavras reservadas:
# break, else, for, function, IF, in, next, repeat, while, FALSE, Inf, 
# NA, NaN, NULL,TRUE ...
# Nao colocar acentuacoes.


in <- 3 + 4

p <- 15 / 3
p

diferenca <- m - p
diferenca

a <- 2
b <- 4
c <- a * b
f


### TIPO BASICO DO OBJETO (MODO)

# numeric: numerico → float
# integer: inteiro  → integer
# complex: numero complexo
# character (string): caractere  → string
# logical (boolean): logicos (True e False)  boolean
# factor: categorias bem definidas. ex: genero (masculino e feminino)
#                                       estado civil(casado, solteiro, viuvo...)
#                                       ano (2019, 2020, 2021...)
y = 2
mode(y)
class(y) # class() = mode() → os 2 tem a msm funcao

y <- as.integer(y)
y = as.integer(y)

y
class(y)
mode(y)

x = 7.5
class(x)
x <- as.integer(x)
class(x)
x

complexo <- 2i
complexo

mode(complexo)
class(complexo)

caractere <- "palavra"
class(caractere)
mode(caractere)

logica <- TRUE
class(logica)

logica <- "TRUE"
class(logica)


genero <- c("masculino","feminino") # c() concatena, 
genero                              
class(genero)

genero <- as.factor(genero)
genero
class(genero)

### TIPO BASICO DO OBJETO (Comprimento)
 
length(genero)

p <- 43
length(p)

q <- "bom dia" 
length(q)

w <- c("bom dia","boa tarde", "boa noite")
length(w)








