import pandas as pd
from openpyxl import load_workbook
from googletrans import Translator

translator = Translator()

# Define filepath
filepath = 'codelijst.xlsx'

# Load Excel file using Pandas
f = pd.ExcelFile(filepath)

# Define an empty list to store individual DataFrames
list_of_dfs = []
list_of_sheets = []

# Iterate through each worksheet
for sheet in f.sheet_names:
    # Parse data from each worksheet as a Pandas DataFrame
    df = f.parse(sheet)

    # And append it to the list
    list_of_dfs.append(df)
    list_of_sheets.append(sheet)

# Initialize the text for the .ttl file
ttl_text = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
ttl_text = ttl_text + "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema> .\n"
ttl_text = ttl_text + "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n"

languages = ['en', 'fr', 'de']  # Example languages

# Process each sheet
for i in range(len(list_of_sheets)):
    sheet = list_of_sheets[i]
    df = list_of_dfs[i]
    
    ttl_text = ttl_text + "<https://data.vlaanderen.be/id/conceptscheme/" + \
        str(df["Klasse"][0]).replace(" ", "_") + "> a skos:ConceptScheme ;\n"
    ttl_text = ttl_text + "<https://www.w3.org/ns/adms#status> <https://data.vlaanderen.be/id/concept/Status/ingebruik> ;\n"
    
    for language in languages:
        ttl_text = ttl_text + 'skos:definition "' + \
            translator.translate(str(df["Definitie"][0]), dest=language).text + '"@' + language + ' ;\n'
        ttl_text = ttl_text + 'skos:prefLabel "' + \
            translator.translate(str(df["Label"][0]), dest=language).text + '"@' + language + ' ;\n'

    if 'subklassevan' in df.columns:
        ttl_text = ttl_text + 'rdfs:subClassOf <https://data.vlaanderen.be/id/concept/' + \
            str(df["subklassevan"][0]) + '> ;\n'

    ttl_text = ttl_text + 'skos:prefLabel "' + str(df["Label"][0]) + '"@nl ;\n'
    ttl_text = ttl_text + 'skos:definition "' + str(df["Definitie"][0]) + '"@nl .\n\n'

    for j in range(1, len(df)):
        if pd.isna(df["Klasse"][j]):
            continue

        ttl_text = ttl_text + "<https://data.vlaanderen.be/id/concept/" + str(df["Klasse"][0]).replace(" ", "_") + "/" + \
            str(df["Klasse"][j]).replace(' ', '_') + "> a skos:Concept ;\n"
        ttl_text = ttl_text + "<https://www.w3.org/ns/adms#status> <https://wegenenverkeer.data.vlaanderen.be/id/concept/DWMStatus/" + str(df["Status"][j]) + "> ;\n"
        ttl_text = ttl_text + 'skos:definition "' + str(df["Definitie"][j]) + '"@nl ;\n'
        ttl_text = ttl_text + 'skos:inscheme <https://data.vlaanderen.be/id/conceptscheme/' + str(df["Klasse"][0]).replace(" ", "_") + '> ;\n'
        ttl_text = ttl_text + 'skos:notation "' + str(df["Notation"][j]) + '" ;\n'
        ttl_text = ttl_text + 'skos:prefLabel "' + str(df["Label"][j]) + '"@nl ;\n'

        for language in languages:
            ttl_text = ttl_text + 'skos:definition "' + translator.translate(str(df["Definitie"][j]), dest=language).text + '"@' + language + ' ;\n'
            ttl_text = ttl_text + 'skos:prefLabel "' + translator.translate(str(df["Label"][j]), dest=language).text + '"@' + language + ' ;\n'

        if 'subklassevan' in df.columns:
            ttl_text = ttl_text + 'rdfs:subClassOf <https://data.vlaanderen.be/id/concept/' + str(df["subklassevan"][j]) + '> ;\n'

        ttl_text = ttl_text + 'skos:topConceptOf <https://data.vlaanderen.be/id/conceptscheme/' + str(df["Klasse"][0]).replace(" ", "_") + '> .\n\n'

# Save the combined text to a .ttl file
with open('combined_output.ttl', 'w') as f:
    f.write(ttl_text)

print("Processing completed and saved to combined_output.ttl")
