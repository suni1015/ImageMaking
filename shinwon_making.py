"""
실제 이미지를 만드는 클래스

"""
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import configparser
import os

pdt_name = ImageFont.truetype("03_resource/NanumBarunGothic.ttf", 20, encoding="UTF-8")
fnt = ImageFont.truetype("03_resource/NanumBarunGothic.ttf", 15, encoding="UTF-8")
fnt_tip = ImageFont.truetype("03_resource/NanumBarunGothic.ttf", 12, encoding="UTF-8")
ini_filepath = f'./03_resource/setting.ini'

result_path = f'./04_result/'
result_all = f'./04_result/all.jpg'
result_fv = f'./04_result/fv.jpg'
result_dv = f'./04_result/dv.jpg'
result_di = f'./04_result/di.jpg'
result_top = f'./04_result/top.jpg'


class MakeImg:
    def __init__(self):
        self.base_width = 700
        self.base_height = 5500
        self.area = (50, 150, 550, 550)
        self.fullimage = Image.new("RGB", (self.base_width, self.base_height), (255, 255, 255))

        self.no_file = ""
        self.no_file_itemnumber = ""
        self.no_dir = ""

        # ini
        self.ini_config = configparser.ConfigParser()
        self.init_INI()

    def clear_data(self):
        self.no_file = ""
        self.no_file_itemnumber = ""

    def init_INI(self):
        if os.path.isfile(ini_filepath):
            print('info : load ini file')
            self.ini_config.read(ini_filepath)
            self.A1 = self.ini_config['IMG_ORDER']['A1']
            self.A2 = self.ini_config['IMG_ORDER']['A2']
            self.A3 = self.ini_config['IMG_ORDER']['A3']
            self.A4 = self.ini_config['IMG_ORDER']['A4']
            self.A5 = self.ini_config['IMG_ORDER']['A5']

            self.A_list = [self.A1, self.A2, self.A3, self.A4, self.A5]

        else:
            print('info : make default ini file')
            self.make_default_ini()

    def make_default_ini(self):
        # Dictionary 포맷으로 ini 저장하는 방법
        self.ini_config['IMG_ORDER'] = {'A1': '_B',
                                        'A2': '_2',
                                        'A3': '_3',
                                        'A4': '_4',
                                        'A5': '_5'}
        with open(ini_filepath, 'w') as configfile:
            self.ini_config.write(configfile)

    def info_product_name_man(self, name, itemnumber, color):
        self.product_info = Image.new("RGB", (self.base_width, 500), (255, 255, 255))
        draw = ImageDraw.Draw(self.product_info)

        img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A1}.jpg")
        img = img.resize((300, 300))
        self.product_info.paste(img, (0, 70))
        logo = Image.new("RGB", (0, 0), (255, 255, 255))
        # 브랜드 로고 자리

        logo = Image.open(f"03_resource/image/Brand_SIEG.jpg")
        self.product_info.paste(logo, (300, 0))

        self.prd_ptr = 140
        draw.text((310, 140), "품번", fill=(80, 80, 80), font=fnt)
        draw.text((310, 170), "색상", fill=(80, 80, 80), font=fnt)
        draw.text((310, 200), "사이즈", fill=(80, 80, 80), font=fnt)
        draw.text((310, 230), "시즌", fill=(80, 80, 80), font=fnt)
        draw.text((310, 260), "세박방법", fill=(80, 80, 80), font=fnt)
        draw.text((310, 290), "원산지", fill=(80, 80, 80), font=fnt)
        draw.text((310, 320), "소재", fill=(80, 80, 80), font=fnt)

        draw.text((310, 70), name, fill=(0, 0, 0), font=pdt_name)

<<<<<<< HEAD
        # self.product_info.save("test_man.jpg")
=======
        self.product_info.save("test_man.jpg")
