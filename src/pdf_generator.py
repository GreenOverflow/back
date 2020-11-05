from pylatex import Document, Tabular, Command, NoEscape
 
from data_fetch import indexes, to_api

def generate_pdf(postal_code):
    
    results = to_api(indexes(postal_code))

    city = results['communeName']
    

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)

    doc.preamble.append(Command('title', f"{city}: fragility score results -- Résultats score de fragilité"))
    doc.preamble.append(Command('author', 'Team 50'))
    doc.append(NoEscape(r'\maketitle'))
    
    doc.append("L'indice de fragilité numérique a été créé afin d'aider à contrer les exclusions d'information.")
    doc.append("\n")
    doc.append("Il permet entre autres de localiser les endroits où les personnes trouvent difficile de s'adapter aux changements causés par la révolution de l'information et d'engager des plans d'actions pour apporter des solutions.")
    
    doc.append("\n \n")
    
    doc.append("The digital fragility index was created to help fight digital exclusion. ")
    doc.append("\n")
    doc.append("It allows you to locate areas where people find it difficult to adjust to changes caused by challenges of digital revolution and set up action plans to provide solutions.")
    doc.append("\n \n")
    with doc.create(Tabular('|c|c|c|c|c|c|c|')) as table:
        table.add_hline()
        table.add_row('Global score', results['regionName'], results['departementName'], 'Interface access', 'Digital access', 'Administrative skills', 'Digital skills')
        table.add_row('Score global', '', '', 'Accès interface', 'Accès info.', 'Comp. administration', 'Comp. info.')
        table.add_hline()
        table.add_row(results['global'], results['region'], results['departement'], results['digitalInterfaceAccess'], results['informationAccess'], results['administrativeCompetences'], results['digitalAndScolarCompetences'])
        table.add_hline()
        
    doc.append("\n \n")

    
    if int(results["global"]) > (276 * 0.8):
        doc.append(f"Le score de {city} est vraiment excellent. Cela veut dire que {city} n'a presque pas d'exclusion numérique.")
        doc.append("\n \n")
        doc.append(f"{city} score is very good. That means {city} doesn't have digital exclusion.")

    elif int(results["global"]) > (276 * 0.6):
        doc.append(f"Le score de {city} est bon. Cela veut dire que {city} n'a pas beaucoup d'exclusion numérique.")
        doc.append("\n \n")
        doc.append(f"{city} score is good. That means {city} doesn't have much digital exclusion.")
    
    elif int(results["global"]) > (276 * 0.4):
        doc.append(f"Le score de {city} est moyen. Cela veut dire que {city} a de l'exclusion numérique.")
        doc.append("\n \n")
        doc.append(f"{city} score is average. That means {city} does have some digital exclusion.")
        
    elif int(results["global"]) > (276 * 0.2):
        doc.append(f"Le score de {city} est assez bas. Cela veut dire que {city} a beaucoup d'exclusion numérique.")
        doc.append("\n \n")
        doc.append(f"{city} score is pretty low. That means {city} does have an amount of digital exclusion.")
        
    else:
        doc.append(f"Le score de {city} est très bas. Cela veut dire que {city} a vraiment beaucoup d'exclusion numérique.")
        doc.append("\n \n")
        doc.append(f"{city} score is very low. That means {city} does have a lot of digital exclusion.")
    
    doc.generate_pdf(f"./report/{postal_code}_stat_report", clean_tex=True, compiler='pdflatex')