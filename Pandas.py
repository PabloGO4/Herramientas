import pandas as pd

class Pandas:

    @staticmethod
    def exportDictToExcel(dictionary, excelPath):
        df = pd.DataFrame.from_dict(dictionary)
        df.to_excel(excelPath)