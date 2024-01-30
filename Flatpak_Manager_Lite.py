import sys
import subprocess
import requests
import cProfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, \
    QLabel, QWidget, QListWidgetItem, QLineEdit, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QThreadPool, QTimer

def main(): 

    class IconLoaderThread(QThread):
        icon_loaded = pyqtSignal(QListWidgetItem, QPixmap)
        terminated = pyqtSignal()

        def __init__(self, item, app_icon_url):
            super().__init__()
            self._item = item
            self._app_icon_url = app_icon_url
            self._icon_pixmap = None
            self._loaded = False

        def run(self):
            try:
                if not self._loaded and self._app_icon_url is not None:
                    icon_data = requests.get(self._app_icon_url).content
                    icon_pixmap = QPixmap()
                    icon_pixmap.loadFromData(icon_data)
                    self._icon_pixmap = icon_pixmap
                    self._loaded = True
                    self.icon_loaded.emit(self._item, icon_pixmap)
            except Exception as e:
                print(f"Error loading icon: {e}")
            self.terminated.emit()


        @property
        def icon_pixmap(self):
            # This property handles lazy loading of the icon
            if not self._loaded:
                self.start()  # Start the thread to load the icon if not loaded yet
                self.wait()  # Wait for the thread to finish loading
            return self._icon_pixmap


    class FlatpakManager(QMainWindow):
        def __init__(self):
            super().__init__()
            self.thread_pool = QThreadPool()

            self.setWindowTitle("Flatpak Manager Lite")
            self.setGeometry(100, 100, 800, 600)

            # Initialize the list to store icon loader threads
            self.icon_loaders = []

            self.init_ui()

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.clear_output)

        def init_ui(self):
            app.setStyle('Fusion')

            # Set a dark color palette
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)

            app.setPalette(dark_palette)

            self.search_bar = QLineEdit(self)
            self.search_bar.setPlaceholderText("Search for packages...")  # Set placeholder text
            self.sort_combobox = QComboBox(self)
            self.sort_combobox.addItem("Sort by Name")
            self.sort_combobox.addItem("Sort by Alpha-Numeric Name")
            self.app_list = QListWidget(self)
            self.status_label = QLabel("", self)
            self.install_button = QPushButton("Install Selected", self)
            self.uninstall_button = QPushButton("Uninstall Selected", self)
            self.update_button = QPushButton("Update Selected", self)

            # Connect signals
            self.install_button.clicked.connect(self.install_selected)
            self.uninstall_button.clicked.connect(self.uninstall_selected)
            self.update_button.clicked.connect(self.update_selected)
            self.search_bar.textChanged.connect(self.filter_apps)  # Connect to filter function
            self.sort_combobox.currentIndexChanged.connect(self.sort_apps)  # Connect to sorting function

            # Set up layout
            button_layout = QHBoxLayout()
            button_layout.addWidget(self.sort_combobox)
            button_layout.addStretch()  # Add stretch to make spacing even
            main_layout = QVBoxLayout()
            main_layout.addWidget(self.search_bar)
            main_layout.addLayout(button_layout)
            main_layout.addWidget(self.app_list)
            main_layout.addWidget(self.status_label)
            button_layout.addWidget(self.install_button)
            button_layout.addWidget(self.uninstall_button)
            button_layout.addWidget(self.update_button)

            # Set central widget
            central_widget = QWidget()
            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

            # Load Flatpak applications from Flathub API
            self.load_flatpak_apps()

        def load_flatpak_apps(self):
            # Fetch the list of Flatpak applications from Flathub API
            url = "https://flathub.org/api/v1/apps"
            response = requests.get(url)

            if response.status_code == 200:
                apps_data = response.json()
                for app_data in apps_data:
                    app_name = app_data["name"]
                    app_summary = app_data["summary"]
                    app_icon_url = app_data["iconDesktopUrl"]
                    flatpak_id = app_data["flatpakAppId"]

                    # Add the application to the QListWidget
                    item = QListWidgetItem()
                    item.setText(f"{app_name} - {app_summary}")
                    item.setData(Qt.UserRole, flatpak_id)  # Store Flatpak ID in item data

                    # Use a separate thread to load icons asynchronously
                    icon_loader = IconLoaderThread(item, app_icon_url)
                    icon_loader.icon_loaded.connect(self.set_icon)
                    icon_loader.finished.connect(icon_loader.deleteLater)  # Clean up the thread
                    icon_loader.start()

                    # Store the thread object in a list
                    self.icon_loaders.append(icon_loader)

                    self.app_list.addItem(item)
            else:
                self.status_label.setText("Error fetching Flatpak apps from Flathub API")

        def set_icon(self, item, pixmap):
            item.setIcon(QIcon(pixmap))

        def install_selected(self):
            selected_item = self.app_list.currentItem()
            if selected_item:
                flatpak_id = selected_item.data(Qt.UserRole)
                self.run_flatpak_command(f"install {flatpak_id} -y")
                self.timer.start(15000)

        def uninstall_selected(self):
            selected_item = self.app_list.currentItem()
            if selected_item:
                flatpak_id = selected_item.data(Qt.UserRole)
                self.run_flatpak_command(f"uninstall {flatpak_id} -y")
                self.timer.start(15000)

        def update_selected(self):  
            selected_item = self.app_list.currentItem()
            if selected_item:
                flatpak_id = selected_item.data(Qt.UserRole)
                self.run_flatpak_command(f"update {flatpak_id} -y")
                self.timer.start(15000)

        def run_flatpak_command(self, command, status_message=""):
            try:
                subprocess.run(["flatpak"] + command.split(), check=True)
                if status_message:
                    self.status_label.setText(f"{status_message} succeeded.")
                    self.timer.start(15000)
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"{status_message} failed. Error: {e}")

        def clear_output(self):
            self.status_label.clear()

        def filter_apps(self):
            search_text = self.search_bar.text().lower()
            for i in range(self.app_list.count()):
                item = self.app_list.item(i)
                app_name = item.text().split(" - ")[0].lower()
                item.setHidden(search_text not in app_name)

        def sort_apps(self):
            # Get the selected sorting criteria
            sorting_criteria = self.sort_combobox.currentText()

            # Perform sorting based on the selected criteria
            if sorting_criteria == "Sort by Name":
                self.sort_items_alpha_numeric(False)
            elif sorting_criteria == "Sort by Alpha-Numeric Name":
                self.sort_items_alpha_numeric(True)

        def sort_items_alpha_numeric(self, alpha_numeric):
            items = [self.app_list.takeItem(0) for _ in range(self.app_list.count())]
            items.sort(key=lambda x: (x.text().split(" - ")[0], x.text()) if alpha_numeric else x.text())

            for item in items:
                self.app_list.addItem(item)

        def closeEvent(self, event):
            # Terminate all icon loader threads before exiting
            for icon_loader in self.icon_loaders:
                icon_loader.quit()
                icon_loader.wait()
            self.thread_pool.waitForDone()
            event.accept()

        def remove_thread(self):
            thread = self.sender()
            self.icon_loaders.remove(thread)

        def load_icon(self):
            icon_loader = IconLoader()
            icon_loader.terminated.connect(self.remove_thread)
            self.thread_pool.start(icon_loader)
            self.icon_loaders.append(icon_loader)

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = FlatpakManager()
        window.show()
        sys.exit(app.exec_())

cProfile.run('main()')
