#########################################
###   ESTRUTURA DOS DADOS - FATORES   ###
#########################################

# Sequencia de valores, definidos por niveis, comumente expressa variaveis categoricas.
# Facilita quando se deseja saber a quantidade de cada categoria.

# Vetor
escolaridade <- c("fundamental", "medio", "superior", "medio", "superior", "fundamental")
print (escolaridade)


# Fator
escolaridade_fator <- as.factor(escolaridade)
print (escolaridade_fator)


escolaridade[3]


escolaridade_fator[3]



summary (escolaridade)
summary (escolaridade_fator)


table(escolaridade) # the table() counts the occurences in the vector taken as parameter
                  #(in this case the vector escolaridade), and shows them, kinda like a pivot table

# Tensao eletrica em residencias (110V, 220V)

tensao_casas <- c(110, 220, 110, 110, 110, 110, 220)
print(tensao_casas)
summary(tensao_casas)

tensao_casas_fator <- as.factor (tensao_casas)
print(tensao_casas_fator)
summary(tensao_casas_fator)



