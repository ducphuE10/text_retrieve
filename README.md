# text_retrieve
(đối với .doc và không phải window os) Cài đặt textract: https://textract.readthedocs.io/en/latest/installation.html

### NOTE
- Nếu sử dụng os là window thì sử dụng các lib (yêu cầu có Microsoft Office) để chuyển .doc thành .pdf hoặc .docx rồi sử dụng các hàm đã viết trước đó.
- Hiện tại đang sử dụng textract thì đang chuyển từ .doc sang .txt nên không handle được text trong bảng.


### UPDATE 1 - UBUNTU
On Ubuntu, you can use LibreOffice's command line interface, "soffice", to convert a Microsoft Word (.doc) file to a Portable Document Format (.pdf) file.
-> sử dụng file doctopdf.py để chuyển định dạng doc hoặc docx về pdf rồi sử dụng hàm extract_text như bình thường