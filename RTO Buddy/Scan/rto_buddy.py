import os
import json
import ghostscript
from PIL import Image
import utils
from config import config
import shutil   # <-- required for smart_compress!!

class RTOBuddy:
    def __init__(self):
        self.config = json.loads(config)
        self.current_compression_pipeline = []

    def get_size_kb(self, path):
        return os.path.getsize(path) / 1024

    def resize_and_compress(self, input_path, output_path, dpi, quality):
        args = [
            "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dDownsampleColorImages=true",
            f"-dColorImageResolution={dpi}",
            "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={output_path}", input_path
        ]
        ghostscript.Ghostscript(*args)

    def smart_compress(self, input_path, output_path, target_kb=400):
        original_kb = self.get_size_kb(input_path)
        # Select starting DPI based on file size
        if original_kb > 2000: start_dpi = 150
        elif original_kb > 1000: start_dpi = 200
        elif original_kb > 500: start_dpi = 250
        else: start_dpi = 300
        dpi, quality = start_dpi, 85
        temp_path = output_path + ".tmp.pdf"
        best_path = None
        for i in range(20):
            self.resize_and_compress(input_path, temp_path, dpi, quality)
            size_kb = self.get_size_kb(temp_path)
            if 280 <= size_kb <= target_kb:
                shutil.move(temp_path, output_path)
                best_path = output_path
                break
            if size_kb > target_kb:
                quality = quality - 5 if quality > 60 else quality
                dpi = dpi - 10 if quality <= 60 else dpi
            if dpi < 100 or quality < 50:
                break
        if not best_path:
            shutil.move(temp_path, output_path)
        return output_path

    def compress_pdf(self, input_path, output_path, quality):
        # DEPRECATED! Use smart_compress instead.
        args = ["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dDownsampleColorImages=true", f"-dColorImageResolution={quality}", "-dNOPAUSE", "-dQUIET", "-dBATCH", f"-sOutputFile={output_path}", input_path]
        ghostscript.Ghostscript(*args)
        # utils.delete_file(input_path)

    def jpg_to_pdf(self, input_path, output_path):
        img_size = utils.get_file_size_in_kb(input_path)
        output_quality = 5 * round((200 / img_size * 100) / 5)
        if output_quality > 100:
            output_quality = 50
        if img_size < 100:
            output_quality = 100
        img = Image.open(input_path)
        img.convert('RGB').save(output_path, quality=output_quality, optimize=True)

    def split_file(self, input_file, output_directory, rto):
        for file in self.config:
            if 'split' in file and file['split'] == True and rto in file['rto']:
                output_file = os.path.join(output_directory, f"temp_{file['file_name']}")
                args = ["gs", "-sDEVICE=pdfwrite", "-dNOPAUSE", "-dQUIET", "-dBATCH", f"-dFirstPage={file['start']}", f"-dLastPage={file['end']}", f"-sOutputFile={output_file}", input_file]
                ghostscript.Ghostscript(*args)
                self.current_compression_pipeline.append(file['file_name'])

    def run_pipeline(self, params):
        """
            params = {
                "vin": "",
                "rto": "",
                "quality": "",
                "input": "",
                "output": "",
                "photos" : {
                    "chassis_photo": "",
                    "front_photo": "",
                    "side_photo": "",
                    "back_photo": ""
                }
            }
        """
        try:
            # Reset compression pipeline to default
            self.current_compression_pipeline = []

            # Create output directory if does not exists
            output_path = os.path.join(params['output'], params['vin'])
            utils.create_directory(output_path)

            # Split input pdf into multiple pdfs and compress them
            if params['input'] != "":
                self.split_file(params['input'], output_path, params['rto'])
                for file in self.config:
                    if file['file_name'] in self.current_compression_pipeline:
                        # --- Replace this line for smart compression ---
                        # self.compress_pdf(os.path.join(output_path, f"temp_{file['file_name']}"), os.path.join(output_path, file['file_name']), params['quality'])
                        self.smart_compress(os.path.join(output_path, f"temp_{file['file_name']}"), os.path.join(output_path, file['file_name']), target_kb=400)
                        # --- End replacement ---

            # Convert input jpg photo to pdf
            for photo in params['photos'].keys():
                if params['photos'][photo] != "":
                    self.jpg_to_pdf(params['photos'][photo], os.path.join(output_path, f"{photo}.pdf"))

            # Open output folder after split and compress
            os.startfile(output_path)

            # Return success message
            return {
                "status": "success",
                "message": "Compressed successfully"
            }

        except Exception as e:
            print({
                "error": type(e).__name__,
                "file": __file__,
                "line": e.__traceback__.tb_lineno,
                "message": str(e)
            })
            return {
                "status": "error",
                "message": str(e)
            }

if __name__ == "__main__":
    rto = RTOBuddy()
    # Example:
    # rto.smart_compress("/Users/farman/Desktop/Vyke/RTO Buddy/1.pdf", "/Users/farman/Desktop/2.pdf", target_kb=400)
    