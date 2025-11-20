import os
import json
import ghostscript
from PIL import Image
import utils
from config import config

class RTOBuddy:
    def __init__(self):
        self.config = json.loads(config)
        self.current_compression_pipeline = []

    def compress_pdf(self, input_path, output_path, quality):
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
                        self.compress_pdf(os.path.join(output_path, f"temp_{file['file_name']}"), os.path.join(output_path, file['file_name']), params['quality'])

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
    rto.compress_pdf("/Users/farman/Desktop/Vyke/RTO Buddy/1.pdf", "/Users/farman/Desktop/2.pdf", 100)
