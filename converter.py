from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QFileDialog, QApplication, QSizePolicy, QFrame
from PyQt6.QtCore import Qt
import shutil
import os
from simulatorPage import RunSimulationPage

   
class ConverterPage(QMainWindow):
    def __init__(self, conversion_type):
        super().__init__()
        project_title = "ENPS Multi-Membrane File Converter GUI"
        self.conversion_type = conversion_type
        self.setWindowTitle(f"{project_title} - {conversion_type} Converter")
        self.setStyleSheet("background-color:#D5D6F5;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Frame
        main_frame = QVBoxLayout(central_widget)
        main_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title and Subtitle
        title_layout = QVBoxLayout()
        title = QLabel("ENPS Multi-Membrane File Converter GUI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #414360; margin-bottom: 40px; margin-top:40px;")
        title_layout.addWidget(title)

        subtitle = QLabel(f"{conversion_type} Converter")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 25px; font-weight: bold; color: #414360; margin-bottom: 40px;")
        title_layout.addWidget(subtitle)
        title_layout.addSpacing(10)

        main_frame.addLayout(title_layout)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)

        main_frame.addLayout(layout)

        # Container Frame 
        container_frame_style = """ 
            border: 8px solid #414360;
            border-radius: 15px;
            padding:15px; 
            background-color: #f7f7ff;
            text-align:center;    
          """
        container_frame = QFrame()
        container_frame.setStyleSheet(container_frame_style)
        container_frame.setFixedWidth(800)  # Set width to 800 pixels
        container_frame.setFixedHeight(300)  # Set height to 250 pixels
        container_layout = QVBoxLayout(container_frame)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(container_frame)

        # Input Field
        input_layout = QHBoxLayout()
        input_label = QLabel(f"Select {conversion_type[:3]} File:")
        input_label.setStyleSheet("font-size: 18px; color: #414360; border:none;")
        input_layout.addWidget(input_label)

        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("font-size: 14px; border:1px solid black; width:400px; height:20px; margin-right:10px; padding:10px; border-radius:10px;")
        self.input_field.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        input_layout.addWidget(self.input_field)

        button_style = """
            QPushButton {
                background-color: #414360;
                border: 4px solid #414360;
                color: white;
                border-radius: 15px;
                padding: 7px 15px;
                font-size: 21px;
                font-weight: bold;
                text-align: center;
                margin:20px;
            }
            QPushButton:hover {
                background-color: #D5D6F5;;
                border-color:#414360;
                color:#414360;  
            }
        """
        browse_button = QPushButton("Browse")
        browse_button.setStyleSheet(button_style)
        browse_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        browse_button.clicked.connect(self.browse_file)
        input_layout.addWidget(browse_button)

        container_layout.addLayout(input_layout)

        # Convert Button
        self.convert_button = QPushButton("Convert")
        self.convert_button.setStyleSheet(button_style)   
        self.convert_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.convert_button.clicked.connect(self.convert_file)
        
        # Horizontal Layout 
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.convert_button)
        button_layout.addStretch()
        container_layout.addLayout(button_layout)

        # Message Label (Initially Hidden)
        self.message_label = QLabel(f"{conversion_type[:3]} File is converted into {conversion_type[-3:]}. Please download the file.")
        self.message_label.setStyleSheet("font-size: 18px; color: green; border:none;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.hide()  # Hide initially
        container_layout.addWidget(self.message_label)

        # Home and Download Buttons (Initially Hidden)
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet(button_style)
        self.home_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.home_button.hide()  # Hide initially
        self.home_button.clicked.connect(self.go_to_home)

        self.download_button = QPushButton("Download")
        self.download_button.setStyleSheet(button_style)
        self.download_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.download_button.hide()  # Hide initially
        self.download_button.clicked.connect(self.download_file)

        self.go_to_simulation_button = QPushButton("Go To Simulation")
        self.go_to_simulation_button.setStyleSheet(button_style)
        self.go_to_simulation_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.go_to_simulation_button.hide()  # Hide initially
        self.go_to_simulation_button.clicked.connect(self.go_to_simulation)

        self.home_download_layout = QHBoxLayout()
        self.home_download_layout.addWidget(self.home_button)
        self.home_download_layout.addWidget(self.download_button)
        self.home_download_layout.addWidget(self.go_to_simulation_button)

        container_layout.addLayout(self.home_download_layout)

        self.showMaximized()

        
    def browse_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("XML files (*.xml);;PeP files (*.pep)")
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        if file_path:
            # Extract the file name from the full file path
            file_name = file_path.split('/')[-1]  
            # Set the file name as the text of the input field
            self.input_field.setText(file_name)
               
    def convert_file(self):
        self.convert_button.hide()
        self.home_button.show()
        self.download_button.show()
        self.go_to_simulation_button.show()
        self.message_label.show()

        input_file_path = self.input_field.text()
        if input_file_path:
            converted_file_path = self.convert_file_algorithm(input_file_path)
            print("File converted successfully")
        else:
            print("No file selected for conversion")

    def convert_file_algorithm(self, input_file_path):
        if self.conversion_type == 'XML to PeP':
            os.system('python3 xmltopep.py ' + input_file_path)
            return 'pepout.pep'  
            
        if self.conversion_type == 'PeP to XML':
            os.system('python3 peptoxml.py ' + input_file_path)
            return 'xmlout.xml'  
            
        if self.conversion_type == 'PeP to PeP':
            os.system('python3 transferValuesPep.py')
            return 'out.pep' 
            
        if self.conversion_type == 'XML to XML':
            os.system('python3 transferValuesXml.py')
            return 'out.xml'  

    def download_file(self):
        converted_file_path = self.convert_file_algorithm(self.input_field.text())
        if converted_file_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", f"{self.conversion_type[-3:].lower()} files (*.{self.conversion_type[-3:].lower()})")
            if save_path:
                shutil.copy(converted_file_path, save_path)

    def go_to_home(self):
        self.close()

    def go_to_simulation(self):
        # Assuming SimulatorPage is defined and imported properly
        self.simulator_page = RunSimulationPage()
        self.simulator_page.show()
        self.close()
