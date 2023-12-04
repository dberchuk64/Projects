import pandas as pd
import sqlite3 as sq

# Reading from SQLite to dfs
table_name01 = 'Activity'
table_name02 = 'Feature'

conn = sq.connect('{}.sqlite'.format(table_name01))
df01 = pd.read_sql('select * from {}'.format(table_name01), conn)
conn.close()

print(df01)

conn = sq.connect('{}.sqlite'.format(table_name02))
df02 = pd.read_sql('select * from {}'.format(table_name02), conn)
conn.close()

print(df02)


# Writing
base_name = 'Education'
conn = sq.connect('{}.sqlite'.format(base_name))
df01.to_sql(table_name01, conn, if_exists='replace', index=False) # writes to file
df02.to_sql(table_name02, conn, if_exists='replace', index=False) # writes to file
conn.close()


# # Close connection
# conn.close()


