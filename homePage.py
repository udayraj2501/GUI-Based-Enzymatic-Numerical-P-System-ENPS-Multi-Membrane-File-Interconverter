from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QApplication, QFrame
from PyQt6.QtCore import Qt
from converter import ConverterPage

class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENPS Multi-Membrane File Converter GUI")
        self.setStyleSheet(" background-color:#D5D6F5; ")  

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
         
        # Title
        title = QLabel("ENPS Multi-Membrane File Converter GUI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #414360; margin-bottom: 20px;")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Convert XML to PeP, PeP to XML!!!")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 18px; color: #414360; margin-bottom: 60px;")
        layout.addWidget(subtitle)

        container_frame_style = """ 
            border:8px solid #414360;
            border-radius:15px;
            background-color: #f7f7ff;
            padding: 60px 40px;

            text-align:center;
          """

        # Container for Buttons Layout
        container_frame = QFrame()
        container_frame.setStyleSheet(container_frame_style)
        container_layout = QVBoxLayout(container_frame)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_style = """
            
            QPushButton {
                background-color: #414360;
                border: 4px solid #414360;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 21px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #D5D6F5;;
                border-color:#414360;
                color:#414360;  
            }
        """
        
        #button1
        row_layout_1 = QHBoxLayout()
        button_xml_to_pep = QPushButton("XML to PeP")
        button_xml_to_pep.setStyleSheet(button_style)
        button_xml_to_pep.setFixedSize(170, 130)
        button_xml_to_pep.clicked.connect(lambda: self.open_converter_page("XML to PeP"))
        row_layout_1.addWidget(button_xml_to_pep)
        row_layout_1.addSpacing(40)
        
        #button2
        button_pep_to_xml = QPushButton("PeP to XML")
        button_pep_to_xml.setStyleSheet(button_style)
        button_pep_to_xml.setFixedSize(170, 130)
        button_pep_to_xml.clicked.connect(lambda: self.open_converter_page("PeP to XML"))
        row_layout_1.addWidget(button_pep_to_xml)

        container_layout.addLayout(row_layout_1)
        # container_layout.addSpacing(40)
        
        # #button3
        # row_layout_2 = QHBoxLayout()
        # button_pep_to_pep = QPushButton("PeP to PeP")
        # button_pep_to_pep.setStyleSheet(button_style)
        # button_pep_to_pep.setFixedSize(170, 130)
        # button_pep_to_pep.clicked.connect(lambda: self.open_converter_page("PeP to PeP"))
        # row_layout_2.addWidget(button_pep_to_pep)
        # row_layout_2.addSpacing(40)
        
        # #button4
        # button_xml_to_xml = QPushButton("XML to XML")
        # button_xml_to_xml.setStyleSheet(button_style)
        # button_xml_to_xml.setFixedSize(170, 130)
        # button_xml_to_xml.clicked.connect(lambda: self.open_converter_page("XML to XML"))
        # row_layout_2.addWidget(button_xml_to_xml)

        # container_layout.addLayout(row_layout_2)

        # Add container frame to main layout
        layout.addWidget(container_frame)
        layout.addSpacing(50)

    def open_converter_page(self, conversion_type):
        self.converter_page = ConverterPage(conversion_type)
        self.converter_page.show()

