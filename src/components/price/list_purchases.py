from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QVBoxLayout,
    QLineEdit,
    QWidget,
    QDialog,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLayout
)

from PySide6.QtCore import (
    Qt,
    QMargins
)

from PySide6.QtGui import QIcon
import sys
import copy

sys.path.append(r'C:\Users\Wesllei\OneDrive\Imagens\OneDrive\Documentos\personal-projects\burite_master_frontend\src')

from src.end_points.list_purchases_all import ListPurchasesAll

import asyncio
from unidecode import unidecode
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

loop = asyncio.get_event_loop()


class ListPurchases(QMainWindow):
    def __init__(self, url: str):
        super().__init__()
        self._url = url
        self._purchases_list = ListPurchasesAll()
        self._purchases = None
        self._fetch = url
        self.setGeometry(100, 100, 1024, 400)
        self.setWindowTitle("Notas não finalizadas!")
        self._run_loop_subgroup = loop.run_until_complete(self.fetch_purchases())
        self._columns = [
            'NF',
            'Fornecedor',
            'Total',
            'Data compra'
        ]
        self._column_to_property = {
            'NF': 'nf',
            'Fornecedor': 'provider',
            'Total': 'value',
            'Data compra': 'date'
        }
        
    async def fetch_purchases(self):
        data = await self._purchases_list.list_prices(self._url)
        self._purchases = data


def main():
    app = QApplication(sys.argv)
    window = ListPurchases('http://192.168.0.112:3004/price-formation')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
