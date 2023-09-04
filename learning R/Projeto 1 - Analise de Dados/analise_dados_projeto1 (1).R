############################################
###    EXPLORA??O E AN?LISE DOS DADOS    ###
############################################

# CARREGAR PACOTES
library(dplyr)
if(!require(rstatix)) install.packages("rstatix") 
library(rstatix)

# BUSCAR DIRET?RIO (PASTA COM OS ARQUIVOS)
setwd("C:/Users/hhhme/Documents/GitHub/for_work/learning R/Projeto 1 - Analise de Dados/dados-covid-sp-master/data")

# ABRIR ARQUIVO
covid_sp_tratado <- read.csv2('covid_sp_tratado.csv', sep = ";", encoding="UTF-8")
View(covid_sp_tratado)

covid_sp_tratado <- read.csv2('covid_sp_tratado.csv', sep = ",")
View(covid_sp_tratado)

glimpse(covid_sp_tratado)

covid_sp_tratado <- read.csv('covid_sp_tratado.csv', sep = ";")
View(covid_sp_tratado)

glimpse(covid_sp_tratado)

covid_sp_tratado$data <- as.Date(covid_sp_tratado$data, format ='%d/%m/%Y')
glimpse(covid_sp_tratado)

covid_sp_tratado$idoso <- as.numeric(covid_sp_tratado$idoso)
glimpse(covid_sp_tratado)

# Excluir coluna idoso(%)
covid_sp_tratado <- select(covid_sp_tratado, -c(18))

# Renomeando a coluna idoso
covid_sp_tratado <- rename(covid_sp_tratado, porcentagem_idoso = "idoso...")


View(covid_sp_tratado)




library("readr")
write_delim(covid_sp_tratado, "covid_sp_tratado.csv", delim = ";")




# Filtro por linha (cidade)

# Campinas
covid_campinas <- covid_sp_tratado %>% filter(municipio=="Campinas")
View(covid_campinas)

covid_campinas["dens_demografica"] <- covid_campinas$pop/covid_campinas$area
View(covid_campinas)

covid_campinas["area"] <- covid_campinas$area/100
# a area estava errada na tabela original e precisou assim ser divido por 100 pra chegar a km²

covid_campinas["dens_demografica"] <- covid_campinas$pop/covid_campinas$area
View(covid_campinas)

# Guarulhos
covid_guarulhos <- covid_sp_tratado[which(covid_sp_tratado$municipio=="Guarulhos"), ]
# ali a funcao which() pega geralmente 2 parametros, linha e coluna;
# como no caso nao há o valor "Guralulhos em nenhuma outra coluna a nao ser municipio,
#nao foi necessario assim especificar a coluna, apenas o valor da linha

covid_guarulhos["area"] <- covid_guarulhos$area/100
# msm problema q se teve com a tabela covid_caampinas. O valor em area nao esta em km²

covid_guarulhos["dens_demografica"] <- covid_guarulhos$pop/covid_guarulhos$area
View(covid_guarulhos)








### ANALISES ESTATISTICAS

# Medidas de centralidade

# Media/mean
mean(covid_campinas$obitos_novos)
mean(covid_campinas$casos_novos)

summarise_at(covid_campinas, vars(obitos_novos, casos_novos), mean)
# a funcao summarise_at ja me da o mean das colunas especificadas como parameto em var()

mean(covid_guarulhos$obitos_novos)
mean(covid_guarulhos$casos_novos)

#verificando rapidao se tem na values na tabela criada covid_guarulhos
sapply(covid_guarulhos, function(x) sum(is.na(x)))


# M?dia m?vel
plot(covid_campinas$data,covid_campinas$casos_mm7d, title("MEDIA MOVEL"), col = "red")
plot(covid_campinas$data,covid_campinas$obitos_mm7d, title("MEDIA MOVEL"), col = "purple")




# Mediana
median(covid_campinas$obitos_novos)
median(covid_campinas$casos_novos)
summarise_at(covid_campinas, vars(obitos_novos, casos_novos), median)

median(covid_guarulhos$obitos_novos)
median(covid_guarulhos$casos_novos)


# Moda

# Criando uma funcao pra "modus" pois R nao tem uma funcao ja embutida pra "modus"
moda <- function(m) {
  valor_unico <- unique(m) #Busca o valor ?nico para a coluna.
  valor_unico[which.max(tabulate(match(m, valor_unico)))] #tabular (contabilizar quantas vezes o valor ?nico aparece) e buscar o maior valor
}

# Obten??o da moda
moda(covid_campinas$obitos_novos)
moda(covid_campinas$casos_novos)

