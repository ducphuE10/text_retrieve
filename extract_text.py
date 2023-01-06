import argparse
import pdfplumber
import re
import tqdm
def check_is_table_row(text):
  if len(re.split(r'\s{2,}', text)) >=3 :
    return True
  return False

#Preprocess page bao gồm 
# - Loại bỏ các trang là table of content
# - Kiểm tra xem một dòng trong page có phải là dòng của table không
def preprocess_page(lst_text,include_tables):
    lst_text_final = []
    num_4dots = 0
    for text in lst_text:
        text = text.strip()
        #check if the page is table of content
        if text.lower() == 'table of contents' or text.lower() == 'contents':
            return []
        if '....' in text:
            num_4dots += 1
            if num_4dots == 3:
                return []
        if not text:
            continue
        if not include_tables:
            if check_is_table_row(text):
                continue
        lst_text_final.append(text)
    
    return lst_text_final

def remove_header(lst_page):
    try:
        page_1 = lst_page[3]
        page_2 = lst_page[4]
        page_3 = lst_page[5]
        header = ''
        
        if page_1[0] == page_2[0] and page_1[0] == page_3[0]:
            header = page_1[0]
                
            lst_page = [page[1:] for page in lst_page if page[0] == header]
        
        return lst_page
    except:
        return lst_page

def get_first_number_from_right(text: str) -> int:
        for i in range(len(text)-1, -1, -1):
            if text[i].isdigit():
                return int(text[i])
        return None

def remove_page_number(lst_page):
    # import ipdb;ipdb.set_trace()
    try:
        page_1 = lst_page[3]
        page_2 = lst_page[4]
        page_3 = lst_page[5]

        x1 = get_first_number_from_right(page_1[-1])
        x2 = get_first_number_from_right(page_2[-1])
        x3 = get_first_number_from_right(page_3[-1])

        if x1+1 == x2 and x2+1 == x3:
            lst_page = [page[:-1] for page in lst_page]
            # print(lst_page[0][:-1])
    except:
        pass
    
    return lst_page

def curves_to_edges(cs):
    edges = []
    for c in cs:
        edges += pdfplumber.utils.rect_to_edges(c)
    return edges

# def not_within_bboxes(obj):
#     """Check if the object is in any of the table's bbox."""
#     def obj_in_bbox(_bbox):
#         v_mid = (obj["top"] + obj["bottom"]) / 2
#         h_mid = (obj["x0"] + obj["x1"]) / 2
#         x0, top, x1, bottom = _bbox
#         return (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)
#     return not any(obj_in_bbox(__bbox) for __bbox in bboxes)

def extract_pdf(pdf_path, include_tables=False):

    def not_within_bboxes(obj):
        def obj_in_bbox(_bbox):
            v_mid = (obj["top"] + obj["bottom"]) / 2
            h_mid = (obj["x0"] + obj["x1"]) / 2
            x0, top, x1, bottom = _bbox
            return (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)
        return not any(obj_in_bbox(__bbox) for __bbox in bboxes)
    
    pdf = pdfplumber.open(pdf_path)

    # Load the first page.
    documents = []
    tqdm.tqdm.write("Processing PDF...")
    for p in pdf.pages:
        if not include_tables:
            ts = {
            "vertical_strategy": "explicit",
            "horizontal_strategy": "explicit",
            "explicit_vertical_lines": curves_to_edges(p.curves + p.edges),
            "explicit_horizontal_lines": curves_to_edges(p.curves + p.edges),
            "intersection_y_tolerance": 10,
            }
            try:
                bboxes = [table.bbox for table in p.find_tables(table_settings=ts)]
            
                lst_text = p.filter(not_within_bboxes).extract_text().split('\n')
            except:
                lst_text = p.extract_text().split('\n')
        else:
            lst_text = p.extract_text().split('\n')
            
        lst_text = preprocess_page(lst_text,include_tables=include_tables)
        if len(lst_text) > 0:
            documents.append(lst_text)
        
    documents = remove_header(documents)
    documents = remove_page_number(documents)
    documents_ = ['\n'.join(page) for page in documents]
    documents__ = '\n'.join(documents_)
    
    return documents__

import docx
def extract_docx(path: str) -> str:
    doc = docx.Document(path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def extract_text(path: str, include_tables=False) -> str:
    if path.endswith('.pdf'):
        return extract_pdf(path, include_tables=include_tables)
    elif path.endswith('.docx') or path.endswith('.doc') or path.endswith('.DOCX') or path.endswith('.DOC'):
        return extract_docx(path)
    else:
        raise Exception("File format not supported")

if __name__ == '__main__':
    # print(extract_pdf("pdf/Midshore_LFG_MR_v1.6_03302022 - CLEAN.pdf"))
    with open("output.txt", "w") as f:
        f.write(extract_pdf("pdf/MidilliVCS PDv1.0sml.pdf", include_tables=True))
        print("Done")
    