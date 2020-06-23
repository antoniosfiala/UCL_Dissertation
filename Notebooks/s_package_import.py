# package library, use to ensure consistency across notebooks, refresh periodically
# general packages
import os # use with os.listdir(_path_)
import requests
import csv
import time
from datetime import datetime
from shutil import copyfile

# data analysis packages
import pandas as pd
pd.options.display.max_columns = None # don't truncate columns
#pd.options.display.max_rows = None

import numpy as np
import matplotlib.pyplot as plt

# custom scripts
import s_file_export
import s_filepaths
import s_un_comtrade_extract as s_un

#=== network analysis
import networkx as nx
#=== gavity modelling
import gme as gme
