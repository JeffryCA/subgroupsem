import pysubgroup as ps
import pandas as pd
import numpy as np
from subgroup_sem import SEMTarget, TestQF

############################################################################################
# imoport and preprocess data
############################################################################################

#data = pd.read_pickle('ess_preprocessed_data.pkl')
#types = data.applymap(type).apply(set)
#print(types[types.apply(len) > 1])

data = pd.read_csv('ess_data.csv').drop(['Unnamed: 0'], axis=1)

print(data.columns)
stop

types = data.applymap(type).apply(set)
str_cols = types[types.apply(len) > 1].index

for str_col in str_cols:
    data[str_col] = data[str_col].fillna('nan')

types = data.applymap(type).apply(set)
print(types[types.apply(len) > 1])

############################################################################################
# define R model and variables
############################################################################################
"""
model = (' # direct effect \n'
        'Y ~ c(cM1,cM2) * Mod_X + c(c_prime1, c_prime2) * X \n'
        '# mediator \n'
        'M ~ c(aM1,aM2) * Mod_X + c(a1,a2) * X \n'
        'Y ~ c(bM1,bM2) * Mod_M + c(b1,b2) * M \n'
        '# indirect effect (a*b) \n'
        'indirect1 := (a1 + 0.0242) * (b1 + 0.0241) \n'
        'indirect2 := (a2 + 0.0241) * (b2 + 0.0241) \n'
        '# direct effect c_prime \n'
        'direct1 := c_prime1 + 0.0242 \n'
        'direct2 := c_prime2 + 0.0242 \n'
        '# total effect \n'
        'total1 := direct1 + indirect1 \n'
        'total2 := direct2 + indirect2')

Wald_Test_contstraints = ('a1==a2\n'
                        'b1==b2\n'
                        'c_prime1==c_prime2\n'
                        'aM1==aM2\n'
                        'bM1==bM2\n'
                        'cM1==cM2')
"""
model = ('# direct effect \n'
        'happy ~  c(c_prime1,c_prime2) * reli \n'
        '# mediator \n'
        'reco ~ c(a1,a2) * reli \n'
        'happy ~ c(b1,b2) * reco \n'
        '# indirect effect (a*b) \n'
        'indirect1 := a1 * b1 \n'
        'indirect2 := a2 * b2 \n'
        '# direct effect c_prime \n'
        'direct1 := c_prime1 \n'
        'direct2 := c_prime2 \n'
        '# total effect \n'
        'total1 := direct1 + indirect1 \n'
        'total2 := direct2 + indirect2')

Wald_Test_contstraints = 'indirect1==indirect2'

############################################################################################
# define and perform subgroup discovery task
############################################################################################

target = SEMTarget(data, model, Wald_Test_contstraints)

# define Variables for Mediator Model
#dic_lavaan = {"religiosity":'X', "happy":'Y', "recognition":'M', "religiosity_x_religiosity_cntry":'Mod_X', "recognition_x_religiosity_cntry":'Mod_M'}
#data.rename(columns=dic_lavaan, inplace=True)

#ignore = ['cntry', 'happy', 'rlgatnd', 'rlgdgr', 'trtrsp', 'trtunf', 'rcndsrv', "religiosity", "recognition", 'recognition_x_religiosity_cntry', 'religiosity_x_religiosity_cntry', 'religiosity_cntry']
#ignore = ignore + ['Y', 'X', 'M', 'Mod_X', 'Mod_M']

ignore = []
cols = ["agea", "maritala", "uempla", "uempli", "hincfel", "edulvla", "rlbglg", "rlgdnm", "trstlgl", "livecntr"]

#print(data.columns)
for col in data.columns:
    if col not in cols:
        ignore = ignore + [col]
#print(ignore)


# define search space
searchSpace = ps.create_selectors(data, ignore=ignore)
searchSpace = [sel for sel in searchSpace if not '=nan' in  str(sel) and 'edulvla=55.0' not in str(sel)]
num_combinations = len(searchSpace) + len(searchSpace)*(len(searchSpace)-1)/2
print ('Size Search Space:' , len(searchSpace), 'Number of combinations', num_combinations)

def q(WT_score):
    return WT_score

def q2(size_sg, indirect1, indirect2):
    if size_sg < 20:
        return -1
    else:
        return size_sg**(0.1) * abs( indirect1 - indirect2 )

task = ps.SubgroupDiscoveryTask(data, target, searchSpace, result_set_size=10, depth=2,
                                qf=ps.GeneralizationAwareQF(TestQF(q, ['WT_score'])))
task2 = ps.SubgroupDiscoveryTask(data, target, searchSpace, result_set_size=10, depth=2,
                                qf=ps.GeneralizationAwareQF(TestQF(q2, ['size_sg', 'indirect1', 'indirect2'])))

result = ps.SimpleDFS().execute(task)
result2 = ps.SimpleDFS().execute(task2)

############################################################################################
# print results and perform p-value corrections
############################################################################################
dic_results = {}

for rank, (q, subgroup) in enumerate(result.to_descriptions()):
    # table
    statistics = target.calculate_statistics(subgroup)
    description = subgroup
    size = statistics['size_sg']
    params = statistics['parameters']
    wald_test = statistics['wald_test_stats']
        
    # Bonferroni correction of the p-Value
    p_bf = wald_test.loc['WT_p','value'] * num_combinations

    dic_results[rank] = {"Rank":rank+1, "score":q,'p_{WT}':p_bf ,
                 "Sg description":description, "size":size , "dir_eff":params.loc['direct1', 'est'],
                  "indir_eff":params.loc['indirect1','est']}

df_results = pd.DataFrame.from_dict(dic_results, orient='index')

#print(df_results.to_latex())

print('\n\n##############################################################################\n\n')

dic_results2 = {}

for rank, (q, subgroup) in enumerate(result2.to_descriptions()):
    # table
    statistics = target.calculate_statistics(subgroup)
    description = subgroup
    size = statistics['size_sg']
    params = statistics['parameters']
    wald_test = statistics['wald_test_stats']
        
    # Bonferroni correction of the p-Value
    p_bf = wald_test.loc['WT_p','value'] * num_combinations
    dic_results2[rank] = {"Rank":rank+1, "score":q, 'WaldTest':wald_test.loc['WT_score','value'], 'p_{WT}':p_bf ,
                 "Sg description":description, "size":size , "dir_eff":params.loc['direct1', 'est'],
                  "indir_eff":params.loc['indirect1','est']}
     
df_results2 = pd.DataFrame.from_dict(dic_results2, orient='index')

#print(df_results2.to_latex())

df_results.to_csv('res1.csv')
df_results2.to_csv('res2.csv')
