# Extract, Transform and Load .csv
#
import pandas as pd
import sqlite3 as sq

df = pd.read_csv('EPM Dataset 2/Data/final_grades_first.csv')
# df = pd.read_csv('EPM Dataset 2/Data/final_grades_second.csv')

print(df)
print(df.columns)

# Шапка
#
# Замена \n на пробел, два пробела на один
df.columns = df.columns.str.replace('\n', ' ')
df.columns = df.columns.str.replace('  ', ' ')

# naming_convention
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.replace('.', '_')
df.columns = df.columns.str.lower()


# Данные
#
# Перевод во float
# Все колонки, кроме ID
for d in df.columns[1:]:
    df[d] = df[d].str.replace(',', '.')
    df[d] = df[d].astype(float)


print(df)
print(df.columns)
print(df.dtypes)

# #
# # ############## SQLite ##############
# #
# base_name = 'Education'
# table_name = 'final_grades_first'
# # table_name = 'final_grades_second'
#
# conn1 = sq.connect('{}.sqlite'.format(base_name)) # creates file
# df.to_sql(table_name, conn1, if_exists='replace', index=False) # writes to file
# conn1.close() # good practice: close connection
#
# print('\n', f"Success - Table '{table_name}.csv' added to DB '{base_name}.sqlite'")