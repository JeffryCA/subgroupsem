library(lavaan)
library(plyr)



# fit Model and get parameters and statistics
rval <- tryCatch({
  d$subgroup <- sg
  fit <- sem(model, data = d, group='subgroup', group.label=c("1","0"))
  params_df <- parameterEstimates(fit)
  stats <- fitMeasures(fit)
  stats_df = data.frame(keyName=names(stats), value=stats, row.names=NULL)
  waldTest_df = ldply (lavTestWald(fit, constraints = Wald_Test_contstraints) , data.frame)
  list(params_df, stats_df, waldTest_df)
}, error = function(e) -1)