summarise_at(covid_campinas, vars(obitos_novos, casos_novos), moda)

moda(covid_guarulhos$obitos_novos)
moda(covid_guarulhos$casos_novos)










covid_julho_campinas <- covid_campinas %>% filter(mes==7)
View(covid_julho_campinas)
moda(covid_julho_campinas$obitos_novos)
moda(covid_julho_campinas$casos_novos)
summarise_at(covid_julho_campinas, vars(obitos_novos, casos_novos), moda)

mean(covid_julho_campinas$obitos_novos)
mean(covid_julho_campinas$casos_novos)

# Histograma

hist(covid_julho_campinas$obitos_novos, col="blue")
hist(covid_julho_campinas$casos_novos, col="red")

# ↓ apenas um testezinho pra ver como q desenha a linha da Normalverteilung, pra ver como q os dados estao verteilt
hist(covid_julho_campinas$obitos_novos, breaks = 20, main = "Histograma")
x <- seq(min(covid_julho_campinas$obitos_novos), max(covid_julho_campinas$obitos_novos), length = 100)
y <- dnorm(x, mean = mean(covid_julho_campinas$obitos_novos), sd = sd(covid_julho_campinas$obitos_novos))
y <- y * sum(diff(hist(covid_julho_campinas$obitos_novos)$mids) * hist(covid_julho_campinas$obitos_novos)$counts)
lines(x, y, col = "blue")

hist(covid_julho_campinas$casos_novos, breaks = 20, main = "Histogram", freq = FALSE)
x <- seq(min(covid_julho_campinas$casos_novos), max(covid_julho_campinas$casos_novos), length = 100)
y <- dnorm(x, mean = mean(covid_julho_campinas$casos_novos), sd = sd(covid_julho_campinas$casos_novos))
y <- y * sum(diff(hist(covid_julho_campinas$casos_novos)$mids) * hist(covid_julho_campinas$casos_novos)$counts)
lines(x, y, col = "red")
###################################################################################################################


hist(covid_campinas$obitos_novos, col="blue")
hist(covid_campinas$casos_novos, col="red")

hist(covid_guarulhos$obitos_novos, col="green")
hist(covid_guarulhos$casos_novos, col="yellow")










# Medidas de posi??o

# M?nimo
min(covid_campinas$obitos_novos)
min(covid_campinas$casos_novos)
summarise_at(covid_campinas, vars(obitos_novos, casos_novos), min)

min(covid_guarulhos$obitos_novos)
min(covid_guarulhos$casos_novos)


# M?ximo
max(covid_campinas$obitos_novos)
max(covid_campinas$casos_novos)
summarise_at(covid_campinas, vars(obitos_novos, casos_novos), max)

max(covid_guarulhos$obitos_novos)
max(covid_guarulhos$casos_novos)

# Amplitude Total
range(covid_campinas$obitos_novos)
range(covid_campinas$casos_novos)
summarise_at(covid_campinas, vars(obitos_novos, casos_novos), range)

range(covid_guarulhos$obitos_novos)
range(covid_guarulhos$casos_novos)

# Quartis
quantile(covid_campinas$obitos_novos)
quantile(covid_campinas$casos_novos)
summarise_at(covid_campinas, vars(obitos_novos, casos_novos), quantile)

quantile(covid_guarulhos$obitos_novos)
quantile(covid_guarulhos$casos_novos)

# Amplitude Interquartil
IQR(covid_campinas$obitos_novos)
IQR(covid_campinas$casos_novos)
summarise_at(covid_campinas, vars(obitos_novos, casos_novos), IQR)

IQR(covid_guarulhos$obitos_novos)
IQR(covid_guarulhos$casos_novos)











summary(covid_campinas$obitos_novos)
summary(covid_campinas$casos_novos)

summary(covid_guarulhos$obitos_novos)
summary(covid_guarulhos$casos_novos)


# Box Plot
summary(covid_julho_campinas$obitos_novos)
boxplot(covid_julho_campinas$obitos_novos)

summary(covid_julho_campinas$casos_novos)
boxplot(covid_julho_campinas$casos_novos)

summary(covid_campinas$casos_novos)
boxplot(covid_campinas$casos_novos)

summary(covid_guarulhos$casos_novos)
boxplot(covid_guarulhos$casos_novos)

# Tratando os outliers

# Identificando e excluindo todos os outliers
covid_guarulhos %>% identify_outliers(casos_novos)
outliers = c(boxplot.stats(covid_guarulhos$casos_novos)$out)
covid_guarulhos_sem_outliers <- covid_guarulhos[-c(which(covid_guarulhos$casos_novos %in% outliers)),  ]
boxplot(covid_guarulhos_sem_outliers$casos_novos)


