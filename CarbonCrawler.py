from subprocess import call
import dearpygui.dearpygui as dpg
import os 
import modules.crawler as crawler
import modules.pdfparser as pdfparser
global word_list, report_name
word_list = []
report_name = ''

def crawl_website(sender, app_data):
    print(f'sender is : {sender}')
    print(f'data is : {app_data}')
    urls = dpg.get_value(item='website')
    crl = crawler.Crawler(urls, dpg.get_value(item="result_folder_tag"))
    crl.start_requests()
    #crl.process_results()
    print(urls)
    print('Done')

def crawl_report(sender, data):
    dpg.set_value(item='status_tag', value='PARSING FILE, this might take a while')#, color=[191,108,0])
    parser = pdfparser.PdfParser(word_list, fpath=dpg.get_value(item='report_name_tag'), store_loc=dpg.get_value(item='result_folder_tag'), fname=report_name)
    parser.parse_and_highlight()
    print('Done Parsing pdf')
    dpg.set_value(item='status_tag', value="I'm DONE !")#, color=[0,181,6])
    
def file_selection(sender, app_data):
    file = list(app_data['selections'].keys())[0]
    fname = app_data['selections'][file]
    print(fname)
    global word_list
    word_list = []
    with open(fname, 'r') as f:
        for line in f:
            word_list += line.split(',')
    dpg.set_value(item="word_list_tag", value="The words I'll be looking for are the following:\n"+str(word_list))
    
def folder_selection(sender, app_data):
    file = list(app_data['selections'].keys())[0]
    fname = app_data['selections'][file][:-len(file)]
    dpg.set_value(item="result_folder_tag", value=str(fname))

def report_selection(sender, app_data):
    print("Sender: ", sender)
    file = list(app_data['selections'].keys())[0]
    fname = app_data['selections'][file]
    global report_name 
    report_name = file
    dpg.set_value(item="report_name_tag", value=str(fname))


dpg.create_context()
#Select word list
with dpg.file_dialog(directory_selector=False,  width=100, height=200, file_count=8, show=False, tag="file_dialog_tag", modal=True, callback=file_selection):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    dpg.add_file_extension(".txt", color=(255, 255, 0, 255))

with dpg.file_dialog(directory_selector=True,  width=100, height=200, file_count=8, show=False, tag="folder_dialog_tag", modal=True, callback=folder_selection):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(150, 255, 150, 255))

with dpg.file_dialog(directory_selector=False,  width=100, height=200, file_count=8, show=False, tag="report_dialog_tag", modal=True, callback=report_selection):
    dpg.add_file_extension(".*")
    dpg.add_file_extension(".pdf", color=(255, 255, 0, 255))
    dpg.add_file_extension("", color=(150, 255, 150, 255))

with dpg.window(tag="main"):
    #Header
    dpg.add_text("I crawl the web and other stuff \(>.>)/")
    dpg.add_spacer(height=3)
    dpg.add_text("Always searching for scope 1,2 and 3 emission data nuggets ...", )
    dpg.add_spacer(height=15)
    dpg.add_separator()

    #WORD LIST CONFIG 
    dpg.add_spacer(height=5)
    dpg.add_button(label="Select word list", callback=lambda: dpg.show_item("file_dialog_tag"))
    dpg.add_spacer(height=5)
    dpg.add_text(default_value='No word list has been selected', color=[255,128,0], tag="word_list_tag", wrap=500)
    dpg.add_spacer(height=10)

    dpg.add_text("Where should I put all my findings ? For now I'm thinking here : ")
    dpg.add_text(os.getcwd()+'/results/result.pdf', tag="result_folder_tag")
    dpg.add_button(label="Select folder", callback=lambda: dpg.show_item("folder_dialog_tag"))
    dpg.add_spacer(height=5)
    dpg.add_separator()

    # REPORT CRAWLER
    dpg.add_spacer(height=5)
    dpg.add_button(label="Select Report to crawl", callback=lambda: dpg.show_item("report_dialog_tag"))
    dpg.add_spacer(height=5)

    dpg.add_text(default_value='No report has been selected', color=[255,128,0], tag="report_name_tag", wrap=500)
    dpg.add_spacer(height=5)
    dpg.add_text(default_value='', color=[255,255,0], tag="status_tag", wrap=500)
    
    dpg.add_spacer(height=5)
    dpg.add_button(label="Crawl report", callback=crawl_report)

    ##WEBSITE SELECTION
    #dpg.add_spacer(height=5)
    #dpg.add_separator()
    #dpg.add_spacer(height=5)
    #dpg.add_separator()
    #dpg.add_spacer(height=5)
    #dpg.add_text(default_value='Enter website (with www.blablabla and .com or .fr pleaaase)')
    #dpg.add_input_text(label='', tag='website')
    #dpg.add_spacer(height=5)
    #dpg.add_checkbox(label='look for text content directly on the site', tag="text_tag")
    #dpg.add_checkbox(label='look for pdfs on pages with matches and download them (will take a little longer if selected)', tag="pdf_tag")

    #dpg.add_button(label="Crawl website", callback=crawl_website)
    #dpg.add_spacer(height=5)
    #dpg.add_separator()

dpg.create_viewport(title='Carbon Crawler', width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()