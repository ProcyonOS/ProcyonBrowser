from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QKeySequence, QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QMenuBar, QMenu, QMessageBox, QTabWidget, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Procyon Browser")
        self.setWindowIcon(QIcon("C:\\Users\\gauth\\OneDrive\\Pictures\\ProcyonBrowser.ico"))

        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Create a new tab
        self.add_new_tab(QUrl("https://gauthamnair2005.wixsite.com/procyonos"))

        # Set the tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

        # Create a toolbar
        toolbar = QToolBar()
        toolbar.setStyleSheet("background-color: black; color: #F0F0F0;")  # Set the toolbar color and text color
        self.addToolBar(toolbar)

        # Add a back action to the toolbar
        back_action = QAction("⬅️ Back", self)
        back_action.setShortcut(QKeySequence("Alt+Left"))
        back_action.triggered.connect(lambda: self.current_web_view().back())
        toolbar.addAction(back_action)

        # Add a forward action to the toolbar
        forward_action = QAction("➡️ Forward", self)
        forward_action.setShortcut(QKeySequence("Alt+Right"))
        forward_action.triggered.connect(lambda: self.current_web_view().forward())
        toolbar.addAction(forward_action)

        # Add a reload action to the toolbar
        reload_action = QAction("🔄 Reload", self)
        reload_action.setShortcut(QKeySequence("F5"))
        reload_action.triggered.connect(lambda: self.current_web_view().reload())
        toolbar.addAction(reload_action)

        # Add a new tab action to the toolbar
        new_tab_action = QAction("🆕 New Tab", self)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(new_tab_action)

        # Add a close tab action to the toolbar
        close_tab_action = QAction("❌ Close Tab", self)
        close_tab_action.setShortcut(QKeySequence("Ctrl+W"))
        close_tab_action.triggered.connect(self.close_current_tab)
        toolbar.addAction(close_tab_action)

        # Add a fullscreen action to the toolbar
        fullscreen_action = QAction("🖵 Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        toolbar.addAction(fullscreen_action)

        # Add a search bar to the toolbar
        self.search_bar = QLineEdit()
        self.search_bar.setStyleSheet("border: 1px solid black; padding: 1px; color: #F0F0F0;")  # Set the search bar style and text color
        self.search_bar.returnPressed.connect(self.load_url)
        toolbar.addWidget(self.search_bar)

        # Create a menu bar
        menu_bar = QMenuBar()
        menu_bar.setStyleSheet("background-color: black; color: #F0F0F0;")  # Set the menu bar color and text color

        # Create a file menu and add it to the menu bar
        file_menu = QMenu("File", self)
        exit_action = QAction("❌ Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Add a save action to the file menu
        save_action = QAction("💾 Save", self)
        save_action.setShortcut(QKeySequence("Save"))
        save_action.triggered.connect(self.save_page)
        file_menu.addAction(save_action)

        menu_bar.addMenu(file_menu)

        # Create an about menu and add it to the menu bar
        about_menu = QMenu("About", self)
        about_action = QAction("ℹ️ About", self)
        about_action.triggered.connect(self.show_about_message)
        about_menu.addAction(about_action)
        menu_bar.addMenu(about_menu)

        # Set the menu bar
        self.setMenuBar(menu_bar)

    def handle_fullscreen_request(self, request):
        if request.toggleOn():
            self.showFullScreen()
        else:
            self.showNormal()
        request.accept()

    def add_new_tab(self, url=None):
        if isinstance(url, bool):
            url = None
        if url is None:
            url = QUrl("about:blank")

        # Create a new web view
        web_view = QWebEngineView()
        web_view.setUrl(url)

        # Connect the titleChanged signal to the update_tab_title method
        web_view.titleChanged.connect(lambda title, web_view=web_view: self.update_tab_title(title, web_view))

        # Handle fullscreen requests
        web_view.page().fullScreenRequested.connect(self.handle_fullscreen_request)

        # Add the new web view to a new tab in the tab widget
        i = self.tab_widget.addTab(web_view, url.toString())

        # Set the current tab to the new tab
        self.tab_widget.setCurrentIndex(i)

    def update_tab_title(self, title, web_view):
        index = self.tab_widget.indexOf(web_view)
        if index != -1:
            self.tab_widget.setTabText(index, title)

    def close_current_tab(self):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(self.tab_widget.currentIndex())
        else:
            self.close()

    def load_url(self):
        url = self.search_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.current_web_view().load(QUrl(url))

    def current_web_view(self):
        return self.tab_widget.currentWidget()

    def save_page(self):
        # Save the current page
        self.current_web_view().page().runJavaScript("document.documentElement.outerHTML", self.write_html_to_file)

    def write_html_to_file(self, html):
        with open("saved_page.html", "w", encoding="utf-8") as file:
            file.write(html)

    def show_about_message(self):
        QMessageBox.about(self, "About", "Procyon Browser\nVersion 1.2.5\nEngine 6.7\n\nGautham Nair")

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())