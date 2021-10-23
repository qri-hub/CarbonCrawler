
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
                rl = page.search_for(word, quads=True)
                if len(rl) != 0 :
                    pages_to_keep.add(page_nb)
                    page.add_squiggly_annot(rl)
            page_nb+=1
        doc.select(list(pages_to_keep))
        doc.save(self.store_loc+".pdf")
        

        