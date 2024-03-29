"""
실제 이미지를 만드는 클래스

"""
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import configparser
import os
import re

pdt_name = ImageFont.truetype("03_resource/NotoSansCJKkr-Regular.otf", 22, encoding="UTF-8")
fnt = ImageFont.truetype("03_resource/NotoSansCJKkr-Regular.otf", 15, encoding="UTF-8")
fnt_bold = ImageFont.truetype("03_resource/NotoSansCJKkr-Bold.otf", 15, encoding="UTF-8")
fnt_FV = ImageFont.truetype("03_resource/NotoSansCJKkr-Regular.otf", 14, encoding="UTF-8")
fnt3 = ImageFont.truetype("03_resource/NotoSansCJKkr-Regular.otf", 13, encoding="UTF-8")
fnt_tip = ImageFont.truetype("03_resource/NotoSansCJKkr-Regular.otf", 12, encoding="UTF-8")
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

        self.prd_index = True

        self.set_index = False

        # ini
        self.ini_config = configparser.ConfigParser()
        self.init_INI()

        self.break_line = Image.new("RGB", (700, 1), (220, 220, 220))

    def clear_data(self):
        self.no_file = ""
        self.no_file_itemnumber = ""
        self.no_dir = ""

    def init_INI(self):
        if os.path.isfile(ini_filepath):
            print('info : load ini file')
            self.ini_config.read(ini_filepath)
            self.A1 = self.ini_config['IMG_ORDER']['A1']
            self.A2 = self.ini_config['IMG_ORDER']['A2']
            self.A3 = self.ini_config['IMG_ORDER']['A3']
            self.A4 = self.ini_config['IMG_ORDER']['A4']
            self.A5 = self.ini_config['IMG_ORDER']['A5']
            self.A6 = self.ini_config['IMG_ORDER']['A6']

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

    def product_index(self):
        if self.prd_index:
            self.prd_index = False
        else:
            self.prd_index = True

    def info_product_name_man(self, name, itemnumber, color, index):
        self.product_info = Image.new("RGB", (self.base_width, 565), (255, 255, 255))
        draw = ImageDraw.Draw(self.product_info)

        img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A1}.jpg")

        if index:
            img = img.resize((330, 330))
            self.product_info.paste(img, (-15, 100))

        elif itemnumber[0] == "P" and not itemnumber[1] in ["A", "X", "Y", "Z"]:
            img = img.resize((330, 330))
            self.product_info.paste(img, (-15, 100))
        elif itemnumber[2] in ["P", "F"]:
            img = img.resize((450, 450))
            self.product_info.paste(img, (-75, 70))
        else:
            img = img.resize((330, 330))
            self.product_info.paste(img, (-15, 100))

        logo = Image.new("RGB", (0, 80), (255, 255, 255))
        # 브랜드 로고 자리

        if self.itemnumber[0] == "P":
            logo = Image.open("03_resource/image/지이크(썸네일).png")
            logo = logo.resize((int(logo.width / 8), int(logo.height / 8)))
        elif self.itemnumber[0] == "F":
            logo = Image.open("03_resource/image/파렌하이트(썸네일).png")
            logo = logo.resize((int(logo.width / 7), int(logo.height / 7)))
        elif self.itemnumber[0] == "Q":
            logo = Image.open("03_resource/image/Brand_아이코닉.jpg")
            logo = logo.crop((250, 0, 750, 300))
            logo = logo.resize((167, 100))

        self.product_info.paste(logo, (305, 110 - logo.height), logo)

        self.prd_ptr = 190

        content_list = ["품번", "색상", "사이즈", "시즌", "세탁방법", "원산지", "소재"]  # 상품정보고시 제작
        for content in content_list:
            draw.text((315, 190 + (content_list.index(content) * 30)), content, fill=(100, 100, 100), font=fnt)
            if not content == "소재":
                self.product_info.paste(self.break_line, (305, 213 + (30 * content_list.index(content))))
        w, h = pdt_name.getsize(name)
        if w < 400:  # 상품이름이 너무길경우
            draw.text((305, 120), name, fill=(25, 25, 25), font=pdt_name)
        else:
            i = len(name) - 1
            while True:
                if name[i] == " ":
                    w, h = pdt_name.getsize(name[:i])
                    if w < 400:
                        break
                i -= 1
            draw.text((305, 120), name[:i], fill=(25, 25, 25), font=pdt_name)
            draw.text((305, 150), name[i + 1:], fill=(25, 25, 25), font=pdt_name)

        # self.product_info.save("test_man.jpg")

    def info_product_man(self, text):
        draw = ImageDraw.Draw(self.product_info)

        if len(text) <= 23 or not text[0] == "[":
            draw.text((420, self.prd_ptr), text, fill=(70, 70, 70), font=fnt)

            if self.prd_index:
                self.prd_ptr += 30
            else:
                self.prd_ptr += 25
        else:
            i = 23
            while True:
                if text[i] == "%":
                    break
                i -= 1

            title = text.split("]")
            title = title[0] + "]"
            w, h = fnt.getsize(title)

            draw.text((420, self.prd_ptr), text[:i + 1], fill=(70, 70, 70), font=fnt)
            self.prd_ptr += 25
            draw.text((420 + w, self.prd_ptr), text[i + 1:], fill=(70, 70, 70), font=fnt)
            self.prd_ptr += 25

        # [겉감]폴리우레탄5%레이온28% <17> 폴리에스터40%

        # self.product_info.save("test_man.jpg")

    def info_product_name(self, name):
        self.product_info = Image.new("RGB", (self.base_width, 490), (255, 255, 255))
        self.tag = Image.open("03_resource/image/Product.jpg")
        self.product_info.paste(self.tag, (0, 30))
        draw = ImageDraw.Draw(self.product_info)

        self.prd_ptr = 150

        '''
        draw.text((20, 150), "품번", fill=(100, 100, 100), font=fnt)
        draw.text((20, 180), "색상", fill=(100, 100, 100), font=fnt)
        draw.text((20, 210), "사이즈", fill=(100, 100, 100), font=fnt)
        draw.text((20, 240), "시즌", fill=(100, 100, 100), font=fnt)
        draw.text((20, 270), "세탁방법", fill=(100, 100, 100), font=fnt)
        draw.text((20, 300), "원산지", fill=(100, 100, 100), font=fnt)
        draw.text((20, 330), "소재", fill=(100, 100, 100), font=fnt)
        '''

        content_list = ["품번", "색상", "사이즈", "시즌", "세탁방법", "원산지", "소재"]  # 상품정보고시 제작
        for content in content_list:
            draw.text((20, 150 + (content_list.index(content) * 30)), content, fill=(100, 100, 100), font=fnt)

        draw.text((20, 80), name, fill=(25, 25, 25), font=pdt_name)

        draw.text((20, 470), "※ 색상 및 리오더 상품에 따라 소재가 케어라벨과 상이할 수 있습니다.", fill=(100, 100, 100), font=fnt3)

    def info_product(self, text):
        draw = ImageDraw.Draw(self.product_info)

        draw.text((135, self.prd_ptr), text, fill=(70, 70, 70), font=fnt)
        self.prd_ptr += 30

        # self.product_info.save("test1.jpg", quallity=95)

    def info_product_name_set(self, name, itemnumber, index):
        self.product_info = Image.new("RGB", (self.base_width, 700), (255, 255, 255))
        draw = ImageDraw.Draw(self.product_info)

        top_code = itemnumber.split("_")[0]
        bottom_code = itemnumber.split("_")[1]

        space = index.split("하의")
        self.top_space = space[0].count('\n')
        self.bottom_space = space[1].count('\n')

        if self.full_code_dir == True:
            try:
                img = Image.open(f"{self.path}/{itemnumber}_1.jpg")
            except:
                img = Image.open(f"{self.path}/{itemnumber}_B.jpg")
            img = img.resize((500, 500))
            self.product_info.paste(img, (-100, 90))
        else:
            try:
                img = Image.open(f"{self.dir}/{top_code}/{top_code}_{self.color}_1.jpg")
            except:
                img = Image.open(f"{self.dir}/{top_code}/{top_code}_{self.color}_B.jpg")
            img2 = Image.open(f"{self.dir}/{bottom_code}/{bottom_code}_{self.color}_6.jpg")

            product_image = Image.new("RGB", (900, 1500), (255, 255, 255))
            product_image.paste(img2, (0, 720))
            product_image.paste(img, (0, 0))
            try:
                product_image.save(f"{self.path}/{itemnumber}_03.jpg")
            except:
                print("결과물 출력에 실패했습니다")
            img = img.resize((300, 300))
            img2 = img2.resize((300, 300))
            self.product_info.paste(img2, (0, 330))
            self.product_info.paste(img, (0, 90))

        logo = Image.new("RGB", (0, 0), (255, 255, 255))
        # 브랜드 로고 자리

        if self.itemnumber[0] == "P":
            logo = Image.open("03_resource/image/지이크(썸네일).png")
            logo = logo.resize((int(logo.width / 8), int(logo.height / 8)))
        elif self.itemnumber[0] == "F":
            logo = Image.open("03_resource/image/파렌하이트(썸네일).png")
            logo = logo.resize((int(logo.width / 7), int(logo.height / 7)))
        elif self.itemnumber[0] == "Q":
            logo = Image.open("03_resource/image/Brand_아이코닉.jpg")
            logo = logo.crop((250, 0, 750, 300))
            logo = logo.resize((167, 100))

        self.product_info.paste(logo, (305, 90 - logo.height), logo)

        draw.text((310, 170), "품번", fill=(100, 100, 100), font=fnt)
        draw.text((310, 200), "색상", fill=(100, 100, 100), font=fnt)
        draw.text((310, 230), "시즌", fill=(100, 100, 100), font=fnt)
        draw.text((310, 260), "세탁방법", fill=(100, 100, 100), font=fnt)
        draw.text((310, 290), "원산지", fill=(100, 100, 100), font=fnt)
        draw.text((310, 330), "[상의]", fill=(100, 100, 100), font=fnt)
        draw.text((310, 355), "사이즈", fill=(100, 100, 100), font=fnt)
        draw.text((310, 380), "소재", fill=(100, 100, 100), font=fnt)

        self.prd_ptr = 380
        for i in range(self.top_space - 2):
            self.prd_ptr += 25

        draw.text((310, self.prd_ptr), "[하의]", fill=(100, 100, 100), font=fnt)
        draw.text((310, self.prd_ptr + 25), "사이즈", fill=(100, 100, 100), font=fnt)
        draw.text((310, self.prd_ptr + 50), "소재", fill=(100, 100, 100), font=fnt)

        w, h = pdt_name.getsize(name)
        if w < 400:  # 상품이름이 너무길경우
            draw.text((305, 110), name, fill=(25, 25, 25), font=pdt_name)
        else:
            i = len(name) - 1
            while True:
                if name[i] == " ":
                    w, h = pdt_name.getsize(name[:i])
                    if w < 400:
                        break
                i -= 1
            draw.text((305, 110), name[:i], fill=(25, 25, 25), font=pdt_name)
            draw.text((305, 140), name[i + 1:], fill=(25, 25, 25), font=pdt_name)

        depart_line = Image.new("RGB", (500, 1), (230, 230, 230))
        for i in range(5):
            self.product_info.paste(depart_line, (305, 196 + (i * 30)))
        self.product_info.paste(depart_line, (305, self.prd_ptr - 15))

        self.prd_ptr = 170

        index2 = index.split("\n")

        while "" in index2:
            index2.remove("")
        while "상의" in index2:
            index2.remove("상의")

        n = index2.index("하의")

        self.top_resource = index2[:n]
        self.bottom_resource = index2[n + 1:]

        # self.product_info.save("test_man.jpg")

    def info_product_set(self, text, i):
        draw = ImageDraw.Draw(self.product_info)

        if i == 0:
            draw.text((380, self.prd_ptr), text, fill=(70, 70, 70), font=fnt)
            self.prd_ptr += 30
        elif i == 1:
            draw.text((380, self.prd_ptr), text, fill=(70, 70, 70), font=fnt)
            self.prd_ptr += 65
        elif i == 2:
            draw.text((380, self.prd_ptr), text, fill=(70, 70, 70), font=fnt)
            self.prd_ptr += 25
        elif i == 3:
            draw.text((380, self.prd_ptr), text, fill=(70, 70, 70), font=fnt)
            self.prd_ptr += 75

        # self.product_info.save("test_man2.jpg")

    def setPath(self, path, itemnumber):
        self.dir = f"{path}"
        self.path = f"{path}/{itemnumber}"
        self.itemnumber = itemnumber

    def checkfile(self, itemnumber, color):

        check = os.path.isdir(self.path)
        if not check:
            print(f"Err : there is no {itemnumber} directory")
            self.no_dir = self.no_dir + itemnumber + "\n"
            self.no_file_itemnumber = self.no_file_itemnumber + itemnumber + "\n"
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

        if not os.path.isdir("04_result"):
            os.makedirs("04_result")

        self.color = color[0]

        return True

    def checkfile_set(self, itemnumber, color):

        item_top = itemnumber.split("_")[0]
        item_bottom = itemnumber.split("_")[1]

        code_list = [item_top, item_bottom]

        for i in code_list:

            check = os.path.isdir(f"{self.dir}/{i}")

            if not check:
                print(f"Err : there is no {i} directory")
                self.no_dir = self.no_dir + i + "\n"
                self.no_file_itemnumber = self.no_file_itemnumber + i + "\n"
                return False
        if os.path.isfile(f"{self.dir}/{itemnumber}/{itemnumber}_B.jpg") or os.path.isfile(
                f"{self.dir}/{itemnumber}/{itemnumber}_1.jpg"):
            self.full_code_dir = True
        else:
            self.full_code_dir = False

        for i in code_list:
            for jpg in ["fv", "dv"]:
                check = os.path.isfile(f"{self.dir}/{i}/{i}_{jpg}.jpg")
                file_name = f"{i}_{jpg}.jpg"

                if not check:
                    print(f'Err : there is no {file_name}')
                    self.no_file = self.no_file + file_name + "\n"
                    self.no_file_itemnumber = self.no_file_itemnumber + itemnumber + "\n"
                    print(self.no_file)
                    return False
        check = os.path.isfile(f"{self.dir}/{itemnumber}/{itemnumber}_1.jpg")
        check2 = os.path.isfile(f"{self.dir}/{itemnumber}/{itemnumber}_B.jpg")
        '''
        if not check and not check2:
            print(f'Err : there is no {itemnumber}_1.jpg')
            self.no_file = self.no_file + itemnumber + "_1.jpg or " + f"{itemnumber}_B.jpg" + "\n"
            self.no_file_itemnumber = self.no_file_itemnumber + itemnumber + "\n"
            print(self.no_file)
            return False
        '''
        if not os.path.isdir("04_result"):
            os.makedirs("04_result")

        self.color = color[0]

        return True

    def makeFV_woman(self, itemnumber, value):

        color_full = value.split("/")
        color_full2 = color_full.reverse()
        comp = re.compile('[^a-zA-Z/]')
        color = comp.sub('', value)
        color = color.split("/")
        color2 = color.reverse()

        self.fullview = Image.new("RGB", (self.base_width, 330 + 100 * (len(color)) + 700 * (len(color) + 1)),
                                  (255, 255, 255))
        img = Image.new("RGB", (0, 0), (255, 255, 255))

        if itemnumber[0] in ["B", "S", "T", "V", "G"]:
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
            img = img.resize((330, 100))

            self.fullview.paste(img, (int((700 - img.width) / 2), 70))
            self.full_ptr = 300

        for n in color:
            self.img = Image.open(f"{self.path}/{itemnumber}_{n}_1.jpg")
            self.img = self.img.resize((700, 700))
            self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
            w, h = fnt.getsize(color_full[color.index(n)])
            ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                               color_full[color.index(n)], font=fnt, fill=(25, 25, 25))
            img = Image.open("03_resource/image/화살표.jpg")
            self.fullview.paste(img, (int((self.base_width / 2) - (w / 2) - 14), self.full_ptr + self.img.height + 4))
            self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color[-1]}_2.jpg")
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        self.full_ptr += self.img.height + 100

    def makeFV1(self, itemnumber, color, color_full):
        self.fullview = Image.new("RGB", (self.base_width, 330 + 1400 + 100), (255, 255, 255))
        img = Image.new("RGB", (0, 0), (255, 255, 255))

        if itemnumber[0] in ["B", "S", "T", "V", "G"]:
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
            img = img.resize((330, 100))

            self.fullview.paste(img, (int((700 - img.width) / 2), 70))
            self.full_ptr = 300

        self.fullview.paste(img, (int((700 - img.width) / 2), 70))
        self.full_ptr = 300

        str_img_file = f"{self.path}/{itemnumber}_{color}_{self.A1}.jpg"
        self.img = Image.open(str_img_file)
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        w, h = fnt.getsize(color_full[0])
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2) + 14, self.full_ptr + self.img.height),
                                           color_full[0], font=fnt, fill=(25, 25, 25))
        img = Image.open("03_resource/image/화살표.jpg")
        self.fullview.paste(img, (int((self.base_width / 2) - (w / 2) - 14), self.full_ptr + self.img.height + 4))

        self.full_ptr += self.img.height + 100
        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A2}.jpg")
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        if self.set_index:
            try:
                self.fullview.save(f"{self.path}/{itemnumber}_fv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")

        return self.fullview

    def makeFV2(self, itemnumber, color1, color2, color_full):
        self.fullview = Image.new("RGB", (self.base_width, 330 + 2100 + 200), (255, 255, 255))

        img = Image.new("RGB", (0, 0), (255, 255, 255))

        if itemnumber[0] in ["B", "S", "T", "V", "G"]:
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
            img = img.resize((330, 100))

            self.fullview.paste(img, (int((700 - img.width) / 2), 70))
            self.full_ptr = 300

        self.img = Image.open(f"{self.path}/{itemnumber}_{color2}_{self.A1}.jpg")
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color_full[1])
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[1], font=fnt, fill=(25, 25, 25))
        img = Image.open("03_resource/image/화살표.jpg")
        self.fullview.paste(img, (int((self.base_width / 2) - (w / 2) - 14), self.full_ptr + self.img.height + 4))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color1}_{self.A1}.jpg")
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color_full[0])
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[0], font=fnt, fill=(25, 25, 25))
        img = Image.open("03_resource/image/화살표.jpg")
        self.fullview.paste(img, (int((self.base_width / 2) - (w / 2) - 14), self.full_ptr + self.img.height + 4))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color1}_2.jpg")
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        if self.set_index:
            try:
                self.fullview.save(f"{self.path}/{itemnumber}_fv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")

        return self.fullview

    def makeFV3(self, itemnumber, color1, color2, color3, color_full):
        self.fullview = Image.new("RGB", (self.base_width, 330 + 2800 + 300), (255, 255, 255))

        img = Image.new("RGB", (0, 0), (255, 255, 255))

        if itemnumber[0] in ["B", "S", "T", "V", "G"]:
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
            img = img.resize((330, 100))

            self.fullview.paste(img, (int((700 - img.width) / 2), 70))
            self.full_ptr = 300

        self.img = Image.open(f"{self.path}/{itemnumber}_{color3}_{self.A1}.jpg")
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color_full[2])
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[2], font=fnt, fill=(25, 25, 25))
        img = Image.open("03_resource/image/화살표.jpg")
        self.fullview.paste(img, (int((self.base_width / 2) - (w / 2) - 14), self.full_ptr + self.img.height + 4))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color2}_{self.A1}.jpg")
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color_full[1])
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[1], font=fnt, fill=(25, 25, 25))
        img = Image.open("03_resource/image/화살표.jpg")
        self.fullview.paste(img, (int((self.base_width / 2) - (w / 2) - 14), self.full_ptr + self.img.height + 4))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color1}_{self.A1}.jpg")
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        w, h = fnt.getsize(color_full[0])
        ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                           color_full[0], font=fnt, fill=(25, 25, 25))
        img = Image.open("03_resource/image/화살표.jpg")
        self.fullview.paste(img, (int((self.base_width / 2) - (w / 2) - 14), self.full_ptr + self.img.height + 4))
        self.full_ptr += self.img.height + 100

        self.img = Image.open(f"{self.path}/{itemnumber}_{color1}_2.jpg")
        self.img = self.img.resize((700, 700))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        if self.set_index:
            try:
                self.fullview.save(f"{self.path}/{itemnumber}_fv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")
        return self.fullview

    def makeFV_acce_woman(self, itemnumber, value):
        if self.itemnumber[3] in ["G"]:
            number_list = list(range(2, 6))  # 풀뷰 사용할 넘버
            self.fv_num = 5
        else:
            number_list = list(range(2, 3))
            self.fv_num = 2
        color_full = value.split("/")
        color_full2 = color_full.reverse()
        comp = re.compile('[^a-zA-Z/]')
        color = comp.sub('', value)
        color = color.split("/")
        color2 = color.reverse()

        self.fullview = Image.new("RGB", (
            self.base_width, 330 + 100 * (len(number_list) + len(color) - 1) + 700 * (len(number_list) + len(color))),
                                  (255, 255, 255))
        img = Image.new("RGB", (0, 0), (255, 255, 255))

        if itemnumber[0] in ["B", "S", "T", "V", "G"]:
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
            img = img.resize((330, 100))

            self.fullview.paste(img, (int((700 - img.width) / 2), 70))
            self.full_ptr = 300

        for n in color:
            self.img = Image.open(f"{self.path}/{itemnumber}_{n}_1.jpg")
            self.img = self.img.resize((700, 700))
            self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
            w, h = fnt.getsize(color_full[color.index(n)])
            ImageDraw.Draw(self.fullview).text(((self.base_width / 2) - (w / 2), self.full_ptr + self.img.height),
                                               color_full[color.index(n)], font=fnt, fill=(25, 25, 25))
            img = Image.open("03_resource/image/화살표.jpg")
            self.fullview.paste(img, (int((self.base_width / 2) - (w / 2) - 14), self.full_ptr + self.img.height + 4))
            self.full_ptr += self.img.height + 100

        for n in number_list:
            self.img = Image.open(f"{self.path}/{itemnumber}_{color[-1]}_{n}.jpg")
            self.img = self.img.resize((700, 700))
            self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
            self.full_ptr += self.img.height + 100

    def makeFV_man(self, itemnumber, color):  # 1 2 3 사용
        self.fullview = Image.new("RGB", (self.base_width, 1800 + 75 + 160), (255, 255, 255))

        self.tag = Image.open("03_resource/image/FullView.jpg")
        self.fullview.paste(self.tag, (0, 30))
        self.full_ptr = 75

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A1}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        img = Image.open("03_resource/image/front_text.jpg")
        self.fullview.paste(img, (700 - img.width + 10, self.full_ptr + 485))
        self.full_ptr += self.img.height + 80

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A2}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        img = Image.open("03_resource/image/side_text.jpg")
        self.fullview.paste(img, (700 - img.width + 10, self.full_ptr + 485))
        self.full_ptr += self.img.height + 80

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A3}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        img = Image.open("03_resource/image/back_text.jpg")
        self.fullview.paste(img, (700 - img.width + 10, self.full_ptr + 485))
        if self.set_index:
            try:
                self.fullview.save(f"{self.path}/{itemnumber}_fv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")

        return self.fullview

    def makeFV_man_2(self, itemnumber, color):  # 1 2 사용
        self.fullview = Image.new("RGB", (self.base_width, 1200 + 75 + 80), (255, 255, 255))

        self.tag = Image.open("03_resource/image/FullView.jpg")
        self.fullview.paste(self.tag, (0, 30))
        self.full_ptr = 75

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A1}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        img = Image.open("03_resource/image/front_text.jpg")
        self.fullview.paste(img, (700 - img.width + 10, self.full_ptr + 485))
        self.full_ptr += self.img.height + 80

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A2}.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        img = Image.open("03_resource/image/back_text.jpg")
        self.fullview.paste(img, (700 - img.width + 10, self.full_ptr + 485))
        if self.set_index:
            try:
                self.fullview.save(f"{self.path}/{itemnumber}_fv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")

        return self.fullview

    def makeFV_man_3(self, itemnumber, color):  # 3 4사용
        self.fullview = Image.new("RGB", (self.base_width, 1800 + 75 + 160), (255, 255, 255))

        self.tag = Image.open("03_resource/image/FullView.jpg")
        self.fullview.paste(self.tag, (0, 30))
        self.full_ptr = 75

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_3.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        img = Image.open("03_resource/image/front_text.jpg")
        self.fullview.paste(img, (700 - img.width + 10, self.full_ptr + 485))
        self.full_ptr += self.img.height + 80

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_4.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        img = Image.open("03_resource/image/back_text.jpg")
        self.fullview.paste(img, (700 - img.width + 10, self.full_ptr + 485))
        self.full_ptr += self.img.height + 80

        set_image = self.fullview
        self.fullview = self.fullview.crop((0, 0, self.base_width, 1200 + 75 + 80))
        if self.set_index:
            try:
                self.fullview.save(f"{self.path}/{itemnumber}_fv.jpg", quallity=100)
                if self.itemnumber[0] == "P" and not itemnumber[1] in ["A", "X", "Y", "Z"]:
                    img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A1}.jpg")
                    img = img.resize((550, 550))
                    set_image.paste(img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
                    set_image.save(f"{self.path}/{itemnumber}_fv.jpg", quallity=100)

                    if self.itemnumber[2] == "P":
                        self.fullview = set_image
                        if self.set_index:
                            self.fullview.save(f"{self.path}/{itemnumber}_fv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")

    def makeFV_acce_man(self, itemnumber, color):
        if self.itemnumber[3] in ["G"]:
            number_list = list(range(1, 5))  # 풀뷰 사용할 넘버
            self.fv_num = 4
        else:
            number_list = list(range(1, 3))
            self.fv_num = 2
        self.fullview = Image.new("RGB", (self.base_width, 75 + 80 * (len(number_list) - 1) + 600 * len(number_list)),
                                  (255, 255, 255))

        self.tag = Image.open("03_resource/image/FullView.jpg")
        self.fullview.paste(self.tag, (0, 30))
        self.full_ptr = 75

        for n in number_list:
            self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{n}.jpg")
            self.img = self.img.resize((600, 600))
            self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
            self.full_ptr += self.img.height + 80

        return self.fullview

    def makeDV(self, itemnumber, color):  # 4 5 6 사용

        detail_ptr = 0
        self.detailview = Image.new("RGB", (self.base_width, 2200 + 150 + 120), (255, 255, 255))
        self.tag = Image.open("03_resource/image/DetailView.jpg")
        self.detailview.paste(self.tag, (0, 30))
        detail_ptr += 100

        str_tmp = f"{self.path}/{itemnumber}_{color}_{self.A4}.jpg"
        self.img = Image.open(str_tmp)
        self.img = self.img.resize((550, 550))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A5}.jpg")
        self.img = self.img.resize((550, 550))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{self.A6}.jpg")
        self.img = self.img.resize((550, 550))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        check1 = os.path.isfile(f"{self.path}/{itemnumber}_{color}_7.jpg")
        if check1:
            img = Image.open(f"{self.path}/{itemnumber}_{color}_7.jpg")
            img = img.resize((550, 550))
            self.detailview.paste(img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))

            self.detailview = self.detailview.crop((0, 0, self.base_width, 2200 + 150 + 120))
        else:
            self.detailview = self.detailview.crop((0, 0, self.base_width, 1650 + 150 + 80))
        if self.set_index:
            try:
                self.detailview.save(f"{self.path}/{itemnumber}_dv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")
        return self.detailview

    def makeDV2(self, itemnumber, color):  # 3 4 5 사용

        detail_ptr = 0
        self.area = (30, 30, 670, 670)
        self.detailview = Image.new("RGB", (self.base_width, 2750 + 150 + 160), (255, 255, 255))
        self.tag = Image.open("03_resource/image/DetailView.jpg")
        self.detailview.paste(self.tag, (0, 30))
        detail_ptr += 100

        str_tmp = f"{self.path}/{itemnumber}_{color}_3.jpg"
        self.img = Image.open(str_tmp)
        self.img = self.img.resize((550, 550))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_4.jpg")
        self.img = self.img.resize((550, 550))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_5.jpg")
        self.img = self.img.resize((550, 550))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        try:
            img = Image.open(f"{self.path}/{itemnumber}_{color}_6.jpg")
            img2 = Image.open(f"{self.path}/{itemnumber}_{color}_7.jpg")

            img = img.resize((550, 550))
            self.detailview.paste(img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
            detail_ptr += self.img.height + 40

            img2 = img2.resize((550, 550))
            self.detailview.paste(img2, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))

        except:
            self.detailview = self.detailview.crop((0, 0, self.base_width, 1650 + 150 + 80))
            pass

        if self.set_index:
            try:
                self.detailview.save(f"{self.path}/{itemnumber}_dv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")
        return self.detailview

    def makeDV3(self, itemnumber, color):  # 남자 지이크 after B시즌

        detail_ptr = 0
        self.detailview = Image.new("RGB", (self.base_width, 2750 + 150 + 160), (255, 255, 255))
        self.tag = Image.open("03_resource/image/DetailView.jpg")
        self.detailview.paste(self.tag, (0, 30))
        detail_ptr += 100

        str_tmp = f"{self.path}/{itemnumber}_{color}_2.jpg"
        self.img = Image.open(str_tmp)
        self.img = self.img.resize((550, 550))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_5.jpg")
        self.img = self.img.resize((550, 550))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_6.jpg")
        self.img = self.img.resize((550, 550))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        check1 = os.path.isfile(f"{self.path}/{itemnumber}_{color}_7.jpg")
        check2 = os.path.isfile(f"{self.path}/{itemnumber}_{color}_8.jpg")
        if check1 and check2:
            img = Image.open(f"{self.path}/{itemnumber}_{color}_7.jpg")
            img2 = Image.open(f"{self.path}/{itemnumber}_{color}_8.jpg")

            img = img.resize((550, 550))
            self.detailview.paste(img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
            detail_ptr += self.img.height + 40

            img2 = img2.resize((550, 550))
            self.detailview.paste(img2, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        elif check1:
            img = Image.open(f"{self.path}/{itemnumber}_{color}_7.jpg")

            img = img.resize((550, 550))
            self.detailview.paste(img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))

            self.detailview = self.detailview.crop((0, 0, self.base_width, 2200 + 150 + 120))

        else:
            self.detailview = self.detailview.crop((0, 0, self.base_width, 1650 + 150 + 80))

        if self.set_index:
            try:
                self.detailview.save(f"{self.path}/{itemnumber}_dv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")
        return self.detailview

    def makeDV_acce(self, itemnumber, color, gender):
        if gender == "남성":
            img_size = 550
        else:
            img_size = 600

        for n in range(0, 11):
            index = os.path.isfile(f"{self.path}/{itemnumber}_{color}_{10 - n}.jpg")
            if index:
                number_list = range(self.fv_num + 1, 10 - n + 1)
                break

        detail_ptr = 0
        self.detailview = Image.new("RGB",
                                    (self.base_width, img_size * len(number_list) + 150 + 40 * (len(number_list) - 1)),
                                    (255, 255, 255))
        self.tag = Image.open("03_resource/image/DetailView.jpg")
        self.detailview.paste(self.tag, (0, 30))
        detail_ptr += 100
        for n in number_list:
            self.img = Image.open(f"{self.path}/{itemnumber}_{color}_{n}.jpg")
            self.img = self.img.resize((img_size, img_size))
            self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
            detail_ptr += self.img.height + 40

    def makeDV_woman(self, itemnumber, color):  # 3 4 5 사용

        detail_ptr = 0
        self.detailview = Image.new("RGB", (self.base_width, 3000 + 150 + 160), (255, 255, 255))
        self.tag = Image.open("03_resource/image/DetailView.jpg")
        self.detailview.paste(self.tag, (0, 30))
        detail_ptr += 100

        str_tmp = f"{self.path}/{itemnumber}_{color}_3.jpg"
        self.img = Image.open(str_tmp)
        self.img = self.img.resize((600, 600))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_4.jpg")
        self.img = self.img.resize((600, 600))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_5.jpg")
        self.img = self.img.resize((600, 600))
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 40

        check1 = os.path.isfile(f"{self.path}/{itemnumber}_{color}_6.jpg")
        check2 = os.path.isfile(f"{self.path}/{itemnumber}_{color}_7.jpg")
        if check1 and check2:
            img1 = Image.open(f"{self.path}/{itemnumber}_{color}_6.jpg")
            img2 = Image.open(f"{self.path}/{itemnumber}_{color}_7.jpg")

            img1 = img1.resize((600, 600))
            self.detailview.paste(img1, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
            detail_ptr += img1.height + 40

            img2 = img2.resize((600, 600))
            self.detailview.paste(img2, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        elif check1:
            img1 = Image.open(f"{self.path}/{itemnumber}_{color}_6.jpg")

            img1 = img1.resize((600, 600))
            self.detailview.paste(img1, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))

            self.detailview = self.detailview.crop((0, 0, self.base_width, 2400 + 150 + 120))

        else:
            self.detailview = self.detailview.crop((0, 0, self.base_width, 1800 + 150 + 80))

        if self.set_index:
            try:
                self.detailview.save(f"{self.path}/{itemnumber}_dv.jpg", quallity=100)
            except:
                print("결과물 출력에 실패했습니다")
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
        self.infoview = Image.new("RGB", (self.base_width, 200 + (len(column1_list) * 40)), (255, 255, 255))
        self.tag = Image.open("03_resource/image/DetailInfo.jpg")
        self.infoview.paste(self.tag, (0, 30))
        self.info_ptr += 90

        # 정보고시 안감 두께 등의 공간
        self.info_table = Image.new("RGB", (self.base_width, 40), (244, 244, 244))
        self.infodata = Image.new("RGB", (self.base_width, 38), (255, 255, 255))
        img = Image.new("RGB", (self.base_width, 1), (222, 222, 222))
        self.info_table.paste(self.infodata, (152, 1))
        self.info_table.paste(img, (0, 39))
        self.infoview.paste(img, (0, self.info_ptr - 1))

        # 표 첫줄

        if "탈부착가능여부" in column1_list:
            for i in range(0, len(column1_list)):
                self.infoview.paste(self.info_table, (0, self.info_ptr))
                w, h = fnt.getsize(column1_list[i])
                textdraw = ImageDraw.Draw(self.infoview)
                if column1_list[i] == "탈부착가능여부":
                    for n in range(0, 4):
                        self.infoview.paste(box, (210 + (n * 120), self.info_ptr + 15))
                else:
                    for n in range(0, 3):
                        self.infoview.paste(box, (210 + (n * 120), self.info_ptr + 15))

                textdraw.text(((76 - (w / 2)), self.info_ptr + 9), column1_list[i], font=fnt, fill=(0, 0, 0,))
                if column1_list[i] == "비침":
                    textdraw.text((230, self.info_ptr + 9), "있음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((350, self.info_ptr + 9), "약간", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((470, self.info_ptr + 9), "없음", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "있음":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "약간":
                        self.infoview.paste(black, (330, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (450, self.info_ptr + 15))
                elif column1_list[i] == "안감":
                    textdraw.text((230, self.info_ptr + 9), "있음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((350, self.info_ptr + 9), "없음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((470, self.info_ptr + 9), "기모", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "있음":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "없음":
                        self.infoview.paste(black, (330, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (450, self.info_ptr + 15))
                elif column1_list[i] == "신축성":
                    textdraw.text((230, self.info_ptr + 9), "있음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((350, self.info_ptr + 9), "약간", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((470, self.info_ptr + 9), "없음", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "있음":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "약간":
                        self.infoview.paste(black, (330, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (450, self.info_ptr + 15))
                elif column1_list[i] == "두께감":
                    textdraw.text((230, self.info_ptr + 9), "얇음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((350, self.info_ptr + 9), "보통", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((470, self.info_ptr + 9), "도톰", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "얇음":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "보통":
                        self.infoview.paste(black, (330, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (450, self.info_ptr + 15))
                elif column1_list[i] == "핏감":
                    textdraw.text((230, self.info_ptr + 9), "슬림핏", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((350, self.info_ptr + 9), "스탠다드", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((470, self.info_ptr + 9), "오버핏", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "슬림핏":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "스탠다드":
                        self.infoview.paste(black, (330, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (450, self.info_ptr + 15))
                elif column1_list[i] == "탈부착가능여부":
                    textdraw.text((230, self.info_ptr + 9), "안감", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((350, self.info_ptr + 9), "후드", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((470, self.info_ptr + 9), "액세서리", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((590, self.info_ptr + 9), "없음", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "안감":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "후드":
                        self.infoview.paste(black, (330, self.info_ptr + 15))
                    elif column2_list[i] == "액세서리":
                        self.infoview.paste(black, (450, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (570, self.info_ptr + 15))
                self.info_ptr += 40

        else:
            for i in range(0, len(column1_list)):
                self.infoview.paste(self.info_table, (0, self.info_ptr))
                w, h = fnt.getsize(column1_list[i])
                textdraw = ImageDraw.Draw(self.infoview)
                if column1_list[i] == "탈부착가능여부":
                    for n in range(0, 4):
                        self.infoview.paste(box, (210 + (n * 120), self.info_ptr + 15))
                else:
                    for n in range(0, 3):
                        self.infoview.paste(box, (210 + (n * 180), self.info_ptr + 15))

                textdraw.text(((76 - (w / 2)), self.info_ptr + 9), column1_list[i], font=fnt, fill=(0, 0, 0,))
                if column1_list[i] == "비침":
                    textdraw.text((230, self.info_ptr + 9), "있음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((410, self.info_ptr + 9), "약간", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((590, self.info_ptr + 9), "없음", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "있음":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "약간":
                        self.infoview.paste(black, (390, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (570, self.info_ptr + 15))
                elif column1_list[i] == "안감":
                    textdraw.text((230, self.info_ptr + 9), "있음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((410, self.info_ptr + 9), "없음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((590, self.info_ptr + 9), "기모", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "있음":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "없음":
                        self.infoview.paste(black, (390, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (570, self.info_ptr + 15))
                elif column1_list[i] == "신축성":
                    textdraw.text((230, self.info_ptr + 9), "있음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((410, self.info_ptr + 9), "약간", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((590, self.info_ptr + 9), "없음", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "있음":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "약간":
                        self.infoview.paste(black, (390, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (570, self.info_ptr + 15))
                elif column1_list[i] == "두께감":
                    textdraw.text((230, self.info_ptr + 9), "얇음", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((410, self.info_ptr + 9), "보통", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((590, self.info_ptr + 9), "도톰", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "얇음":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "보통":
                        self.infoview.paste(black, (390, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (570, self.info_ptr + 15))
                elif column1_list[i] == "핏감":
                    textdraw.text((230, self.info_ptr + 9), "슬림핏", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((410, self.info_ptr + 9), "스탠다드", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((590, self.info_ptr + 9), "오버핏", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "슬림핏":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "스탠다드":
                        self.infoview.paste(black, (390, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (570, self.info_ptr + 15))
                elif column1_list[i] == "탈부착가능여부":
                    textdraw.text((230, self.info_ptr + 9), "안감", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((350, self.info_ptr + 9), "후드", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((470, self.info_ptr + 9), "액세서리", font=fnt, fill=(0, 0, 0,))
                    textdraw.text((590, self.info_ptr + 9), "없음", font=fnt, fill=(0, 0, 0,))
                    if column2_list[i] == "안감":
                        self.infoview.paste(black, (210, self.info_ptr + 15))
                    elif column2_list[i] == "후드":
                        self.infoview.paste(black, (330, self.info_ptr + 15))
                    elif column2_list[i] == "액세서리":
                        self.infoview.paste(black, (450, self.info_ptr + 15))
                    else:
                        self.infoview.paste(black, (570, self.info_ptr + 15))
                self.info_ptr += 40

        # self.infoview.save("test_info.jpg", quallity=95)

        return self.infoview

    def makeSet(self, item_code_top, item_code_bottom):

        self.FV_top = Image.open(f"{self.dir}/{item_code_top}/{item_code_top}_fv.jpg")
        self.DV_top = Image.open(f"{self.dir}/{item_code_top}/{item_code_top}_dv.jpg")
        self.info_full_top = Image.open(f"{self.dir}/{item_code_top}/{item_code_top}_02.jpg")

        try:
            self.FV_bottom = Image.open(f"{self.dir}/{item_code_bottom}/{item_code_bottom}_fv_set.jpg")
        except:
            self.FV_bottom = Image.open(f"{self.dir}/{item_code_bottom}/{item_code_bottom}_fv.jpg")
        self.DV_bottom = Image.open(f"{self.dir}/{item_code_bottom}/{item_code_bottom}_dv.jpg")
        self.info_full_bottom = Image.open(f"{self.dir}/{item_code_bottom}/{item_code_bottom}_02.jpg")

    def info_size(self, size_count):

        if 80 + (40 * size_count) > 280:
            self.sizeview = Image.new("RGB", (self.base_width, 80 + 110 + (40 * size_count)), (255, 255, 255))
        else:
            self.sizeview = Image.new("RGB", (self.base_width, 280 + 80), (255, 255, 255))

        self.size_img = Image.new("RGB", (1, 1), (255, 255, 255))

        if self.itemnumber[0] in ["B", "S", "T", "V", "G"]:  # 여성구분
            if self.itemnumber[2] == "A":
                if self.itemnumber[3] == "F":
                    self.size_img = Image.open("03_resource/image/여성_스카프.jpg")
                    self.size_img = self.size_img.resize((240, 240))
                    self.size_img = self.size_img.crop((15, 40, 240, 210))
                elif self.itemnumber[3] == "E":
                    self.size_img = Image.open("03_resource/image/여성_스카프.jpg")
                    self.size_img = self.size_img.resize((240, 240))
                    self.size_img = self.size_img.crop((15, 40, 240, 210))
                elif self.itemnumber[3] == "G":
                    self.size_img = Image.open("03_resource/image/가방.jpg")
                    self.size_img = self.size_img.crop((25, 30, 250, 220))
                elif self.itemnumber[3] == "P":
                    self.size_img = Image.open("03_resource/image/공통_양말.jpg")
                    self.size_img = self.size_img.crop((0, 40, 245, 225))
                elif self.itemnumber[3] == "S":
                    self.size_img = Image.open("03_resource/image/여성_신발.jpg")
                    self.size_img = self.size_img.crop((14, 40, 300, 274))

            elif self.itemnumber[2] in ["F", "P"]:
                self.size_img = Image.open("03_resource/image/여성_팬츠.jpg")

            elif self.itemnumber[2] == "S":
                self.size_img = Image.open("03_resource/image/여성_치마.jpg")

            elif self.itemnumber[2] == "O":
                self.size_img = Image.open("03_resource/image/여성_원피스.jpg")
            else:
                self.size_img = Image.open("03_resource/image/여성_셔츠.jpg")

            if self.itemnumber[2] in ["F", "P"]:
                self.sizeview.paste(self.size_img, (510, 30))
            else:
                self.sizeview.paste(self.size_img, (self.base_width - self.size_img.width + 10, 30))

        else:  # 남성

            if self.itemnumber[2] == "A":
                if self.itemnumber[3] == "L":
                    self.size_img = Image.open("03_resource/image/벨트.jpg")
                    self.size_img = self.size_img.crop((8, 80, 320, 240))

                elif self.itemnumber[3] == "T":
                    self.size_img = Image.open("03_resource/image/넥타이.jpg")

                elif self.itemnumber[3] == "S":
                    self.size_img = Image.open("03_resource/image/남성_신발.jpg")
                    self.size_img = self.size_img.crop((0, 50, 314, 264))
                elif self.itemnumber[3] == "G":
                    self.size_img = Image.open("03_resource/image/가방.jpg")
                    self.size_img = self.size_img.crop((25, 30, 250, 220))

                elif self.itemnumber[3] == "P":
                    self.size_img = Image.open("03_resource/image/공통_양말.jpg")
                    self.size_img = self.size_img.crop((0, 40, 245, 225))
                elif self.itemnumber[3] == "F":
                    self.size_img = Image.open("03_resource/image/여성_스카프.jpg")
                    self.size_img = self.size_img.resize((240, 240))
                    self.size_img = self.size_img.crop((15, 40, 240, 210))


            elif self.itemnumber[2] in ["B", "C", "U", "I"]:
                self.size_img = Image.open("03_resource/image/상의.jpg")

            elif self.itemnumber[2] in ["F", "P"]:
                self.size_img = Image.open("03_resource/image/팬츠.jpg")
            elif self.itemnumber[2] in ["D", "E", "G", "H", "L", "M", "N", "J", "V"]:
                self.size_img = Image.open("03_resource/image/자켓.jpg")

            if self.itemnumber[2] in ["F", "P"]:
                self.sizeview.paste(self.size_img, (440, 30))
            else:
                self.sizeview.paste(self.size_img, (self.base_width - self.size_img.width + 10, 30))

        self.grey = True
        # 사이즈 고시할 공간
        if self.itemnumber[2] in ["F", "P"]:
            self.table_width = 510
        else:
            self.table_width = self.base_width - self.size_img.width + 10

        self.table_height = 40

        self.size_table = Image.new("RGB", (self.table_width, self.table_height), (255, 255, 255))  # (480, 40)
        self.size_table_grey = Image.new("RGB", (self.table_width, self.table_height), (244, 244, 244))
        img = Image.new("RGB", (self.table_width, 1), (222, 222, 222))

        self.size_table_grey.paste(img, (0, 0))
        self.size_table_grey.paste(img, (0, 39))

        self.size_table.paste(img, (0, 39))

        tag = Image.open("03_resource/image/SizeSpec.jpg")
        self.sizeview.paste(tag, (0, 0))

        w, h = fnt_tip.getsize("단위(cm)")
        if self.itemnumber[2] in ["F", "P"]:
            ImageDraw.Draw(self.sizeview).text((450, 50), "단위(cm)", font=fnt_tip, fill=(51, 51, 51))
        else:
            ImageDraw.Draw(self.sizeview).text((self.table_width - w - 10, 50), "단위(cm)", font=fnt_tip,
                                               fill=(51, 51, 51))

        self.size_ptr = 70

        # self.sizeview.save("test_size.jpg", quallity=95)

    def size_insert(self, value):

        if value == "nan":
            value = ""
        value_list = value.split("\n")

        if self.grey:
            self.sizeview.paste(self.size_table_grey, (0, self.size_ptr))
            self.grey = False

        else:
            self.sizeview.paste(self.size_table, (0, self.size_ptr))
        num = 1
        for n in value_list:  # 사이즈 어깨넓이 등
            w, h = fnt.getsize(n)

            size_inch = n.split("(")
            if len(size_inch) > 1:
                w1, h1 = fnt.getsize(size_inch[0])
                w2, h2 = fnt.getsize(size_inch[1])

                ImageDraw.Draw(self.sizeview).text(
                    (((self.table_width / len(value_list) * num) - (self.table_width / len(value_list) / 2) - (
                            (w1 + w2) / 2)),
                     (self.size_ptr + 25 - h1)),
                    size_inch[0], font=fnt, fill=(60, 60, 60))
                ImageDraw.Draw(self.sizeview).text(
                    (((self.table_width / len(value_list) * num) - (self.table_width / len(value_list) / 2) - (
                            (w1 + w2) / 2) + w1),
                     (self.size_ptr + 25 - h1)),
                    "(" + size_inch[1], font=fnt_bold, fill=(60, 60, 60))
                num += 1

            else:
                if self.itemnumber[2] in ["F", "P"]:
                    ImageDraw.Draw(self.sizeview).text(
                        (((self.table_width / len(value_list) * num) - (self.table_width / len(value_list) / 2) - (
                                w / 2)),
                         (self.size_ptr + 25 - h)),
                        n, font=fnt, fill=(60, 60, 60))
                else:
                    ImageDraw.Draw(self.sizeview).text(
                        (((self.table_width / len(value_list) * num) - (self.table_width / len(value_list) / 2) - (
                                w / 2)),
                         (self.size_ptr + 25 - h)),
                        n, font=fnt, fill=(60, 60, 60))
                num += 1
        self.size_ptr += self.table_height

        # self.sizeview.save("test_size2.jpg", quallity=95)

    def info_tip(self):
        self.tip_view = Image.new("RGB", (self.base_width, 180), (255, 255, 255))
        self.tag = Image.open("03_resource/image/Tip.jpg")
        self.tip_view.paste(self.tag, (0, 0))
        self.tip_ptr = 50

        ImageDraw.Draw(self.tip_view).text((15, self.tip_ptr), "- 사이즈 스펙은 실측 사이즈 기준입니다.(가슴둘레는 라벨사이즈 기준)", font=fnt3,
                                           fill=(60, 60, 60))
        self.tip_ptr += 20
        ImageDraw.Draw(self.tip_view).text((15, self.tip_ptr), "- 사이즈는 측정 방법과 생산 과정에 따라 약간의 오차가 발생할 수 있습니다.",
                                           font=fnt3, fill=(60, 60, 60))
        self.tip_ptr += 20
        ImageDraw.Draw(self.tip_view).text((15, self.tip_ptr),
                                           "- 제품 안쪽 라벨에 표기된 사이즈는 표준 신체 사이즈를 표기한 것이므로, 실측사이즈와 차이가 있을 수 있습니다.",
                                           font=fnt3, fill=(60, 60, 60))

    def combineImg(self, item_code):

        fullimage_material = [self.fullview, self.detailview, self.product_info, self.info_full]

        self.fullimage = Image.new("RGB", (self.base_width,
                                           self.fullview.height + self.detailview.height + self.info_full.height + self.product_info.height),
                                   (255, 255, 255))
        self.fullimage_ptr = 0

        for image in fullimage_material:
            self.fullimage.paste(image, (0, self.fullimage_ptr))
            self.fullimage_ptr += image.height

        self.fullimage_extend = Image.new("RGB", (860, self.fullimage.height), (255, 255, 255))
        self.fullimage_extend.paste(self.fullimage, (80, 0))

        try:
            self.fullimage_extend.save(f"./04_result/{item_code}.jpg", quallity=100)
            self.fullimage_extend.save(f"{self.path}/{item_code}_01.jpg", quallity=100)
        except:
            print("결과물 출력에 실패했습니다")

    def combineImg_man(self, item_code):
        self.fullimage = Image.new("RGB", (self.base_width,
                                           self.fullview.height + self.detailview.height + self.info_full.height + self.product_info.height),
                                   (255, 255, 255))
        fullimage_material = [self.product_info, self.fullview, self.detailview, self.info_full]
        self.fullimage_ptr = 0
        '''
        self.fullimage.paste(self.product_info, (0, 0))
        self.fullimage.paste(self.fullview, (0, self.product_info.height))
        self.fullimage.paste(self.detailview, (0, self.product_info.height + self.fullview.height))
        self.fullimage.paste(self.info_full,
                             (0, self.product_info.height + self.fullview.height + self.detailview.height))
        '''
        r = True
        n = True
        for image in fullimage_material:
            self.fullimage.paste(image, (0, self.fullimage_ptr))
            self.fullimage_ptr += image.height
            if r == True:
                if n == True:
                    self.fullimage.paste(self.break_line, (0, self.fullimage_ptr - 1))
                    n = False
                else:
                    self.fullimage.paste(self.break_line, (0, self.fullimage_ptr - 1))
                    r = False

        self.fullimage_extend = Image.new("RGB", (860, self.fullimage.height), (255, 255, 255))

        self.fullimage_extend.paste(self.fullimage, (80, 0))

        try:
            self.fullimage_extend.save(f"./04_result/{item_code}.jpg", quallity=100)
            self.fullimage_extend.save(f"{self.path}/{item_code}_01.jpg", quallity=100)
        except:
            print("결과물 출력에 실패")

    def combineInfo(self):
        self.info_tip()

        self.info_full = Image.new("RGB", (
            self.base_width, self.infoview.height + self.sizeview.height + self.tip_view.height), (255, 255, 255))

        self.info_full.paste(self.infoview, (0, 0))
        self.info_full.paste(self.sizeview, (0, self.infoview.height))
        self.info_full.paste(self.tip_view, (0, self.infoview.height + self.sizeview.height))

        extand_image = Image.new("RGB", (860, self.info_full.height), (255, 255, 255))
        extand_image.paste(self.info_full, (80, 0))

        try:
            extand_image.save(f"{self.path}/{self.itemnumber}_02.jpg", quallity=100)
        except:
            print("결과물 출력에 실패")

    def combineSet(self, item_code):
        self.fullimage_material = [self.product_info, self.FV_top, self.DV_top, self.info_full_top, self.FV_bottom,
                                   self.DV_bottom, self.info_full_bottom]

        self.fullimage = Image.new("RGB", (self.base_width,
                                           self.product_info.height + self.FV_top.height + self.DV_top.height + self.info_full_top.height + self.FV_bottom.height + self.DV_bottom.height + self.info_full_bottom.height),
                                   (255, 255, 255))

        self.fullimage_ptr = 0

        self.fullimage.paste(self.product_info, (0, self.fullimage_ptr))
        self.fullimage_ptr += self.product_info.height

        self.fullimage.paste(self.break_line, (0, self.fullimage_ptr - 1))

        self.fullimage.paste(self.FV_top, (0, self.fullimage_ptr))
        self.fullimage_ptr += self.FV_top.height

        self.fullimage.paste(self.break_line, (0, self.fullimage_ptr - 1))

        self.fullimage.paste(self.DV_top, (0, self.fullimage_ptr))
        self.fullimage_ptr += self.DV_top.height

        self.fullimage.paste(self.info_full_top, (-80, self.fullimage_ptr))
        self.fullimage_ptr += self.info_full_top.height

        self.fullimage.paste(self.FV_bottom, (0, self.fullimage_ptr))
        self.fullimage_ptr += self.FV_bottom.height

        self.fullimage.paste(self.break_line, (0, self.fullimage_ptr - 1))

        self.fullimage.paste(self.DV_bottom, (0, self.fullimage_ptr))
        self.fullimage_ptr += self.DV_bottom.height

        self.fullimage.paste(self.info_full_bottom, (-80, self.fullimage_ptr))
        self.fullimage_ptr += self.info_full_bottom.height

        self.fullimage_extend = Image.new("RGB", (860, self.fullimage.height), (255, 255, 255))
        self.fullimage_extend.paste(self.fullimage, (80, 0))

        self.fullimage_2 = Image.new("RGB", (860, self.info_full_top.height + self.info_full_bottom.height),
                                     (255, 255, 255))

        self.fullimage_2.paste(self.info_full_top, (0, 0))
        self.fullimage_2.paste(self.info_full_bottom, (0, self.info_full_top.height))

        try:
            self.fullimage_extend.save(f"./04_result/{item_code}_full_image.jpg", quallity=100)
            self.fullimage_extend.save(f"{self.path}/{item_code}_01.jpg", quallity=100)

            self.fullimage_2.save(f"{self.path}/{item_code}_02.jpg", quallity=100)
        except:
            print("결과물 출력에 실패")

    def thumbnail(self, color_list, x, y):
        thumbnail = Image.open(f"{self.path}/{self.itemnumber}_{color_list[0]}_{self.A1}.jpg")
        thumbnail = thumbnail.resize((900, 900))

        mask_im = Image.new("L", (thumbnail.width * 10, thumbnail.height * 10), 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse(((int(x) - 35) * 10, (int(y) - 35) * 10, (int(x) + 35) * 10, (int(y) + 35) * 10), fill=255)
        mask_im = mask_im.resize(thumbnail.size)

        base_y = 825 - int(y)
        base_x = 855 - int(x)
        if not len(color_list) == 1:
            for color in color_list:
                thumb = Image.open(f"{self.path}/{self.itemnumber}_{color}_{self.A1}.jpg")
                thumbnail.paste(thumb, (base_x, base_y), mask_im)
                base_y -= 75
        elif self.itemnumber[0] in ["B", "S", "T", "V", "G"]:  # 여성의경우 1개여도 실행
            for color in color_list:
                thumb = Image.open(f"{self.path}/{self.itemnumber}_{color}_{self.A1}.jpg")
                thumbnail.paste(thumb, (base_x, base_y), mask_im)
                base_y -= 75

        # 브랜드별 로고
        if self.itemnumber[0] == "B":
            logo = Image.open("03_resource/image/베스띠벨리(썸네일).png")
        elif self.itemnumber[0] == "S":
            logo = Image.open("03_resource/image/씨(썸네일).png")
        elif self.itemnumber[0] == "T":
            logo = Image.open("03_resource/image/비키(썸네일).png")
        elif self.itemnumber[0] == "V":
            logo = Image.open("03_resource/image/이사베이(썸네일).png")
        elif self.itemnumber[0] == "P":
            logo = Image.open("03_resource/image/지이크(썸네일).png")
            logo = logo.resize((int(logo.width / 7), int(logo.height / 7)))
        elif self.itemnumber[0] == "F":
            logo = Image.open("03_resource/image/파렌하이트(썸네일).png")
            logo = logo.resize((int(logo.width / 7), int(logo.height / 7)))
        elif self.itemnumber[0] == "Q":
            logo = Image.open("03_resource/image/Brand_아이코닉.jpg")
            logo = logo.crop((250, 100, 250 + 500, 100 + 110))
            logo = logo.resize((int(logo.width / 2), int(logo.height / 2)))

        thumbnail.paste(logo, (900 - logo.width - 10, 10), logo)
        try:
            thumbnail.save(f"{self.path}/{self.itemnumber}.jpg")
        except:
            print("결과물 출력에 실패")

    def thumbnail_exam(self, x, y):

        mask_im = Image.new("L", (9000, 9000), 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse(((int(x) - 35) * 10, (int(y) - 35) * 10, (int(x) + 35) * 10, (int(y) + 35) * 10), fill=255)
        mask_im = mask_im.resize((900, 900))

        mask_im.show()

    def thumbnail_set(self, color_list, x, y):
        if self.full_code_dir:
            try:
                thumbnail = Image.open(f"{self.path}/{self.itemnumber}_{self.A1}.jpg")
            except:
                if self.A1 == "1":
                    thumbnail = Image.open(f"{self.path}/{self.itemnumber}_B.jpg")
                else:
                    thumbnail = Image.open(f"{self.path}/{self.itemnumber}_1.jpg")
        else:
            thumbnail = Image.new("RGB", (900, 900), (255, 255, 255))

            img = Image.open(f"{self.path}/{self.itemnumber}_03.jpg")
            img = img.resize((int(img.width / 5 * 3), int(img.height / 5 * 3)))
            thumbnail.paste(img, (450 - int(img.width / 2), 0))

        mask_im = Image.new("L", (thumbnail.width * 10, thumbnail.height * 10), 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse(((int(x) - 35) * 10, (int(y) - 35) * 10, (int(x) + 35) * 10, (int(y) + 35) * 10), fill=255)
        mask_im = mask_im.resize(thumbnail.size)

        base_y = 825 - int(y)
        base_x = 855 - int(x)
        if not len(color_list) == 1:
            for color in color_list:
                thumb = Image.open(f"{self.path}/{self.itemnumber}_{color}_{self.A1}.jpg")
                thumbnail.paste(thumb, (base_x, base_y), mask_im)
                base_y -= 75
        elif self.itemnumber[0] in ["B", "S", "T", "V", "G"]:  # 여성의경우 1개여도 실행
            for color in color_list:
                thumb = Image.open(f"{self.path}/{self.itemnumber}_{color}_{self.A1}.jpg")
                thumbnail.paste(thumb, (base_x, base_y), mask_im)
                base_y -= 75

        # 브랜드별 로고
        if self.itemnumber[0] == "B":
            logo = Image.open("03_resource/image/베스띠벨리(썸네일).png")
        elif self.itemnumber[0] == "S":
            logo = Image.open("03_resource/image/씨(썸네일).png")
        elif self.itemnumber[0] == "T":
            logo = Image.open("03_resource/image/비키(썸네일).png")
        elif self.itemnumber[0] == "V":
            logo = Image.open("03_resource/image/이사베이(썸네일).png")
        elif self.itemnumber[0] == "P":
            logo = Image.open("03_resource/image/지이크(썸네일).png")
            logo = logo.resize((int(logo.width / 7), int(logo.height / 7)))
        elif self.itemnumber[0] == "F":
            logo = Image.open("03_resource/image/파렌하이트(썸네일).png")
            logo = logo.resize((int(logo.width / 7), int(logo.height / 7)))
        elif self.itemnumber[0] == "Q":
            logo = Image.open("03_resource/image/Brand_아이코닉.jpg")
            logo = logo.crop((250, 100, 250 + 500, 100 + 110))
            logo = logo.resize((int(logo.width / 2), int(logo.height / 2)))

        thumbnail.paste(logo, (900 - logo.width - 10, 10), logo)

        try:
            thumbnail.save(f"{self.path}/{self.itemnumber}.jpg")
        except:
            print("결과물 출력에 실패")
        print(thumbnail.width)


if __name__ == '__main__':
    mkImage = MakeImg()

# mkImage.combineImg()
