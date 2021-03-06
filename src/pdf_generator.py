from pylatex import Document, Tabular, Command, NoEscape, Section, VerticalSpace
 
from data_fetch import indexes, to_api

def generate_pdf(postal_code):
    BREAK_LINE = "\n \n \n"

    results = to_api(indexes(postal_code))

    city = results['communeName']
    

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm", "rmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)

    doc.preamble.append(Command('title', f"{city} - {postal_code}"))
    doc.preamble.append(Command('author', 'Team 50'))
    doc.append(NoEscape(r'\maketitle'))
    
    doc.append(VerticalSpace("25pt"))
    with doc.create(Section("RÉSULTATS SCORE DE FRAGILITÉ", numbering=False)):
        doc.append("L'indice de fragilité numérique a été créé afin d'aider à contrer les exclusions d'information.")
        doc.append("\n")
        doc.append("Il permet entre autres de localiser les endroits où les personnes trouvent difficile de s'adapter aux changements causés par la révolution de l'information et d'engager des plans d'actions pour apporter des solutions.")
        doc.append(BREAK_LINE)
        
        with doc.create(Tabular('|c|c|c|c|c|c|c|')) as table:
            table.add_hline()
            table.add_row('Score global', results['regionName'], results['departementName'], 'Accès interface', 'Accès info.', 'Comp. administration', 'Comp. info.')
            table.add_hline()
            table.add_row(results['global'], results['region'], results['departement'], results['digitalInterfaceAccess'], results['informationAccess'], results['administrativeCompetences'], results['digitalAndScolarCompetences'])
            table.add_hline()
        doc.append(BREAK_LINE)
            
        if int(results["global"]) > (276 * 0.8):
            doc.append(f"Le score de {city} est vraiment excellent. Cela veut dire que {city} n'a presque pas d'exclusion numérique.")
        elif int(results["global"]) > (276 * 0.6):
            doc.append(f"Le score de {city} est bon. Cela veut dire que {city} n'a pas beaucoup d'exclusion numérique.")
        elif int(results["global"]) > (276 * 0.4):
            doc.append(f"Le score de {city} est moyen. Cela veut dire que {city} a de l'exclusion numérique.")   
        elif int(results["global"]) > (276 * 0.2):
            doc.append(f"Le score de {city} est assez bas. Cela veut dire que {city} a beaucoup d'exclusion numérique.") 
        else:
            doc.append(f"Le score de {city} est très bas. Cela veut dire que {city} a vraiment beaucoup d'exclusion numérique.")
    
        doc.append(BREAK_LINE + BREAK_LINE)
    
    with doc.create(Section("FRAGILITY SCORE RESULTS", numbering=False)):
        doc.append("The digital fragility index was created to help fight digital exclusion.")
        doc.append("\n")
        doc.append("It allows you to locate areas where people find it difficult to adjust to changes caused by challenges of digital revolution and set up action plans to provide solutions.")
        doc.append(BREAK_LINE)
        
        with doc.create(Tabular('|c|c|c|c|c|c|c|')) as table:
            table.add_hline()
            table.add_row('Global score', results['regionName'], results['departementName'], 'Interface access', 'Digital access', 'Administrative skills', 'Digital skills')
            table.add_hline()
            table.add_row(results['global'], results['region'], results['departement'], results['digitalInterfaceAccess'], results['informationAccess'], results['administrativeCompetences'], results['digitalAndScolarCompetences'])
            table.add_hline()
        doc.append(BREAK_LINE)
        
        if int(results["global"]) > (276 * 0.8):
            doc.append(f"{city} score is very good. That means {city} doesn't have digital exclusion.")
        elif int(results["global"]) > (276 * 0.6):
            doc.append(f"{city} score is good. That means {city} doesn't have much digital exclusion.")
        elif int(results["global"]) > (276 * 0.4):
            doc.append(f"{city} score is average. That means {city} does have a few of digital exclusion.") 
        elif int(results["global"]) > (276 * 0.2):
            doc.append(f"{city} score is pretty low. That means {city} does have some digital exclusion.")
        else:
            doc.append(f"{city} score is very low. That means {city} does have a lot of digital exclusion.")
            
    doc.generate_pdf(f"./report/{postal_code}_stat_report", clean_tex=True, compiler='pdflatex')

