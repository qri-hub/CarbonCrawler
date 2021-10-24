
import fitz
from fitz.fitz import Outline

class PdfParser():

    def __init__(self, word_list, fpath, store_loc) -> None:
        self.word_list = word_list
        self.fpath = fpath
        self.store_loc = store_loc
    
    def parse_and_highlight(self):
        doc = fitz.open(self.fpath)
        page_nb = 0
        pages_to_keep = set()
        for page in doc : 
            for word in self.word_list: 
                searches_results = page.search_for(word, quads=True)
                if len(searches_results) != 0 :
                    pages_to_keep.add(page_nb)
                    page.add_highlight_annot(searches_results)
            for ewd in ['MWh','mwh','GWh','gwh','GJ','TJ','gj','tj']:
                regex_results_energy = page.search_for(ewd, quads=False)
                if len(regex_results_energy) != 0:
                    print(regex_results_energy)
                    for r in regex_results_energy : 
                        page.add_rect_annot(r)
            page_nb+=1
        doc.select(list(pages_to_keep))
        doc.save(self.store_loc+".pdf")
        

        