# Extract, Transform and Load .txt
#

import pandas as pd
import sqlite3 as sq


df = pd.read_table('EPM Dataset 2/features.txt', delimiter=' ', header=None, names=['feature_id', 'name'])

# Удаление пробелов в конце строки
df['name'] = df['name'].str.strip()

print(df, '\n')
print(df.dtypes)




# # Удаление пробелов в начале и конце строк
# print(df.dtypes)
#
# # cols = df.columns
# # print(cols)
#
# # for i in cols:
# #     print(i)
# #     df[i] = df[i].str.strip()   # .std - for digits



# #
# # ######### logs.txt #########
# #
#
# df = pd.read_table('EPM Dataset 2/Data/logs.txt', delimiter = '\t', header = 0)
#
# # Шапка
# #
# # naming_convention
# df.columns = df.columns.str.replace(' ', '_')
# df.columns = df.columns.str.lower()
#
# print(df.columns, '\n')
# print(df.dtypes, '\n')
# print(df)



# #
# # ############## SQLite ##############
# #
# base_name = 'Education'
# # table_name = 'logs'
# table_name = 'feature'
#
# conn1 = sq.connect('{}.sqlite'.format(base_name)) # creates file
# df.to_sql(table_name, conn1, if_exists='replace', index=False) # writes to file
# conn1.close() # close connection
#
# print('\n', f"Success - Table '{table_name}' added to DB '{base_name}.sqlite'")

