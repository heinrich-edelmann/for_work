#######################################
###    IMPORTA??O DE DATA FRAMES    ###
#######################################






setwd("C:/Users/hhhme/Documents/GitHub/for_work/learning R/importacao_Dataframes")

# pra abrir arquivo txt

df1 <- read.table("partks.txt")
df1
View(df1)

# pra abrir arquivo csv

df2 <- read.csv("mola.csv")
df2
summary(df2)

df3 <- read.csv("questoes.csv")

df3 <- read.csv("questoes.csv", encoding = "latin-1")

df3 <- read.csv("questoes.csv", encoding = "iso-8859-1")

df3 <- read.csv("questoes.csv", encoding = "UTF-8")


# Arquivo excel

install.packages("readxl")
library(readxl)

df4 <- read_xlsx("registro.xlsx")