>>>>>>> parent of 67c3732 (bug fix)

    def info_product_man(self, text):
        draw = ImageDraw.Draw(self.product_info)

        draw.text((400, self.prd_ptr), text, fill=(0, 0, 0), font=fnt)
        self.prd_ptr += 30

        self.product_info.save("test_man.jpg")

    def info_product_name(self, name):
        self.product_info = Image.new("RGB", (self.base_width, 500), (255, 255, 255))
        self.tag = Image.open("03_resource/image/Product.jpg")
        self.product_info.paste(self.tag, (0, 20))
        draw = ImageDraw.Draw(self.product_info)

        self.prd_ptr = 150
        draw.text((20, 150), "품번", fill=(80, 80, 80), font=fnt)
        draw.text((20, 180), "색상", fill=(80, 80, 80), font=fnt)
        draw.text((20, 210), "사이즈", fill=(80, 80, 80), font=fnt)
        draw.text((20, 240), "시즌", fill=(80, 80, 80), font=fnt)
        draw.text((20, 270), "세박방법", fill=(80, 80, 80), font=fnt)
        draw.text((20, 300), "원산지", fill=(80, 80, 80), font=fnt)
        draw.text((20, 330), "소재", fill=(80, 80, 80), font=fnt)

        draw.text((20, 80), name, fill=(0, 0, 0), font=pdt_name)

    def info_product(self, text):
        draw = ImageDraw.Draw(self.product_info)

        draw.text((135, self.prd_ptr), text, fill=(0, 0, 0), font=fnt)
        self.prd_ptr += 30

        # self.product_info.save("test1.jpg", quallity=95)

    def setPath(self, path, itemnumber):
        self.path = f"{path}/{itemnumber}"
        self.itemnumber = itemnumber

    def checkfile(self, itemnumber, color):

        check = os.path.isdir(self.path)
        if not check:
            print(f"Err : there is no {itemnumber} directory")
            self.no_dir = self.no_dir + itemnumber + "\n"
            self.no_file_itemnumber = self.no_file_itemnumber + itemnumber + "\n"
            return False

        for number in self.A_list:
            check = os.path.isfile(f"{self.path}/{itemnumber}_{color[0]}_{number}.jpg")
            file_name = f"{itemnumber}_{color[0]}_{number}.jpg"
            if not check:
                print(f'Err : there is no {file_name}')
                self.no_file = self.no_file + file_name + "\n"
                self.no_file_itemnumber = self.no_file_itemnumber + itemnumber + "\n"
                print(self.no_file)
                return False

        if not len(color) == 1:
            for n in color:
                check = os.path.isfile(f"{self.path}/{itemnumber}_{n}_{self.A1}.jpg")
                file_name = f"{itemnumber}_{n}_{self.A1}.jpg"
                if not check:
                    print(f'Err : there is no {file_name}')
                    self.no_file = self.no_file + file_name + "\n"
                    self.no_file_itemnumber = self.no_file_itemnumber + itemnumber + "\n"
                    print(self.no_file)
                    return False
        return True

    def makeFV1(self, itemnumber, color, color_full):
        self.fullview = Image.new("RGB", (self.base_width, 1500), (255, 255, 255))
        img = Image.new("RGB", (0, 0), (255, 255, 255))

        if itemnumber[0] == ("B" or "S" or "T" or "V" or "G"):
            if itemnumber[0] == "B":
                img = Image.open("03_resource/image/Brand_베스띠벨리.jpg")
            elif itemnumber[0] == "S":
                img = Image.open("03_resource/image/Brand_씨.jpg")
            elif itemnumber[0] == "T":
                img = Image.open("03_resource/image/Brand_비키.jpg")
            elif itemnumber[0] == "V":
                img = Image.open("03_resource/image/Brand_이사베이.jpg")
            elif itemnumber[0] == "G":
                img = img
            self.fullview.paste(img, (0, 0))
            self.full_ptr = 250
        else:
            self.tag = Image.open("03_resource/image/FullView.jpg")
            self.fullview.paste(self.tag, (0, 20))
            self.full_ptr = 80

        str_img_file = f"{self.path}/{itemnumber}_{color}_{self.A1}.jpg"
        self.img = Image.open(str_img_file)
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        w, h = fnt.getsize(color)
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[0], font=fnt, fill=(0, 0, 0))

        self.full_ptr += self.img.height + 100
        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A2}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        '''
        self.full_ptr += self.img.height + 100
        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_3.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        '''
        self.fullview.save(f"{self.path}/fv.jpg", quallity=100)

        return self.fullview

    def makeFV2(self, itemnumber, color1, color2, color_full):
        self.fullview = Image.new("RGB", (self.base_width, 2200), (255, 255, 255))

        img = Image.new("RGB", (0, 0), (255, 255, 255))

        if itemnumber[0] == ("B" or "S" or "T" or "V" or "G"):
            if itemnumber[0] == "B":
                img = Image.open("03_resource/image/Brand_베스띠벨리.jpg")
            elif itemnumber[0] == "S":
                img = Image.open("03_resource/image/Brand_씨.jpg")
            elif itemnumber[0] == "T":
                img = Image.open("03_resource/image/Brand_비키.jpg")
            elif itemnumber[0] == "V":
                img = Image.open("03_resource/image/Brand_이사베이.jpg")
            elif itemnumber[0] == "G":
                img = img
            self.fullview.paste(img, (0, 0))
            self.full_ptr = 250
        else:
            self.tag = Image.open("03_resource/image/FullView.jpg")
            self.fullview.paste(self.tag, (0, 20))
            self.full_ptr = 80

        self.img = Image.open(f"{self.path}/{itemnumber}_{color2}_{self.A1}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color2)
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[1], font=fnt, fill=(0, 0, 0))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color1}_{self.A1}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color1)
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[0], font=fnt, fill=(0, 0, 0))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color1}_2.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        self.fullview.save(f"{self.path}/fv.jpg", quallity=100)

        return self.fullview

    def makeFV3(self, itemnumber, color1, color2, color3, color_full):
        self.fullview = Image.new("RGB", (self.base_width, 2900), (255, 255, 255))

        img = Image.new("RGB", (0, 0), (255, 255, 255))

        if itemnumber[0] == ("B" or "S" or "T" or "V" or "G"):
            if itemnumber[0] == "B":
                img = Image.open("03_resource/image/Brand_베스띠벨리.jpg")
            elif itemnumber[0] == "S":
                img = Image.open("03_resource/image/Brand_씨.jpg")
            elif itemnumber[0] == "T":
                img = Image.open("03_resource/image/Brand_비키.jpg")
            elif itemnumber[0] == "V":
                img = Image.open("03_resource/image/Brand_이사베이.jpg")
            elif itemnumber[0] == "G":
                img = img
            self.fullview.paste(img, (0, 0))
            self.full_ptr = 250
        else:
            self.tag = Image.open("03_resource/image/FullView.jpg")
            self.fullview.paste(self.tag, (0, 20))
            self.full_ptr = 80

        self.img = Image.open(f"{self.path}/{itemnumber}_{color3}_{self.A1}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color2)
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[2], font=fnt, fill=(0, 0, 0))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color2}_{self.A1}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color2)
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[1], font=fnt, fill=(0, 0, 0))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color1}_{self.A1}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color1)
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[0], font=fnt, fill=(0, 0, 0))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color1}_2.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        self.fullview.save(f"{self.path}/fv.jpg", quallity=100)

        return self.fullview

    def makeDV(self, itemnumber, color):

        detail_ptr = 0
        self.area = (50, 150, 550, 550)
        self.detailview = Image.new("RGB", (self.base_width, 1300), (255, 255, 255))
        self.tag = Image.open("03_resource/image/DetailView.jpg")
        self.detailview.paste(self.tag, (0, 0))
        detail_ptr += 50

        str_tmp = f"{self.path}/{itemnumber}_{color}_{self.A3}.jpg"
        self.img = Image.open(str_tmp)
        self.img = self.img.resize((600, 600))
        self.img = self.img.crop(self.area)
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 10

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A4}.jpg")
        self.img = self.img.resize((600, 600))
        self.img = self.img.crop(self.area)
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 10

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A5}.jpg")
        self.img = self.img.resize((600, 600))
        self.img = self.img.crop(self.area)
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))

        self.detailview.save(f"{self.path}/dv.jpg", quallity=100)

        return self.detailview

    def makeInfo(self, column1, column2):
        self.info_ptr = 0

        # column1 = "비침/n안감/n신축성/n두께감/n탈부착가능여부"
        # column2 = "없음/n있음/n없음/n보통/n없음"
        column1_list = column1.split("\n")
        column2_list = column2.split("\n")

        box = Image.new("RGB", (10, 10), (0, 0, 0))
        black = Image.new("RGB", (10, 10), (0, 0, 0))
        white = Image.new("RGB", (8, 8), (255, 255, 255))
        box.paste(white, (1, 1))

        # 태그
        self.infoview = Image.new("RGB", (self.base_width, 70 + (len(column1_list) * 45)), (255, 255, 255))
        self.tag = Image.open("03_resource/image/DetailInfo.jpg")
        self.infoview.paste(self.tag, (0, 0))
        self.info_ptr += 70

        # 정보고시 안감 두께 등의 공간
        self.info_table = Image.new("RGB", (self.base_width, 47), (244, 244, 244))
        self.infodata = Image.new("RGB", (self.base_width, 43), (255, 255, 255))
        self.info_table.paste(self.infodata, (152, 2))

        # 표 첫줄

        for i in range(0, len(column1_list)):
            self.infoview.paste(self.info_table, (0, self.info_ptr))
            w, h = fnt.getsize(column1_list[i])
            textdraw = ImageDraw.Draw(self.infoview)
            if column2_list[i] == "탈부착가능여부":
                for n in range(0, 4):
                    self.infoview.paste(box, (210 + (n * 120), self.info_ptr + 20))
            else:
                for n in range(0, 3):
                    self.infoview.paste(box, (210 + (n * 120), self.info_ptr + 20))

            textdraw.text(((76 - (w / 2)), self.info_ptr + 16), column1_list[i], font=fnt, fill=(0, 0, 0,))
            if column1_list[i] == "비침":
                textdraw.text((230, self.info_ptr + 16), "있음", font=fnt, fill=(0, 0, 0,))
                textdraw.text((350, self.info_ptr + 16), "약간", font=fnt, fill=(0, 0, 0,))
                textdraw.text((470, self.info_ptr + 16), "없음", font=fnt, fill=(0, 0, 0,))
                if column2_list[i] == "있음":
                    self.infoview.paste(black, (210, self.info_ptr + 20))
                elif column2_list[i] == "약간":
                    self.infoview.paste(black, (330, self.info_ptr + 20))
                else:
                    self.infoview.paste(black, (450, self.info_ptr + 20))
            elif column1_list[i] == "안감":
                textdraw.text((230, self.info_ptr + 16), "있음", font=fnt, fill=(0, 0, 0,))
                textdraw.text((350, self.info_ptr + 16), "없음", font=fnt, fill=(0, 0, 0,))
                textdraw.text((470, self.info_ptr + 16), "기모", font=fnt, fill=(0, 0, 0,))
                if column2_list[i] == "있음":
                    self.infoview.paste(black, (210, self.info_ptr + 20))
                elif column2_list[i] == "없음":
                    self.infoview.paste(black, (330, self.info_ptr + 20))
                else:
                    self.infoview.paste(black, (450, self.info_ptr + 20))
            elif column1_list[i] == "신축성":
                textdraw.text((230, self.info_ptr + 16), "있음", font=fnt, fill=(0, 0, 0,))
                textdraw.text((350, self.info_ptr + 16), "약간", font=fnt, fill=(0, 0, 0,))
                textdraw.text((470, self.info_ptr + 16), "없음", font=fnt, fill=(0, 0, 0,))
                if column2_list[i] == "있음":
                    self.infoview.paste(black, (210, self.info_ptr + 20))
                elif column2_list[i] == "약간":
                    self.infoview.paste(black, (330, self.info_ptr + 20))
                else:
                    self.infoview.paste(black, (450, self.info_ptr + 20))
            elif column1_list[i] == "두께감":
                textdraw.text((230, self.info_ptr + 16), "얆음", font=fnt, fill=(0, 0, 0,))
                textdraw.text((350, self.info_ptr + 16), "보통", font=fnt, fill=(0, 0, 0,))
                textdraw.text((470, self.info_ptr + 16), "도톰", font=fnt, fill=(0, 0, 0,))
                if column2_list[i] == "얆음":
                    self.infoview.paste(black, (210, self.info_ptr + 20))
                elif column2_list[i] == "보통":
                    self.infoview.paste(black, (330, self.info_ptr + 20))
                else:
                    self.infoview.paste(black, (450, self.info_ptr + 20))
            elif column1_list[i] == "핏감":
                textdraw.text((230, self.info_ptr + 16), "슬림핏", font=fnt, fill=(0, 0, 0,))
                textdraw.text((350, self.info_ptr + 16), "스탠다드", font=fnt, fill=(0, 0, 0,))
                textdraw.text((470, self.info_ptr + 16), "오버핏", font=fnt, fill=(0, 0, 0,))
                if column2_list[i] == "슬림핏":
                    self.infoview.paste(black, (210, self.info_ptr + 20))
                elif column2_list[i] == "스탠다드":
                    self.infoview.paste(black, (330, self.info_ptr + 20))
                else:
                    self.infoview.paste(black, (450, self.info_ptr + 20))
            elif column1_list[i] == "탈부착가능여부":
                textdraw.text((230, self.info_ptr + 16), "안감", font=fnt, fill=(0, 0, 0,))
                textdraw.text((350, self.info_ptr + 16), "후드", font=fnt, fill=(0, 0, 0,))
                textdraw.text((470, self.info_ptr + 16), "액세서리", font=fnt, fill=(0, 0, 0,))
                textdraw.text((590, self.info_ptr + 16), "없음", font=fnt, fill=(0, 0, 0,))
                if column2_list[i] == "안감":
                    self.infoview.paste(black, (210, self.info_ptr + 20))
                elif column2_list[i] == "후드":
                    self.infoview.paste(black, (330, self.info_ptr + 20))
                elif column2_list[i] == "액세서리":
                    self.infoview.paste(black, (450, self.info_ptr + 20))
                else:
                    self.infoview.paste(black, (570, self.info_ptr + 20))
            self.info_ptr += 45

        # self.infoview.save("test_info.jpg", quallity=95)

        return self.infoview

    def info_size(self, size_count):

        if 80 + (40 * size_count) > 250:
            self.sizeview = Image.new("RGB", (self.base_width, 80 + (40 * size_count)), (255, 255, 255))
        else:
            self.sizeview = Image.new("RGB", (self.base_width, 250), (255, 255, 255))

        self.grey = True
        # 사이즈 고시할 공간
        self.size_table = Image.new("RGB", (self.base_width - 220, 40), (244, 244, 244))  # (480, 40)
        self.size_table_grey = Image.new("RGB", (self.base_width - 220, 40), (244, 244, 244))
        self.img = Image.new("RGB", (self.base_width - 220, 38), (255, 255, 255))
        self.size_table.paste(self.img, (1, 0))

        self.img = Image.open("03_resource/image/SizeSpec.jpg")
        self.sizeview.paste(self.img, (0, 0))

        img = Image.new("RGB", (0, 0), (255, 255, 255))

        if self.itemnumber[0] == ("B" or "S" or "T" or "V" or "G"):  # 여성구분
            if self.itemnumber[2] == "A":
                if self.itemnumber[3] == "F":
                    img = Image.open("03_resource/image/여성_스카프.jpg")

                elif self.itemnumber[3] == "G":
                    img = Image.open("03_resource/image/가방.jpg")

            elif self.itemnumber[2] == "F":
                img = Image.open("03_resource/image/여성_팬츠.jpg")

            elif self.itemnumber[2] == "S":
                img = Image.open("03_resource/image/여성_치마")

            elif self.itemnumber[2] == "O":
                img = Image.open("03_resource/image/여성_원피스.jpg")

            else:
                img = Image.open("03_resource/image/여성_셔츠.jpg")


        else:  # 남성
            if self.itemnumber[2] == "A":
                if self.itemnumber[3] == "L":
                    img = Image.open("03_resource/image/벨트.jpg")

                elif self.itemnumber[3] == "I":
                    img = Image.open("03_resource/image/넥타이.jpg")

                elif self.itemnumber[3] == "S":
                    img = Image.open("03_resource/image/신발.jpg")
                elif self.itemnumber[3] == "G":
                    img = Image.open("03_resource/image/가방.jpg")


            elif self.itemnumber[2] == ("B" or "C" or "U" or "I"):
                img = Image.open("03_resource/image/상의.jpg")

            elif self.itemnumber[2] == ("F"):
                img = Image.open("03_resource/image/팬츠.jpg")
            else:
                img = Image.open("03_resource/image/자켓.jpg")

        img = img.resize((200, 200))
        self.sizeview.paste(img, (500, int((self.sizeview.height - img.height) / 2)))

        ImageDraw.Draw(self.sizeview).text((40, 440), "단위(cm)", font=fnt_tip, fill=(51, 51, 51))

        self.size_ptr = 70

        # self.sizeview.save("test_size.jpg", quallity=95)

    def size_insert(self, value):
        value_list = value.split("\n")

        if self.grey:
            self.sizeview.paste(self.size_table_grey, (0, self.size_ptr))
            self.grey = False
        else:
            self.sizeview.paste(self.size_table, (0, self.size_ptr))
        num = 1
        for n in value_list:  # 사이즈 어깨넓이 등
            w, h = fnt.getsize(n)
            ImageDraw.Draw(self.sizeview).text(
                (((480 / len(value_list) * num) - (480 / len(value_list) / 2) - (w / 2)), (self.size_ptr + 25 - h)),
                n, font=fnt, fill=(0, 0, 0))
            num += 1
        self.size_ptr += 40

        # self.sizeview.save("test_size2.jpg", quallity=95)

    def info_tip(self):
        self.tip_view = Image.new("RGB", (self.base_width, 150), (255, 255, 255))
        self.tag = Image.open("03_resource/image/Tip.jpg")
        self.tip_view.paste(self.tag, (0, 0))
        self.tip_ptr = 70

        ImageDraw.Draw(self.tip_view).text((20, self.tip_ptr), "-사이즈 스펙은 실측 사이즈 기준입니다.(가슴둘레는 라벨사이즈 기준)", font=fnt_tip,
                                           fill=(60, 60, 60))
        self.tip_ptr += 25
        ImageDraw.Draw(self.tip_view).text((20, self.tip_ptr), "-사이즈는 측정 방법과 생산 과정에 따라 약간의 오차가 발생할 수 있습니다.",
                                           font=fnt_tip, fill=(60, 60, 60))
        self.tip_ptr += 25
        ImageDraw.Draw(self.tip_view).text((20, self.tip_ptr),
                                           "-제품 안쪽 라벨에 표기된 사이즈는 표준 신체 사이즈를 표기한 것이므로, 실측사이즈와 차이가 있을 수 있습니다.",
                                           font=fnt_tip, fill=(60, 60, 60))

    def combineImg(self, item_code):
        self.fullimage = Image.new("RGB", (self.base_width,
                                           self.fullview.height + self.detailview.height + self.info_full.height + self.product_info.height),
                                   (255, 255, 255))
        self.fullimage.paste(self.fullview, (0, 0))
        self.fullimage.paste(self.detailview, (0, self.fullview.height))
        self.fullimage.paste(self.product_info, (0, self.fullview.height + self.detailview.height))
        self.fullimage.paste(self.info_full,
                             (0, self.fullview.height + self.detailview.height + self.product_info.height))

        self.fullimage.save(f"./04_result/{item_code}_full_image.jpg", quallity=100)
        self.fullimage.save(f"{self.path}/{item_code}_result.jpg", quallity=100)

    def combineImg_man(self, item_code):
        self.fullimage = Image.new("RGB", (self.base_width,
                                           self.fullview.height + self.detailview.height + self.info_full.height + self.product_info.height),
                                   (255, 255, 255))
        self.fullimage.paste(self.product_info, (0, 0))
        self.fullimage.paste(self.fullview, (0, self.product_info.height))
        self.fullimage.paste(self.detailview, (0, self.product_info.height + self.fullview.height))
        self.fullimage.paste(self.info_full,
                             (0, self.product_info.height + self.fullview.height + self.detailview.height))

        self.fullimage.save(f"./04_result/{item_code}_full_image.jpg", quallity=100)
        self.fullimage.save(f"{self.path}/{item_code}_result.jpg", quallity=100)

    def combineInfo(self):
        self.info_tip()

        self.info_full = Image.new("RGB", (
            self.base_width, self.infoview.height + self.sizeview.height + self.tip_view.height + 200), (255, 255, 255))

        self.info_full.paste(self.infoview, (0, 0))
        self.info_full.paste(self.sizeview, (0, self.infoview.height + 100))
        self.info_full.paste(self.tip_view, (0, self.infoview.height + self.sizeview.height + 200))

        self.info_full.save(f"{self.path}/di.jpg", quallity=100)


