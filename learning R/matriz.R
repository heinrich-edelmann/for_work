############################################
###    ESTRUTURA DOS DADOS - MATRIZES    ###
############################################

# Conjunto de registros com linhas e colunas, 
# contendo somente numeros ou somente caracteres. 

?matrix  # a interrogacao ? em frente ao nome de algum elemento da a descricao desse elemento, seus parametros e como usa-lo, ou da pra ir na sessao Help e digitar o nome do elemento
?factor

matriz <- matrix(c(1,5,10,30,15,8),nrow=3,ncol=2,byrow=TRUE)
print(matriz)

matriz <- matrix(c(4,8,12,16,20,24),nrow=3,ncol=2,byrow=FALSE)
print(matriz)

matriz <- matrix(c(4,8,12,16,20,24),nrow=3,ncol=2,byrow=TRUE)
print(matriz)


# com o parametro byrow=TRUE a matriz é preechinda porlinha 
# com byrow=FALSE a matriz é preenchida por coluna

matriz [1,2]

?rbind # → binds vectors, matrizes or data-frames

vetorA <- c(2,5,8)
vetorB <- c(3,6,9)
matriz2 <- rbind(vetorA, vetorB)
matriz2

matriz2 [2,1]

matriz3=matrix(2:9, ncol = 2, byrow = TRUE)
matriz3

matriz3=matrix(2:9, ncol = 2)
matriz3


# Numero de linhas e colunas.
dim(matriz3) # dim() da as dimensoes
nrow(matriz3) # n de linhas
ncol(matriz3) # n de colunas

# Nomear linhas e colunas
dimnames(matriz3) <- list(c("Linha1","Linha2","Linha3","Linha4"), #dimnames() renomeia as linhas/colunas
                          c("Coluna1", "Coluna2"))
matriz3             # ↑↑ os valores em list foram dados bem na sequencia "linhas" e depois "colunas"
                    # list(linhas,colunas)

matriz4=matrix(2:13, nrow = 4, byrow=TRUE,
               dimnames = list(c("Linha1","Linha2","Linha3","Linha4"),
                               c("Coluna1", "Coluna2","Coluna3")))
matriz4


matriz4=matrix(2:13, nrow = 4, byrow=FALSE,
               dimnames = list(c("Linha1","Linha2","Linha3","Linha4"),
                               c("Coluna1", "Coluna2","Coluna3")))
matriz4

# Produto de um n?mero por uma matriz
produto <- 2 * matriz4
produto

# Soma ou subtra??o de matrizes
matriz5 = matrix(c(1,5,15,8),nrow=2,ncol=2,byrow=TRUE)
matriz5
matriz6 = matrix(c(2,4,6,10),nrow=2,ncol=2,byrow=TRUE)
matriz6

soma = matriz5+matriz6
soma

subtracao = matriz5-matriz6
subtracao


# Multiplicacao Matricial

produto_matriz = matriz5 %*% matriz6 # pra multiplicacao matricial
produto_matriz

# Media das linhas ou colunas
matriz5 = matrix(c(1,5,15,8),nrow=2,ncol=2,byrow=TRUE)
matriz5

media_coluna <- colMeans(matriz5)
media_coluna

media_linha <- rowMeans(matriz5)
media_linha

# Soma das linhas ou colunas
soma_linhas <- rowSums(matriz5)
soma_linhas

soma_colunas <- colSums(matriz5)
soma_colunas

# Matriz com caracteres
matriz7 = matrix(c("segunda","terca","quarta","quinta"),nrow=2,ncol=2,byrow=FALSE)
matriz7







