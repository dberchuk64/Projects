# import sqlite3 as sq
#
# # Connection to data base
# base_name = 'Education'
# conn = sq.connect('{}.sqlite'.format(base_name))
#
#
# # !!!!!!!!!!!!!! drop table !!!!!!!!!!!!!!
# # conn.execute("DROP TABLE intermediate_grades")
# # conn.execute("DROP TABLE final_grades_second")
# conn.execute("DROP TABLE processes")
#
# conn.close()
#
# print('Data dropped successfully')