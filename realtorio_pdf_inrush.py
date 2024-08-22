import numpy as np
from engineering_notation import EngNumber
from docxtpl import DocxTemplate, InlineImage
import datetime as dt
from docx2pdf import convert

#dt.datetime.now().strftime("%d-%b-%Y")
# create a document object
docx = DocxTemplate("Inrush_template_word2.docx")


context = {
    "Correntes_figura": str(EngNumber(i_pico_inical)),
    "corrente_pico": str(EngNumber(i_pico_inical)),
    "frequencia_oscilacao": str(EngNumber(omega/(2*np.pi))),
    "inrush_inominal": str(i_pico_inical/(I_fn[0]*np.sqrt(2)))
}
docx.render(context)
docx.save('Relatorio_Inrush_DAX.docx')

# convert word file to a pdf file
# convert('Relatorio_Inrush_DAX.docx', 'Relatorio_Inrush_DAX.pdf')