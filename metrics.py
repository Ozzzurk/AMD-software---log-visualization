import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import datetime


current_date = datetime.datetime.now()
current_datetime = datetime.datetime.now().strftime("%d-%m-%y_%H-%M")


current_directory = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(current_directory + "\\metrics"):
    os.makedirs(current_directory + "\\metrics")
folder_path = current_directory
output_path = current_directory + "\\metrics"
new_directory_path = os.path.join(output_path, current_datetime)
items = os.listdir(folder_path)


# Отфильтруйте только файлы с расширением .csv
csv_files = [f for f in items if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith('.csv') and f.lower().startswith('hardware')]

# Проверка наличия файлов .csv
print("\n--------------------------------Проверка на наличие подходящих файлов-------------------------------")
if csv_files:
    print(f"В текущей папке найдены файлы .csv:")
    for index, file in enumerate(csv_files):
        print(f"{index + 1} - {file}")
    print("--------------------------------------------------------------------------------------------------")
else:
    print(f"В текущей папке нет файлов .csv.")
    sys.exit("Программа завершена по причине отсутствия подходящих файлов для обработки.")


while 1:
    n = int(input("\nВведите номер файла на чтение: "))
    if 0 < n < len(csv_files):
        break
    else:
        print("Вы вышли за пределы массива.")


df = pd.read_csv(csv_files[n-1])
print("\nВы загрузили файл: ", csv_files[n-1])
columns = df.columns

print("\nДоступные графики:")
numeric_columns = df.select_dtypes(include='number').columns.tolist()
available_columns = {i+1: col for i, col in enumerate(numeric_columns)}
for i, col in available_columns.items():
    print(f"{i}. {col}")

selected_columns = input("\nКакие графики строить (выбор числами, через пробел): ")
selected_indices = list(map(int, selected_columns.split()))

for index  in selected_indices:
    if 0 <= index < len(columns):
        column_name = columns[index]
        plt.figure(figsize=(20, 6))
        plt.plot(df.index, df[column_name], label=column_name)

        plt.xlabel('Индекс')
        plt.ylabel('Значения')
        plt.title(column_name)
        plt.legend()
        
        
        if not os.path.exists(new_directory_path):
            os.makedirs(new_directory_path)
            #print(f"Директория {new_directory_path} создана успешно.")
        
            
        save_path = os.path.join(new_directory_path, f"{column_name}_{current_datetime}.jpeg")
        #print(save_path)
        plt.savefig(save_path, format='jpeg')

        plt.close()
        
    else:
        sys.exit("\nПрограмма завершена по причине отсутствия подходящих данных для обработки.")
        
print(f"\nИзображения сохранены в папке {new_directory_path}")
