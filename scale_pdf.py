# import PyPDF2
# import fitz 
# pdf = "./LUONG DINH HUAN-Developer.pdf"
# output_image_path = "image.jpg"
# pdf = PyPDF2.PdfReader(pdf)
# page0 = pdf.pages[0]

# writer = PyPDF2.PdfWriter()  # create a writer to save the updated results
# writer.add_page(page0)
# with open("YOUR OUTPUT PDF FILE PATH.pdf", "wb+") as f:
#     writer.write(f)


from PyPDF2 import PdfReader, PdfWriter

# Đọc tệp PDF đầu vào
reader = PdfReader("YOUR OUTPUT PDF FILE PATH.pdf")

# Khởi tạo một đối tượng PdfWriter để ghi dữ liệu vào tệp PDF mới
writer = PdfWriter()

# Lặp qua từng trang trong tệp PDF đầu vào, cắt và thêm vào tệp PDF mới
for i, page in enumerate(reader.pages):
    # Cắt trang dựa trên tọa độ (x, y)
    page.cropbox.lower_right = (42, 115)
    page.cropbox.lower_right = (500, 245)

    # Thêm trang đã cắt vào tệp PDF mới
    writer.add_page(page)

# Ghi dữ liệu vào tệp PDF mới
with open("samples_cropped.pdf", "wb") as fp:
    writer.write(fp)
