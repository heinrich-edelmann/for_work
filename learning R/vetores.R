#########################################
###   ESTRUTURA DOS DADOS - VETORES   ###
#########################################

# Sequ?ncia de valores num?ricos ou caracteres

vetor <- c(1,2,3,4,5,6,7)
class(vetor)

dias <- c("segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo")
class(dias)

juntando <- c(vetor, dias)
juntando
class(juntando)

gastos_dia <- c(400, 300, 100, 500, 150, 430, 70)
gastos_dia
class(gastos_dia)
length(gastos_dia)

ordem_crescente <- sort(gastos_dia) # sort() → msm logica do SORTED BY
ordem_crescente

total <- sum(gastos_dia) # soma dos valores do vetor
total

minimo <- min(gastos_dia)
min(gastos_dia)

max(gastos_dia)
maximo <- max(gastos_dia)

media <- mean(gastos_dia)
mean(gastos_dia)

limite <- (gastos_dia <= 300)
limite

intervalo <- (3:8)
intervalo           # diferente de python, ele inclui o 3 e o 8 no intervalo (3:8)

passo <- seq(2,47,by=5) # seq(inicio,fim, by = passos a se contar), ae ficam os numeros de 2 a 47 com 5 de intervalo
passo

repeticao <- rep(2,8) # rep(numero a ser repetido, vezes que o valor sera repetido)
repeticao

repeticao_multipla <- rep(c(3,5),c(4,6))
repeticao_multipla
# da pra escrever a msm logica das 2 formas ↑▬↓
repeticao_multipla2 <- c(rep(1,10),rep(3,5))
repeticao_multipla2


repeticao_programada <- rep(3:5, each = 3) # repete os numeros de 3 a 5, 3 vezes cada
repeticao_programada

repeticao_programada_2 <- rep(3:6,3) # diferente de repeticao_programada↑ ele repete o intervalo de 3 a 6, 3 vezes
repeticao_programada_2

vetor2 <- c(2,4,6,8,10,12)
vetor3 <- c(vetor2,14) # incluindo registro num vetor
vetor3
class(vetor3)
vetor3 <- as.integer(vetor3)

vetor4 <- c(vetor3,"pares")
vetor4
class(vetor4)

posicao <- vetor3[5]
posicao         # DIFERENTE DE PYTHON AS POSICOES COMECAM COM A POSICAO 1 E NAO CM A POSICAO 0
vetor3[4]

posicao_inexistente <- vetor3[8]
posicao_inexistente

posicao_excluida <- vetor3[-3]   # a posicao em numero negativo exclui o elemento da posicao
posicao_excluida                 # aqui foi excluido assim a posicao [3] q era o numero 6

posicao_excluida <- vetor3[-5]
posicao_excluida









