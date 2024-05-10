"""

This script is used to visualize bounding boxes in Bird's Eye View (BEV) using PyQt5. The bounding boxes are read from a JSON file and drawn on a canvas.

The script follows these steps:
1. Define the data structure: Determine how to represent the bounding boxes in BEV. Generally, you need to know the position (x, y coordinates), width, height, and possible rotation angle of each bounding box.
2. Read the data: Read the bounding box data from a JSON or other data source. Ensure all data is formatted with the correct coordinates and dimensions.
3. Initialize the canvas: Create a canvas (possibly a QPixmap, QImage, or other graphic object) that represents the BEV area, choose an appropriate size to accommodate all bounding boxes.
4. Canvas coordinate conversion: If the original coordinates are not based on the top left corner of the canvas, you need to convert the bounding box coordinates to the canvas coordinate system. This may require scaling and translation operations.
5. Draw the bounding boxes: For each bounding box in the BEV data: a. Create a bounding box graphic element based on the coordinates and dimensions. b. Apply rotation transformation if necessary. c. Set the attributes of the bounding box, such as color, border, etc. d. Draw the bounding box on the canvas.
6. Layer control: If implementing layer control: a. Create a separate layer for each set of bounding boxes in the JSON file. b. When the user selects to show or hide the layer through the controls on the interface (such as buttons or checkboxes), update the canvas to show or hide the relevant bounding boxes.
7. Render the canvas: After all graphic elements are drawn, display the canvas in the widget (such as QLabel) on the user interface.
8. User interaction: Allow users to toggle the display/hide of bounding boxes through user interface controls, and switch between viewing different sets of bounding boxes.
9. Refresh the canvas: a. Each time the user interaction changes the visibility of the bounding box, clear the canvas and redraw the currently selected bounding box. b. Update the user interface to reflect the latest canvas status.
10. Error handling: Ensure that the program can gracefully handle any exceptions, such as format errors in the data file, invalid coordinates, etc.
"""


import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QVBoxLayout, QPushButton, QWidget, QRadioButton, QButtonGroup, QLabel
from PyQt5.QtGui import QTransform, QPainter, QColor, QPixmap, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QRectF

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化画布
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)

        # 加载底图
        self.background = QGraphicsPixmapItem(QPixmap('background.png'))
        self.scene.addItem(self.background)

        # 读取数据
        self.data = self.read_data('data_folder')  # 读取文件夹中的所有JSON文件

        # 创建图层
        self.layers = {key: self.create_layer(value) for key, value in self.data.items()}

        # 创建单选按钮组
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(False)
        self.button_group.buttonClicked[int].connect(self.toggle_layer)

        # 添加切换图层显示的按钮
        self.buttons = [self.create_button(i, key) for i, key in enumerate(self.layers.keys())]

        # 添加上一个和下一个按钮
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_prev)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        for button in self.buttons:
            layout.addWidget(button)
        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)

        # 设置主窗口
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # 初始化索引
        self.index = 0

    def read_data(self, foldername):
        # 读取文件夹中的所有JSON文件
        data = {}
        for filename in os.listdir(foldername):
            if filename.endswith('.json'):
                with open(os.path.join(foldername, filename), 'r') as f:
                    data[filename] = json.load(f)
        return data

    def create_layer(self, data):
        # 创建图层
        items = [QGraphicsRectItem(d['x'], d['y'], d['width'], d['height']) for d in data]
        for item in items:
            self.scene.addItem(item)
            item.setVisible(False)  # 默认隐藏所有图层
        return items

    def create_button(self, layer_index, layer_name):
        # 创建按钮
        button = QRadioButton(layer_name)
        self.button_group.addButton(button, layer_index)
        return button

    def toggle_layer(self, layer_index):
        # 切换图层显示
        layer_name = self.button_group.button(layer_index).text()
        for item in self.layers[layer_name]:
            item.setVisible(not item.isVisible())

    def show_prev(self):
        # 显示上一个时间戳的结果
        self.index = (self.index - 1) % len(self.data)
        self.refresh_canvas()

    def show_next(self):
        # 显示下一个时间戳的结果
        self.index = (self.index + 1) % len(self.data)
        self.refresh_canvas()

    def refresh_canvas(self):
        # 刷新画布
        self.scene.clear()
        self.scene.addItem(self.background)  # 重新添加底图
        self.create_layer(self.data[list(self.data.keys())[self.index]])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())