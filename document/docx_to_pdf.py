from docx2pdf import convert
import sys
import os

def docx_to_pdf(input_path, output_path=None):
    if not os.path.exists(input_path):
        print("Dosya bulunamadı")
        return

    if output_path:
        convert(input_path, output_path)
    else:
        convert(input_path)

    print("PDF created")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python docx2pdf.py input.docx [output|output.pdf]")
        sys.exit(1)

    input_docx = sys.argv[1]

    output_pdf = None
    if len(sys.argv) >= 3:
        out = sys.argv[2]

        if not out.lower().endswith(".pdf"):
            out += ".pdf"

        output_pdf = out
    else:
        base = os.path.splitext(os.path.basename(input_docx))[0]
        output_pdf = base + ".pdf"

    docx_to_pdf(input_docx, output_pdf)
