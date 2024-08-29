from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QFileDialog, QApplication, QSizePolicy, QTextEdit, QFrame, QSpacerItem
from PyQt6.QtCore import Qt
import subprocess

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
    }
    QPushButton:hover {
        background-color: #D5D6F5;
        border-color:#414360;
        color:#414360;  
    }
"""

class RunSimulationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sequential Python Simulator and Parallel Python Simulator")
        self.setStyleSheet("background-color:#D5D6F5;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Frame
        main_frame = QVBoxLayout(central_widget)
        main_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("Sequential Python Simulator and Parallel Python Simulator")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #414360;")
        main_frame.addWidget(title)

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
        container_frame.setFixedWidth(670)  # Set width to 650 pixels
        container_frame.setFixedHeight(200)  # Set height to 200 pixels
        container_layout = QVBoxLayout(container_frame)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(container_frame)

        # Input Field
        input_layout = QHBoxLayout()
        input_label = QLabel("Select Input File:")
        input_label.setStyleSheet("font-size: 18px; color: #414360; border:none;")
        input_layout.addWidget(input_label)

        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("font-size: 14px; border:1px solid black; width:300px; height:20px; margin-right:10px; padding:10px; border-radius:10px;")
        self.input_field.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        input_layout.addWidget(self.input_field)

        browse_button = QPushButton("Browse")
        browse_button.setStyleSheet(button_style)
        browse_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        browse_button.clicked.connect(self.browse_file)
        input_layout.addWidget(browse_button)

        container_layout.addLayout(input_layout)
        # Add spacer item to create space between input and buttons
        container_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Run Simulation Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sequential_button = QPushButton("Sequential Simulator(PeP)")
        sequential_button.setStyleSheet(button_style)
        sequential_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        sequential_button.clicked.connect(self.run_sequential_simulation)
        buttons_layout.addWidget(sequential_button)

        parallel_button = QPushButton("Parallel Simulator(GPUPeP)")
        parallel_button.setStyleSheet(button_style)
        parallel_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        parallel_button.clicked.connect(self.run_parallel_simulation)
        buttons_layout.addWidget(parallel_button)

        container_layout.addLayout(buttons_layout)

        # Result Title
        result_title = QLabel("Result")
        result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #414360; margin-top: 20px; margin-bottom: 10px;")
        layout.addWidget(result_title)

        # Output Fields
        output_layout = QHBoxLayout()
        output_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Sequential Output Box
        sequential_output_frame = QFrame()
        sequential_output_frame_layout = QVBoxLayout(sequential_output_frame)

        sequential_title = QLabel("Sequential python simulator(PeP)")
        sequential_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sequential_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #414360;")
        sequential_output_frame_layout.addWidget(sequential_title)

        self.sequential_output = QTextEdit()
        self.sequential_output.setStyleSheet("font-size: 14px; border:1px solid black; width:250px; height:300px; margin-right:10px; padding:10px; border-radius:10px;")
        self.sequential_output.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.sequential_output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sequential_output.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sequential_output.setReadOnly(True)
        sequential_output_frame_layout.addWidget(self.sequential_output)

        output_layout.addWidget(sequential_output_frame)

        # Parallel Output Box
        parallel_output_frame = QFrame()
        parallel_output_frame_layout = QVBoxLayout(parallel_output_frame)

        parallel_title = QLabel("Parallel python simulator(GPUPeP)")
        parallel_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parallel_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #414360;")
        parallel_output_frame_layout.addWidget(parallel_title)

        self.parallel_output = QTextEdit()
        self.parallel_output.setStyleSheet("font-size: 14px; border:1px solid black; width:250px; height:300px; margin-left:10px; padding:10px; border-radius:10px;")
        self.parallel_output.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.parallel_output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.parallel_output.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.parallel_output.setReadOnly(True)
        parallel_output_frame_layout.addWidget(self.parallel_output)

        output_layout.addWidget(parallel_output_frame)

        main_frame.addLayout(output_layout)

        self.showMaximized()

    def browse_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PeP files (*.pep)")
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        if file_path:
            # Extract the file name from the full file path
            file_name = file_path.split('/')[-1]  
            # Set the file name as the text of the input field
            self.input_field.setText(file_name)

    def run_sequential_simulation(self):
        input_file_path = self.input_field.text()
        if input_file_path:
            # Run sequential simulation command
            command = f"python3 pep.py {input_file_path} -n 1000"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.sequential_output.setText(result.stdout)
        else:
            self.sequential_output.setText("No input file selected.")

    def run_parallel_simulation(self):
        input_file_path = self.input_field.text()
        if input_file_path:
            # Run parallel simulation command
            command = f"python3 gpupep.py {input_file_path} -n 1000 -p"
           
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.parallel_output.setText(result.stdout)
        else:
            self.parallel_output.setText("No input file selected.")

if __name__ == "__main__":
    app = QApplication([])
    run_simulation_page = RunSimulationPage()
    run_simulation_page.show()
    app.exec()
