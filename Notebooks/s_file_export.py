"""
Package documentation:
Function to export compressed panda dataframes to two locations (with preset defaults)
"""

#==== Custom import test
def f_file_test():
    print("package with f_export loaded")

#==== Import custom code
try:
    import s_filepaths
    path_store = s_filepaths.path_store
    path_live = s_filepaths.path_live

except:
    print("Could not import s_filepaths. Reverting to default blank values (current directory).")
    path_store = ""
    path_live = ""

# Export function with compression
def f_df_export(p_df,p_name,p_copy = True, p_loc1 = path_store, p_loc2 = path_live, p_loc1_pre = "store_", p_loc2_pre = "input_",p_compression = "gzip"):
    """This function saves and gzips a file in location 1 and makes a copy in location 2.
    location 1 is intended for storage and has a time stamp (default to path_store)
    location 2 is intended for live use and has a set name (default to path_live)

    both are time gziped

    p_df : pandas dataframe that can be exported to csv
    p_name : name to give to file
    p_copy : Boolean on whether to copy file or not

    p_loc1 : path string (default path_store)
    p_loc2 : path string (default path_live)

    p_loc1_pre : prefix for loc1 file (remember underscore!)
    p_loc2_pre : prefix for loc1 file (remember underscore!)

    p_compression : default gzip

    """

    #=== local package import
    from datetime import datetime
    from shutil import copyfile
    #===

    # set current time and version
    temp_now = datetime.now()
    time_of_export = temp_now.strftime("%Y%m%d_%H%M")
    # Back up repository
    temp_back_up_name = f"{p_loc1}{p_loc1_pre}{p_name}_{time_of_export}.csv"

    # export
    compression_type = p_compression
    temp_compress_name = temp_back_up_name+"."+compression_type
    p_df.to_csv(temp_back_up_name+"."+compression_type,compression = compression_type)
    print(f"Export | {temp_back_up_name} | COMPLETE")
    # copy to live folder
    if p_copy:
        temp_live_name = f"{p_loc2}{p_loc2_pre}{p_name}.csv.{compression_type}"
        copyfile(temp_compress_name,temp_live_name)
        print(f"COPY   | {temp_live_name} | COMPLETE")
    else:
        print(f"COPY   | SKIP")
