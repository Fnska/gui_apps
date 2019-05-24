import sys
from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import QPixmap
from PIL import Image
import os

from numpy import array, max

from ui import main
from plot_app import approx_ellipse_img_V3


count = 0
file_path, ext = None, None


class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Ellipse Fit")

        self.analise_btn.clicked.connect(self.analise)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave_as.triggered.connect(self.save_file_as)
        self.clear_btn.clicked.connect(self.clearing)

    def counter(self):
        global count
        self.output_info.clear()
        self.output_info.setText(str(count))
        count += 1

    def open_file(self):
        global file_path, ext
        file_path, ext = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '/File Name',
                                                               'Images (*.png *.xpm *.jpg)')
        if file_path:
            self.input_image.setPixmap(QPixmap(file_path))
            im = Image.open(file_path).convert('I')
            a = array(im)
            self.line_max.setText(str(max(a)))

    def save_file_as(self):
        p = QtGui.QPixmap.grabWidget(self.output_image)
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File As', '', '*.png')
        p.save(file_name[0], 'PNG')

    def clearing(self):
        global file_path
        if file_path and (self.line_cut.text() != '' and self.line_max.text() != ''):
            im = Image.open(file_path).convert('I')
            output = approx_ellipse_img_V3.el_im_app(im,
                                                     int(self.line_max.text()),
                                                     file_path,
                                                     delta_ring=int(self.line_delta.text()),
                                                     low_value_i_sub=int(self.line_cut.text()),
                                                     points_plot=self.combo_points.currentIndex(),
                                                     update=2
                                                     )
            self.output_image.setPixmap(output[0])
            os.remove(output[0])
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Please input I_cut and I_max')
            msg.setWindowTitle("Input warning")
            msg.exec_()

    def analise(self):
        global file_path
        if file_path and (self.combo_modes.currentIndex() == 0):
            if self.line_cut.text() == '' or self.line_max.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Please input I_cut and I_max')
                msg.setWindowTitle("Input warning")
                msg.exec_()
            else:
                im = Image.open(file_path).convert('I')
                output = approx_ellipse_img_V3.el_im_app(im,
                                                         int(self.line_max.text()),
                                                         file_path,
                                                         delta_ring=int(self.line_delta.text()),
                                                         low_value_i_sub=int(self.line_cut.text()),
                                                         points_plot=self.combo_points.currentIndex(),
                                                         update=self.combo_update.currentIndex()
                                                         )
                self.output_image.setPixmap(output[0])
                os.remove(output[0])
                self.output_info.setText('I_max = ' + str(output[1][0][2]) + '\n' +
                                         'I_sub = ' + str(output[1][1][2]) + '\n' +
                                         'x_a = ' + str(output[1][2][2]) + '\n' +
                                         'y_b = ' + str(output[1][3][2]) + '\n' +
                                         'c = ' + str(output[1][4][2]) + '\n' +
                                         'x_c = ' + str(output[1][5][2][0]) + '\n' +
                                         'y_c = ' + str(output[1][5][2][1]) + '\n' +
                                         'e = ' + str(output[1][6][2]) + '\n' +
                                         'r_p = ' + str(output[1][7][2]) + '\n' +
                                         'r_a = ' + str(output[1][8][2]) + '\n')

        if file_path and (self.combo_modes.currentIndex() == 1):
            im = Image.open(file_path).convert('I')
            output = approx_ellipse_img_V3.img_3d_interp(im, file_path)
            self.output_image.setPixmap(output)
            os.remove(output)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qt_app = MyQtApp()
    qt_app.show()
    app.exec_()
