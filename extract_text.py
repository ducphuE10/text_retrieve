import argparse
import pdfplumber
import re
import tqdm
def check_is_table_row(text):
  if len(re.split(r'\s{2,}', text)) >=3 :
    return True
  return False

def preprocess_page(lst_text):
    lst_text_final = []
    for text in lst_text:
        text = text.strip()
        if len(text.split(" ")) <= 1:
            continue
        if not text: 
            continue
        if check_is_table_row(text):
            continue
        lst_text_final.append(text)
    
    return lst_text_final[:-1]

def preprocess_documents(lst_page):
    num_pages = len(lst_page)
    pages_1 = lst_page[num_pages//2]
    pages_2 = lst_page[num_pages//4]
    pages_3 = lst_page[num_pages*3//4]
    header = ''
    if pages_1[0] == pages_2[0] and pages_1[0] == pages_3[0]:
        header = pages_1[0]
        lst_page = [page[1:] for page in lst_page if page[0] == header]
        
    return lst_page

def curves_to_edges(cs):
    edges = []
    for c in cs:
        edges += pdfplumber.utils.rect_to_edges(c)
    return edges

def not_within_bboxes(obj):
    """Check if the object is in any of the table's bbox."""
    def obj_in_bbox(_bbox):
        v_mid = (obj["top"] + obj["bottom"]) / 2
        h_mid = (obj["x0"] + obj["x1"]) / 2
        x0, top, x1, bottom = _bbox
        return (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)
    return not any(obj_in_bbox(__bbox) for __bbox in bboxes)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    pdf_path = parser.parse_args().pdf_path

    # pdf_path = "pdf/MidilliVCS PDv2.00fnlsml.pdf"
    # pdf_path = "pdf/Midshore Verra Registry Communication Agreement - Blue Source LLC_signed.pdf"
    pdf = pdfplumber.open(pdf_path)

    # Load the first page.
    documents = []
    tqdm.tqdm.write("Processing PDF...")
    for p in pdf.pages:
        # Table settings.
        ts = {
            "vertical_strategy": "explicit",
            "horizontal_strategy": "explicit",
            "explicit_vertical_lines": curves_to_edges(p.curves + p.edges),
            "explicit_horizontal_lines": curves_to_edges(p.curves + p.edges),
            "intersection_y_tolerance": 10,
        }

        # Get the bounding boxes of the tables on the page.
        try:
            bboxes = [table.bbox for table in p.find_tables(table_settings=ts)]
        
            lst_text = p.filter(not_within_bboxes).extract_text().split('\n')
        except:
            lst_text = p.extract_text().split('\n')
        
        lst_text = preprocess_page(lst_text)
        documents.append(lst_text)
        

    documents = preprocess_documents(documents)
    documents_ = ['\n'.join(page) for page in documents]
    documents__ = '\n'.join(documents_)
    with open("output.txt", "w") as f:
        f.write(documents__)
        print("Done")