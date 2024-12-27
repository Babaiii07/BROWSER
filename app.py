import subprocess
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, 
                             QLineEdit, QVBoxLayout, QWidget, QTextEdit, 
                             QDialog, QPushButton, QLabel, QToolButton)
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QFont, QPixmap

def generate_text_with_llama(prompt):
    command = ["ollama", "run", "llama3.2"]
    prompt = prompt + "in 30 words"

    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate(input=prompt, timeout=30)

        if output:
            return output.strip()
        elif error:
            return f"Error occurred: {error.strip()}"
        else:
            return "No response received from the model."

    except subprocess.TimeoutExpired:
        process.kill()
        return "The request timed out. Please try again."

    except Exception as e:
        return f"An exception occurred: {str(e)}"

class ChatDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Buzz - Powered by Agnik and Parthib")
        self.setGeometry(400, 300, 600, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f4ff;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        
        self.prompt_label = QLabel("💬 Ask Question:")
        self.prompt_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(self.prompt_label)
        
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Type your question here...")
        self.prompt_input.setStyleSheet("""
            QLineEdit {
                color: #444;
                background-color: #ffffff;
                border: 2px solid #dcdcdc;
                border-radius: 12px;
                padding: 12px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #6c63ff;
                box-shadow: 0 0 10px rgba(108, 99, 255, 0.4);
            }
        """)
        layout.addWidget(self.prompt_input)
        
        self.response_display = QTextEdit()
        self.response_display.setReadOnly(True)
        self.response_display.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                color: #333;
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 12px;
                font-size: 14px;
                margin-top: 10px;
            }
        """)
        layout.addWidget(self.response_display)
        

        self.send_button = QPushButton("🚀 Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #6c63ff;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c63ff, stop:1 #4b47b3);
                color: #fff;
                font-size: 16px;
                padding: 10px;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a54d1;
            }
            QPushButton:pressed {
                background-color: #4b47b3;
            }
        """)
        self.send_button.clicked.connect(self.handle_send)
        layout.addWidget(self.send_button)
        
        self.setLayout(layout)
    
    def handle_send(self):
        prompt = self.prompt_input.text()
        if prompt:
            self.response_display.append(f"<b>User:</b> {prompt}\n")
            
            response = generate_text_with_llama(prompt)
            
        
            self.add_robot_response(response)
            self.prompt_input.clear()

    def add_robot_response(self, response_text):
        """Display robot response with an icon."""
        response_html = f"""
        <table style="width: 100%;">
            <tr>
                <td><img src="robot.png" width="35" height="35"></td>
                <td style="padding-left: 10px; vertical-align: middle;">
                    <b>NetworkBuzz:</b> {response_text}
                </td>
            </tr>
        </table>
        """
        self.response_display.append(response_html)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Web Browser")
        self.setGeometry(300, 150, 1000, 800)

     
        navbar = QToolBar("Navigation")
        navbar.setIconSize(QSize(24, 24))
        self.addToolBar(navbar)

    
        back_btn = QAction(QIcon("back.png"), "Back", self)
        back_btn.triggered.connect(self.browser_back)
        navbar.addAction(back_btn)

  
        forward_btn = QAction(QIcon("forward.png"), "Forward", self)
        forward_btn.triggered.connect(self.browser_forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon("reload.png"), "Reload", self)
        reload_btn.triggered.connect(self.browser_reload)
        navbar.addAction(reload_btn)


        home_btn = QAction(QIcon("home.png"), "Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)


        chat_btn = QToolButton()
        chat_btn.setText("💬 Network Buzz")
        chat_btn.setStyleSheet("""
            QToolButton {
                background-color: #6c63ff;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 8px;
                margin-left: 10px;
            }
            QToolButton:hover {
                background-color: #5a54d1;
            }
        """)
        chat_btn.clicked.connect(self.open_chat)
        navbar.addWidget(chat_btn)


        self.url_bar = QLineEdit()
        self.url_bar.setFont(QFont("Arial", 12))
        self.url_bar.setPlaceholderText("Enter URL here")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)


        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_chat(self):
        self.chat_dialog = ChatDialog()
        self.chat_dialog.exec_()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def browser_back(self):
        self.browser.back()

    def browser_forward(self):
        self.browser.forward()

    def browser_reload(self):
        self.browser.reload()

app = QApplication(sys.argv)
window = Browser()
window.show()
sys.exit(app.exec_())
