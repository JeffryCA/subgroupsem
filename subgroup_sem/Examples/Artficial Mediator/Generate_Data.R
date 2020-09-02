library(lavaan)

#mediator Model
model.1 <- '# direct effect
             Y ~ 0.1 *X
           # mediator
             M ~ .9 *X
             Y ~ .8 *M
             '

model.2 <- '# direct effect
             Y ~ .8 *X
             # mediator
             M ~ .3 *X
             Y ~ .4 *M
             '

model <- ' # direct effect
             Y ~ c*X
           # mediator
             M ~ a*X
             Y ~ b*M
           # indirect effect (a*b)
             ab := a*b
           # total effect
             total := c + (a*b)
             '

# second dataset
a1 <- rep('A1', 1000)
a2 <- rep('A2', 1000)
b1 <- rep('B1', 1000)
b2 <- rep('B2', 1000)

# generate data
set.seed(12345)
Data_1 <- simulateData(model.1, sample.nobs=1000)
Data_2 <- simulateData(model.2, sample.nobs=3000)

# merge data
df_a1b1 <- data.frame(x=a1, y=b1)
df_a1b2 <- data.frame(x=a1, y=b2)
df_a2b1 <- data.frame(x=a2, y=b1)
df_a2b2 <- data.frame(x=a2, y=b2)

df_3000 <- rbind(rbind(df_a1b2, df_a2b1), df_a2b2)

Data <- rbind(cbind(df_a1b1,Data_1) , cbind(df_3000, Data_2))

# generate noise
for (i in 1:20) {
  size_probability = runif(1, min=0, max=1)
  Data <- cbind(Data, rbinom(4000, 1, size_probability))
  names(Data)[ncol(Data)] <- paste0("N", i)
}

write.table(Data,file='artificial_data.csv', sep=",")





