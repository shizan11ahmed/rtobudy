import os
import PyPDF4
import tkinter as tk
import warnings
from tkinter import filedialog as fd
from rto_buddy import RTOBuddy

warnings.filterwarnings("ignore")

class RTOBuddyInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.minsize(475, 600)
        self.window.resizable(0,1)
        self.window.title("RTO Buddy")
        self.sp_obj = RTOBuddy()
        self._initialize_values()

    def _initialize_values(self):
        self.input_file_path = ""
        self.output_folder_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        self.chassis_photo_path = ""
        self.vehicle_front_photo_path = ""
        self.vehicle_side_photo_path = ""
        self.vehicle_back_photo_path = ""

    def _initialize_widgets(self):
        # App title and error / success message
        self.app_title = tk.Label(text="RTO Buddy: Scanning and compression solution", foreground="blue", font=("Arial", 12, "bold"))
        self.app_message = tk.Label(text="", foreground="red", font=("Arial", 10, "bold"))

        # Customer name / VIN entry
        self.vin_title = tk.Label(text="VIN Number / Name Of Customer")
        self.vin_input_value = tk.StringVar()
        self.vin_input = tk.Entry(width=35, textvariable=self.vin_input_value)

        # RTO location input
        self.rto_location_title = tk.Label(text="Select RTO location")
        self.rto_location_value = tk.IntVar(value=1)
        self.rto_location_one = tk.Radiobutton(text="Home District", variable=self.rto_location_value, value=1)
        self.rto_location_two = tk.Radiobutton(text="Other District (Local ID & Affidavit)", variable=self.rto_location_value, value=2)

        # Compression quality input
        self.compression_quality_title = tk.Label(text="Select compression quality")
        self.compression_quality_value = tk.IntVar(value=100)
        self.compression_quality_one = tk.Radiobutton(text="80 dpi", variable=self.compression_quality_value, value=80)
        self.compression_quality_two = tk.Radiobutton(text="90 dpi", variable=self.compression_quality_value, value=90)
        self.compression_quality_three = tk.Radiobutton(text="100 dpi (Recommended)", variable=self.compression_quality_value, value=100)
        
        # Output folder selection
        self.select_output_folder_button = tk.Button(text="Click to change output folder", command=self._change_output_folder)
        self.selected_output_folder_title = tk.Label(text=self.output_folder_path, foreground="purple", wraplength=200)

        # Input pdf file selection
        self.select_file_button = tk.Button(text="Click to select input pdf file", command=self._select_input_file)
        self.selected_file_title = tk.Label(text="", foreground="purple", wraplength=200)

        # Chassis photo selection
        self.select_chassis_photo_button = tk.Button(text="Click to select chassis photo", command=self._select_chassis_photo)
        self.selected_chassis_photo_title = tk.Label(text="", foreground="purple", wraplength=200)

        # Vehicle front photo selection        
        self.select_vehicle_front_photo_button = tk.Button(text="Click to select vehicle front photo", command=self._select_vehicle_front_photo)
        self.selected_vehicle_front_photo_title = tk.Label(text="", foreground="purple", wraplength=200)

        # Vehicle side photo selection        
        self.select_vehicle_side_photo_button = tk.Button(text="Click to select vehicle side photo", command=self._select_vehicle_side_photo)
        self.selected_vehicle_side_photo_title = tk.Label(text="", foreground="purple", wraplength=200)

        # Vehicle back photo selection
        self.select_vehicle_back_photo_button = tk.Button(text="Click to select vehicle back photo", command=self._select_vehicle_back_photo)
        self.selected_vehicle_back_photo_title = tk.Label(text="", foreground="purple", wraplength=200)

        # Submit button
        self.compress_split_button = tk.Button(text="Compress and split", bg="green", fg="white", height=2, width=20, font=("Arial", 12, "bold"), command=self._compress_and_split)

    def _select_input_file(self):
        filetypes = [('PDF files', '*.pdf')]
        self.input_file_path = fd.askopenfilename(title='Select input file', filetypes=filetypes)
        self.selected_file_title['text'] = os.path.normpath(self.input_file_path)

    def _change_output_folder(self):
        output_folder_path = fd.askdirectory()
        if output_folder_path != "":
            self.output_folder_path = output_folder_path
            self.selected_output_folder_title['text'] = os.path.normpath(self.output_folder_path)

    def _select_chassis_photo(self):
        filetypes = [('JPEG', '*.jpg *.jpeg *.jfif')]
        self.chassis_photo_path = fd.askopenfilename(title='Select input file', filetypes=filetypes)
        self.selected_chassis_photo_title['text'] = os.path.normpath(self.chassis_photo_path)

    def _select_vehicle_front_photo(self):
        filetypes = [('JPEG', '*.jpg *.jpeg *.jfif')]
        self.vehicle_front_photo_path = fd.askopenfilename(title='Select input file', filetypes=filetypes)
        self.selected_vehicle_front_photo_title['text'] = os.path.normpath(self.vehicle_front_photo_path)

    def _select_vehicle_side_photo(self):
        filetypes = [('JPEG', '*.jpg *.jpeg *.jfif')]
        self.vehicle_side_photo_path = fd.askopenfilename(title='Select input file', filetypes=filetypes)
        self.selected_vehicle_side_photo_title['text'] = os.path.normpath(self.vehicle_side_photo_path)

    def _select_vehicle_back_photo(self):
        filetypes = [('JPEG', '*.jpg *.jpeg *.jfif')]
        self.vehicle_back_photo_path = fd.askopenfilename(title='Select input file', filetypes=filetypes)
        self.selected_vehicle_back_photo_title['text'] = os.path.normpath(self.vehicle_back_photo_path)

    def _change_app_message(self, message, fg):
        self.app_message['text'] = message
        self.app_message['foreground'] = fg

    def _reset_ui(self):
        self._initialize_values()
        self.vin_input_value.set("")
        self.rto_location_value.set(1)
        self.compression_quality_value.set(100)
        self.selected_file_title['text'] = ""
        self.selected_chassis_photo_title['text'] = ""
        self.selected_vehicle_front_photo_title['text'] = ""
        self.selected_vehicle_side_photo_title['text'] = ""
        self.selected_vehicle_back_photo_title['text'] = ""

    def _compress_and_split(self):
        params = {
            "vin": self.vin_input_value.get(),
            "rto": self.rto_location_value.get(),
            "quality": self.compression_quality_value.get(),
            "input": self.input_file_path,
            "output": self.output_folder_path,
            "photos" : {
                "chassis_photo": self.chassis_photo_path,
                "front_photo": self.vehicle_front_photo_path,
                "side_photo": self.vehicle_side_photo_path,
                "back_photo": self.vehicle_back_photo_path
            }
        }
        if params['vin'] == "":
            self._change_app_message("Error: VIN or customer name is required.", "red")
            return
        elif params['rto'] == "":
            self._change_app_message("Error: Please select RTO location.", "red")
            return       
        elif params['output'] == "":
            self._change_app_message("Error: Please select output folder.", "red")
            return
        elif params['input'] == "" and params['photos']['chassis_photo'] == "" and params['photos']['front_photo'] == "" and params['photos']['side_photo'] == "" and params['photos']['back_photo'] == "":
            self._change_app_message("Error: Input file or vehicle photo is required.", "red")
            return
        if params['input'] != "":
            pages = PyPDF4.PdfFileReader(open(params['input'], 'rb'), strict=False).numPages
            if (params['rto'] == 1 and pages != 10) or params['rto'] == 2 and pages != 12:
                self._change_app_message("Error: Input pdf file in not valid.", "red")
                return
        response = self.sp_obj.run_pipeline(params)
        if 'status' in response:
            if response['status'] == "success":
                self._change_app_message(response['message'], "green")
                self._reset_ui()
            elif response['status'] == "error":
                self._change_app_message(response['message'], "red")

    def build_ui(self):
        # Initialize widgets
        self._initialize_widgets()

        # App title
        self.app_title.grid(row=0, columnspan=2, pady=(15, 0))

        # App message bar
        self.app_message.grid(row=1, columnspan=2, pady=(0, 15))

        # VIN Input
        self.vin_title.grid(row=2, column=0, sticky = tk.E, padx=15, pady=5)
        self.vin_input.grid(row=2, column=1, sticky = tk.W, padx=15, pady=5)

        # RTO location selection
        self.rto_location_title.grid(row=3, column=0, sticky = tk.E, padx=15, pady=5)
        self.rto_location_one.grid(row=3, column=1, sticky = tk.W, padx=15, pady=5)
        self.rto_location_two.grid(row=4, column=1, sticky = tk.W, padx=15, pady=5)

        # Compression quality selection
        self.compression_quality_title.grid(row=5, column=0, sticky = tk.E, padx=15, pady=5)
        self.compression_quality_one.grid(row=5, column=1, sticky = tk.W, padx=15, pady=5)
        self.compression_quality_two.grid(row=6, column=1, sticky = tk.W, padx=15, pady=5)
        self.compression_quality_three.grid(row=7, column=1, sticky = tk.W, padx=15, pady=5)

        # Output folder selection
        self.select_output_folder_button.grid(row=8, column=0, sticky = tk.E, padx=15, pady=5)
        self.selected_output_folder_title.grid(row=8, column=1, sticky = tk.W, padx=15, pady=5)

        # Input file selection
        self.select_file_button.grid(row=9, column=0, sticky = tk.E, padx=15, pady=5)
        self.selected_file_title.grid(row=9, column=1, sticky = tk.W, padx=15, pady=5)

        # Chassis photo selection
        self.select_chassis_photo_button.grid(row=10, column=0, sticky = tk.E, padx=15, pady=5)
        self.selected_chassis_photo_title.grid(row=10, column=1, sticky = tk.W, padx=15, pady=5)

        # Vehicle front photo selection
        self.select_vehicle_front_photo_button.grid(row=11, column=0, sticky = tk.E, padx=15, pady=5)
        self.selected_vehicle_front_photo_title.grid(row=11, column=1, sticky = tk.W, padx=15, pady=5)

        # Vehicle side photo selection        
        self.select_vehicle_side_photo_button.grid(row=12, column=0, sticky = tk.E, padx=15, pady=5)
        self.selected_vehicle_side_photo_title.grid(row=12, column=1, sticky = tk.W, padx=15, pady=5)

        # Vehicle back photo selection
        self.select_vehicle_back_photo_button.grid(row=13, column=0, sticky = tk.E, padx=15, pady=5)
        self.selected_vehicle_back_photo_title.grid(row=13, column=1, sticky = tk.W, padx=15, pady=5)

        # Submit button
        self.compress_split_button.grid(row=14, columnspan=2, pady=20)

    def render_ui(self):
        # self.window.iconbitmap(os.path.join(os.path.dirname(__file__)), "icon.ico")
        self.window.mainloop()

if __name__ == "__main__":
    RBI = RTOBuddyInterface()
    RBI.build_ui()
    RBI.render_ui()
