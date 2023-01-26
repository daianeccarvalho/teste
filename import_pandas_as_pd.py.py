import pandas as pd
from datetime import datetime
df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
                    index=['row 1', 'row 2'],
                    columns=['col 1', 'col 2'])
df1.to_excel("output.xlsx")  # doctest: +SKIP
df2 = df1.copy()
with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
    hoje = datetime.today()
    df1.to_excel(writer, sheetname= '_base_inconcistencias_propriedades.xlsx')
    df2.to_excel(writer, sheet_name='Sheet_name_2')