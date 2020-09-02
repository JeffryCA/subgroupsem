import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer

############################################################################################
# imoport and preprocess data
############################################################################################

# Variable descriptions:
# https://www.europeansocialsurvey.org/docs/round3/survey/ESS3_appendix_a3_e01_0.pdf

data_raw = pd.read_stata('ESS3/ESS3e03_7.dta', convert_categoricals=False)
weights = data_raw[['dweight', 'pspwght', 'pweight', 'cntry']] # Desig-, Post-stratification-, Population Size weight 

############################################################################################
# choosing variables and combining to create scores
############################################################################################

data = data_raw[['cntry', 'happy', 'rlgatnd', 'rlgdgr', 'trtrsp', 'trtunf', 'rcndsrv','agea', 'maritala', 'uempla', 'uempli', 'hincfel', 'edulvla', 'rlgblg', 'rlgdnm', 'trstlgl', 'livecntr']] # ,'health'
print('Raw Size: ', data.shape)
data = data.dropna(subset=['cntry', 'happy', 'rlgatnd', 'rlgdgr', 'trtrsp', 'trtunf', 'rcndsrv'])
print('Size after dropping missing values: ', data.shape)

data['rlgatnd'] = max(data['rlgatnd']) - data['rlgatnd'] # invert scales
data['trtunf'] = max(data['trtunf']) - data['trtunf'] # invert scales 

############################################################################################
# CFA to combine varibales
############################################################################################

from factor_analyzer import (ConfirmatoryFactorAnalyzer, ModelSpecificationParser)
df = data[['rlgatnd','rlgdgr','trtrsp','trtunf','rcndsrv']]
model_dict = {'religionsity':['rlgatnd','rlgdgr'], 'recognition':['trtrsp','trtunf' ,'rcndsrv']}
model_spec = ModelSpecificationParser.parse_model_specification_from_dict(df, model_dict)
cfa = ConfirmatoryFactorAnalyzer(model_spec, disp=False)
cfa.fit(df.values)
print("Factor loadings:\n", cfa.loadings_)
latent_factors = cfa.transform(df.values)
data['religiosity'] = latent_factors[:,0]
data['recognition'] = latent_factors[:,1]

############################################################################################
# create ccountry religiosity score
############################################################################################

df_weights_cntry = weights.groupby('cntry', as_index=False)['pweight'].mean()
df_reli_cntry = data.groupby('cntry', as_index=False)['religiosity'].mean()
MEAN_CNTRY_RELI = np.sum( df_weights_cntry['pweight'] * df_reli_cntry['religiosity'] / np.sum(df_weights_cntry['pweight']) )
#robjects.globalenv['Mod_Mean'] = MEAN_CNTRY_RELI
print('Country Religiosity Average', MEAN_CNTRY_RELI)
data = data.join(df_reli_cntry.set_index('cntry'), on='cntry', how='left', rsuffix='_cntry')


# center data
data[['recognition', 'religiosity', 'happy']] = data[['recognition', 'religiosity', 'happy']].apply(lambda x: x - x.mean())

############################################################################################
# generate interaction terms (for moderation)
############################################################################################

data['religiosity_x_religiosity_cntry'] = data['religiosity'] * data['religiosity_cntry']
data['recognition_x_religiosity_cntry'] = data['recognition'] * data['religiosity_cntry']

############################################################################################
# change respective columns to categorical ones
############################################################################################

to_str = ['maritala', 'uempla', 'uempli', 'hincfel', 'edulvla', 'rlgblg', 'rlgdnm', 'livecntr'] #'health',

for attr in to_str:
        data[attr] = data[attr].apply(str)

data.to_pickle('ess_preprocessed_data.pkl') # save data

############################################################################################
### Test cronbach's alpha
############################################################################################

print('Cronbachs alpha')
def CronbachAlpha(itemscores):
    itemscores = np.asarray(itemscores)
    itemvars = itemscores.var(axis=0, ddof=1)
    tscores = itemscores.sum(axis=1)
    nitems = itemscores.shape[1]

    return (nitems / (nitems-1)) * (1 - (itemvars.sum() / tscores.var(ddof=1)))

religiosity = data[['rlgatnd', 'rlgdgr']].values
recognition = data[['trtrsp', 'trtunf', 'rcndsrv']].values
print('religiosity: ', CronbachAlpha(religiosity))
print('recognition: ', CronbachAlpha(recognition))





