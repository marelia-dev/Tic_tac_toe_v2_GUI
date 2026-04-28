import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QLabel
from PyQt6.QtCore import QTimer, Qt
from ui.main_ui import Ui_MainWindow
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtGui import QIcon

from models.game import Zaidimas
from models.players import Zaidejas
from models.cpu import CPUZaidejas
from models.scores import Skaiciuokle


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("TIC TAC TOE v2")
        self.resize(700, 720)

        self.skaiciuokle = Skaiciuokle()
        self.current_game = None
        self.zaidejas1 = None
        self.zaidejas2 = None

        self.buttons = [self.ui.btn_1, self.ui.btn_2, self.ui.btn_3,
                        self.ui.btn_4, self.ui.btn_5, self.ui.btn_6,
                        self.ui.btn_7, self.ui.btn_8, self.ui.btn_9]

        # === ФИКС СЪЕЗЖАНИЯ КОЛОНОК ===
        for btn in self.buttons:
            btn.setFixedSize(150, 130)  # размер кнопок
            btn.setStyleSheet("""
                        QPushButton {
                            font-size: 70px;             # размер символов
                            font-weight: bold;
                            qproperty-alignment: AlignCenter;
                            background-color: #2d2d2d;
                            border: 2px solid #555555;
                            border-radius: 8px;
                        }
                    """)

        # Анимация заголовка
        self.title_labels = [self.ui.lbl_t1, self.ui.lbl_i1, self.ui.lbl_c,
                             self.ui.lbl_t2, self.ui.lbl_a, self.ui.lbl_c2,
                             self.ui.lbl_t3, self.ui.lbl_o, self.ui.lbl_e]
        self.colors = ["#FF5252", "#FF9800", "#FFEB3B", "#4CAF50", "#2196F3", "#9C27B0", "#E91E63"]
        self.title_offset = 0

        self.title_timer = QTimer(self)
        self.title_timer.timeout.connect(self.animate_title)
        self.title_timer.start(250)

        # Подключение кнопок
        self.ui.btn_new_game.clicked.connect(self.show_choose_players)
        self.ui.btn_stats.clicked.connect(self.show_stats)
        self.ui.btn_add_player.clicked.connect(self.add_player)
        self.ui.btn_exit.clicked.connect(self.close)

        self.ui.btn_back_to_menu.clicked.connect(self.show_main_menu)
        self.ui.btn_back_to_menu_from_game.clicked.connect(self.show_main_menu)
        self.ui.btn_back_from_stats.clicked.connect(self.show_main_menu)
        self.ui.btn_start_game.clicked.connect(self.start_new_game)
        # Меню "Apie"
        self.ui.menuApie.setTitle("Apie")

        # Создаём действие и сразу подключаем
        action = self.ui.menuApie.addAction("Apie programą")
        action.triggered.connect(self.show_about)

        self.update_player_lists()
        # Подключаем иконку приложения
        from PyQt6.QtGui import QIcon
        icon = QIcon("ttt.ico")
        self.setWindowIcon(icon)

        # Чтобы иконка была и в QMessageBox, QInputDialog и т.д.
        app = QApplication.instance()
        if app:
            app.setWindowIcon(icon)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_menu)

        self.footer_label = QLabel("v2.0  •  Sukūrė marelia-dev", self)
        self.footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer_label.setStyleSheet("color: #777777; font-size: 12px;")
        self.footer_label.setGeometry(0, self.height() - 40, self.width(), 30)

        # Обновляем позицию при изменении размера окна
        self.resizeEvent = self.custom_resize_event

    def custom_resize_event(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'footer_label'):
            self.footer_label.setGeometry(0, self.height() - 40, self.width(), 30)

    def animate_title(self):
        for i, label in enumerate(self.title_labels):
            color = self.colors[(i + self.title_offset) % len(self.colors)]
            label.setStyleSheet(f"color: {color};")
        self.title_offset = (self.title_offset + 1) % len(self.colors)

    def update_player_lists(self):
        real_players = list(self.skaiciuokle.skaicius.keys())
        cpu_options = ["CPU Lengvas", "CPU Vidutinis", "CPU Sunkus"]
        all_options = real_players + cpu_options

        self.ui.combo_player1.clear()
        self.ui.combo_player2.clear()
        self.ui.combo_player1.addItems(all_options)
        self.ui.combo_player2.addItems(all_options)

    def show_main_menu(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_menu)
        self.title_timer.start()
        self.clear_game_board()

    def show_choose_players(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_choose_players)
        self.title_timer.stop()

    def start_new_game(self):
        name1 = self.ui.combo_player1.currentText()
        name2 = self.ui.combo_player2.currentText()

        if name1 == name2 and not (name1.startswith("CPU") and name2.startswith("CPU")):
            QMessageBox.warning(self, "Klaida", "Žaidėjai turi būti skirtingi!")
            return

        self.zaidejas1 = self.create_player(name1)
        self.zaidejas2 = self.create_player(name2)

        self.current_game = Zaidimas(self.zaidejas1, self.zaidejas2)

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_game)
        self.title_timer.stop()

        self.ui.lbl_game_title.setText(f"{self.zaidejas1} vs {self.zaidejas2}")
        self.ui.lbl_current_player.setText(f"Eilė: {self.zaidejas1}")

        self.clear_game_board()

        for i, btn in enumerate(self.buttons):
            try:
                btn.clicked.disconnect()
            except:
                pass
            btn.clicked.connect(lambda checked=False, pos=i+1: self.make_move(pos))

        if isinstance(self.zaidejas1, CPUZaidejas):
            QTimer.singleShot(1000, self.cpu_move)

    def create_player(self, name: str):
        if name.startswith("CPU"):
            level = {"CPU Lengvas": 1, "CPU Vidutinis": 2, "CPU Sunkus": 3}.get(name, 1)
            return CPUZaidejas("CPU", name, level=level)
        else:
            parts = name.split(maxsplit=1)
            return Zaidejas(parts[0], parts[1] if len(parts) > 1 else "")

    def make_move(self, poz: int):
        if not self.current_game or isinstance(self.current_game.einantis, CPUZaidejas):
            return
        if self.current_game.laukas.uzimtas(poz):
            return

        simbolis = "❌" if self.current_game.einantis == self.current_game.zaidejas1 else "⭕"
        self.buttons[poz-1].setText(simbolis)
        self.current_game.padaryti_ejima(poz)

        if self.check_game_end():
            return

        self.current_game.einantis = self.current_game.zaidejas2 if self.current_game.einantis == self.current_game.zaidejas1 else self.current_game.zaidejas1
        self.ui.lbl_current_player.setText(f"Eilė: {self.current_game.einantis}")

        if isinstance(self.current_game.einantis, CPUZaidejas):
            QTimer.singleShot(1000, self.cpu_move)

    def cpu_move(self):
        if not self.current_game or not isinstance(self.current_game.einantis, CPUZaidejas):
            return

        poz = self.current_game.einantis.gauti_ejima(self.current_game.laukas)
        simbolis = "❌" if self.current_game.einantis == self.current_game.zaidejas1 else "⭕"

        self.buttons[poz-1].setText(simbolis)
        self.current_game.padaryti_ejima(poz)

        if self.check_game_end():
            return

        self.current_game.einantis = self.current_game.zaidejas2 if self.current_game.einantis == self.current_game.zaidejas1 else self.current_game.zaidejas1
        self.ui.lbl_current_player.setText(f"Eilė: {self.current_game.einantis}")

        if isinstance(self.current_game.einantis, CPUZaidejas):
            QTimer.singleShot(1000, self.cpu_move)

    def check_game_end(self):
        if self.current_game.laukas.baigta():
            winner = self.current_game.einantis
            QMessageBox.information(self, "Žaidimas baigtas", f"Laimėjo {winner}!              ")

            # === СОХРАНЯЕМ РЕЗУЛЬТАТ В СТАТИСТИКУ ===
            if self.zaidejas1 and self.zaidejas2:
                # Сохраняем для обоих игроков
                self.skaiciuokle.prideti_rezultata(self.zaidejas1, self.zaidejas2, winner)

            self.ask_play_again()
            return True

        if self.current_game.laukas.lygiosios():
            QMessageBox.information(self, "Žaidimas baigtas", "Lygiosios!                   ")

            # === СОХРАНЯЕМ НИЧЬЮ ===
            if self.zaidejas1 and self.zaidejas2:
                self.skaiciuokle.prideti_rezultata(self.zaidejas1, self.zaidejas2, None)

            self.ask_play_again()
            return True
        return False

    def ask_play_again(self):
        reply = QMessageBox.question(
            self,
            "Žaidimas baigtas",
            "Ar norite žaisti dar kartą su tais pačiais žaidėjais?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.start_new_game()
        else:
            self.show_main_menu()

    def clear_game_board(self):
        for btn in self.buttons:
            btn.setText("")
            btn.setEnabled(True)

    def show_stats(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_stats)
        self.title_timer.stop()
        self.load_statistics()

    def load_statistics(self):
        """Загружаем статистику в таблицу"""
        table = self.ui.table_stats

        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Žaidėjas", "Pergalės", "Pralaimėjimai", "Lygiosios", "Viso žaidimų"])

        stats = self.skaiciuokle.skaicius
        table.setRowCount(len(stats))

        row = 0
        for full_name, data in stats.items():
            self.ui.table_stats.setItem(row, 0, QTableWidgetItem(full_name.title()))
            self.ui.table_stats.setItem(row, 1, QTableWidgetItem(str(data.get('p', 0))))
            self.ui.table_stats.setItem(row, 2, QTableWidgetItem(str(data.get('pr', 0))))
            self.ui.table_stats.setItem(row, 3, QTableWidgetItem(str(data.get('l', 0))))
            self.ui.table_stats.setItem(row, 4, QTableWidgetItem(str(data.get('total_games', 0))))
            row += 1

        # === ТВОИ ЖЕЛАЕМЫЕ ШИРИНЫ КОЛОНОК ===
        table.setColumnWidth(0, 120)  # Žaidėjas
        table.setColumnWidth(1, 120)  # Pergalės
        table.setColumnWidth(2, 120)  # Pralaimėjimai
        table.setColumnWidth(3, 120)  # Lygiosios
        table.setColumnWidth(4, 125)  # Viso žaidimų

        table.horizontalHeader().setStretchLastSection(False)  # не растягивать последнюю

    def add_player(self):
        from PyQt6.QtGui import QIcon

        dialog = QInputDialog(self)
        dialog.setWindowTitle("Pridėti žaidėją")
        dialog.setLabelText("Įveskite vardą ir pavardę:")
        dialog.resize(450, 140)
        dialog.setWindowIcon(QIcon("ttt.ico"))

        ok = dialog.exec()
        vardas = dialog.textValue()

        if ok and vardas.strip():
            parts = vardas.strip().split(maxsplit=1)
            naujas = Zaidejas(parts[0], parts[1] if len(parts) > 1 else "")
            self.skaiciuokle.prideti_zaideja(naujas)
            self.update_player_lists()
            QMessageBox.information(self, "Sėkmė", f"Žaidėjas pridėtas: {naujas}")

    def show_about(self):
        QMessageBox.about(self,
                          "Apie programą",
                          """<h3>TIC TAC TOE v2</h3>
                          <p>Žaidimas sukurtas naudojant PyQt6 + Qt Designer</p>
                          <p><b>Autorius:</b> marelia-dev</p>
                          <p><b>Versija:</b> 2.0</p>
                          <p>2026</p>""")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    dark_style = """
    QMainWindow, QWidget, QStackedWidget { background-color: #121212; color: #e0e0e0; }
    QPushButton {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 2px solid #555;
        border-radius: 10px;
        padding: 12px;
    }
    QPushButton:hover { background-color: #3a3a3a; }
    QComboBox { background-color: #1e1e1e; color: white; padding: 8px; }
    QLabel { color: #e0e0e0; }
    """
    app.setStyleSheet(dark_style)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())