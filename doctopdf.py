import subprocess



def doc_to_pdf(doc_path):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", doc_path])
    
doc_to_pdf("doc/Waste management_PoA_Design-Consultation CME Response.docx")