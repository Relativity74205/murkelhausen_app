import tabula
path = "../Kontoauszug_724197900_20220430.pdf"

df = tabula.read_pdf(
    path,
    pages='all',
    guess=False,
    area=[275, 57, 791, 573],
    columns=[55, 65, 90],
    relative_columns=True,
)
