import pysubgroup as ps
import pandas as pd
from subgroup_sem import SEMTarget, TestQF

############################################################################################
# imoport and preprocess data
############################################################################################

data = pd.read_csv('artificial_data.csv')[['x', 'y', 'X', 'Y', 'M', 'N1', 'N2']]

# check sg sizes
#print(data.astype(bool).sum(axis=0))

############################################################################################
# define R model
############################################################################################

model = (' # direct effect \n'
        'Y ~ c(c1,c2)*X \n'
        '# mediator \n'
        'M ~ c(a1,a2)*X \n'
        'Y ~ c(b1,b2)*M \n'
        '# indirect effect (a*b) \n'
        'indirect1 := a1*b1 \n' 
        'indirect2 := a2*b2 \n'
        '# total effect \n'
        'total1 := c1 + (a1*b1) \n'
        'total2 := c2 + (a2*b2) \n'
        '# direct effect \n'
        'direct1 := c1 \n'
        'direct2 := c2 \n'
        '# rest \n'
        'Y ~~ c(r1_1,r1_2)*Y \n'
        'X ~~ c(r2_1,r2_2)*X \n'
        'M ~~ c(r3_1,r3_2)*M \n'
        'Y ~ c(r4_1,r4_2)*1 \n'
        'X ~ c(r5_1,r5_2)*1 \n'
        'M ~ c(r6_1,r6_2)*1')

wald_test_contstraints = 'c1==c2'

############################################################################################
# define and perform subgroup discovery task
############################################################################################

target = SEMTarget (data, model, wald_test_contstraints)

searchSpace = ps.create_selectors(data, ignore=["X", "Y", "M"])
num_combinations = len(searchSpace) + len(searchSpace)*(len(searchSpace)-1)/2
print(num_combinations)

def q(WT_score):
	return WT_score

task = ps.SubgroupDiscoveryTask(data, target, searchSpace, result_set_size=10,
                                depth=2, qf=ps.GeneralizationAwareQF(TestQF(q, ['WT_score'])))

result = ps.SimpleDFS().execute(task)

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
    
    dic_results[rank] = {"Rank":rank+1, "score":q, 'p_{WT}':p_bf, "Sg description":description, "size":size,
                         "dir_eff":params.loc['c1', 'est'], "indir_eff":params.loc['indirect1','est']}

    print('Nr. {0:}, q: {1:}, Sg: {2}, Size: {3:}'.format(rank+1, q, description, size))

df_results = pd.DataFrame.from_dict(dic_results, orient='index')

#print(df_results.to_latex())


