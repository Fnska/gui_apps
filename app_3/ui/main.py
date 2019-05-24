# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui',
# licensing of 'main.ui' applies.
#
# Created: Tue May 21 21:19:22 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1320, 829)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_image = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_image.sizePolicy().hasHeightForWidth())
        self.input_image.setSizePolicy(sizePolicy)
        self.input_image.setMinimumSize(QtCore.QSize(640, 480))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.input_image.setFont(font)
        self.input_image.setStyleSheet("background-color: rgb(167, 173, 186);")
        self.input_image.setText("")
        self.input_image.setObjectName("input_image")
        self.horizontalLayout.addWidget(self.input_image)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setStyleSheet("")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.output_image = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_image.sizePolicy().hasHeightForWidth())
        self.output_image.setSizePolicy(sizePolicy)
        self.output_image.setMinimumSize(QtCore.QSize(640, 480))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.output_image.setFont(font)
        self.output_image.setStyleSheet("background-color: rgb(167, 173, 186);")
        self.output_image.setText("")
        self.output_image.setObjectName("output_image")
        self.horizontalLayout.addWidget(self.output_image)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setStyleSheet("")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setContentsMargins(20, -1, 0, 0)
        self.formLayout.setSpacing(8)
        self.formLayout.setObjectName("formLayout")
        self.label_max = QtWidgets.QLabel(self.centralwidget)
        self.label_max.setMaximumSize(QtCore.QSize(60, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_max.setFont(font)
        self.label_max.setStyleSheet("")
        self.label_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_max.setObjectName("label_max")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_max)
        self.line_max = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_max.sizePolicy().hasHeightForWidth())
        self.line_max.setSizePolicy(sizePolicy)
        self.line_max.setMinimumSize(QtCore.QSize(120, 20))
        self.line_max.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_max.setFont(font)
        self.line_max.setStyleSheet("")
        self.line_max.setText("")
        self.line_max.setObjectName("line_max")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.line_max)
        self.label_delta = QtWidgets.QLabel(self.centralwidget)
        self.label_delta.setMinimumSize(QtCore.QSize(0, 0))
        self.label_delta.setMaximumSize(QtCore.QSize(60, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_delta.setFont(font)
        self.label_delta.setStyleSheet("")
        self.label_delta.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_delta.setObjectName("label_delta")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_delta)
        self.line_delta = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_delta.sizePolicy().hasHeightForWidth())
        self.line_delta.setSizePolicy(sizePolicy)
        self.line_delta.setMinimumSize(QtCore.QSize(120, 20))
        self.line_delta.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_delta.setFont(font)
        self.line_delta.setStyleSheet("")
        self.line_delta.setObjectName("line_delta")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.line_delta)
        self.label_cut = QtWidgets.QLabel(self.centralwidget)
        self.label_cut.setMaximumSize(QtCore.QSize(60, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_cut.setFont(font)
        self.label_cut.setStyleSheet("")
        self.label_cut.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_cut.setObjectName("label_cut")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_cut)
        self.label_modes = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_modes.setFont(font)
        self.label_modes.setObjectName("label_modes")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_modes)
        self.combo_modes = QtWidgets.QComboBox(self.centralwidget)
        self.combo_modes.setMinimumSize(QtCore.QSize(0, 20))
        self.combo_modes.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.combo_modes.setFont(font)
        self.combo_modes.setStyleSheet("")
        self.combo_modes.setObjectName("combo_modes")
        self.combo_modes.addItem("")
        self.combo_modes.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.combo_modes)
        self.label_output = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_output.setFont(font)
        self.label_output.setObjectName("label_output")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_output)
        self.combo_update = QtWidgets.QComboBox(self.centralwidget)
        self.combo_update.setMinimumSize(QtCore.QSize(0, 20))
        self.combo_update.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.combo_update.setFont(font)
        self.combo_update.setObjectName("combo_update")
        self.combo_update.addItem("")
        self.combo_update.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.combo_update)
        self.label_type = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_type.setFont(font)
        self.label_type.setObjectName("label_type")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_type)
        self.combo_points = QtWidgets.QComboBox(self.centralwidget)
        self.combo_points.setMinimumSize(QtCore.QSize(0, 20))
        self.combo_points.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.combo_points.setFont(font)
        self.combo_points.setObjectName("combo_points")
        self.combo_points.addItem("")
        self.combo_points.addItem("")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.combo_points)
        self.clear_btn = QtWidgets.QPushButton(self.centralwidget)
        self.clear_btn.setMaximumSize(QtCore.QSize(230, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.clear_btn.setFont(font)
        self.clear_btn.setObjectName("clear_btn")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.clear_btn)
        self.analise_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analise_btn.sizePolicy().hasHeightForWidth())
        self.analise_btn.setSizePolicy(sizePolicy)
        self.analise_btn.setMinimumSize(QtCore.QSize(120, 0))
        self.analise_btn.setMaximumSize(QtCore.QSize(230, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.analise_btn.setFont(font)
        self.analise_btn.setStyleSheet("")
        self.analise_btn.setAutoDefault(False)
        self.analise_btn.setDefault(False)
        self.analise_btn.setFlat(False)
        self.analise_btn.setObjectName("analise_btn")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.analise_btn)
        self.line_cut = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_cut.sizePolicy().hasHeightForWidth())
        self.line_cut.setSizePolicy(sizePolicy)
        self.line_cut.setMinimumSize(QtCore.QSize(120, 20))
        self.line_cut.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_cut.setFont(font)
        self.line_cut.setStyleSheet("")
        self.line_cut.setText("")
        self.line_cut.setObjectName("line_cut")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.line_cut)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.output_info = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.output_info.setFont(font)
        self.output_info.setStyleSheet("")
        self.output_info.setText("")
        self.output_info.setMargin(20)
        self.output_info.setObjectName("output_info")
        self.horizontalLayout_2.addWidget(self.output_info)
        spacerItem = QtWidgets.QSpacerItem(550, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1320, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label_max.setText(QtWidgets.QApplication.translate("MainWindow", "I _max:", None, -1))
        self.label_delta.setText(QtWidgets.QApplication.translate("MainWindow", "Delta:", None, -1))
        self.line_delta.setText(QtWidgets.QApplication.translate("MainWindow", "5000", None, -1))
        self.label_cut.setText(QtWidgets.QApplication.translate("MainWindow", "I _cut:", None, -1))
        self.label_modes.setText(QtWidgets.QApplication.translate("MainWindow", "Modes:", None, -1))
        self.combo_modes.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "2d ellipse", None, -1))
        self.combo_modes.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "3d plot", None, -1))
        self.label_output.setText(QtWidgets.QApplication.translate("MainWindow", "Output:", None, -1))
        self.combo_update.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "Update", None, -1))
        self.combo_update.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "Add", None, -1))
        self.label_type.setText(QtWidgets.QApplication.translate("MainWindow", "Type:", None, -1))
        self.combo_points.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "Line", None, -1))
        self.combo_points.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "Line + Points", None, -1))
        self.clear_btn.setText(QtWidgets.QApplication.translate("MainWindow", "Clear", None, -1))
        self.analise_btn.setText(QtWidgets.QApplication.translate("MainWindow", "Research", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.actionOpen.setText(QtWidgets.QApplication.translate("MainWindow", "Open...", None, -1))
        self.actionOpen.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+O", None, -1))
        self.actionSave_as.setText(QtWidgets.QApplication.translate("MainWindow", "Save as...", None, -1))
        self.actionSave_as.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, -1))
        self.actionQuit.setText(QtWidgets.QApplication.translate("MainWindow", "Quit", None, -1))
        self.actionQuit.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Q", None, -1))
