# subgroup_sem_ISMIS

In statistics, mediation models aim to identify and explain the direct and indirect effects of an independent variable on a dependent variable. 
In heterogeneous data, the observed effects might vary for parts of the data. 
In this [paper](...), we develop an approach for identifying interpretable data subgroups that induce exceptionally different effects in a mediation model. 
For that purpose, we introduce mediation models as a novel model class for the exceptional model mining framework,
introduce suitable interestingness measures for several subtasks, and demonstrate the benefits of our approach on synthetic and empirical datasets.

In this repository is the code used for the analysis in the papaer.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for reproducibility and testing purposes.

### Prerequisites

* [R(>= 3.4)](https://cran.r-project.org/mirrors.html)
* Python3

Ideally one should have a  package to create a virtual environments. We recommend having [Virtualenv](https://virtualenv.pypa.io/en/stable/) 
and the R package [packrat](https://rstudio.github.io/packrat/).

### Installing
First clone the repository
```
git clone https://github.com/JeffryCA/subgroupsem.git --recursive
```

Install R packages:
Optional first step in the directory of your project: 

```
install.packages('packrat')
packrat::init()
```
This should install all the needed R packages and create a folder with a local R library for the project. If there is some problem installing some R package, try to install them separatly first.
Alternatively install:

```
install.packages('lavaan')
install.packages('plyr')
install.packages('essurvey')
install.packages('tidyverse')
install.packages('rjson')
```

Install subgroup_sem:
Optional first step in the directory of your project:

```
Virtualenv env
source env/bin/activate
```

Second step, installing pysubgroup and subgroup_sem:

```
# in the directry of the cloned repositry
pip install -e pysubgroup
pip install -e .
```

If it doesn't work because of trouble installing [rpy2](https://rpy2.github.io/), try to install that package first

```
pip install rpy2 # for MacOS check https://stackoverflow.com/questions/52361732/installing-rpy2-on-macos
```

## Running the examples
The examples are stored in the folder Examples.
To run the exapmle with the artficial data set run commands in the corresponding folder

```
Rscript Generate_Data.R
```

to create the data and

```
python3 Mediator_subgroup_discovery.py
```
to run the example.

To run the example with the European Social Survey data one first needs to make an account to be able to download the dataset. For that please visit the website [download ESS data](https://www.europeansocialsurvey.org/user/new).
After create a file in your terminal

```
vim config.json
```

and write in it:
```
{ "mail": "<your mail from ESS account>" }
```
After that you can run

```
Rscript ess_data.R
```

to download the necessary data, and finally

```
python3 ESS_subgroup_discovery.py
```

to run the subgroup discovery task.

## Authors of the paper

* **Florian Lemmerich** - *Initial work* - [Pysubgroup](https://github.com/flemmerich/pysubgroup)
* **Christoph Kiefer**
* **Benedikt Langenberg**
* **Jeffry Cacho Aboukhalil**
* **Axel Mayer**

## License

... 

## Cite