if __name__ == '__main__':
    itemnumber = "PBJAX2032"
    color = "GY"

    mkImage = MakeImg()

    path = "D:\\GitHub\\ImageMaking\\01_data\\man"

    mkImage.setPath("D:/GitHub/ImageMaking/01_data/신원몰/man", itemnumber)
    # mkImage.setPath("D:\GitHub\ImageMaking\01_data\man\PBJAX2032")

    column1 = "비침/n안감/n신축성/n두께감/n탈부착가능여부"
    column2 = "없음/n있음/n없음/n보통/n없음"

    mkImage.makeInfo(column1, column2)
    mkImage.info_size(2)
    mkImage.size_insert("사이즈/n어깨넓이/n가슴둘레/n소매길이/n전체길이")
    mkImage.size_insert("100/n55/n66/n77/n88")
    mkImage.info_tip()
    mkImage.combineInfo()

    mkImage.info_product_name_man("이테리 울 체크 더블 그레이 셋업 정장 자켓", "PBJAX2032", "GY")
    mkImage.info_product_man("PBJAX2032")
    mkImage.info_product_man("그레이(GY)")
    mkImage.info_product_man("95, 97, 100, 103, 105, 110")
    mkImage.info_product_man("가을/겨울")
    mkImage.info_product_man("본 제품은 반드시 드라이크리닝하십시오")
    mkImage.info_product_man("필리핀")
    mkImage.info_product_man("[겉감]폴리에스터1%모99%")
    mkImage.info_product_man("[소매안감]레이온(비스코스)48%폴리에스터52%")

    # mkImage.combineImg()
