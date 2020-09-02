import pkg_resources
from io import StringIO
import pandas as pd

def get_artificial_data():
    data = pd.read_csv(pkg_resources.resource_filename('subgroup_sem', 'data/artificial_data.csv'))
    return data
