# Extract, Transform and Load from 'Data/Processes'
#
import pandas as pd
import sqlite3 as sq
import os

from etl_func import dt_normalize_list

def df2sql(data_frame, base_name: str, table_name: str):
    # Запись df в базу SQLite

    conn1 = sq.connect('{}.sqlite'.format(base_name)) # creates file
    data_frame.to_sql(table_name, conn1, if_exists='append', index=False) # writes to file
    conn1.close() # close connection

    return print('\n', f"Success - Table '{table_name}' added to DB '{base_name}.sqlite'")



# print(os.listdir('EPM Dataset 2/Data/Processes'))

work_dir = 'EPM Dataset 2/Data/Processes'
fd_1 = os.listdir(work_dir)                 # f - files & folders

print(fd_1)
print(os.listdir(work_dir + '/' + fd_1[0]), '\n')

fd_2 = os.listdir(work_dir + '/' + fd_1[0])[0]
print(fd_2)
print('fd_1[0]', fd_1[0])

read_header = ['session', 'student_id', 'exercise', 'activity', 'start_time', 'end_time', 'idle_time', 'mouse_wheel', 'mouse_wheel_click', 'mouse_click_left', 'mouse_click_right', 'mouse_movement', 'keystroke']
i = 0
for d in fd_1:
    print('i', i, '| d', d)
    fd_2 = os.listdir(work_dir + '/' + fd_1[i])
    print(fd_1[i], f'files: {len(fd_2)}', fd_2, '\n')

    for f in fd_2:
        read_dir = work_dir + "/" + d + "/" + f
        print('\n', 'read_dir', read_dir)

        # Чтение таблицы
        df = pd.read_table(read_dir, delimiter=',', header=None, names=read_header)

        # Очистка time от пробелов
        df['start_time'] = df['start_time'].str.strip()
        df['end_time'] = df['end_time'].str.strip()

        # Формат даты и времени
        df['start_time'] = dt_normalize_list(df['start_time'])
        df['end_time'] = dt_normalize_list(df['end_time'])

        # Запись в базу
        # df2sql(df, 'Education', 'processes')

    i += 1

print('\n')
print(df.head(n=10).to_string(index=False))

# #
# # ETL
# #
#
#
# # th =
# read_dir = work_dir + "/" + fd_1[0] + "/" + fd_2[0]
# print(read_dir)
#
# accd = fd_1[0].lower().replace(' ', '_')
# # print('accd', accd, '\n')
#
# read_header = [accd, 'student_id', 'exercise', 'activity', 'start_time', 'end_time', 'idle_time', 'mouse_wheel', 'mouse_wheel_click', 'mouse_click_left', 'mouse_click_right', 'mouse_movement', 'keystroke']
# print('read_header', read_header, '\n')
# # df = pd.read_table(read_dir, delimiter = ',', header = None, names = ['activity_id', 'activity', 'A', 'B', 'C', 'D', 'E'])
# df = pd.read_table(read_dir, delimiter = ',', header = None, names = read_header)
#
# print(df)
# print(type(df))
# print(df.loc[[-1]])



# #
# # ############## SQLite ##############
# #
# base_name = 'Education'
# table_name = 'processes_1'
#
# conn1 = sq.connect('{}.sqlite'.format(base_name)) # creates file
# df.to_sql(table_name, conn1, if_exists='replace', index=False) # writes to file
# conn1.close() # close connection
#
# print('\n', f"Success - Table '{table_name}' added to DB '{base_name}.sqlite'")