# Excluindo alguns outliers
covid_campinas %>% identify_outliers(casos_novos)
covid_campinas_sem_outliers<-covid_campinas %>% filter(data != "2020-06-19")
boxplot(covid_campinas_sem_outliers$casos_novos)


# O summary resulta em resumo estat?stico
# de todas as vari?veis num?ricas/inteiras
summary (covid_guarulhos)





# Medidas de Dispers?o

# Vari?ncia
var(covid_campinas$obitos_novos)
var(covid_campinas$casos_novos)

var(covid_guarulhos$obitos_novos)
var(covid_guarulhos$casos_novos)

var(covid_julho_campinas$obitos_novos)
var(covid_julho_campinas$casos_novos)  


# Desvio padr?o
sd(covid_campinas$obitos_novos)
sd(covid_campinas$casos_novos)

sd(covid_guarulhos$obitos_novos)
sd(covid_guarulhos$casos_novos)

sd(covid_julho_campinas$obitos_novos)
sd(covid_julho_campinas$casos_novos)









# TESTES DE NORMALIDADE

# Existem 4 testes de normalidade principais (num?ricos) e dois testes gr?ficos:
# Shapiro-Wilk (limite de 5000 amostras)
# Anderson-Darling
# Kolmogorov_Smirnov
# Cramer-Von Mises
# Histograma
# QQplot

# N?vel de signific?ncia DE 0,05(5%) ou n?vel de confian?a de 95%(MAIS UTILIZADO):
# Quando o par?metro p > 0,05 (distribui??o normal).


if(!require(nortest)) install.packages("nortest")
library(nortest)

#Histograma
hist(covid_campinas$casos_novos, probability=T, col="blue")
lines(density(covid_campinas$casos_novos) , col="red")

# QQPLOT (GR?FICO DE DISTRIBUI??O NORMAL)
qqnorm(covid_campinas$casos_novos)
qqline(covid_campinas$casos_novos)

# Shapiro-Wilk
shapiro.test(covid_campinas$casos_novos)

# Anderson-Darling
ad.test(covid_campinas$casos_novos)

# Kolmogorov_Smirnov
lillie.test(covid_campinas$casos_novos)

#Cramer-Von Mises
cvm.test(covid_campinas$casos_novos)













# CORRELA??O LINEAR
# method: "pearson" para dados param?tricos(normalidade e homocedasticidade))
#         "spearman" (volume grande de dados n?o param?tricos)
#         "kendall" (volume pequeno de dados n?o param?tricos)

plot(covid_campinas$casos,covid_campinas$obitos)
cor(covid_campinas$casos,covid_campinas$obitos,method = "spearman")

regressao <- lm(formula= obitos ~ casos, data=covid_campinas) #modelo de regress?o
regressao$coefficients
summary(regressao)

### Equa??o: obitos=51.67+0,0337*casos

### Coeficiente de determina??o (ajustado): 0,9832







### GR?FICO DE LINHA COM AJUSTE DE RETA  COM GGPLOT2

if(!require(ggplot2)) install.packages("ggplot2") 
library(ggplot2)
if(!require(ggpubr)) install.packages("ggpubr") #equa??o da reta no gr?fico
library(ggpubr)

ggplot(data = covid_campinas, mapping = aes(x = casos, y = obitos)) +
  geom_point() +
  geom_smooth(method = "lm", col = "red") +
  stat_regline_equation(aes(label = paste(..eq.label.., ..adj.rr.label..,
                            sep = "*plain(\" ,   \")~~")), label.x = 15000,
                            label.y = 1800) +
  theme_gray()


if(!require(corrplot)) install.packages("corrplot")                               
library(corrplot) # gr?fico de correla??o 

matriz_corr <- cor(covid_campinas[5:13], method = "spearman")
View(matriz_corr)

corrplot(matriz_corr, method = "color")
corrplot(matriz_corr, method="color", 
         type="full", order="original", 
         addCoef.col = "black", # adiciona o coeficiente ? matriz
         tl.col="black", tl.srt=45, # cor e rota??o do nome das vari?veis
)



# GR?FICOS LINEARES POR CIDADES

covid_cidades<-covid_sp_tratado %>% filter (municipio  %in% c("Campinas", "Guarulhos", "Sorocaba"))
View(covid_cidades)

ggplot(covid_cidades, aes(x = casos, y = obitos, color = municipio)) +
  geom_line() +
  labs(title = "Evolu??o dos ?bitos em fun??o dos casos de COVID",
       x = "Casos",
       y = "?bitos") +
  theme_classic()




