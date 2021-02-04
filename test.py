import pandas as pd
import sys

table_1 = "사이즈/n어깨넓이/n가슴둘레/n소매길이/n전체길이"
table_2 = "95/n42.9/n99/n61/n71"
table_3 = "97/n43.6/n101.5/n61.5/n72"
table_4 = "100/n44.4/n104/n62.5/n73"

list_1 = table_1.split("/n")
list_2 = table_2.split("/n")
list_3 = table_3.split("/n")
list_4 = table_4.split("/n")

list_b = [list_1, list_2, list_3, list_4]

list_1_a = [list_1[0], list_2[0], list_3[0], list_4[0]]
list_2_a = [list_1[1], list_2[1], list_3[1], list_4[1]]
list_3_a = [list_1[2], list_2[2], list_3[2], list_4[2]]
list_4_a = [list_1[3], list_2[3], list_3[3], list_4[3]]

list_a = [list_1_a, list_2_a, list_3_a, list_4_a]

for i in list_a:
    print(i)

for i in list_b:
    print(i)