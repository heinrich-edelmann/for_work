##################################
###    TRATAMENTO DOS DADOS    ###
##################################

# BAIXAR PACOTES, CASO ELES AINDA N?O ESTEJAM BAIXADOS
if(!require(dplyr)) install.packages("dplyr") 
if(!require(lubridate)) install.packages("lubridate") 



# CARREGAR PACOTES
library(dplyr)
library(lubridate)

# BUSCAR DIRETÓRIO (PASTA COM OS ARQUIVOS)
setwd("C:/Users/hhhme/Documents/GitHub/for_work/learning R/Projeto 1 - Analise de Dados/dados-covid-sp-master/data")

# ABRIR ARQUIVO
covid_sp <- read.csv('dados_covid_sp.csv', sep = ";")
View(covid_sp)

cl <- colnames(covid_sp)
cl






covid_sp <- read.csv2('dados_covid_sp.csv', sep = ";", encoding="UTF-8")
View(covid_sp)
head(covid_sp)







# Renomeando variáveis (colunas)
covid_sp_alterado <- rename(covid_sp, municipio = nome_munic)
View(covid_sp_alterado)


covid_sp_alterado <- rename(covid_sp_alterado, data = datahora,
                    rotulo_mapa = map_leg,codigo_mapa = map_leg_s)
View(covid_sp_alterado)

# EXCLUIR UMA COLUNA (POR NOME)
covid_sp_alterado$cod_ra <- NULL
# nome_Dataframe$nome_coluna <- NULL

# EXCLUIR UMA COLUNA (POR N?MERO)
covid_sp_alterado <- select(covid_sp_alterado, - c(21))

# df -< select(df, - c(numero_da_coluna))    "menos a concatenacao da coluna e seus elementos"

# EXCLUIR V?RIAS COLUNAS (POR NOME)
covid_sp_alterado <- subset(covid_sp_alterado, select = -c(codigo_ibge, cod_drs))

# df <- subset(df, select = -c(coluna1, coluna2))

# EXCLUIR V?RIAS COLUNAS (POR N?MERO)
covid_sp_alterado <- select(covid_sp_alterado, -c(14,15))

covid_sp_alterado <- select(covid_sp_alterado, -c(17:19))


# EXCLUIR UMA LINHA (POR NUMERO)
covid_sp_alterado <- slice(covid_sp_alterado, -c(239660))

# df <- slice(df, -c(numero_da_linha))

covid_sp_alterado <- slice(covid_sp_alterado, -c(239661:239666))

# EXCLUIR VÁRIAS LINHAS (POR NOME)
covid_sp_alterado <- covid_sp_alterado %>% filter(municipio!="Ignorado")

#df <- df %>% filter(coluna!=value)

#  %>% is from a package designed to make data analysis more intuitiv
#      it's known as pipe operator and it is used to "pipe" data through a function, 
#       the data gets out then verarbeitet

View(covid_sp_alterado)



setwd("C:/Users/hhhme/Documents/GitHub/for_work/learning R/Projeto 1 - Analise de Dados/dados-covid-sp-master/data")

covid_sp_alterado <- read.csv2('covid_sp_tratado.csv', sep = ";")
View(covid_sp_alterado)


# Verificando missing values NA

# NA = valores ausentes
# NAN = not a number(valor indefinido)
sapply(covid_sp_alterado, function(x) sum(is.na(x)))
sapply(covid_sp_alterado, function(x) sum(is.nan(x)))



#Substituir valores missing

########### Função mutate all temporariamente desabilitada ######
if(!require(tidyr)) install.packages("tidyr")
 library(tidyr)

covid_sp_alterado2 <- covid_sp_alterado %>% mutate_all(replace_na, 54)
View(covid_sp_alterado2)
###################################################################

### OPÇÃO:
covid_sp_alterado2 <- replace(x = covid_sp_alterado,list = is.na(covid_sp_alterado),
                 values = 54)

# df <- replace(x = df, value_tobe_replaced, new_value)

#OU

covid_sp_alterado2$semana_epidem[covid_sp_alterado2$semana_epidem == 54] <- 2021

# df_that_will_be_changed$coluna[referencia] <- new_value

covid_sp_alterado2$semana_epidem[covid_sp_alterado2$data >= '01-01-2021' &
                                   covid_sp_alterado2$data <= '07-01-2021'  ] <- 54

# df$coluna_cm_valor_a_ser_replaced[df$outra_coluna >= valor_nessa_coluna &
#                                    df$outra_coluna >= valor_nessa_coluna] <- new_value

# ↓variavel q sera alterada  ↓coluna onde a alteracao ira ocorrer
covid_sp_alterado2$semana_epidem[covid_sp_alterado2$data >= '08-01-2021' &
                                    covid_sp_alterado2$data <= '14-01-2021'  ] <- 55
#                                          [ referencia ]                         ↑ new value




#VERIFICAÇÃO DA TIPAGEM DOS ATRIBUTOS (Variáveis)
# EXISTEM 7 TIPOS BÁSICOS:
# character (caracteres)
# integer (números inteiros)
# numeric (números reais)
# logical (falso ou verdadeiro)
# complex (números complexos)
# factor (fator: Sequência de valores definidos por níveis)
# date (data)
str(covid_sp_alterado2)
# OU
glimpse(covid_sp_alterado2)

#Transformação da tipagem de atributos
covid_sp_alterado2$semana_epidem <- as.integer(covid_sp_alterado2$semana_epidem)
glimpse(covid_sp_alterado2)
View(covid_sp_alterado2)


covid_sp_alterado2_data <- covid_sp_alterado2$data

View(covid_sp_alterado2_data)

covid_sp_alterado2_data <- as.Date(covid_sp_alterado2_data, format ='%Y-%m-%d')
glimpse(covid_sp_alterado2_data)



covid_sp_alterado2$data <- as.Date(covid_sp_alterado2$data, format ='%Y-%m-%d')
glimpse(covid_sp_alterado2)

covid_sp_alterado2 <- covid_sp_alterado2 %>% mutate(data = format(data, "%d/%m/%Y"))
glimpse(covid_sp_alterado2)

# ↑↑↑ alterar o jeito q a data foi colocada

# Alterar várias variáveis de uma única vez
#covid_sp_alterado2[1:17] <- lapply(covid_sp_alterado2[1:17], as.character)
#glimpse(covid_sp_alterado2)


# Criação de colunas
covid_sp_alterado2["idoso(%)"]<-(covid_sp_alterado2$pop_60/covid_sp_alterado2$pop)*100
View(covid_sp_alterado2)
# pra criacao de novas colunas usa-se []

covid_sp_alterado2 <- select(covid_sp_alterado2, - c(19))


#Exportação de arquivos
write.table(covid_sp_alterado2, file ="covid_sp_tratado.txt", sep = ",")


# Opção de exportação de arquivos
install.packages("readr", dependencies = TRUE)
library("readr")
write_delim(covid_sp_alterado2, "covid_sp_tratado.csv", delim = ";")

