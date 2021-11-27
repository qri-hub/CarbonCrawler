from os import listdir
from os.path import isfile, join
import shutil
import fitz
from fitz.fitz import Outline

class PdfParser():

    def __init__(self, word_list, fpath, store_loc, fname) -> None:
        self.word_list = word_list
        self.fpath = fpath
        self.store_loc = store_loc
        self.fname=fname

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
                        page.add_circle_annot(r)
            page_nb+=1
        doc.select(list(pages_to_keep))
        doc.save(self.store_loc+self.fname+"_parsed.pdf")


def word_list(fname):
    word_list = []
    with open(fname, 'r') as f:
        for line in f:
            word_list += line.split(',')
    return word_list

def main():
    mpath = 'C:\\Users\\Quense\\Documents\\CarbonCrawler\\pool\\'
    rpath = 'C:\\Users\\Quense\\Documents\\CarbonCrawler\\results_pool\\'
    spath = 'C:\\Users\\Quense\\Documents\\CarbonCrawler\\processed\\'
    annual_word_path = 'C:\\Users\\Quense\\Documents\\CarbonCrawler\\word_list_annual.txt'
    sustain_word_path = 'C:\\Users\\Quense\\Documents\\CarbonCrawler\\word_list_report.txt'
    word_list_annual = word_list(annual_word_path)
    word_list_sustain = word_list(sustain_word_path)

    list_files = [f for f in listdir(mpath) if isfile(join(mpath, f))]
    for f in list_files:
        if 'sustain' in f:
            print('Sustain : {}'.format(f))
            parser = PdfParser(word_list=word_list_sustain, fpath=mpath+f, store_loc=rpath, fname=f)
            parser.parse_and_highlight()
        elif 'annual' in f:
            print('Annual : {}'.format(f))
            parser = PdfParser(word_list=word_list_annual, fpath=mpath+f, store_loc=rpath, fname=f)
            parser.parse_and_highlight()
        shutil.move(mpath+f, 'C:\\Users\\Quense\\Documents\\CarbonCrawler\\processed\\'+f)

if __name__ == '__main__':
    main()