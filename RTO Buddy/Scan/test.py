import ghostscript

def compress_pdf(input_path, output_path, quality):
    args = [
        "",  # argv[0] is ignored, can be any string
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dDownsampleColorImages=true",
        f"-dColorImageResolution={quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    ghostscript.Ghostscript(*args)

compress_pdf("/Users/farman/Desktop/Vyke/RTO Buddy/1.pdf", "/Users/farman/Desktop/2.pdf", 100)
