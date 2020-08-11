from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(550, 442)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(550, 442))
        Form.setMaximumSize(QtCore.QSize(550, 442))
        self.start_button = QtWidgets.QPushButton(Form)
        self.start_button.setGeometry(QtCore.QRect(230, 170, 93, 28))
        self.start_button.setObjectName("start_button")
        self.end_button = QtWidgets.QPushButton(Form)
        self.end_button.setGeometry(QtCore.QRect(400, 170, 93, 28))
        self.end_button.setObjectName("end_button")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 20, 461, 135))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.save_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.save_button.setMinimumSize(QtCore.QSize(93, 28))
        self.save_button.setMaximumSize(QtCore.QSize(93, 28))
        self.save_button.setObjectName("save_button")
        self.gridLayout.addWidget(self.save_button, 2, 1, 1, 1)
        self.name_file_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.name_file_label.setObjectName("name_file_label")
        self.gridLayout.addWidget(self.name_file_label, 0, 0, 1, 1)
        self.inf_file_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.inf_file_label.setObjectName("inf_file_label")
        self.gridLayout.addWidget(self.inf_file_label, 2, 0, 1, 1)
        self.error_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.error_button.setMinimumSize(QtCore.QSize(93, 28))
        self.error_button.setMaximumSize(QtCore.QSize(93, 28))
        self.error_button.setObjectName("error_button")
        self.gridLayout.addWidget(self.error_button, 3, 1, 1, 1)
        self.error_file_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.error_file_label.setObjectName("error_file_label")
        self.gridLayout.addWidget(self.error_file_label, 3, 0, 1, 1)
        self.open_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.open_button.setMinimumSize(QtCore.QSize(93, 28))
        self.open_button.setMaximumSize(QtCore.QSize(93, 28))
        self.open_button.setAutoDefault(False)
        self.open_button.setObjectName("open_button")
        self.gridLayout.addWidget(self.open_button, 0, 1, 1, 1)
        self.specimen_file_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.specimen_file_label.setObjectName("specimen_file_label")
        self.gridLayout.addWidget(self.specimen_file_label, 1, 0, 1, 1)
        self.specimen_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.specimen_button.setMinimumSize(QtCore.QSize(93, 28))
        self.specimen_button.setMaximumSize(QtCore.QSize(93, 28))
        self.specimen_button.setObjectName("specimen_button")
        self.gridLayout.addWidget(self.specimen_button, 1, 1, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(50, 220, 441, 171))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.help_Button = QtWidgets.QPushButton(Form)
        self.help_Button.setGeometry(QtCore.QRect(50, 170, 93, 28))
        self.help_Button.setObjectName("help_Button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "crawler for nsii"))
        self.start_button.setText(_translate("Form", "开始"))
        self.end_button.setText(_translate("Form", "结束"))
        self.save_button.setText(_translate("Form", "选择位置"))
        self.name_file_label.setText(_translate("Form", "物种名位置："))
        self.inf_file_label.setText(_translate("Form", "县级分布地保存位置："))
        self.error_button.setText(_translate("Form", "选择位置"))
        self.error_file_label.setText(_translate("Form", "错误分布地保存位置："))
        self.open_button.setText(_translate("Form", "导入物种名"))
        self.specimen_file_label.setText(_translate("Form", "标本信息保存位置："))
        self.specimen_button.setText(_translate("Form", "选择位置"))
        self.help_Button.setText(_translate("Form", "帮助"))
