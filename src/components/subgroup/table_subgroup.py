from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAbstractItemView, QCheckBox
from PySide6.QtCore import Qt
import sys

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

        self.setWindowTitle("Exemplo de Tabela")
        self.setGeometry(100, 100, 1024, 400)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(3)  # Definindo o número de linhas
        columns = [
            '',
            'ID',
            'Nome',
            'Quantidade',
            'Despesa Fixa',
            'Total despesa fixa',
            'Total despesa variável',
            'Total Faturamento',
            'Total custo',
            'Total Desconto',
            'Lucro do Subgrupo',
            'Porcentagem Desconto'
            'Quantidade Devolvida',
            'Porcentagem Faturamento'
            'Porcentagem Custo',
            'Porcentagem de Lucro Total',
            'Porcentagem despesa Fixa',
            'Atualizado em',
        ]
        self.tableWidget.setColumnCount(len(columns))  # Definindo o número de colunas

        # Agora você pode chamar o método fetch_subgroup
        self._run_loop_subgroup = loop.run_until_complete(self.fetch_subgroup())

    async def fetch_subgroup(self):
        data = await self._fetch(self._url)
        self._subgroups = data

        # Definição das colunas
        columns = [
            '',
            'ID',
            'Nome',
            'QTD',
            'Despesa Fixa',
            'Total despesa fixa',
            'Total despesa variável',
            'Total Faturamento',
            'Total custo',
            'Total Desconto',
            'Lucro do Subgrupo',
            'Porcentagem Desconto',
            'Quantidade Devolvida',
            'Porcentagem Faturamento',
            'Porcentagem Custo',
            'Porcentagem de Lucro Total',
            'Porcentagem despesa Fixa',
            'Atualizado em',
        ]

        # Mapeamento de nomes de colunas para chaves correspondentes em 'row'
        column_to_property = {
            'ID': 'codSubgroup',
            'Nome': 'nameSubgroup',
            'QTD': 'amountQuantity',
            'Despesa Fixa': 'fixedUnitExpense',
            'Total despesa fixa': 'amountFixed',
            'Total despesa variável': 'amountVariableExpense',
            'Total Faturamento': 'amountInvoicing',
            'Total custo': 'amountCost',
            'Total Desconto': 'amountDiscount',
            'Lucro do Subgrupo': 'subgroupProfit',
            'Porcentagem Desconto': 'discountPercentage',
            'Quantidade Devolvida': 'amountQuantityReturned',
            'Porcentagem Faturamento': 'invoicingPercentage',
            'Porcentagem Custo': 'costPercentage',
            'Porcentagem de Lucro Total': 'subgroupProfitPercentage',
            'Porcentagem despesa Fixa': 'fixedExpensePercentage',
            'Atualizado em': 'updatedAt',
        }

        column_size = {
            'ID': 20,
            'Nome': 230,
            'QTD': 70,
            'Despesa Fixa': 30,
            'Total despesa fixa': 40,
            'Total despesa variável': 40,
            'Total Faturamento': 60,
            'Total custo': 60,
            'Total Desconto': 40,
            'Lucro do Subgrupo': 40,
            'Porcentagem Desconto': 20,
            'Quantidade Devolvida': 30,
            'Porcentagem Faturamento': 20,
            'Porcentagem Custo': 20,
            'Porcentagem de Lucro Total': 20,
            'Porcentagem despesa Fixa': 20,
            'Atualizado em': 40,
        }
        
        # Definindo o número de linhas e colunas na tabela
        self.tableWidget.setRowCount(len(self._subgroups))
        self.tableWidget.setColumnCount(len(columns))

        # Preenchimento da tabela
        for row_index, row in enumerate(self._subgroups):
            for col_index, col_name in enumerate(columns):
                # Obter a chave correspondente ao nome da coluna
                property_name = column_to_property.get(col_name)
                if property_name is not None:
                    # Obtendo o valor da propriedade do dicionário
                    cell_value = row.get(property_name,
                                         '')  # Aqui pegamos diretamente o valor da propriedade com a chave correta em row
                    # Convertendo o valor para string
                    cell_value_str = str(cell_value)
                    # Criando o item da célula da tabela
                    item = QTableWidgetItem(cell_value_str)
                    # Definindo o item na posição correta na tabela
                    self.tableWidget.setItem(row_index, col_index, item)
                    self.tableWidget.setColumnWidth(col_index, column_size[col_name])
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            self.tableWidget.setCellWidget(row_index, 0, checkbox)
            self.tableWidget.setColumnWidth(0, 15)

        # Definição dos nomes das colunas
        self.tableWidget.setHorizontalHeaderLabels(columns)

        # Define que não é permitido editar os valores dos itens da tabela
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Define que quando um item for clicado seleciona todos os elementos daquela linha
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Define que não vai exibir a numeração das linhs
        self.tableWidget.verticalHeader().setVisible(False)
        
        self.setCentralWidget(self.tableWidget)


def main():
    app = QApplication(sys.argv)
    window = MyWindow('http://localhost:3003/subgroup')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
