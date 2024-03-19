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
    Signal
)

from PySide6.QtGui import QIcon
import sys
import copy

sys.path.append(r'C:\Users\Wesllei\OneDrive\Imagens\OneDrive\Documentos\personal-projects\burite_master_frontend\src')

from src.end_points.list_purchases_all import ListPurchasesAll
from src.components.price.create_price import PriceList

import asyncio
from unidecode import unidecode
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

loop = asyncio.get_event_loop()


class ListPurchases(QMainWindow):
    data_ready = Signal(list)

    def __init__(self, url: str):
        super().__init__()
        self._url = url
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
        self._column_size = {
            'NF': 20,
            'Fornecedor': 300,
            'Total': 80,
            'Data compra': 85
        }
        # Criando a tabela
        self.tableWidget = QTableWidget()
        # Definindo o número colunas na tabela
        self.tableWidget.setColumnCount(len(self._columns))
        # Definição dos nomes das colunas
        self.tableWidget.setHorizontalHeaderLabels(self._columns)
        # Define que não é permitido editar os valores dos itens da tabela
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Define que a tabela só pode selecionar um item
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # Define que quando um item for clicado seleciona todos os elementos daquela linha
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Define que não vai exibir a numeração das linhs
        self.tableWidget.verticalHeader().setVisible(False)
        self._purchases_list = ListPurchasesAll()
        self._purchases = None
        self._fetch = url
        self.setGeometry(100, 100, 1024, 400)
        self.setWindowTitle("Notas não finalizadas!")
        self._run_loop_subgroup = loop.run_until_complete(self.fetch_purchases())
        self.data_ready.connect(self._fill_table)
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.cellDoubleClicked.connect(self._create_nf_purchase)
        self.price_window = None

    async def fetch_purchases(self):
        data = await self._purchases_list.list_prices(self._url)
        self._purchases = data
        self._fill_table(data)

    def _fill_table(self, data_table):
        # Definindo o número de linhas
        self.tableWidget.setRowCount(len(data_table))
        # Preenchimento da tabela
        for row_index, row in enumerate(data_table):
            for col_index, col_name in enumerate(self._columns):
                # Obter a chave correspondente ao nome da coluna
                property_name = self._column_to_property.get(col_name)
                if property_name is not None:
                    # Obtendo o valor da propriedade do dicionário
                    cell_value = row.get(property_name, '')  # Aqui pegamos diretamente o valor da propriedade com a 
                    # chave correta
                    # em row
                    # Convertendo o valor para string
                    cell_value_str = str(cell_value)
                    # Criando o item da célula da tabela
                    item = QTableWidgetItem(cell_value_str)
                    # Definindo que os textos dentro da célula ficará centralizado 
                    item.setTextAlignment(Qt.AlignCenter)
                    # Definindo o item na posição correta na tabela
                    self.tableWidget.setItem(row_index, col_index, item)
                    self.tableWidget.setColumnWidth(col_index, self._column_size[col_name])

    def _create_nf_purchase(self, row):
        num_nf = self.tableWidget.item(row, 0).text()

        if self.price_window is None:
            self.price_window = PriceList(num_nf)
            self.price_window.show()
            self.setEnabled(False)  # Desabilita a janela principal
            self.price_window.finished.connect(self.enable_main_window)
        else:
            self.price_window.close()
            self.price_window = PriceList(num_nf)
            self.price_window.show()
            self.setEnabled(False)  # Desabilita a janela principal
            self.price_window.finished.connect(self.enable_main_window)

    def enable_main_window(self):
        self.setEnabled(True)

    def closeEvent(self, event):
        if self.price_window is not None and self.price_window.isVisible():
            event.ignore()  # Cancela o evento de fechamento
        else:
            super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = ListPurchases('http://192.168.0.112:3004/price-formation')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
