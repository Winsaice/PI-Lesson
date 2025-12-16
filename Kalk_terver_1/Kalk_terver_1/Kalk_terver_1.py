from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtWidgets import (QApplication, QGridLayout, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QTabWidget, QAbstractItemView)
from PyQt5.QtCore import QLine, Qt
import numpy as np
import math

class HorizontalStatsCalculator(QMainWindow):
    # Функиця инициализации программы
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор дискретных случайных величин")
        self.setGeometry(100, 100, 1000, 700)  
        
        # Основополагающие элементы
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.setup_tab1()
        self.setup_tab2()

        self.tabs.addTab(self.tab1, "Расчётные работы")
        self.tabs.addTab(self.tab2, "Ряды распределения")
        self.setCentralWidget(self.tabs)

    # Первая вкладка
    def setup_tab1(self):
        # Основные элементы и их настройки
        self.add_col_btnx = QPushButton("+ Добавить столбец X")
        self.add_col_btny = QPushButton("+ Добавить столбец Y")
        self.del_col_btnx = QPushButton("- Удалить столбец X")
        self.del_col_btny = QPushButton("- Удалить столбец Y")
        self.l_koefx = QLabel("Введите коэфицент для X:")
        self.koefx = QLineEdit()
        self.koefx.setValidator(QIntValidator(1, 999, self))
        self.l_stepx = QLabel("Введите степень для X:")
        self.stepx = QLineEdit()
        self.stepx.setValidator(QIntValidator(1, 999, self))
        self.l_koefy = QLabel("Введите коэфицент для Y:")
        self.koefy = QLineEdit()
        self.koefy.setValidator(QIntValidator(1, 999, self))
        self.l_stepy = QLabel("Введите степень для Y:") 
        self.stepy = QLineEdit()
        self.stepy.setValidator(QIntValidator(1, 999, self))
        self.calculate_btn = QPushButton("Рассчитать")
        self.clear_btn = QPushButton("О!")
        self.result_labelx = QLabel("Результаты для X:")
        self.result_labely = QLabel("Результаты для Y:")
        self.table = QTableWidget() 
        self.table.setRowCount(2) 
        self.table.setColumnCount(5)
        self.table.setVerticalHeaderLabels(["X (значения)", "P (вероятности)"])
        self.table.resizeColumnsToContents()
        self.table2 = QTableWidget() 
        self.table2.setRowCount(2) 
        self.table2.setColumnCount(5)
        self.table2.setVerticalHeaderLabels(["Y (значения)", "P (вероятности)"])
        self.table2.resizeColumnsToContents()
        # Стили
        self.table.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid #cccccc;
                }
            QTableWidget::item::selected 
                {
                Color:red; 
                Background: #EFF4FF; 
                }
        """)
        self.table2.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid #cccccc;
                }
            QTableWidget::item::selected 
                {
                Color:red; 
                Background: #EFF4FF; 
                }
        """)
        self.result_labelx.setStyleSheet("""
            font: 14px;
        """)
        self.result_labely.setStyleSheet("""
            font: 14px;
        """)

        # Компоновка
        main_layout = QVBoxLayout()
        btn_layout = QGridLayout()
        l_layout = QHBoxLayout()

        main_layout.addWidget(self.table)
        main_layout.addWidget(self.table2)
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(l_layout)
        
        btn_layout.addWidget(self.add_col_btnx, 0, 0)
        btn_layout.addWidget(self.del_col_btnx, 0, 1)
        btn_layout.addWidget(self.l_koefx, 0, 2)
        btn_layout.addWidget(self.koefx, 0, 3)
        btn_layout.addWidget(self.l_stepx, 0, 4)
        btn_layout.addWidget(self.stepx, 0, 5)
        btn_layout.addWidget(self.clear_btn, 0, 6)
        btn_layout.addWidget(self.add_col_btny, 1, 0)
        btn_layout.addWidget(self.del_col_btny, 1, 1)
        btn_layout.addWidget(self.l_koefy, 1, 2)
        btn_layout.addWidget(self.koefy, 1, 3)
        btn_layout.addWidget(self.l_stepy, 1, 4)
        btn_layout.addWidget(self.stepy, 1, 5)
        btn_layout.addWidget(self.calculate_btn, 1, 6)
        l_layout.addWidget(self.result_labelx)
        l_layout.addWidget(self.result_labely)

        self.tab1.setLayout(main_layout)

        # Сигналы
        self.add_col_btnx.clicked.connect(self.add_columnx)
        self.del_col_btnx.clicked.connect(self.delete_columnx)
        self.add_col_btny.clicked.connect(self.add_columny)
        self.del_col_btny.clicked.connect(self.delete_columny)
        self.koefx.editingFinished.connect(self.save_koefx)
        self.koefy.editingFinished.connect(self.save_koefy)
        self.stepx.editingFinished.connect(self.save_stepx)
        self.stepy.editingFinished.connect(self.save_stepy)
        self.calculate_btn.clicked.connect(self.calculate_stats)

    # Функции первой вкладки
    # Добавление колонок
    def add_columnx(self):
        self.table.insertColumn(self.table.columnCount())
        self.table.resizeColumnsToContents()

    def add_columny(self):
        self.table2.insertColumn(self.table2.columnCount())
        self.table2.resizeColumnsToContents()

    # Удаление колонок
    def delete_columnx(self):
        if self.table.columnCount() > 1:  
            self.table.removeColumn(self.table.columnCount() - 1)

    def delete_columny(self):
        if self.table2.columnCount() > 1:  
            self.table2.removeColumn(self.table2.columnCount() - 1)

    # Сохранение коэфицента
    def save_koefx(self):
        global koef_itemx
        koef_itemx = self.koefx.text()

    def save_koefy(self):
        global koef_itemy
        koef_itemy = self.koefy.text()
        
    # Сохранение степени
    def save_stepx(self):
        global step_itemx
        step_itemx = self.stepx.text()

    def save_stepy(self):
        global step_itemy
        step_itemy = self.stepy.text()
    
    # Основная расчётная функция
    def calculate_stats(self):
        try:
            # Проверка коэфицента
            koef_itemx = self.koefx.text()
            if not koef_itemx:
                koef_itemx = 1.0
            elif koef_itemx:
                koef_itemx = int(koef_itemx)

            koef_itemy = self.koefy.text()
            if not koef_itemy:
                koef_itemy = 1.0
            elif koef_itemy:
                koef_itemy = int(koef_itemy)

            # Проверка степени
            step_itemx = self.stepx.text()
            if not step_itemx:
                step_itemx = 1.0
            elif step_itemx:
                step_itemx = int(step_itemx)

            step_itemy = self.stepy.text()
            if not step_itemy:
                step_itemy = 1.0
            elif step_itemy:
                step_itemy = int(step_itemy)

            # Сбор данных
            x_values = []
            y_values = []
            p_valuesx = []
            p_valuesy = []
            p_sumx = 0.0
            p_sumy = 0.0
            for col in range(self.table.columnCount()):
                x_item = self.table.item(0, col)  
                p_itemx = self.table.item(1, col)
                try:
                    if x_item:
                        x_values.append(int(x_item.text()) ** step_itemx * koef_itemx)
                    if p_itemx:
                        p_valuesx.append(float(p_itemx.text()))
                        p_sumx += (float(p_itemx.text()))
                except:
                    raise ValueError("Введите данные в таблицу X!")
            col = 0
            for col in range(self.table2.columnCount()):
                y_item = self.table2.item(0, col)  
                p_itemy = self.table2.item(1, col)
                try:
                    if y_item:
                        y_values.append(int(y_item.text()) ** step_itemy * koef_itemy)
                    if p_itemy:
                        p_valuesy.append(float(p_itemy.text()))
                        p_sumy += (float(p_itemy.text()))
                except:
                    raise ValueError("Введите данные в таблицу Y!")

            # Проверки
            if len(x_values) != self.table.columnCount():
                raise ValueError("Введите данные в таблицу X!")
            if len(y_values) != self.table2.columnCount():
                raise ValueError("Введите данные в таблицу Y!")
            if len(p_valuesx) != self.table.columnCount():
                raise ValueError("Введите данные в таблицу X!")
            if len(p_valuesy) != self.table2.columnCount():
                raise ValueError("Введите данные в таблицу Y!")
            if not math.isclose(p_sumx, 1.0, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("Сумма вероятностей X не равна 1!")
            if not math.isclose(p_sumy, 1.0, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("Сумма вероятностей Y не равна 1!")

            # Конвертация в numpy массивы
            x_values = np.array(x_values)
            p_valuesx = np.array(p_valuesx)
            
            # Расчёты
            mat = np.sum(x_values * p_valuesx)
            alf1 = mat
            alf2 = np.sum(p_valuesx * np.power(x_values, 2))
            alf3 = np.sum(p_valuesx * np.power(x_values, 3))
            alf4 = np.sum(p_valuesx * np.power(x_values, 4))
            alf5 = np.sum(p_valuesx * np.power(x_values, 5))
            dis = np.sum(alf2 - mat**2)
            sig = np.sqrt(dis)
            mu1 = alf1 - alf1**1
            mu2 = alf2 - alf1**2 
            mu3 = alf3 - alf1**3
            mu4 = alf4 - alf1**4
            mu5 = alf5 - alf1**5 
            asi = mu3 / (sig**3)  
            eks = (mu4 / np.power(sig, 4)) - 3 
            
            # Преобразование x_values для читаемого вывода
            v = ""
            for i in range(len(x_values)):
                sxo = x_values[i]
                sxo = str(int(sxo))
                if sxo == str(int(x_values[-1])):
                    v += sxo + "."
                else:
                    v += sxo + ", "

            # Вывод результатов
            result_text = (f"Результаты для списка по X: {v}\n"
                f"Cумма вероятностей: {p_sumx:.4f}\n"
                f"Мат. ожидание: {mat:.4f}\n"
                f"Дисперсия: {dis:.4f}\n"
                f"Сигма: {sig:.4f}\n"
                f"a1: {alf1:.4f}, a2: {alf2:.4f}, a3: {alf3:.4f}, a4: {alf4:.4f}, a5: {alf5:.4f}\n"
                f"μ1: {mu1:.4f}, μ2: {mu2:.4f}, μ3: {mu3:.4f}, μ4: {mu4:.4f}, μ5: {mu5:.4f}\n"
                f"Асимметрия: {asi:.4f}\n"
                f"Эксцесс~: {eks:.4f}")
            self.result_labelx.setText(result_text)

            # Конвертация в numpy массивы
            y_values = np.array(y_values)
            p_valuesy = np.array(p_valuesy)
            
            # Расчёты
            mat = np.sum(y_values * p_valuesy)
            alf1 = mat
            alf2 = np.sum(p_valuesy * np.power(y_values, 2))
            alf3 = np.sum(p_valuesy * np.power(y_values, 3))
            alf4 = np.sum(p_valuesy * np.power(y_values, 4))
            alf5 = np.sum(p_valuesy * np.power(y_values, 5))
            dis = np.sum(alf2 - mat**2)
            sig = np.sqrt(dis)
            mu1 = alf1 - alf1**1
            mu2 = alf2 - alf1**2 
            mu3 = alf3 - alf1**3
            mu4 = alf4 - alf1**4
            mu5 = alf5 - alf1**5 
            asi = mu3 / (sig**3)  
            eks = (mu4 / np.power(sig, 4)) - 3 
            
            # Преобразование x_values для читаемого вывода
            v = ""
            for i in range(len(y_values)):
                sxo = y_values[i]
                sxo = str(int(sxo))
                if sxo == str(int(y_values[-1])):
                    v += sxo + "."
                else:
                    v += sxo + ", "

            # Вывод результатов
            result_text = (f"Результаты для списка по Y: {v}\n"
                f"Cумма вероятностей: {p_sumy:.4f}\n"
                f"Мат. ожидание: {mat:.4f}\n"
                f"Дисперсия: {dis:.4f}\n"
                f"Сигма: {sig:.4f}\n"
                f"a1: {alf1:.4f}, a2: {alf2:.4f}, a3: {alf3:.4f}, a4: {alf4:.4f}, a5: {alf5:.4f}\n"
                f"μ1: {mu1:.4f}, μ2: {mu2:.4f}, μ3: {mu3:.4f}, μ4: {mu4:.4f}, μ5: {mu5:.4f}\n"
                f"Асимметрия: {asi:.4f}\n"
                f"Эксцесс~: {eks:.4f}")
            self.result_labely.setText(result_text)


        # Вывод ошибок
        except ValueError as e:
            self.result_labelx.setText(f"Ошибка: {str(e)}")
            self.result_labely.setText("")

    # Вторая вкладка
    def setup_tab2(self):
        # Основные элементы и их настройки
        self.table_input = QTableWidget() 
        self.table_input.setRowCount(3) 
        self.table_input.setColumnCount(3)
        item = QTableWidgetItem("*  | -\n+ | p")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table_input.setItem(0, 0, item)
        item = QTableWidgetItem("Y")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table_input.setItem(0, 1, item)
        item = QTableWidgetItem("X")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table_input.setItem(1, 0, item)
        item = QTableWidgetItem("P")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table_input.setItem(1, 1, item)
        self.table_input.setMinimumSize(0, 150)
        self.table_input.setMaximumSize(99999, 99999)
        self.table_input.resizeRowsToContents()
        self.table_input.resizeColumnsToContents()
        self.res_table = QTableWidget()
        self.res_table.setMinimumSize(0, 125)
        self.res_table.setMaximumSize(99999, 125)
        self.res_table.setRowCount(2)
        self.res_table.setColumnCount(0)
        self.res_table.setVerticalHeaderLabels(["X * Y", "P (вероятности)"])
        self.res_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.res_table2 = QTableWidget()
        self.res_table2.setMinimumSize(0, 125)
        self.res_table2.setMaximumSize(99999, 125)
        self.res_table2.setRowCount(2)
        self.res_table2.setColumnCount(0)
        self.res_table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.res_table2.setVerticalHeaderLabels(["X - Y", "P (вероятности)"])
        self.res_table3 = QTableWidget()
        self.res_table3.setMinimumSize(0, 125)
        self.res_table3.setMaximumSize(99999, 125)
        self.res_table3.setRowCount(2)
        self.res_table3.setColumnCount(0)
        self.res_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.res_table3.setVerticalHeaderLabels(["X + Y", "P (вероятности)"])
        self.add_col_btn2 = QPushButton("+ Добавить столбец")
        self.add_row_btn2 = QPushButton("+ Добавить строку")
        self.del_col_btn2 = QPushButton("- Удалить столбец")
        self.del_row_btn2 = QPushButton("- Удалить строку")
        self.calculate_btn2 = QPushButton("Рассчитать")
        self.clear_btn2 = QPushButton("Очистить!")
        self.l_koef_x = QLabel("Введите коэфицент для X:")
        self.koef_x = QLineEdit()
        self.koef_x.setValidator(QIntValidator(1, 999, self))
        self.l_step_x = QLabel("Введите степень для X:")
        self.step_x = QLineEdit()
        self.step_x.setValidator(QIntValidator(1, 999, self))
        self.l_koef_y = QLabel("Введите коэфицент для Y:")
        self.koef_y = QLineEdit()
        self.koef_y.setValidator(QIntValidator(1, 999, self))
        self.l_step_y = QLabel("Введите степень для Y:")
        self.step_y = QLineEdit()
        self.step_y.setValidator(QIntValidator(1, 999, self))
        self.result_label2 = QLabel("Результаты: ")

        # Стили
        self.table_input.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid #cccccc;
                }
            QTableWidget::item::selected 
                {
                Color:red; 
                Background: #EFF4FF; 
                }
        """)
        self.res_table.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid #cccccc;
                }
            QTableWidget::item::selected 
                {
                Color:red; 
                Background: #EFF4FF; 
                }
        """)
        self.res_table2.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid #cccccc;
                }
            QTableWidget::item::selected 
                {
                Color:red; 
                Background: #EFF4FF; 
                }
        """)
        self.res_table3.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid #cccccc;
                }
            QTableWidget::item::selected 
                {
                Color:red; 
                Background: #EFF4FF; 
                }
        """)
        self.result_label2.setStyleSheet("""
            font: 14px;
        """)
        
        # Компановка
        main_layout = QVBoxLayout()
        btn_grid = QGridLayout()
        btn_layout2 = QHBoxLayout()
        res_layout = QVBoxLayout()

        main_layout.addWidget(self.table_input)
        main_layout.addLayout(btn_grid)
        main_layout.addLayout(btn_layout2)
        main_layout.addWidget(self.result_label2)
        main_layout.addLayout(res_layout)
        
        btn_grid.addWidget(self.add_row_btn2, 0, 0)
        btn_grid.addWidget(self.del_row_btn2, 1, 0)
        btn_grid.addWidget(self.add_col_btn2, 0, 1)
        btn_grid.addWidget(self.del_col_btn2, 1, 1)
        btn_grid.addWidget(self.l_koef_x, 0, 2)
        btn_grid.addWidget(self.koef_x, 0, 3)
        btn_grid.addWidget(self.l_step_x, 1, 2)
        btn_grid.addWidget(self.step_x, 1, 3)
        btn_grid.addWidget(self.l_koef_y, 0, 4)
        btn_grid.addWidget(self.koef_y, 0, 5)
        btn_grid.addWidget(self.l_step_y, 1, 4)
        btn_grid.addWidget(self.step_y, 1, 5)
        btn_grid.addWidget(self.clear_btn2, 0, 6)
        btn_grid.addWidget(self.calculate_btn2, 1, 6)
        
        res_layout.addWidget(self.res_table)
        res_layout.addWidget(self.res_table2)
        res_layout.addWidget(self.res_table3)

        self.tab2.setLayout(main_layout)

        # Подключение сигналов
        self.add_col_btn2.clicked.connect(self.add_column2)
        self.add_row_btn2.clicked.connect(self.add_row2)
        self.del_col_btn2.clicked.connect(self.delete_column2)
        self.del_row_btn2.clicked.connect(self.delete_row2)
        self.calculate_btn2.clicked.connect(self.calculate_stats2)
        self.clear_btn2.clicked.connect(self.clear_tables2)

    # Функции второй вкладки
    # Добавление строк
    def add_row2(self):
        self.table_input.insertRow(self.table_input.rowCount())
        self.table_input.resizeRowsToContents()
        self.table_input.resizeColumnsToContents()

    # Добавление колонок
    def add_column2(self):
        self.table_input.insertColumn(self.table_input.columnCount())
        self.table_input.resizeRowsToContents()
        self.table_input.resizeColumnsToContents()

    # Удаление строк
    def delete_row2(self):
        if self.table_input.rowCount() > 3:  
            self.table_input.removeRow(self.table_input.rowCount() - 1)

    # Удаление колонок
    def delete_column2(self):
        if self.table_input.columnCount() > 3:  
            self.table_input.removeColumn(self.table_input.columnCount() - 1)

    # Сохранение коэфицента x
    def save_koef_x(self):
        global koef_item_x
        koef_item_x = self.koef_x.text()
        
    # Сохранение степени x
    def save_step_x(self):
        global step_item_x
        step_item_x = self.step_x.text()

    # Сохранение коэфицента y
    def save_koef_y(self):
        global koef_item_y
        koef_item_y = self.koef_y.text()
        
    # Сохранение степени y
    def save_step_y(self):
        global step_item_y
        step_item_y = self.step_y.text()

    # Очистка таблиц
    def clear_tables2(self):
        while self.table_input.rowCount() > 2:  
            self.table_input.removeRow(self.table_input.rowCount() - 1)
        else:
            self.table_input.insertRow(self.table_input.rowCount())

        while self.table_input.columnCount() > 2:  
            self.table_input.removeColumn(self.table_input.columnCount() - 1)
        else:
            self.table_input.insertColumn(self.table_input.columnCount())
        self.table_input.resizeColumnsToContents()

        while self.res_table.columnCount() > 0:
            self.res_table.removeColumn(self.res_table.columnCount() - 1)
        while self.res_table2.columnCount() > 0:
            self.res_table2.removeColumn(self.res_table2.columnCount() - 1)
        while self.res_table3.columnCount() > 0:
            self.res_table3.removeColumn(self.res_table3.columnCount() - 1)

        self.result_label2.setText("Результаты: ")

    # Основная расчётная функция
    def calculate_stats2(self):
        try:
            # Проверка коэфицента x
            koef_item_x = self.koef_x.text()
            if not koef_item_x:
                koef_item_x = 1.0
            elif koef_item_x:
                koef_item_x = int(koef_item_x)
            
            # Проверка степени x
            step_item_x = self.step_x.text()
            if not step_item_x:
                step_item_x = 1.0
            elif step_item_x:
                step_item_x = int(step_item_x)
 
            # Проверка коэфицента y
            koef_item_y = self.koef_y.text()
            if not koef_item_y:
                koef_item_y = 1.0
            elif koef_item_y:
                koef_item_y = int(koef_item_y)

            # Проверка степени y
            step_item_y = self.step_y.text()
            if not step_item_y:
                step_item_y = 1.0
            elif step_item_y:
                step_item_y = int(step_item_y)
 
            # Сбор данных
            x_values2 = []
            y_values2 = []
            px_values = []
            py_values = []
            px_sum = 0.0
            py_sum = 0.0
            for row in range(self.table_input.rowCount()):
                x_item2 = self.table_input.item(row+2, 0)  
                px_item2 = self.table_input.item(row+2, 1) 
                try:
                    if x_item2:
                        x_values2.append(int(x_item2.text()) ** step_item_x * koef_item_x)
                    if px_item2:
                        px_values.append(float(px_item2.text()))
                        px_sum += (float(px_item2.text()))
                except:
                    raise ValueError("Введите данные в таблицу!")
            for col2 in range(self.table_input.columnCount()):
                y_item2 = self.table_input.item(0, col2+2)  
                py_item2 = self.table_input.item(1, col2+2) 
                try:
                    if y_item2:
                        y_values2.append(int(y_item2.text()) ** step_item_y * koef_item_y)
                    if py_item2:
                        py_values.append(float(py_item2.text()))
                        py_sum += (float(py_item2.text()))
                except:
                    raise ValueError("Введите данные в таблицу!")

            # Проверки
            if len(x_values2) + 2 != self.table_input.rowCount():
                raise ValueError("Введите данные в таблицу!")
            if len(y_values2) + 2 != self.table_input.columnCount():
                raise ValueError("Введите данные в таблицу!")
            if len(px_values) + 2 != self.table_input.rowCount():
                raise ValueError("Введите данные в таблицу!")
            if len(py_values) + 2 != self.table_input.columnCount():
                raise ValueError("Введите данные в таблицу!")
            if not math.isclose(px_sum, 1.0, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("Сумма вероятностей X не равна 1!")
            if not math.isclose(py_sum, 1.0, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("Сумма вероятностей Y не равна 1!")

            # Расчёты для вводной таблицы
            list1 = []
            list2 = []
            list3 = []
            list4 = []
            list4_2 = []
            list4_3 = []
            for xr in range(len(x_values2)):
                for yc in range(len(y_values2)):
                    otv1 = x_values2[xr] * y_values2[yc]
                    otv1 = int(otv1)
                    list1.append(otv1)
                    otv2 = x_values2[xr] - y_values2[yc]
                    otv2 = int(otv2)
                    list2.append(otv2)
                    otv3 = x_values2[xr] + y_values2[yc]
                    otv3 = int(otv3)
                    list3.append(otv3)
                    otv4 = px_values[xr] * py_values[yc]
                    list4.append(otv4)
                    list4_2.append(otv4)
                    list4_3.append(otv4)
                    item = QTableWidgetItem(f"{otv1}  |  {otv2}\n{otv3}  |  {otv4:.4f}")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_input.setItem(xr + 2, yc + 2, item) 
                    self.table_input.resizeRowsToContents()
                    self.table_input.resizeColumnsToContents()

            # Расчёты для пер
            otr = 0
            otr2 = 0
            while otr < len(list1):
                otr2 = otr + 1
                list1, list4 = zip(*sorted(zip(list1, list4)))
                list1 = list(list1)
                list4 = list(list4)
                while otr2 < len(list1):
                    if list1[otr] == list1[otr2]:
                        list4[otr] += list4[otr2]
                        del list1[otr]
                        del list4[otr2]
                    else:
                        otr2 += 1
                if self.res_table.columnCount() < len(list1):
                    self.res_table.insertColumn(self.res_table.columnCount())
                self.res_table.setItem(0, otr, QTableWidgetItem(f"{list1[otr]}"))
                self.res_table.setItem(1, otr, QTableWidgetItem(f"{list4[otr]:.4f}"))
                otr += 1
                if self.res_table.columnCount() > len(list1):
                    self.res_table.removeColumn(self.res_table.columnCount() - (self.res_table.columnCount() - len(list1)))
                self.res_table.resizeColumnsToContents()

            otr = 0
            otr2 = 0
            while otr < len(list2):
                otr2 = otr + 1
                list2, list4_2 = zip(*sorted(zip(list2, list4_2)))
                list2 = list(list2)
                list4_2 = list(list4_2)
                while otr2 < len(list2):
                    if list2[otr] == list2[otr2]:
                        list4_2[otr] += list4_2[otr2]
                        del list2[otr]
                        del list4_2[otr2]
                    else:
                        otr2 += 1
                if self.res_table2.columnCount() < len(list2):
                    self.res_table2.insertColumn(self.res_table2.columnCount())
                self.res_table2.setItem(0, otr, QTableWidgetItem(f"{list2[otr]}"))
                self.res_table2.setItem(1, otr, QTableWidgetItem(f"{list4_2[otr]:.4f}"))
                otr += 1
                if self.res_table2.columnCount() > len(list2):
                    self.res_table2.removeColumn(self.res_table2.columnCount() - (self.res_table2.columnCount() - len(list2)))
                self.res_table2.resizeColumnsToContents()

            otr = 0
            otr2 = 0
            while otr < len(list3):
                otr2 = otr + 1
                list3, list4_3 = zip(*sorted(zip(list3, list4_3)))
                list3 = list(list3)
                list4_3 = list(list4_3)
                while otr2 < len(list3):
                    if list3[otr] == list3[otr2]:
                        list4_3[otr] += list4_3[otr2]
                        del list3[otr]
                        del list4_3[otr2]
                    else:
                        otr2 += 1
                if self.res_table3.columnCount() < len(list3):
                    self.res_table3.insertColumn(self.res_table3.columnCount())
                self.res_table3.setItem(0, otr, QTableWidgetItem(f"{list3[otr]}"))
                self.res_table3.setItem(1, otr, QTableWidgetItem(f"{list4_3[otr]:.4f}"))
                otr += 1
                if self.res_table3.columnCount() > len(list3):
                    self.res_table3.removeColumn(self.res_table3.columnCount() - (self.res_table3.columnCount() - len(list3)))
                self.res_table3.resizeColumnsToContents()

            # Читабельный вывод x_values2, y_values2
            v = ""
            h = ""
            for i in range(len(x_values2)):
                sxo = x_values2[i]
                sxo = str(int(sxo))        
                if sxo == str(int(x_values2[-1])):
                    v += sxo + "."
                else:
                    v += sxo + ", "
            for i in range(len(y_values2)):
                syo = y_values2[i]
                syo = str(int(syo))
                if syo == str(int(y_values2[-1])):
                    h += syo + "."
                else:
                    h += syo + ", "

            self.result_label2.setText(f"Результаты для строк:\nX:{v}\nY:{h}")

        # Вывод ошибок
        except ValueError as e:
            self.result_label2.setText(f"Ошибка: {str(e)}")
            print(f"Ошибка: {str(e)}")

# Запуск программы
if __name__ == "__main__":
    app = QApplication([])
    window = HorizontalStatsCalculator()
    window.show()
    app.exec_()
