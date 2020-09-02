from timeit import default_timer as timer
import pysubgroup as ps
from subgroup_sem import SEMTarget, TestQF
from subgroup_sem.tests.DataSets import get_artificial_data


if __name__ == '__main__':
    data = get_artificial_data()
    model = ('# direct effect \n'
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

    wald_test_contstraints = 'a1==a2 \n b1==b2 \n c1==c2'

    target = SEMTarget (data, model, wald_test_contstraints)
    searchSpace = ps.create_selectors(data, ignore=["X", "Y", "M"])
    def q(WT_score):
        return WT_score
    task = ps.SubgroupDiscoveryTask(data, target, searchSpace, result_set_size=10, depth=2, qf=TestQF(q, ['WT_score']))

    print("running DFS")
    start = timer()
    result = ps.SimpleDFS().execute(task)
    end = timer()

    print("Time elapsed: ", (end - start))
    for (q, sg) in result.to_descriptions():
        print(str(q) + ":\t" + str(sg))

