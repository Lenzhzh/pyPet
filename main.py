from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

from ui.console import logger
from component.pet import Deskpet


if __name__ == '__main__':
    logger.hide()
    pet = Deskpet()
    sys.exit(app.exec())