import eng_to_sinhala as es
import pandas as pd
import pickle
import importlib
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("data_save_file", type=str, default="")
parser.add_argument("failures_save_file", type=str, default="")
parser.add_argument("--start_idx", type=int, default=0)
parser.add_argument("--end_idx", type=int, default=0)
args = parser.parse_args()

# Change filename here
data = pd.read_csv('failure_data.csv')

es.setup()

es.bulk_translate(data[args.start_idx:args.end_idx], args.data_save_file, args.failures_save_file)