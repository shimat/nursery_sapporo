import pandas as pd
import tabula

dfs = tabula.read_pdf(
    "R5ukeireyotesu1124_sasikae_1125_syuryo.pdf", 
    lattice=True, 
    pages="all",
    pandas_options={"header": [0, 1]}
)


for df in dfs:
    ward = df.iloc[:, 0].str.replace("\r", "")[2]
    print(ward)

    upper = df.iloc[0:3, 1:]
    lower = df.iloc[3:, :]
    print(upper)
    print(lower)	
    print(upper.shape)
    print(lower.shape)

    _, upper_cols = upper.shape
    replace_table = {str(i+1):f"C{i}" for i in range(upper_cols)}
    upper = upper.rename(columns=replace_table)
    print(replace_table)
    print(upper)
    
    df = pd.concat([df.iloc[0:2, 1:], df.iloc[2:, :]], axis=0)
    #print(df)
    #df.to_excel(f"{ward}.xlsx", index=None)
    break