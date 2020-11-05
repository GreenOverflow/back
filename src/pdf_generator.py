from pylatex import Document, Tabular, Command, NoEscape
from .data_fetch import indexes, to_api


def generate_pdf(postal_code):
    results = to_api(indexes(postal_code))

    city = results['communeName']

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)

    doc.preamble.append(Command('title', f"{city} fragility score results"))
    doc.preamble.append(Command('author', 'Team 50'))
    doc.append(NoEscape(r'\maketitle'))

    doc.append("The digital fragility index was created to help fight digital exclusion. ")
    doc.append("\n")
    doc.append(
        "It allows you to locate areas where people find it difficult to adjust to changes caused by challenges of digital revolution and set up action plans to provide solutions.")
    doc.append("\n \n")
    with doc.create(Tabular('|c|c|c|c|c|c|c|')) as table:
        table.add_hline()
        table.add_row(('Global score', results['regionName'], results['departementName'], 'Digital access',
                       'Digital access', 'Administrative skills', 'Digital skills'))
        table.add_hline()
        table.add_row(results['global'], results['region'], results['departement'], results['digitalInterfaceAccess'],
                      results['informationAccess'], results['administrativeCompetences'],
                      results['digitalAndScolarCompetences'])
        table.add_hline()

    doc.generate_pdf(f"./report/{postal_code}_stat_report", clean_tex=True, compiler='pdflatex')
