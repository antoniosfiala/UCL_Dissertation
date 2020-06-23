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
import numpy as np
import matplotlib.pyplot as plt

# custom scripts
import s_file_export
import s_filepaths

#=== network analysis
import networkx as nx
