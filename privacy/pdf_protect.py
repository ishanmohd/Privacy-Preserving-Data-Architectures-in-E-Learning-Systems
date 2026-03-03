from pypdf import PdfReader, PdfWriter
import io

def add_pdf_password(pdf_bytes, password):

    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    output_stream = io.BytesIO()
    writer.write(output_stream)

    return output_stream.getvalue()
