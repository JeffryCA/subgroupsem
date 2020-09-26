from pysubgroup.measures import AbstractInterestingnessMeasure, \
    BoundedInterestingnessMeasure
import pysubgroup as ps
import numpy as np
from rpy2.robjects import r, pandas2ri
from rpy2 import robjects
from rpy2.robjects.conversion import localconverter
import pandas as pd
from collections import namedtuple
import pkg_resources

class SEMTarget(object):
    """ SEM class object. Initialize by passing a model and and the constraints for the wald test, both in lavaan (R) sintax.
    It is important to use vectors of lenght 2 for the parameters - the first is used for the subgroup, the second for the complement.
    Example:
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
        'direct2 := c2')

        wald_test_contstraints = 'c1==c2'
    """
    def __init__(self, data, model, wald_test_constraints):
        self.filename = pkg_resources.resource_filename('subgroup_sem', 'Calculate_Statistics.R')
        self.data = data
        base_statistics = {} # statistics of Model with all data ? 
        #self.model = model
        #self.wald_test_constraints = wald_test_constraints
        robjects.globalenv['model'] = model
        robjects.globalenv['Wald_Test_contstraints'] = wald_test_constraints
        pass

    def __repr__(self):
        return "T: Structural Equation Model"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        return str(self) < str(other)

    def get_attributes(self):
        return []

    def calculate_statistics(self, subgroup):
        """This function calculates the parameters, madel statistics and wald test scores for a given subgroup.

        Parameters
        ----------
        subgroup : <class 'pysubgroup.subgroup_description.Conjunction'>
            subgroup description; from the results object you can get them with result.to_descriptions()


        Returns
        -------
        statistics dicctionary with keys: ['parameters', 'model_stats', 'wald_test_stats']

        """

        instances, size = ps.get_cover_array_and_size(subgroup, len(self.data), self.data)

        statistics = {}
        statistics['size_sg'] = size

        robjects.globalenv['sg'] = robjects.IntVector(instances)
        r.source(self.filename)
        with localconverter(robjects.default_converter + pandas2ri.converter):
            parameters = robjects.conversion.rpy2py( robjects.r['rval'][0] ).set_index('label')
            model_stats = robjects.conversion.rpy2py( robjects.r['rval'][1].set_index('keyName') ) 
            wald_test_stats = robjects.conversion.rpy2py( robjects.r['rval'][2].set_index('.id') ).rename(index={'.id':'key'}, columns={'X..i..':'value'}).rename(index={'stat':'WT_score', 'p.value':'WT_p', 'df':'WT_df', 'se':'WT_se'})

            wald_test_stats['value'] = pd.to_numeric(wald_test_stats['value'], errors='coerce')

            statistics['parameters'] = parameters
            statistics['model_stats'] = model_stats
            statistics['wald_test_stats'] = wald_test_stats

        return statistics

  

class TestQF(AbstractInterestingnessMeasure):
    """ The class TestQF is used to create a quality function based on parameters gotten from lavaan in R.

    Parameters
    ----------
    ququality_function : callable
        The test qualify function qf().

    parameters_list: list of strings
        Arguments of the quality function in the order given to qf().
        Possible parameters:
            'size_sg' for subgroup size
            parameters listed in the lavaan function fitMeasures(fit); visit the lavaan website for more info
            parameters listed in parameterEstimates(fit); visit the lavaan website for more info
            Wald Test scores: 'WT_score', 'WT_p', 'WT_df', 'WT_se', checkout the lavaan function lavTestWald for more info


    parameters_type_dic : dic
        Diccionary that maps model parameters included in parameters list 
        to all the possible values one can extract from parameterEstimates(fit).
        If a parameter is in parameters_list but not in the dictionry,
        the value of a parameter 'est' is taken as default.
        Default = {}
    """

    tpl = namedtuple('TestQF_parameters', ('parameters', 'model_stats', 'wald_test_stats'))

    def __init__(self, quality_function, parameters_list, parameters_type_dic = {}):
        self.quality_function =  quality_function
        self.parameters_list =  parameters_list
        self.parameters_type_dic = parameters_type_dic
        self.has_constant_statistics = True
        self.required_stat_attrs = ('parameters', 'model_stats', 'wald_test_stats')
        
    def calculate_constant_statistics(self, task_data, task_target):
        with localconverter(robjects.default_converter + pandas2ri.converter): 
            robjects.globalenv['d'] = robjects.conversion.py2rpy(task_data)
        self.data = task_data
        self.filename = task_target.filename


    def evaluate(self, subgroup, target, data, statistics=None):
        statistics = self.ensure_statistics(subgroup, target, data, statistics)

        if len(statistics.wald_test_stats) == 1:
            print(subgroup, -1)
            return -1

        print(subgroup)
        return self.choose(subgroup, statistics)

    def calculate_statistics(self, subgroup, target, data, statistics=None):
        if 'nan' in str(subgroup):
            return TestQF.tpl([-1], [-1], [-1])

        instances, size = ps.get_cover_array_and_size(subgroup, len(data), data)

        if (size < 10):
            return TestQF.tpl([-1], [-1], [-1])

        try:
            if instances == slice(None, None, None):
                print('Warning')
                instances = np.ones(size)
        except:
            pass
        
        robjects.globalenv['sg'] = robjects.IntVector(instances)
        r.source(self.filename)
        with localconverter(robjects.default_converter + pandas2ri.converter):
            if len(robjects.r['rval']) == 1:
                return TestQF.tpl([-1], [-1], [-1])

            parameters = robjects.conversion.rpy2py( robjects.r['rval'][0] ).set_index('label')
            model_stats = robjects.conversion.rpy2py( robjects.r['rval'][1].set_index('keyName') ) 
            wald_test_stats = robjects.conversion.rpy2py( robjects.r['rval'][2].set_index('.id') ).rename(index={'.id':'key'}, columns={'X..i..':'value'}).rename(index={'stat':'WT_score', 'p.value':'WT_p', 'df':'WT_df', 'se':'WT_se'})

        return TestQF.tpl(parameters, model_stats, wald_test_stats)

    def choose(self, subgroup, statistics):
        dic_results = {}
        try:
        	dic_parameters = statistics._asdict()['parameters'].drop('').to_dict('index')
        except KeyError:
        	dic_parameters = statistics._asdict()['parameters'].to_dict('index')
        dic_model_stats = statistics._asdict()['model_stats'].to_dict()['value']
        dic_wald_test_stats = statistics._asdict()['wald_test_stats'].to_dict()['value']

        dic_results.update(dic_parameters)
        dic_results.update(dic_model_stats)
        dic_results.update(dic_wald_test_stats)

        args = []
        for key in self.parameters_list:
            if key == 'size_sg':
                instances, size = ps.get_cover_array_and_size(subgroup, len(self.data), self.data)
                args.append(size)
            elif key in dic_parameters.keys():
                if len(self.parameters_type_dic) == 0:
                    args.append(float(dic_results[key]['est']))
                else:
                    args.append(float(dic_results[key][self.parameters_type_dic[key]]))
            else:
                args.append(float(dic_results[key]))

        return self.quality_function(*args)


    def is_applicable(self, subgroup):
        return isinstance(subgroup.target, SEMTarget)

    def supports_weights(self):
        return False


