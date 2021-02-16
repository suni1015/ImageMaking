"""
View 클래스

"""
import sys
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import re

from shinwon_data import Shinwon
from shinwon_making import MakeImg

form_class = uic.loadUiType("ui_imageMaking.ui")[0]


###### CLASS ######
class WindowClass(QMainWindow, form_class):
    filename = None

    def __init__(self):
        super().__init__()
        self.sw_obj = Shinwon()  # sw_obj = Shinwon('BYJAX1234-0')
        self.mkimg = MakeImg()

        self.poombun = None

        self.setupUi(self)
        self.setStyleSheet("background-color: white;")

        self.btn_file_open.clicked.connect(self.OnfileOpen)
        self.btn_img_make_single.clicked.connect(self.Makeimage_single)
        self.btn_img_make_multi.clicked.connect(self.Makeimage_multi)
        self.edt_poombun.returnPressed.connect(self.OnEnterPoombun)
        self.edt_poombun.textChanged[str].connect(self.onChangedPoombun)

    @pyqtSlot()
    def OnfileOpen(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', '', 'Excel File(*.xls *.xlsx)')
        if self.filename[0]:

            xl_name = self.filename[0].split("/")
            self.label_file_path.setText(xl_name[-1])
            self.path = os.path.dirname(self.filename[0])
        else:
            self.tb_poombun_info.setPlainText("안내 : 파일 선택을 취소하셨습니다.")
            return

        self.sw_obj.openFile_clothInfo(self.filename[0])  # 엑셀 -> dataframe 으로 로딩.

    # QLineEdit 의 엔터 입력시 발생하는 이벤트 (not use here)
    @pyqtSlot()
    def OnEnterPoombun(self):
        return

    @pyqtSlot()
    def onChangedPoombun(self):
        self.poombun = self.edt_poombun.text().upper()
        self.edt_poombun.setText(self.poombun)

        if len(self.poombun) != 9:
            # self.tb_poombun_info.clear()
            self.tb_poombun_info.setPlainText("안내 : 품번체계는 9자 입니다.")
            return
        self.sw_obj.clear_product_info()  # 이전 품번 정보를 클리어한다.
        self.sw_obj.set_poombun(self.poombun)  # 품번 정보 입력
        self.sw_obj.decode_poombun()  # 품번 정보 디코딩(파싱)

        if self.filename:
            ret = self.sw_obj.parse_excel_data()  # 품번 기반으로 엑셀에서 정보를 가져온다.
            if not ret:
                self.tb_poombun_info.setPlainText("안내 : 입력하신 품번은 정보고시 파일에 존재하지 않습니다.")
                return

        dic_prod_info = self.sw_obj.get_product_info()

        str_0 = dic_prod_info["브랜드"]

        self.tb_poombun_info.clear()
        for key, value in dic_prod_info.items():
            print('*', key, '-', value)
            str_pf = '*' + key + '-' + value
            self.tb_poombun_info.append(str_pf)

    def Makeimage(self):
        if len(self.poombun) != 9:
            # self.tb_poombun_info.clear()
            self.tb_poombun_info.setPlainText("품번이 유효하지 않습니다")
            return
        else:
            value = self.sw_obj.dic_product["컬러"]
            comp = re.compile('[^a-zA-Z/]')
            color = comp.sub('', value)
            color = color.split("/")
            # 색분류
            print(color)

            self.mkimg.setPath(self.path, self.poombun)
            len(color)
            if len(color) == 1:
                self.mkimg.makeFV1(self.poombun, color[0])
            else:
                self.mkimg.makeFV2(self.poombun, color[0], color[1])

            self.mkimg.makeDV(self.poombun, color[0])
            self.mkimg.makeInfo(self.sw_obj.dic_product["상품특성"], self.sw_obj.dic_product["상품특성 값"])

            self.mkimg.info_product_name(self.sw_obj.dic_product["상품명"])
            self.mkimg.info_product(self.poombun)
            self.mkimg.info_product(self.sw_obj.dic_product["컬러"])
            self.mkimg.info_product(self.sw_obj.dic_product["기준\n사이즈"])
            self.mkimg.info_product(self.sw_obj.dic_product["시즌"])
            self.mkimg.info_product(self.sw_obj.dic_product["세탁방법"])
            self.mkimg.info_product(self.sw_obj.dic_product["원산지"])
            self.mkimg.info_product(self.sw_obj.dic_product["소재"])

            self.mkimg.combineImg(self.poombun)

            return

    def isNaN(self, num):
        return num != num

    @pyqtSlot()
    def Makeimage_multi(self):

        self.mkimg.clear_data()

        # exception : 품번 리스트가 열려 있는가
        list_poombun = self.sw_obj.get_list_poombun()
        if list_poombun is None:
            print('품번 리스트가 없습니다. 엑셀 파일을 다시 열어주세요.')
            self.tb_poombun_info.append('품번 리스트가 없습니다. 엑셀 파일을 다시 열어주세요.')
            return

        count = 0
        self.tb_poombun_info.append("\nInfo : 이미지화를 시작합니다.")
        for poombun in list_poombun:
            count = count + 1
            self.tb_poombun_info.append("\nImage making" + str(count))
            var_tf = self.isNaN(poombun)
            if var_tf:
                self.tb_poombun_info.append("ERR : 품번체계 오류(NaN)")
                continue
            if len(poombun) != 9:
                self.tb_poombun_info.append("ERR : 품번체계는 9자 입니다.")
                continue
            self.tb_poombun_info.append("품번 : " + poombun)

            self.poombun = poombun
            self.sw_obj.set_poombun(poombun)
            self.sw_obj.clear_product_info()  # 이전 품번 정보를 클리어한다.
            self.sw_obj.decode_poombun()  # 품번 정보 디코딩(파싱)

            if self.filename:
                ret = self.sw_obj.parse_excel_data()  # 품번 기반으로 엑셀에서 정보를 가져온다.
                if not ret:
                    self.tb_poombun_info.append("안내 : 입력하신 품번은 정보고시 파일에 존재하지 않습니다.")
                    return

            dic_prod_info = self.sw_obj.get_product_info()
            #self.Makeimage()
            self.mkimg.setPath(self.path, self.poombun)

            value = self.sw_obj.dic_product["컬러"]
            self.color_full = value.split("/")
            comp = re.compile('[^a-zA-Z/]')
            color = comp.sub('', value)
            color = color.split("/")

            if self.mkimg.checkfile(self.poombun, color):
                self.Makeimage_single()
            else:
                self.tb_poombun_info.setPlainText(f"-실패한 품번-\n{self.mkimg.no_file_itemnumber}-없는이미지-\n{self.mkimg.no_file}\n-경로없음-\n{self.mkimg.no_dir}")
        self.tb_poombun_info.append("\nInfo : 이미지화를 완료했습니다.")

        return

    @pyqtSlot()
    def Makeimage_single(self):

        if len(self.poombun) != 9:
            # self.tb_poombun_info.clear()
            self.tb_poombun_info.setPlainText("품번이 유효하지 않습니다")
            return
        else:
            value = self.sw_obj.dic_product["컬러"]
            comp = re.compile('[^a-zA-Z/]')
            color = comp.sub('', value)
            color = color.split("/")


            len(color)
            if len(color) == 1:
                self.mkimg.makeFV1(self.poombun, color[0], self.color_full)
            elif len(color) == 2:
                self.mkimg.makeFV2(self.poombun, color[0], color[1], self.color_full)
            elif len(color) == 3:
                self.mkimg.makeFV3(self.poombun, color[0], color[1], color[2], self.color_full)

            self.mkimg.makeDV(self.poombun, color[0])

            if "S/S" in self.sw_obj.dic_product["시즌"]:
                season = "봄/여름"
            else:
                season = "가을/겨울"

            product_name = self.sw_obj.dic_product["상품명"].split("(")


            self.mkimg.info_product_name(product_name[0])
            self.mkimg.info_product(self.poombun)
            self.mkimg.info_product(self.sw_obj.dic_product["컬러"])
            self.mkimg.info_product(self.sw_obj.dic_product["기준\n사이즈"])
            self.mkimg.info_product(season)
            self.mkimg.info_product(self.sw_obj.dic_product["세탁방법"])
            self.mkimg.info_product(self.sw_obj.dic_product["원산지"])
            self.mkimg.info_product(self.sw_obj.dic_product["소재"])

            self.mkimg.makeInfo(self.sw_obj.dic_product["상품특성"], self.sw_obj.dic_product["상품특성 값"])
            self.mkimg.info_size(self.sw_obj.size_count + 1)
            self.mkimg.size_insert(self.sw_obj.dic_product["실측사이즈(cm)"])
            for n in range(0, self.sw_obj.size_count):
                self.mkimg.size_insert(self.sw_obj.dic_product[f"사이즈{n}"])

            self.mkimg.combineInfo()
            self.mkimg.combineImg(self.poombun)

            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
