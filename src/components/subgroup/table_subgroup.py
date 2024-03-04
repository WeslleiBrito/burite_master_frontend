from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAbstractItemView,
                               QVBoxLayout, QLineEdit, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sys
from unidecode import unidecode

sys.path.append(r'C:\Users\Wesllei\OneDrive\Imagens\OneDrive\Documentos\personal-projects\burite_master_frontend\src')

from src.end_points.subgroups import Subgroup

import asyncio

loop = asyncio.get_event_loop()


class MyWindow(QMainWindow):
    def __init__(self, url: str):
        super().__init__()
        self._loop = asyncio.get_event_loop()
        self._url = url
        self._fetch = Subgroup().get_resume_subgroups
        self._subgroups = []

        self.setGeometry(100, 100, 1024, 400)
        self.setWindowTitle("Subgrupos")
        self.setWindowIcon(QIcon(r'C:\Users\Wesllei\OneDrive\Imagens\OneDrive\Documentos\personal-projects'
                                 r'\burite_master_frontend\src\assets\business_package_box_products_2343.ico'))
        # Criando a tabela
        self.tableWidget = QTableWidget()

        # Criando a caixa de pesquisa
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.filter_subgroup)
        # Incluido um placeholder a caixa de pesquisa
        self.search_box.setPlaceholderText("Buscar subgrupo")

        # Agora você pode chamar o método fetch_subgroup
        self._run_loop_subgroup = loop.run_until_complete(self.fetch_subgroup())

        # Define que não é permitido editar os valores dos itens da tabela
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Define que a tabela só pode selecionar um item
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # Define que quando um item for clicado seleciona todos os elementos daquela linha
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Define que não vai exibir a numeração das linhs
        self.tableWidget.verticalHeader().setVisible(False)

        self.setCentralWidget(self.tableWidget)

        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.tableWidget)

        # Centraliza o layout em um widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def filter_subgroup(self, text):
        base = self._subgroups
        list_filter = [subgroup for subgroup in base if
                       unidecode(text).lower() in unidecode(subgroup['nameSubgroup']).lower()]

        self.tableWidget.setRowCount(len(list_filter))

        columns = [
            'ID',
            'Nome',
            'Despesa Fixa',
            'Base Lucro Subgrupo',
            'Atualizado em',
        ]

        column_to_property = {
            'ID': 'codSubgroup',
            'Nome': 'nameSubgroup',
            'Despesa Fixa': 'fixedUnitExpense',
            'Base Lucro Subgrupo': 'plucro',
            'Atualizado em': 'updatedAt',
        }

        column_size = {
            'ID': 20,
            'Nome': 460,
            'Despesa Fixa': 80,
            'Base Lucro Subgrupo': 130,
            'Atualizado em': 150,
        }

        # Preenchimento da tabela
        for row_index, row in enumerate(list_filter):
            for col_index, col_name in enumerate(columns):
                # Obter a chave correspondente ao nome da coluna
                property_name = column_to_property.get(col_name)
                if property_name is not None:
                    # Obtendo o valor da propriedade do dicionário
                    cell_value = row.get(property_name, '')  # Aqui pegamos diretamente o valor da propriedade com a 
                    # chave correta
                    # em row
                    # Convertendo o valor para string
                    cell_value_str = str(cell_value)
                    # Criando o item da célula da tabela
                    item = QTableWidgetItem(cell_value_str)
                    # Definindo o item na posição correta na tabela
                    self.tableWidget.setItem(row_index, col_index, item)
                    self.tableWidget.setColumnWidth(col_index, column_size[col_name])

    async def fetch_all(self):
        self._subgroups = await self._fetch(self._url)

    async def fetch_subgroup(self):
        data = await self._fetch(self._url)
        self._subgroups = data

        # Definição das colunas
        columns = [
            'ID',
            'Nome',
            'Despesa Fixa',
            'Base Lucro Subgrupo',
            'Atualizado em',
        ]

        # Mapeamento de nomes de colunas para chaves correspondentes em 'row'
        column_to_property = {
            'ID': 'codSubgroup',
            'Nome': 'nameSubgroup',
            'Despesa Fixa': 'fixedUnitExpense',
            'Base Lucro Subgrupo': 'plucro',
            'Atualizado em': 'updatedAt',
        }

        column_size = {
            'ID': 20,
            'Nome': 460,
            'Despesa Fixa': 80,
            'Base Lucro Subgrupo': 130,
            'Atualizado em': 150,
        }

        # Definindo o número de linhas e colunas na tabela
        self.tableWidget.setRowCount(len(self._subgroups))
        self.tableWidget.setColumnCount(5)

        # Definição dos nomes das colunas
        self.tableWidget.setHorizontalHeaderLabels(columns)

        # Preenchimento da tabela
        for row_index, row in enumerate(self._subgroups):
            for col_index, col_name in enumerate(columns):
                # Obter a chave correspondente ao nome da coluna
                property_name = column_to_property.get(col_name)
                if property_name is not None:
                    # Obtendo o valor da propriedade do dicionário
                    cell_value = row.get(property_name, '')  # Aqui pegamos diretamente o valor da propriedade com a 
                    # chave correta
                    # em row
                    # Convertendo o valor para string
                    cell_value_str = str(cell_value)
                    # Criando o item da célula da tabela
                    item = QTableWidgetItem(cell_value_str)
                    # Definindo o item na posição correta na tabela
                    self.tableWidget.setItem(row_index, col_index, item)
                    self.tableWidget.setColumnWidth(col_index, column_size[col_name])


def main():
    app = QApplication(sys.argv)
    window = MyWindow('http://localhost:3003/subgroup')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
