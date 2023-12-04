# Extract, Transform and Load .csv
#
import pandas as pd
import sqlite3 as sq

#
df = pd.read_csv('EPM Dataset 2/Data/intermediate_grades.csv')

print(df)

# Шапка
#
# naming_convention
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.lower()

# Данные
#
# Перевод во float
# Все колонки, кроме ID
for d in df.columns[1:]:
    df[d] = df[d].str.replace(',', '.')
    df[d] = df[d].astype(float)


print(df)
# print(df.dtypes)


# #
# # ############## SQLite ##############
# #
# base_name = 'Education'
# table_name = 'intermediate_grades'
#
# conn1 = sq.connect('{}.sqlite'.format(base_name)) # creates file
# df.to_sql(table_name, conn1, if_exists='replace', index=False) # writes to file
# conn1.close() # close connection
#
# print('\n', f"Success - Table '{table_name}' added to DB '{base_name}.sqlite'")