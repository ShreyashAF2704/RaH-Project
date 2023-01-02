import tabula
import pandas as pd

df = tabula.read_pdf(r"C:\Users\Sahil\Documents\Shreyash_files\Projects\Amberflux RaH Project\DTCScraper\MC-10184330-0001.pdf", pages='all')
for i in range(len(df)):
    print(df[i])