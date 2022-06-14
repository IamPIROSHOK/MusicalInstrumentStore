import os
import sys
from datetime import datetime
from pprint import pprint

from PySide6.QtCore import QDate
from PySide6.QtGui import Qt

from MyDBInterface import MyDBInterface

os.system('''pyside6-rcc res.qrc -o res_rc.py
pyside6-uic MainWindow.ui > ui_mainwindow.py'''.replace('\n', '&'))

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox

from ui_mainwindow import Ui_MainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # fixes
        self.ui.browser.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # ResizeToContents
        self.ui.browser.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # ResizeToContentsr
        self.ui.browser_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # ResizeToContents
        self.ui.browser_2.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # ResizeToContentsr
        # fixes
        # create db exemplar
        self.db = MyDBInterface()
        self.fill_browser()
        self.fill_browser_2()
        # create db exemplar
        # connects 1
        self.ui.browser.currentCellChanged.connect(self.row_changed)
        self.ui.btn_remove.clicked.connect(self.btn_remove_clicked)
        self.ui.btn_save.clicked.connect(self.btn_save_clicked)
        self.ui.btn_create.clicked.connect(self.btn_create_clicked)

        # connects 2
        self.ui.browser_2.currentCellChanged.connect(self.row_changed_2)
        self.ui.btn_remove_2.clicked.connect(self.btn_remove_2_clicked)
        self.ui.btn_save_2.clicked.connect(self.btn_save_2_clicked)
        self.ui.btn_create_2.clicked.connect(self.btn_create_2_clicked)

        # change 1
        self.ui.input_brand.textChanged.connect(self.inputsChange)
        self.ui.input_price.valueChanged.connect(self.inputsChange)
        self.ui.input_model.textChanged.connect(self.inputsChange)
        self.ui.input_typename.currentTextChanged.connect(self.inputsChange)

        # change 2
        self.ui.input_warehouse.currentTextChanged.connect(self.inputsChange_2)
        self.ui.input_product.currentTextChanged.connect(self.inputsChange_2)
        self.ui.input_number.valueChanged.connect(self.inputsChange_2)

        self.show()

    def fill_browser(self):
        rows = self.db.select_goods()
        self.ui.browser.setRowCount(len(rows))
        for i, row in enumerate(rows):
            id, Brand, Price, Model, ProductType = row
            self.ui.browser.setItem(i, 0, QTableWidgetItem(Brand))
            self.ui.browser.setItem(i, 1, QTableWidgetItem(str(Price)))
            self.ui.browser.setItem(i, 2, QTableWidgetItem(Model))
            self.ui.browser.setItem(i, 3, QTableWidgetItem(ProductType))
            self.ui.browser.item(i, 0).setData(Qt.UserRole, id)
        self.updateAvailability()

    def btn_create_clicked(self):
        Brand = self.ui.input_brand_2.text()
        Price = self.ui.input_price_2.value()
        Model = self.ui.input_model_2.text()
        Type_name = self.ui.input_typename_2.currentText()
        if not self.db.can_i_add__goods(Brand, Model, Type_name):
            QMessageBox.warning(self, 'Ошибка', 'Такие данные уже существуют :(')
            return
        self.db.add_goods(Brand, Price, Model, Type_name)

        self.fill_browser()

    def btn_remove_clicked(self):
        row = self.ui.browser.currentRow()
        id = self.ui.browser.item(row, 0).data(Qt.UserRole)
        self.db.remove_good(id)
        self.ui.browser.removeRow(row)

    def row_changed(self):
        self.updateAvailability()
        rowsCount = self.ui.browser.rowCount()
        currentRow = self.ui.browser.currentRow()
        if currentRow < 0 or currentRow > rowsCount - 1:
            return
        Brand = self.ui.browser.item(currentRow, 0).text()
        Price = int(self.ui.browser.item(currentRow, 1).text())
        Model = self.ui.browser.item(currentRow, 2).text()
        TypeName = self.ui.browser.item(currentRow, 3).text()
        self.ui.input_brand.setText(Brand)
        self.ui.input_price.setValue(Price)
        self.ui.input_model.setText(Model)
        self.ui.input_typename.setCurrentText(TypeName)
        self.ui.btn_save.setEnabled(False)

    def updateAvailability(self):
        rowsCount = self.ui.browser.rowCount()
        currentRow = self.ui.browser.currentRow()
        correctRow = not (currentRow < 0 or currentRow > rowsCount - 1)
        self.ui.btn_remove.setEnabled(rowsCount > 0 and correctRow)

    def inputsChange(self):
        self.ui.btn_save.setEnabled(True)

    def btn_save_clicked(self):
        row = self.ui.browser.currentRow()
        id = self.ui.browser.item(row, 0).data(Qt.UserRole)
        Brand = self.ui.input_brand.text()
        Price = self.ui.input_price.value()
        Model = self.ui.input_model.text()
        TypeName = self.ui.input_typename.currentText()

        NewBrend =self.ui.browser.item(row,0).text()
        NewModel=self.ui.browser.item(row,2).text()
        NewTypeName=self.ui.browser.item(row,3).text()
        is_cell_changed = NewBrend != Brand or NewModel != Model or NewTypeName!=TypeName
        if is_cell_changed and not self.db.can_i_add__goods(Brand, Model, TypeName):
            QMessageBox.warning(self, 'Ошибка', 'Такие данные уже существуют :(')
            return
        self.db.change_good(id, Brand, Price, Model, TypeName)
        self.ui.btn_save.setEnabled(False)
        self.ui.browser.item(row, 0).setText(Brand)
        self.ui.browser.item(row, 1).setText(str(Price))
        self.ui.browser.item(row, 2).setText(Model)
        self.ui.browser.item(row, 3).setText(TypeName)


    ###########################################################################################################

    def fill_browser_2(self):
        rows = self.db.select_warehouses_to_goods()
        self.ui.browser_2.setRowCount(len(rows))
        for i, row in enumerate(rows):
            idWarehouse, idGood, Warehouse, Product, Number = row
            self.ui.browser_2.setItem(i, 0, QTableWidgetItem(Warehouse))
            self.ui.browser_2.setItem(i, 1, QTableWidgetItem(Product))
            self.ui.browser_2.setItem(i, 2, QTableWidgetItem(str(Number)))
        self.updateAvailability_2()

        products = self.db.select_products()
        self.ui.input_product.addItems(products)
        self.ui.input_product_2.addItems(products)
        warehouses = self.db.select_warehouses()
        self.ui.input_warehouse.addItems(warehouses)
        self.ui.input_warehouse_2.addItems(warehouses)

    def updateAvailability_2(self):
        rowsCount = self.ui.browser_2.rowCount()
        currentRow = self.ui.browser_2.currentRow()
        correctRow = not (currentRow < 0 or currentRow > rowsCount - 1)
        self.ui.btn_remove_2.setEnabled(rowsCount > 0 and correctRow)

    def row_changed_2(self):
        self.updateAvailability_2()
        rowsCount = self.ui.browser_2.rowCount()
        currentRow = self.ui.browser_2.currentRow()
        if currentRow < 0 or currentRow > rowsCount - 1:
            return
        Warehouse = self.ui.browser_2.item(currentRow, 0).text()
        Product = self.ui.browser_2.item(currentRow, 1).text()
        Number = int(self.ui.browser_2.item(currentRow, 2).text())
        self.ui.input_warehouse.setCurrentText(Warehouse)
        self.ui.input_product.setCurrentText(Product)
        self.ui.input_number.setValue(Number)
        self.updateAvailability_2()
        self.ui.btn_save_2.setEnabled(False)

    def btn_save_2_clicked(self):
        row = self.ui.browser_2.currentRow()
        warehouse = self.ui.browser_2.item(row, 0).text()
        product = self.ui.browser_2.item(row, 1).text()
        warehouse_new = self.ui.input_warehouse.currentText()
        product_new = self.ui.input_product.currentText()
        number_new = self.ui.input_number.value()
        is_compound_key_changed = warehouse != warehouse_new or product != product_new
        if is_compound_key_changed and not self.db.can_i_add_warehouse_to_goods(warehouse_new, product_new):
            QMessageBox.warning(self, 'Ошибка', 'Такие данные уже существуют :(')
            return
        self.db.del_warehouses_to_goods(warehouse, product)

        self.db.add_warehouses_to_goods(warehouse_new, product_new, number_new)
        self.ui.browser_2.item(row, 0).setText(warehouse_new)
        self.ui.browser_2.item(row, 1).setText(product_new)
        self.ui.browser_2.item(row, 2).setText(str(number_new))

    def btn_create_2_clicked(self):
        warehouse_new = self.ui.input_warehouse_2.currentText()
        product_new = self.ui.input_product_2.currentText()
        number_new = self.ui.input_number_2.value()
        if not self.db.can_i_add_warehouse_to_goods(warehouse_new, product_new):
            QMessageBox.warning(self, 'Ошибка', 'Такие данные уже существуют :(')
            return

        self.db.add_warehouses_to_goods(warehouse_new, product_new, number_new)
        self.fill_browser_2()

    def btn_remove_2_clicked(self):
        row = self.ui.browser_2.currentRow()
        warehouse = self.ui.browser_2.item(row, 0).text()
        product = self.ui.browser_2.item(row, 1).text()
        self.db.del_warehouses_to_goods(warehouse, product)
        self.ui.browser_2.removeRow(row)

    def inputsChange_2(self):
        self.ui.btn_save_2.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec())
