from setuptools import setup, find_packages

setup(
    name='subgroupsem',
    version='0.0.1',
    packages=find_packages(),
#    package_dir={'subgroup_sem': 'subgroup_sem', 'subgroup_sem.tests': "subgroup_sem.tests"},
    package_data={'subgroup_sem': ['data/artificial_data.csv', 'Calculate_Statistics.R', 'Examples/Artficial Mediator/Generate_Data.R',
                'Examples/European Social Survey/ess_data.R']},
    url='na',
    license='',
    author='',
    author_email='',
    description='subgroup_sem is a Python library to combine Subgroup Discovery with Structural Equation Modelling.',
    install_requires=[
              'pandas', 'scipy', 'numpy', 'matplotlib', 'rpy2', 'tzlocal'
          ],
    python_requires='>=3.6',
    include_package_data=True
)
