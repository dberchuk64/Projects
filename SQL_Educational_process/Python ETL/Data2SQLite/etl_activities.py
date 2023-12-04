import pandas as pd

df = pd.read_table('EPM Dataset 2/activities.txt', delimiter = ' ', header = None, names = ['activity_id', 'activity', 'A', 'B', 'C', 'D', 'E'])

# NaN clearing
df = df.fillna('')

# df['New'] = df['Activity'] + ' ' + df['A'] + ' ' + df['B'] + ' ' + df['C'] + ' ' + df['D'] + ' ' + df['E'] # Конкатенация с NaN даёт NaN

# df['New'] = ''
# df['New'] = df['New'] + df['D']

# con_cols = ['activity', 'A', 'B', 'C', 'D', 'E']
con_cols = df.columns[1:]
df['New'] = ''
for i in con_cols:
    # print(i)
    df['New'] = df['New'] + ' ' + df[i]

# # Удаление пробелов в конце строки
df['New'] = df['New'].str.strip()

# Удаление лишних столбцов
df = df.drop(columns = con_cols, axis = 1)

# Rename - Возврат исходного имени столбца
df = df.rename(columns = {'New': con_cols[0]})

# # Удаление пробелов в конце строки
# df['Activity'] = df['Activity'].str.strip()


# cols = ['A', 'B', 'C', 'D']
# df['New'] = df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis = 1)



print(df, '\n')
print(df.dtypes)

# df2 = df.fillna('')
# print(df2)




#
# ############## SQLite ##############
# 
import sqlite3 as sq

# table_name = 'activity'

# # Writing to SQLite from df
# conn1 = sq.connect('{}.sqlite'.format(table_name)) # creates file
# df.to_sql(table_name, conn1, if_exists='replace', index=False) # writes to file
# conn1.close() # good practice: close connection

# # Reading from SQLite to df
# conn = sq.connect('{}.sqlite'.format(table_name))
# df4 = pd.read_sql('select * from {}'.format(table_name), conn)
# conn.close()
#
# print(df4)


# #
# # ############## SQLite ##############
# #
# base_name = 'Education'
# # table_name = 'logs'
# table_name = 'activity'
#
# conn1 = sq.connect('{}.sqlite'.format(base_name)) # creates file
# df.to_sql(table_name, conn1, if_exists='replace', index=False) # writes to file
# conn1.close() # close connection
#
# print('\n', f"Success - Table '{table_name}' added to DB '{base_name}.sqlite'")