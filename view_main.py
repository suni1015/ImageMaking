import errno
import sys
# import urllib.request
#from typing import Any, Union

from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
"""
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from docx.shared import Pt
from docx.shared import Inches

import cv2
import threading
"""
import os
import logging
import time
import re
import numpy as np

#from PIL import Image

from data_shinwon import Shinwon

form_class = uic.loadUiType("ui_imageMaking.ui")[0]


###### CLASS ##########
class WindowClass(QMainWindow, form_class):
    filename = None

    def __init__(self):
        super().__init__()
        self.sw_obj = Shinwon()  # sw_obj = Shinwon('BYJAX1234-0')

        self.setupUi(self)
        self.setStyleSheet("background-color: white;")

        self.btn_file_open.clicked.connect(self.OnfileOpen)
        self.edt_poombun.returnPressed.connect(self.OnEnterPoombun)
        self.edt_poombun.textChanged[str].connect(self.onChangedPoombun)


    @pyqtSlot()
    def OnfileOpen(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', '', 'Excel File(*.xls *.xlsx)')
        if self.filename[0]:
            self.label_file_path.setText(self.filename[0])
        else:
            self.tb_poombun_info.setPlainText("안내 : 파일 선택을 취소하셨습니다.")
            return

        self.sw_obj.openFile_clothInfo(self.filename[0])    # 엑셀 -> dataframe 으로 로딩.


    # QLineEdit 의 엔터 입력시 발생하는 이벤트 (not use here)
    @pyqtSlot()
    def OnEnterPoombun(self):
        return
        
    @pyqtSlot()
    def onChangedPoombun(self):
        poombun = self.edt_poombun.text().upper()
        self.edt_poombun.setText(poombun)

        if len(poombun) != 9:
            #self.tb_poombun_info.clear()
            self.tb_poombun_info.setPlainText("안내 : 품번체계는 9자 입니다.")
            return
        self.sw_obj.clear_product_info()    # 이전 품번 정보를 클리어한다.
        self.sw_obj.set_poombun(poombun)    # 품번 정보 입력
        self.sw_obj.decode_poombun()        # 품번 정보 디코딩(파싱)

        if self.filename:
            ret = self.sw_obj.parse_excel_data()      # 품번 기반으로 엑셀에서 정보를 가져온다.
            if not ret:
                self.tb_poombun_info.setPlainText("안내 : 입력하신 품번은 정보고시 파일에 존재하지 않습니다.")
                return

        dic_prod_info = self.sw_obj.get_product_info()

        self.tb_poombun_info.clear()
        for key, value in dic_prod_info.items():
            print('*', key, '-', value)
            str_pf = '*' + key + '-' + value
            self.tb_poombun_info.append(str_pf)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()