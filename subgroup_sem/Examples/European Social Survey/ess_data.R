library(essurvey)
library(tidyverse)
library(rjson)

# How to download the data is explained here with more detail.
# https://cran.r-project.org/web/packages/essurvey/vignettes/intro_ess.html

dir <- getwd()

json_data = fromJSON(file='config.json')
mail = json_data['mail']

set_email(mail) # mail corresponding to account at ESS

download_rounds(3,
                output_dir = dir,
                format = 'stata')

#########################################
#### New !!
library(foreign)
library(lavaan)
library(dplyr)
file <- paste0(dir,"/ESS3/ESS3e03_7.dta")
d <- read.dta(file, convert.factors = T)

data <- d %>% select(cntry, happy, rlgatnd, rlgdgr, trtrsp, trtunf, rcndsrv,agea, maritala, uempla, uempli, hincfel, edulvla, rlgblg, rlgdnm, trstlgl, livecntr)


for (name in c("rlgatnd", "rlgdgr", "trtrsp", "trtunf", "rcndsrv", "happy")){
  data[,name] <- as.numeric(data[,name])
}

data$rlgatnd_R <- max(data$rlgatnd, na.rm = T) - data$rlgatnd
data$trtunf_R <- max(data$trtunf, na.rm = T) - data$trtunf


syn <- '
reli =~ rlgatnd_R + rlgdgr
reco =~ trtrsp + trtunf_R + rcndsrv
'
fit <- sem(syn, data, missing = "fiml")
summary(fit, fit.measures = T)


fs <- lavPredict(fit)
data <- cbind(data, fs)

write.csv(data, 'ess_data.csv')


#catnames <- c('maritala', 'uempla', 'uempli', 'hincfel', 'edulvla', 'rlgblg', 'rlgdnm', 'livecntr')
#for (name in catnames){
#  dat[,name] <- as.factor(dat[,name])
#}
