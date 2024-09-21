import codecs

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import (LAParams, LTChar, LTFigure, LTLine, LTTextBox,
                             LTTextLine)
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import TextConverter
from io import StringIO

class PdfDocument(object):

    class _BoxText:
        def __init__(self, x0, y0, x1, y1, text):
            self._x0 = x0;
            self._y0 = y0;
            self._x1 = x1;
            self._y1 = y1;
            self._text = text

    @staticmethod
    def __extractBoxTextFromLayout(layout, listBoxText):

        for objLayout in layout:
            if isinstance(objLayout, LTTextBox) or isinstance(objLayout, LTTextLine):
                textBox = objLayout.get_text()
                boxText = PdfDocument._BoxText(objLayout.x0, objLayout.y0, objLayout.x1, objLayout.y1, textBox)
                listBoxText.append(boxText)
            elif isinstance(objLayout, LTFigure):
                line = ''
                previousLine = ''
                for element in objLayout:
                    if isinstance(element, LTChar):
                        if not previousLine or element.y0 == previousLine:
                            line = line + element.get_text()
                        else:
                            boxText = PdfDocument._BoxText(element.x0, element.y0, element.x1, element.y1, line)
                            listBoxText.append(boxText)
                            line = ''
                            line = line + element.get_text()
                        previousLine = element.y0


    @staticmethod
    def __extractTextBoxs(nameFilePdf):

        listBoxText = []

        fp = open(nameFilePdf, "rb")
        
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        
        parser = PDFParser(fp)        
        document = PDFDocument(parser)

        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            PdfDocument.__extractBoxTextFromLayout(layout, listBoxText)

        fp.close()
        
        return listBoxText

    def __init__(self, nameFilePdf):
        
        self._listBoxText = PdfDocument.__extractTextBoxs(nameFilePdf)
        self._contentPdf = PdfDocument.__extractTextFromPdf(nameFilePdf)

    def exportFileText(self, nameFileText):
        
        file = codecs.open(nameFileText, "w", "utf-8")
        
        for box in self._listBoxText:
            strBox = "[{},{},{},{}] = {}\n".format(box._x0, box._y0, box._x1, box._y1, box._text)
            file.write(strBox)
            
        file.close()

    
    def __extractTextFromPdf(pdf_path, num_pages=2):
        # Crear un objeto StringIO para almacenar el texto extraído
        output_string = StringIO()
        with open(pdf_path, 'rb') as fh:
            # Crear un objeto PDFResourceManager
            resource_manager = PDFResourceManager()
            # Crear un objeto StringIO para almacenar el texto extraído
            converter = TextConverter(resource_manager, output_string, laparams=LAParams())
            # Crear un objeto PDFPageInterpreter
            interpreter = PDFPageInterpreter(resource_manager, converter)
            # Iterar sobre las páginas del PDF
            for page_num, page in enumerate(PDFPage.get_pages(fh, caching=True, check_extractable=True)):
                if page_num >= num_pages:
                    break
                    # Interpeta la página
                interpreter.process_page(page)
        # Obtener el texto extraído del objeto StringIO
        return output_string.getvalue()    