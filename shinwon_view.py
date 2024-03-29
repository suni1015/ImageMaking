"""
View 클래스

"""
import sys
import time

import qdarkgraystyle
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import re
import threading

from shinwon_data import Shinwon
from shinwon_making import MakeImg

form_class = uic.loadUiType("./03_resource/ui_imageMaking.ui")[0]


###### CLASS ######
class WindowClass(QMainWindow, form_class):
    filename = None
    still = False
    button = True

    def __init__(self):

        super().__init__()
        self.sw_obj = Shinwon()  # sw_obj = Shinwon('BYJAX1234-0')
        self.mkimg = MakeImg()

        self.poombun = None

        self.image_path = None

        self.setupUi(self)
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())

        self.btn_file_open.clicked.connect(self.OnfileOpen)
        self.btn_path.clicked.connect(self.OnSelectPath)
        self.btn_img_make_single.clicked.connect(self.Makeimage_single)
        self.btn_img_make_multi.clicked.connect(self.Makeimage_thread)
        self.edt_poombun.returnPressed.connect(self.OnEnterPoombun)
        self.edt_poombun.textChanged[str].connect(self.onChangedPoombun)
        self.btn_exam.clicked.connect(self.thumbnail_exam)

    def button_on_off(self):
        if self.button:
            self.btn_file_open.setEnabled(False)
            self.btn_img_make_multi.setEnabled(False)
            self.btn_path.setEnabled(False)
            self.button = False
        else:
            self.btn_file_open.setEnabled(True)
            self.btn_img_make_multi.setEnabled(True)
            self.btn_path.setEnabled(True)
            self.button = True

    @pyqtSlot()
    def OnfileOpen(self):

        self.image_path = None
        self.label_file_path_2.setText('...')

        self.filename = QFileDialog.getOpenFileName(self, 'Open File', '', 'Excel File(*.xls *.xlsx)')
        if self.filename[0]:

            xl_name = self.filename[0].split("/")
            self.label_file_path.setText(xl_name[-1])
            self.path = os.path.dirname(self.filename[0])
        else:
            self.tb_poombun_info.setPlainText("안내 : 파일 선택을 취소하셨습니다.")
            return

        self.sw_obj.openFile_clothInfo(self.filename[0])  # 엑셀 -> dataframe 으로 로딩.

    @pyqtSlot()
    def OnSelectPath(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, "select Directory")

        if self.dir_path:

            self.image_path = self.dir_path
            self.label_file_path_2.setText(self.dir_path)
        else:
            return

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

    def isNaN(self, num):
        return num != num

    @pyqtSlot()
    def Makeimage_multi(self):
        self.still = True

        self.mkimg.clear_data()
        self.mkimg.init_INI()

        if self.check_set.isChecked():
            self.mkimg.set_index = True
        else:
            self.mkimg.set_index = False

        self.success_count = 0
        self.fail_count = 0

        # exception : 품번 리스트가 열려 있는가
        list_poombun = self.sw_obj.get_list_poombun()

        if not self.radio_set.isChecked() and not self.radio_single.isChecked():
            self.tb_poombun_info.setPlainText('단품 세트 중 하나를 선택해 주세요.')
            return

        if list_poombun is None:
            print('품번 리스트가 없습니다. 엑셀 파일을 다시 열어주세요.')
            self.tb_poombun_info.append('품번 리스트가 없습니다. 엑셀 파일을 다시 열어주세요.')
            return

        count = 0
        self.tb_poombun_info.append("\nInfo : 이미지화를 시작합니다.")
        for poombun in list_poombun:
            time.sleep(0.01)
            count = count + 1
            self.tb_poombun_info.append("\nImage making" + str(count))
            var_tf = self.isNaN(poombun)
            if var_tf:
                self.tb_poombun_info.append("ERR : 품번체계 오류(NaN)")
                continue
            '''
            if len(poombun) != 9:
                self.tb_poombun_info.append("ERR : 품번체계는 9자 입니다.")
                continue
            '''
            if len(poombun) == 9:
                self.sw_obj.bSET_poombun = False

            elif len(poombun) == 19:
                self.sw_obj.bSET_poombun = True

            else:
                self.tb_poombun_info.append("ERR : 품번 길이 오류")
                continue

            self.tb_poombun_info.append("품번 : " + poombun)

            self.poombun = poombun
            self.sw_obj.set_poombun(poombun)

            self.sw_obj.clear_product_info()  # 이전 품번 정보를 클리어한다.

            if self.filename:
                if self.sw_obj.bSET_poombun == False:
                    self.sw_obj.decode_poombun()  # 품번 정보 디코딩(파싱)
                    ret = self.sw_obj.parse_excel_data()  # 품번 기반으로 엑셀에서 정보를 가져온다.
                elif self.sw_obj.bSET_poombun == True:
                    self.sw_obj.decode_poombun_set()  # 품번 정보 디코딩(파싱)
                    ret = self.sw_obj.parse_excel_data_set()  # 품번 기반으로 엑셀에서 정보를 가져온다.
                else:
                    self.tb_poombun_info.append("ERR : 일반 품번인지 Set 품번인지 구분하지 못했습니다")
                    self.fail_count += 1
                    continue

                if not ret:
                    self.tb_poombun_info.append("안내 : 입력하신 품번은 정보고시 파일에 존재하지 않습니다.")
                    continue  # return

            dic_prod_info = self.sw_obj.get_product_info()
            # self.Makeimage()
            if not self.image_path == None:
                self.mkimg.setPath(self.image_path, self.poombun)
            else:
                self.mkimg.setPath(self.path, self.poombun)

            # 추후 '컬럼' key 통일 시킨 후 아래 구분 구문 제거해도 됨.
            if self.sw_obj.bSET_poombun == False:
                value = dic_prod_info["컬러"]
            if self.sw_obj.bSET_poombun == True:
                value = dic_prod_info["컬러명 ( 한글/영문 )"]

            self.color_full = value.split("/")
            comp = re.compile('[^a-zA-Z/]')
            color = comp.sub('', value)
            self.color = color.split("/")
            if self.sw_obj.bSET_poombun == False:  # 단품 제작
                if self.mkimg.checkfile(self.poombun, self.color):
                    self.Makeimage_single()
                else:
                    self.fail_count += 1
            elif self.sw_obj.bSET_poombun == True:  # 세트 제작
                if self.mkimg.checkfile_set(self.poombun, self.color):
                    self.Makeimage_set()
                    self.success_count += 1
                else:
                    self.fail_count += 1
            verScrollBar = self.tb_poombun_info.verticalScrollBar()
            verScrollBar.setValue(verScrollBar.maximum())

        self.tb_poombun_info.append("\nInfo : 이미지화를 완료했습니다.")

        self.tb_poombun_info.append(f"\n 완료: {self.success_count}건\n 오류: {self.fail_count}건")
        self.tb_poombun_info.append(
            f"\n-경로없음-\n{self.mkimg.no_dir}\n-이미지없음-\n{self.mkimg.no_file}")
        # \n-실패한 품번-\n{self.mkimg.no_file_itemnumber}

        verScrollBar = self.tb_poombun_info.verticalScrollBar()
        verScrollBar.setValue(verScrollBar.maximum())

        self.still = False
        self.button_on_off()

        return

    def Makeimage_thread(self):
        self.button_on_off()

        th = threading.Thread(target=self.Makeimage_multi)
        th.daemon = True
        if not self.still == True:
            th.start()
        else:
            print('still')

    @pyqtSlot()
    def Makeimage_single(self):
        try:
            if len(self.poombun) != 9:
                # self.tb_poombun_info.clear()
                self.tb_poombun_info.append(f"{self.poombun}의 품번이 유효하지 않습니다")
                return
            else:
                if not self.format_radio_1.isChecked():
                    if self.format_radio_2.isChecked():
                        self.Makeimage_P_style()
                    elif self.format_radio_3.isChecked():
                        self.Makeimage_P_style_B()
                    elif self.format_radio_4.isChecked():
                        self.Makeimage_F_style()
                    elif self.format_radio_5.isChecked():
                        self.Makeimage_WOMAN_style()
                    elif self.format_radio_6.isChecked():
                        self.Makeimage_acce_style()
                    return
                else:
                    if self.sw_obj.dic_product['성별'] == '남성':

                        if self.poombun[2] in ["A"]:  # FV
                            self.Makeimage_acce_style()

                        elif self.poombun[0] == "P":

                            if self.poombun[1] in ["A", "X", "Y", "Z"]:
                                self.Makeimage_P_style_B()
                            else:
                                self.Makeimage_P_style()

                        elif self.poombun[0] == "F":
                            self.Makeimage_P_style()
                        else:
                            self.Makeimage_NONE_style()

                    else:
                        if self.poombun[2] in ["A"]:
                            self.Makeimage_acce_style()
                        else:
                            self.Makeimage_WOMAN_style()

            self.success_count += 1
            return

        except FileNotFoundError as ex:

            error = str(ex).split("/")
            self.tb_poombun_info.append(f"'{error[-1]} 가 없습니다")

            # error = str(ex).split("'")
            # self.tb_poombun_info.append(f"'{error[1]} 가 없습니다")
            self.fail_count += 1
            return

    @pyqtSlot()
    def Makeimage_set(self):
        if len(self.poombun) != 19:
            # self.tb_poombun_info.clear()
            self.tb_poombun_info.append(f"{self.poombun}의 품번이 유효하지 않습니다")
            return
        else:
            value = self.sw_obj.dic_product_set['컬러명 ( 한글/영문 )']
            comp = re.compile('[^a-zA-Z/]')
            color = comp.sub('', value)
            color = color.split("/")

            poombun = self.poombun.split("_")
            # poombun[0]=상의 poombun[1]=하의

            if "S/S" in self.sw_obj.dic_product_set["시즌"]:
                season = "봄/여름"
            else:
                season = "가을/겨울"

            index2 = self.sw_obj.dic_product_set['사이즈'].split("\n")

            while "" in index2:
                index2.remove("")
            while "상의" in index2:
                index2.remove("상의")

            n = index2.index("하의")

            top_size = index2[0]
            bottom_size = index2[2]

            # product_name = self.sw_obj.dic_product_set["상품명"].split("(")
            product_name = self.sw_obj.dic_product_set["상품명"].replace(f"({self.poombun})", "")

            if self.sw_obj.dic_product_set['성별'] == '남성':

                self.mkimg.makeSet(poombun[0], poombun[1])

                self.mkimg.info_product_name_set(product_name, self.poombun, self.sw_obj.dic_product_set["소재"])

                self.mkimg.info_product_set(self.poombun, 0)
                self.mkimg.info_product_set(self.sw_obj.dic_product_set['컬러명 ( 한글/영문 )'], 0)
                self.mkimg.info_product_set(season, 0)
                self.mkimg.info_product_set(self.sw_obj.dic_product_set["세탁방법"], 0)
                self.mkimg.info_product_set(self.sw_obj.dic_product_set["원산지"], 1)

                self.mkimg.info_product_set(top_size, 2)
                for i in self.mkimg.top_resource:
                    self.mkimg.info_product_set(i, 2)
                self.mkimg.prd_ptr += 50

                self.mkimg.info_product_set(bottom_size, 2)
                for i in self.mkimg.bottom_resource:
                    self.mkimg.info_product_set(i, 2)

                self.mkimg.combineSet(self.poombun)
                if self.check_thumb.isChecked():
                    self.mkimg.thumbnail_set(color, self.thumbnail_x.text(), self.thumbnail_y.text())
            return

    def Makeimage_P_style_B(self):

        if len(self.poombun) != 9:
            # self.tb_poombun_info.clear()
            self.tb_poombun_info.append(f"{self.poombun}의 품번이 유효하지 않습니다")
            return
        else:
            if self.poombun[2] in ["J", "V"]:
                self.mkimg.makeFV_man(self.poombun, self.color[0])
                self.mkimg.makeDV(self.poombun, self.color[0])
            else:
                self.mkimg.makeFV_man_3(self.poombun, self.color[0])
                self.mkimg.makeDV3(self.poombun, self.color[0])

            self.mkimg.makeInfo(self.sw_obj.dic_product["상품특성"], self.sw_obj.dic_product["상품특성 값"])
            self.mkimg.info_size(self.sw_obj.size_count + 1)
            self.mkimg.size_insert(self.sw_obj.dic_product["실측사이즈(cm)"])
            for n in range(0, self.sw_obj.size_count):
                self.mkimg.size_insert(str(self.sw_obj.dic_product[f"사이즈{n}"]))

            # float (nan)

            self.mkimg.combineInfo()

            if "S/S" in self.sw_obj.dic_product["시즌"]:
                season = "봄/여름"
            else:
                season = "가을/겨울"

            product_name = self.sw_obj.dic_product["상품명"].replace(f"({self.poombun})", "")

            self.mkimg.info_product_name_man(product_name, self.poombun, self.color[0], True)
            self.mkimg.info_product_man(self.poombun)
            self.mkimg.info_product_man(self.sw_obj.dic_product["컬러"])
            self.mkimg.info_product_man(self.sw_obj.dic_product["기준\n사이즈"])
            self.mkimg.info_product_man(season)
            self.mkimg.info_product_man(self.sw_obj.dic_product["세탁방법"])
            self.mkimg.info_product_man(self.sw_obj.dic_product["원산지"])

            list_material = self.sw_obj.dic_product["소재"].split("\n")

            self.mkimg.product_index()
            for i in list_material:
                self.mkimg.info_product_man(i)
            self.mkimg.product_index()

            self.mkimg.combineImg_man(self.poombun)

            if self.check_thumb.isChecked():
                self.mkimg.thumbnail(self.color, self.thumbnail_x.text(), self.thumbnail_y.text())

            return

    def Makeimage_P_style(self):

        if len(self.poombun) != 9:
            # self.tb_poombun_info.clear()
            self.tb_poombun_info.append(f"{self.poombun}의 품번이 유효하지 않습니다")
            return
        else:
            self.mkimg.makeFV_man_2(self.poombun, self.color[0])
            self.mkimg.makeDV2(self.poombun, self.color[0])

            self.mkimg.makeInfo(self.sw_obj.dic_product["상품특성"], self.sw_obj.dic_product["상품특성 값"])
            self.mkimg.info_size(self.sw_obj.size_count + 1)
            self.mkimg.size_insert(self.sw_obj.dic_product["실측사이즈(cm)"])
            for n in range(0, self.sw_obj.size_count):
                self.mkimg.size_insert(str(self.sw_obj.dic_product[f"사이즈{n}"]))

            # float (nan)

            self.mkimg.combineInfo()

            if "S/S" in self.sw_obj.dic_product["시즌"]:
                season = "봄/여름"
            else:
                season = "가을/겨울"

            product_name = self.sw_obj.dic_product["상품명"].replace(f"({self.poombun})", "")

            self.mkimg.info_product_name_man(product_name, self.poombun, self.color[0], False)
            self.mkimg.info_product_man(self.poombun)
            self.mkimg.info_product_man(self.sw_obj.dic_product["컬러"])
            self.mkimg.info_product_man(self.sw_obj.dic_product["기준\n사이즈"])
            self.mkimg.info_product_man(season)
            self.mkimg.info_product_man(self.sw_obj.dic_product["세탁방법"])
            self.mkimg.info_product_man(self.sw_obj.dic_product["원산지"])

            list_material = self.sw_obj.dic_product["소재"].split("\n")

            self.mkimg.product_index()
            for i in list_material:
                self.mkimg.info_product_man(i)
            self.mkimg.product_index()

            self.mkimg.combineImg_man(self.poombun)

            if self.check_thumb.isChecked():
                self.mkimg.thumbnail(self.color, self.thumbnail_x.text(), self.thumbnail_y.text())

        return


    def Makeimage_F_style(self):
        if len(self.poombun) != 9:
            # self.tb_poombun_info.clear()
            self.tb_poombun_info.append(f"{self.poombun}의 품번이 유효하지 않습니다")
            return
        else:
            self.mkimg.makeFV_man_2(self.poombun, self.color[0])
            self.mkimg.makeDV2(self.poombun, self.color[0])

            self.mkimg.makeInfo(self.sw_obj.dic_product["상품특성"], self.sw_obj.dic_product["상품특성 값"])
            self.mkimg.info_size(self.sw_obj.size_count + 1)
            self.mkimg.size_insert(self.sw_obj.dic_product["실측사이즈(cm)"])
            for n in range(0, self.sw_obj.size_count):
                self.mkimg.size_insert(str(self.sw_obj.dic_product[f"사이즈{n}"]))

            # float (nan)

            self.mkimg.combineInfo()

            if "S/S" in self.sw_obj.dic_product["시즌"]:
                season = "봄/여름"
            else:
                season = "가을/겨울"

            product_name = self.sw_obj.dic_product["상품명"].replace(f"({self.poombun})", "")

            self.mkimg.info_product_name_man(product_name, self.poombun, self.color[0], False)
            self.mkimg.info_product_man(self.poombun)
            self.mkimg.info_product_man(self.sw_obj.dic_product["컬러"])
            self.mkimg.info_product_man(self.sw_obj.dic_product["기준\n사이즈"])
            self.mkimg.info_product_man(season)
            self.mkimg.info_product_man(self.sw_obj.dic_product["세탁방법"])
            self.mkimg.info_product_man(self.sw_obj.dic_product["원산지"])

            list_material = self.sw_obj.dic_product["소재"].split("\n")

            self.mkimg.product_index()
            for i in list_material:
                self.mkimg.info_product_man(i)
            self.mkimg.product_index()

            self.mkimg.combineImg_man(self.poombun)

            if self.check_thumb.isChecked():
                self.mkimg.thumbnail(self.color, self.thumbnail_x.text(), self.thumbnail_y.text())

        return


    def Makeimage_NONE_style(self):
        if len(self.poombun) != 9:
            # self.tb_poombun_info.clear()
            self.tb_poombun_info.append(f"{self.poombun}의 품번이 유효하지 않습니다")
            return
        else:
            if self.poombun[2] in ["F", "P"]:
                self.mkimg.makeFV_man_2(self.poombun, self.color[0])
            else:
                self.mkimg.makeFV_man(self.poombun, self.color[0])

            self.mkimg.makeDV(self.poombun, self.color[0])

            self.mkimg.makeInfo(self.sw_obj.dic_product["상품특성"], self.sw_obj.dic_product["상품특성 값"])
            self.mkimg.info_size(self.sw_obj.size_count + 1)
            self.mkimg.size_insert(self.sw_obj.dic_product["실측사이즈(cm)"])
            for n in range(0, self.sw_obj.size_count):
                self.mkimg.size_insert(str(self.sw_obj.dic_product[f"사이즈{n}"]))

            # float (nan)

            self.mkimg.combineInfo()

            if "S/S" in self.sw_obj.dic_product["시즌"]:
                season = "봄/여름"
            else:
                season = "가을/겨울"

            product_name = self.sw_obj.dic_product["상품명"].replace(f"({self.poombun})", "")

            self.mkimg.info_product_name_man(product_name, self.poombun, self.color[0], False)
            self.mkimg.info_product_man(self.poombun)
            self.mkimg.info_product_man(self.sw_obj.dic_product["컬러"])
            self.mkimg.info_product_man(self.sw_obj.dic_product["기준\n사이즈"])
            self.mkimg.info_product_man(season)
            self.mkimg.info_product_man(self.sw_obj.dic_product["세탁방법"])
            self.mkimg.info_product_man(self.sw_obj.dic_product["원산지"])

            list_material = self.sw_obj.dic_product["소재"].split("\n")

            self.mkimg.product_index()
            for i in list_material:
                self.mkimg.info_product_man(i)
            self.mkimg.product_index()

            self.mkimg.combineImg_man(self.poombun)

            if self.check_thumb.isChecked():
                self.mkimg.thumbnail(self.color, self.thumbnail_x.text(), self.thumbnail_y.text())

        return


    def Makeimage_WOMAN_style(self):
        if len(self.poombun) != 9:
            self.tb_poombun_info.append(f"{self.poombun}의 품번이 유효하지 않습니다")
            return
        else:
            self.mkimg.makeInfo(self.sw_obj.dic_product["상품특성"], self.sw_obj.dic_product["상품특성 값"])
            self.mkimg.info_size(self.sw_obj.size_count + 1)
            self.mkimg.size_insert(self.sw_obj.dic_product["실측사이즈(cm)"])
            for n in range(0, self.sw_obj.size_count):
                self.mkimg.size_insert(str(self.sw_obj.dic_product[f"사이즈{n}"]))

            self.mkimg.combineInfo()

            if "S/S" in self.sw_obj.dic_product["시즌"]:
                season = "봄/여름"
            else:
                season = "가을/겨울"

            product_name = self.sw_obj.dic_product["상품명"].replace(f"({self.poombun})", "")

            self.mkimg.makeFV_woman(self.poombun, self.sw_obj.dic_product["컬러"])

            self.mkimg.makeDV_woman(self.poombun, self.color[0])

            self.mkimg.info_product_name(product_name)
            self.mkimg.info_product(self.poombun)
            self.mkimg.info_product(self.sw_obj.dic_product["컬러"])
            self.mkimg.info_product(self.sw_obj.dic_product["기준\n사이즈"])
            self.mkimg.info_product(season)
            self.mkimg.info_product(self.sw_obj.dic_product["세탁방법"])
            self.mkimg.info_product(self.sw_obj.dic_product["원산지"])

            self.mkimg.info_product(self.sw_obj.dic_product["소재"])

            self.mkimg.combineImg(self.poombun)

        if self.check_thumb.isChecked():
            self.mkimg.thumbnail(self.color, self.thumbnail_x.text(), self.thumbnail_y.text())

        return


    def Makeimage_acce_style(self):
        if len(self.poombun) != 9:
            self.tb_poombun_info.append(f"{self.poombun}의 품번이 유효하지 않습니다")
            return
        else:
            self.mkimg.makeInfo(self.sw_obj.dic_product["상품특성"], self.sw_obj.dic_product["상품특성 값"])
            self.mkimg.info_size(self.sw_obj.size_count + 1)
            self.mkimg.size_insert(self.sw_obj.dic_product["실측사이즈(cm)"])
            for n in range(0, self.sw_obj.size_count):
                self.mkimg.size_insert(str(self.sw_obj.dic_product[f"사이즈{n}"]))

            self.mkimg.combineInfo()

            if "S/S" in self.sw_obj.dic_product["시즌"]:
                season = "봄/여름"
            else:
                season = "가을/겨울"

            product_name = self.sw_obj.dic_product["상품명"].replace(f"({self.poombun})", "")

            if self.sw_obj.dic_product['성별'] == '남성':
                self.mkimg.makeFV_acce_man(self.poombun, self.color[0])
                self.mkimg.makeDV_acce(self.poombun, self.color[0], self.sw_obj.dic_product['성별'])

                self.mkimg.info_product_name_man(product_name, self.poombun, self.color[0], False)
                self.mkimg.info_product_man(self.poombun)
                self.mkimg.info_product_man(self.sw_obj.dic_product["컬러"])
                self.mkimg.info_product_man(self.sw_obj.dic_product["기준\n사이즈"])
                self.mkimg.info_product_man(season)
                self.mkimg.info_product_man(self.sw_obj.dic_product["세탁방법"])
                self.mkimg.info_product_man(self.sw_obj.dic_product["원산지"])

                list_material = self.sw_obj.dic_product["소재"].split("\n")

                self.mkimg.product_index()
                for i in list_material:
                    self.mkimg.info_product_man(i)
                self.mkimg.product_index()

                self.mkimg.combineImg_man(self.poombun)
            else:
                self.mkimg.makeFV_acce_woman(self.poombun, self.sw_obj.dic_product["컬러"])
                self.mkimg.makeDV_acce(self.poombun, self.color[0], self.sw_obj.dic_product['성별'])

                self.mkimg.info_product_name(product_name)
                self.mkimg.info_product(self.poombun)
                self.mkimg.info_product(self.sw_obj.dic_product["컬러"])
                self.mkimg.info_product(self.sw_obj.dic_product["기준\n사이즈"])
                self.mkimg.info_product(season)
                self.mkimg.info_product(self.sw_obj.dic_product["세탁방법"])
                self.mkimg.info_product(self.sw_obj.dic_product["원산지"])

                self.mkimg.info_product(self.sw_obj.dic_product["소재"])

                self.mkimg.combineImg(self.poombun)

            if self.check_thumb.isChecked():
                self.mkimg.thumbnail(self.color, self.thumbnail_x.text(), self.thumbnail_y.text())

        return

    def thumbnail_exam(self):
        self.mkimg.thumbnail_exam(self.thumbnail_x.text(), self.thumbnail_y.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
