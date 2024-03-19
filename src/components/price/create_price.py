import sys

sys.path.append(r'C:\Users\Wesllei\OneDrive\Imagens\OneDrive\Documentos\personal-projects\burite_master_frontend\src')

from src.end_points.create_price import Prices

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
import copy
import asyncio
from unidecode import unidecode
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

loop = asyncio.get_event_loop()


class PriceList(QMainWindow):
    def __init__(self, nf: str):
        super().__init__()
        self._nf = nf
        self._search_nf = Prices()
        self.setWindowTitle("Criação da nota")
        self.setLayout(QVBoxLayout())
        self.setGeometry(
            100,
            100,
            1024,
            400
        )

        self._columns = [
            'Código',
            'Quantidade',
            'Descrição',
            'Custo',
            'Despesa Fixa',
            'Despesa Variavel',
            'Comissão',
            'Desconto Máximo',
            'Lucro R$',
            'Lucro %',
            'Venda'
        ]

        self._column_to_property = {
            'Código': 'code',
            'Quantidade': 'inputQuantity',
            'Descrição': 'nameProduct',
            'Custo': 'costValue',
            'Despesa Fixa': 'expenseFixedUnit',
            'Despesa Variavel': 'expenseVariableUnit',
            'Comissão': 'commission',
            'Desconto Máximo': 'discountValueMax',
            'Lucro R$': 'profitUnit',
            'Lucro %': 'profitPercentage',
            'Venda': 'newSalePrice'
        }

        self._column_size = {
            'Código': 50,
            'Quantidade': 70,
            'Descrição': 300,
            'Custo': 60,
            'Despesa Fixa': 100,
            'Despesa Variavel': 120,
            'Comissão': 80,
            'Desconto Máximo': 130,
            'Lucro R$': 70,
            'Lucro %': 70,
            'Venda': 80
        }
        self.showMaximized()
        self._tableProducts = QTableWidget()
        self._tableProducts.setColumnCount(len(self._columns))
        self._tableProducts.setHorizontalHeaderLabels(self._columns)
        self.setCentralWidget(self._tableProducts)
        layout = QVBoxLayout()
        layout.addWidget(self._tableProducts)

        # Centraliza o layout em um widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self._run_loop_subgroup = loop.run_until_complete(self.fetch_purchase_nf())

    def _fill_table(self, data_table):
        print(data_table)
        # Definindo o número de linhas
        self._tableProducts.setRowCount(len(data_table))

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
                    self._tableProducts.setItem(row_index, col_index, item)
                    self._tableProducts.setColumnWidth(col_index, self._column_size[col_name])

    async def fetch_purchase_nf(self):
        data = await self._search_nf.create_price_nfe(url_=f'http://localhost:3003/price-formation/{self._nf}')
        self._fill_table(data['products'])
