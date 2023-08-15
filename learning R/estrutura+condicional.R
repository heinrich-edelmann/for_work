###############################################
###    ESTRUTURA CONDICIONAL - if e else    ###
###############################################


x <- 13
if (x < 10) {
  print("x ? menor que 10!")
} else {
  print("x ? maior ou igual a 10")
}




y <- 21
if (y < 20) {
  print("y é menor que 20!")
} else if (y == 20){
  print("y é igual a 20")
} else {
  print("y é maior que 20")
}



w <- 13
ifelse(w %% 2 == 0, "par", "impar") # ifelse() → funcao feita pra simplificar o uso de if else
# %% → resto

ifelse(w %% 2 != 0 & w %% 3 != 0 & w %% 5 != 0 & w %% 7 != 0, "primo", "nao-primo")



nota <- 5
if (nota >= 6){
  print('Aprovado')
} else if (nota >= 5 & nota< 6){
  print('Recuperacao')
} else {
  print('Reprovado')
}




