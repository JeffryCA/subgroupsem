# subgroupsem

One Paragraph of project description goes here

### Prerequisites

* [R(>= 3.4)](https://cran.r-project.org/mirrors.html), R(>4.0.0) if you want to use packrat
* Python3

Ideally one should have a  package to create a virtual environments. We recommend having [Virtualenv](https://virtualenv.pypa.io/en/stable/) 
and the R package [packrat](https://rstudio.github.io/packrat/).

### Installing

Install R packages:
Optional first step in the directory of your project: 

```
install.packages('packrat')
packrat::init()
```

Second step:

```
install.packages('lavaan')
install.packages('plyr')
```

Install subgroup_sem:
Optional first step in the directory of your project:

```
Virtualenv env
source env/bin/activate
```

Second step, installing subgroup_sem:

```
pip install -e .
pip install -e pysubgroup
```

If it doesn't work because of trouble installing [rpy2](https://rpy2.github.io/), try to install that package first

```
pip install rpy2
```

## How to use

```
############################################################################################
# load important packages
############################################################################################

import pysubgroup as ps
from subgroup_sem import SEMTarget, TestQF

############################################################################################
# load dataset
############################################################################################

from subgroup_sem.tests.DataSets import get_artificial_data
data = get_artificial_data()

############################################################################################
# define R model and the constraints for the Wald test in lavaan sintax, 
# we use vectors c(x1, x2) to compute the model for the subgroup and the complement 
############################################################################################

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

############################################################################################
# define quality function
############################################################################################

def q(WT_score):
    return WT_score

############################################################################################
# define and perform subgroup discovery task
############################################################################################

target = SEMTarget (data, model, wald_test_contstraints)
searchSpace = ps.create_selectors(data, ignore=["X", "Y", "M"])
task = ps.SubgroupDiscoveryTask(data, target, searchSpace, result_set_size=10, depth=2, 
                                qf=TestQF(quality_function = q, parameters_list = ['WT_score'], parameters_type_dic={}))
result = ps.SimpleDFS().execute(task)

############################################################################################
# print the results
############################################################################################

for (q, sg) in result.to_descriptions():
    print(str(q) + ":\t" + str(sg))
```
The first lines import the necessary packages and data.
After we define the model and the constraints for the Wald test in [lavaan](http://lavaan.ugent.be/tutorial/index.html) sintax.
Next we define our quality function. This data is used to define the target and the task. 
The class TestQF takes as arguments the quality function, next are the arguments in order that will be passed to this function. 
The elements of the list can be chosen from:

* 'size_sg' for subgroup size
* parameters listed in fitMeasures(fit)
* parameters listed in parameterEstimates(fit)
* [Wald Test](https://rdrr.io/cran/lavaan/man/lavTestWald.html) scores: 'WT_score', 'WT_p', 'WT_df', 'WT_se'

parameters_type_dic: For all the parameter in parameterEstimates(fit) one has the option of choosing the type ('est' for the value itself, 'z' for the z score, 'pvalue' for the p value).
For example:
```
parameters_type_dic = {direct1:'est', total1:'pvalue'}
```
If parameters_type_dic remains empty the value of the parameter will be taken.
For more information about the options visit the [lavaan website](http://lavaan.ugent.be/tutorial/inspect.html).


## Authors

* **Florian Lemmerich** - *Initial work* - [Pysubgroup](https://github.com/flemmerich/pysubgroup)
* **Christoph Kiefer**
* **Benedikt Langenberg**
* **Jeffry Cacho Aboukhalil**
* **Axel Mayer**
* **Felix Stamm**

## License

Copyright 2016-2020 Florian Lemmerich, Christoph Kiefer, Benedikt Langenberg, Jeffry Cacho Aboukhalil, Axel Mayer, Felix Stamm

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


## Cite

... 

