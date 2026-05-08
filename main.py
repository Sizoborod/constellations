import os
import random
import sys
from pathlib import Path

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QWidget, QLabel, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

'''with open('namestarrs.txt', 'r', encoding='utf-8') as f:
    for name in f.readlines():
        print(name.strip())
        os.makedirs(name.strip(), exist_ok=True)'''


class ImageTextApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_folder = None
        self.current_images = []
        self.current_text_file = None
        self.text_content = ""
        self.showing_image = True  # True - показываем картинку, False - текст
        self.initUI()

    def initUI(self):
        """Инициализация интерфейса"""
        self.setWindowTitle('Изображение или текст')
        self.setGeometry(200, 200, 900, 800)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Label для отображения контента
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 28pt;
                border: 2px solid #ccc;
                background-color: #f0f0f0;
                padding: 10px;
            }
        """)
        self.label.setMinimumSize(400, 400)
        layout.addWidget(self.label)

        # Кнопка "Далее"
        self.button = QPushButton('Далее')
        self.button.setFixedHeight(40)
        self.button.clicked.connect(self.on_next_clicked)
        layout.addWidget(self.button)

        # Первоначальная загрузка
        self.load_random_content()

    def get_subfolders(self):
        """Получить список подпапок в текущем каталоге"""
        current_dir = Path.cwd()
        subfolders = [f for f in current_dir.iterdir() if f.is_dir()]
        return subfolders

    def load_images_from_folder(self, folder_path):
        """Загрузить все изображения из папки"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
        images = []

        for file in folder_path.iterdir():
            if file.is_file() and file.suffix.lower() in image_extensions:
                images.append(file)

        return images

    def load_text_from_file(self, folder_path):
        """Загрузить текстовый файл из папки"""
        # print(folder_path.name, type(folder_path))
        text_file = folder_path.name + '/readme.txt'
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return text_file, content
        except Exception as e:
            print(f"Ошибка чтения файла {text_file}: {e} из папки {folder_path}")
            return None, ""

        return None, ""

    def load_random_content(self):
        """Загрузить случайную папку и случайный контент"""
        subfolders = self.get_subfolders()

        if not subfolders:
            self.label.setText("Нет доступных папок в текущем каталоге")
            self.button.setEnabled(False)
            return

        # Выбираем случайную папку
        self.current_folder = random.choice(subfolders)

        # Загружаем изображения из папки
        self.current_images = self.load_images_from_folder(self.current_folder)

        # Загружаем текстовый файл из папки
        text_file, self.text_content = self.load_text_from_file(self.current_folder)

        if not self.current_images and not text_file:
            self.label.setText(f"В папке '{self.current_folder.name}' нет изображений и текстовых файлов")
            self.button.setEnabled(False)
            return

        self.button.setEnabled(True)
        self.showing_image = True
        print('Показываем случайное изображение или текст')
        s = '\n'
        print(f'{self.current_folder} *** \n{s.join([file.name for file in self.current_images])}\n*************')
        # Показываем случайное изображение или текст
        self.show_random_image_or_text()

    def show_random_image_or_text(self):
        """Показать случайное изображение или текст"""
        # Решаем что показывать: изображение или текст
        show_image = False

        if self.current_images and self.text_content:
            # Если есть и то, и другое - выбираем случайно
            show_image = True
        elif self.current_images:
            show_image = True
        elif self.text_content:
            show_image = False
        else:
            self.label.setText("Нет доступного контента")
            return

        if show_image:
            # Показываем случайное изображение
            image_file = random.choice(self.current_images)
            pixmap = QPixmap(str(image_file))

            if not pixmap.isNull():
                # Масштабируем изображение под размер label с сохранением пропорций
                scaled_pixmap = pixmap.scaled(
                    self.label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.label.setPixmap(scaled_pixmap)
                self.showing_image = True
            else:
                self.label.setText(f"Не удалось загрузить изображение: {image_file.name}")
        else:
            # Показываем текст
            self.label.setText(self.text_content)
            self.label.setWordWrap(True)
            self.showing_image = False

    def on_next_clicked(self):
        """Обработчик нажатия кнопки 'Далее'"""
        if self.showing_image:
            # Сейчас показано изображение - показываем текст
            if self.text_content:
                self.label.setText(self.text_content)
                self.label.setWordWrap(True)
                self.showing_image = False
            else:
                # Если текста нет, показываем новое случайное содержимое
                self.load_random_content()
        else:
            # Показан текст - показываем новое случайное содержимое
            self.load_random_content()

    def resizeEvent(self, event):
        """При изменении размера окна перемасштабируем изображение"""
        if self.showing_image and isinstance(self.label.pixmap(), QPixmap):
            pixmap = self.label.pixmap()
            if pixmap and not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = ImageTextApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
