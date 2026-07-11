import pandas as pd
import sweetviz as sv
df=pd.read_excel(r"D:\ecommerce_sales_data.xlsx")
report = sv.analyze(df)
report.show_html("EDA_Report.html")
