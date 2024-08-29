from PyQt6.QtWidgets import QApplication
from homePage import HomePage
from resultPage import ResultPage
from simulatorPage import RunSimulationPage

if __name__ == "__main__":
    app = QApplication([])
    window = HomePage()
    window.showMaximized()
    app.exec()




