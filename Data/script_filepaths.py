# This script allows one to load and correct raw files before saving them again.
file_path_0_raw       = "./0_raw/"
file_path_1_backup    = "./1_raw_processed_backup/"
file_path_2_input     = "./2_raw_processed_input/"
file_path_3_generated = "./3_generated_inputs/"

from datetime import datetime
from shutil import copyfile

# Custom import test
def f_file_test():
    print("Funciton package loaded")

# Export function with compression
def f_export(p_df,p_name):

    global file_path_1_backup,file_path_2_input

    # set current time and version
    temp_now = datetime.now()
    time_of_export = temp_now.strftime("%Y%m%d_%H%M")
    # Back up repository
    temp_back_up_name = f"{file_path_1_backup}store_{p_name}_{time_of_export}.csv"
    # export
    compression_type = "gzip"
    temp_compress_name = temp_back_up_name+"."+compression_type
    p_df.to_csv(temp_back_up_name+"."+compression_type,compression = compression_type)
    # copy to live folder
    temp_live_name = f"{file_path_2_input}input_{p_name}.csv.{compression_type}"
    copyfile(temp_compress_name,temp_live_name)
