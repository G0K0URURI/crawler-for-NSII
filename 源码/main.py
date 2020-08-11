import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import ui
import crawler


class Main(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ui.Ui_Form()
        self.ui.setupUi(self)
        self.ui.open_button.clicked.connect(self.get_open_file)
        self.ui.save_button.clicked.connect(self.get_save_file)
        self.ui.error_button.clicked.connect(self.get_error_file)
        self.ui.specimen_button.clicked.connect(self.get_specimen_file)
        self.ui.start_button.clicked.connect(self.start)
        self.ui.end_button.clicked.connect(self.stop)
        self.ui.help_Button.clicked.connect(self.show_help)

        self.name_file = ''
        self.location_file = ''
        self.error_file = ''
        self.specimen_file = ''
        self.output_flag = False
        self.ui.end_button.setEnabled(False)

    def get_open_file(self):
        self.name_file = QFileDialog.getOpenFileName(self, "导入物种名", ".", "Text Files (*.txt)")[0]
        self.ui.name_file_label.setText('物种名目录位置：'+self.name_file)

    def get_save_file(self):
        self.location_file = QFileDialog.getSaveFileName(self, "选择县级分布地保存位置", ".", "Text Files (*.txt)")[0]
        self.ui.inf_file_label.setText('县级分布地保存位置：'+self.location_file)

    def get_specimen_file(self):
        self.specimen_file = QFileDialog.getSaveFileName(self, "选择县级分布地保存位置", ".", "Text Files (*.txt)")[0]
        self.ui.specimen_file_label.setText('标本信息保存位置：'+self.specimen_file)

    def get_error_file(self):
        self.error_file = QFileDialog.getSaveFileName(self, "选择有误地名保存位置", ".", "Text Files (*.txt)")[0]
        self.ui.error_file_label.setText('错误分布地保存位置：' + self.error_file)

    def output(self, s):
        # 与爬虫线程相连的槽函数，用于显示必要信息
        # s 为爬虫线程传出的需要显示的信息
        if self.output_flag:
            self.ui.plainTextEdit.undo()
        self.ui.plainTextEdit.appendPlainText(s)
        self.ui.plainTextEdit.moveCursor(self.ui.plainTextEdit.textCursor().End)
        if '/' in s:
            self.output_flag = True
        else:
            self.output_flag = False
        if s == '查找完成':
            self.ui.end_button.setEnabled(False)
            self.ui.open_button.setEnabled(True)
            self.ui.specimen_button.setEnabled(True)
            self.ui.save_button.setEnabled(True)
            self.ui.error_button.setEnabled(True)
            self.ui.start_button.setEnabled(True)

    def start(self):
        # 开始爬虫线程
        if self.name_file == '':
            QMessageBox.information(self, '提示', '请先导入物种名', QMessageBox.Yes, QMessageBox.Yes)
        elif self.specimen_file == '':
            QMessageBox.information(self, '提示', '请先选择标本信息保存位置', QMessageBox.Yes, QMessageBox.Yes)
        elif self.location_file == '':
            QMessageBox.information(self, '提示', '请先选择县级分布地保存位置', QMessageBox.Yes, QMessageBox.Yes)
        elif self.error_file == '':
            QMessageBox.information(self, '提示', '请先选择有误地名保存位置', QMessageBox.Yes, QMessageBox.Yes)
        else:
            self.thread_1 = crawler.Thread_1(self.name_file, self.location_file, self.error_file, self.specimen_file)
            self.thread_1._signal.connect(self.output)
            self.ui.end_button.setEnabled(True)
            self.ui.open_button.setEnabled(False)
            self.ui.specimen_button.setEnabled(False)
            self.ui.save_button.setEnabled(False)
            self.ui.error_button.setEnabled(False)
            self.ui.start_button.setEnabled(False)
            self.thread_1.start()
        #     names = open(self.name_file, 'r', encoding='UTF-8').readlines()
        #     for name in names:
        #         name = name.replace('\r', '')
        #         inf_file = open(self.save_file, 'w', encoding='UTF-8')
        #         self.query_specimen(name, inf_file)

    def stop(self):
        self.thread_1.terminate()
        # self.thread_1.wait()
        self.ui.end_button.setEnabled(False)
        self.ui.open_button.setEnabled(True)
        self.ui.specimen_button.setEnabled(True)
        self.ui.save_button.setEnabled(True)
        self.ui.error_button.setEnabled(True)
        self.ui.start_button.setEnabled(True)
        self.output('已停止爬取')

    def show_help(self):
        QMessageBox.question(self, '帮助', '本程序用于从NSII上爬取标本信息，并利用高德地图筛选县级分布地。\n'
                                            + '其中，标本信息文件包含了标本的中文名、学名、采集地、属名、采集人、种名、科名，' +
                                 '县级分布地文件包含了采集地精度为县级或以上的标本的物种名、采集地省、市、县以及县级经度、纬度和行政区划代码，' +
                                '错误分布地文件包含了采集地精度为县级以下的标本的物种名和采集地。', QMessageBox.Yes, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
