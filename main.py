from utils.openml_data_loader import download_and_save


# download_and_save(save_path="data/raw",suite_id_or_name ="OpenML-CC18" )

with open("openmlcc18_tasks.txt","r") as file:
    dataset_id_list = [int(num) for num in file.read().split()]
    
print(dataset_id_list)

for d_id in dataset_id_list:
    download_and_save(save_path=r"data\raw", dataset_name_or_id = d_id)