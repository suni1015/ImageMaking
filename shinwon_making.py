# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

pdt_name = ImageFont.truetype("01_data/NanumGothic.ttf", 20, encoding="UTF-8")
fnt = ImageFont.truetype("01_data/NanumGothic.ttf", 15, encoding="UTF-8")
fnt_tip = ImageFont.truetype("01_data/NanumGothic.ttf", 12, encoding="UTF-8")


class MakeImg:
    def __init__(self):
        self.base_width = 700
        self.base_height = 5500
        self.area = (50, 150, 550, 550)
        self.fullimage = Image.new("RGB", (self.base_width, self.base_height), (255, 255, 255))

        self.product_info = Image.new("RGB", (self.base_width, 500), (255, 255, 255))
        self.tag = Image.open("01_data/image/Product.jpg")
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

    def info_product_name(self, text):
        draw = ImageDraw.Draw(self.product_info)
        draw.text((20, 80), text, fill=(0, 0, 0), font=pdt_name)

    def info_product(self, text):

        draw = ImageDraw.Draw(self.product_info)

        draw.text((135, self.prd_ptr), text, fill=(0, 0, 0), font=fnt)
        self.prd_ptr += 30

        self.product_info.save("test1.jpg", quallity=95)

    def setPath(self, path, itemnumber):
        self.path = f"{path}/{itemnumber}"

    def makeFV1(self, itemnumber, color):
        self.full_ptr = 0
        self.fullview = Image.new("RGB", (self.base_width, 1500), (255, 255, 255))
        self.tag = Image.open("01_data/image/FullView.jpg")
        self.fullview.paste(self.tag, (0, 20))

        self.full_ptr += 50
        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_B.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        self.full_ptr += self.img.height + 100
        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_2.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        '''
        self.full_ptr += self.img.height + 100
        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_3.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))
        '''
        self.fullview.save("test.jpg", quality=95)

        return self.fullview

    def makeFV2(self, itemnumber, color2, color1):
        self.full_ptr = 0
        self.fullview = Image.new("RGB", (self.base_width, 2100), (255, 255, 255))
        self.tag = Image.open("01_data/image/FullView.jpg")
        self.fullview.paste(self.tag, (0, 20))

        self.full_ptr += 50
        self.img = Image.open(f"{self.path}/{itemnumber}_{color1}_B.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        self.full_ptr += self.img.height + 100
        self.img = Image.open(f"{self.path}/{itemnumber}_{color2}_B.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        self.full_ptr += self.img.height + 100
        self.img = Image.open(f"{self.path}/{itemnumber}_{color2}_2.jpg")
        self.img = self.img.resize((600, 600))
        self.fullview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), self.full_ptr))

        self.fullview.save("test.jpg", quality=95)

        return self.fullview

    def makeDV(self, itemnumber, color):

        detail_ptr = 0
        self.area = (50, 150, 550, 550)
        self.detailview = Image.new("RGB", (self.base_width, 1300), (255, 255, 255))
        self.tag = Image.open("01_data/image/DetailVeiw.jpg")
        self.detailview.paste(self.tag, (0, 0))
        detail_ptr += 50

        str_tmp = f"{self.path}/{itemnumber}_{color}_3.jpg"
        self.img = Image.open(str_tmp)
        self.img = self.img.resize((600, 600))
        self.img = self.img.crop(self.area)
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 10

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_4.jpg")
        self.img = self.img.resize((600, 600))
        self.img = self.img.crop(self.area)
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))
        detail_ptr += self.img.height + 10

        self.img = Image.open(f"{self.path}/{itemnumber}_{color}_5.jpg")
        self.img = self.img.resize((600, 600))
        self.img = self.img.crop(self.area)
        self.detailview.paste(self.img, (int((self.base_width / 2) - (self.img.width / 2)), detail_ptr))

        self.detailview.save("test_detail.jpg", quallity=95)

        return self.detailview

    def makeInfo(self):
        self.info_ptr = 0

        text = "비침/n있음/n약간/n없음/n23"
        list = text.split("/n")

        box = Image.new("RGB", (10, 10), (0, 0, 0))
        white = Image.new("RGB", (8, 8), (255, 255, 255))
        box.paste(white, (1, 1))

        # 태그
        self.infoview = Image.new("RGB", (self.base_width, 1000), (255, 255, 255))
        self.tag = Image.open("01_data/image/DetailInfo.jpg")
        self.infoview.paste(self.tag, (0, 0))
        self.info_ptr += 70

        # 정보고시 안감 두께 등의 공간
        self.info_table = Image.new("RGB", (self.base_width, 47), (244, 244, 244))
        self.infodata = Image.new("RGB", (self.base_width, 43), (255, 255, 255))
        self.info_table.paste(self.infodata, (152, 2))

        # 사이즈 고시할 공간
        self.size_table = Image.new("RGB", (self.base_width - 250, 40), (244, 244, 244))
        self.img = Image.new("RGB", (self.base_width - 250, 38), (255, 255, 255))
        self.size_table.paste(self.img, (1, 0))

        # 표 첫줄
        self.infoview.paste(self.info_table, (0, self.info_ptr))

        self.drawtext(self.infoview, list[0], 50, self.info_ptr + 15)

        for i in range(0, 4):
            self.drawtext(self.infoview, list[i + 1], 230 + (i * 120), self.info_ptr + 16)
            self.infoview.paste(box, (210 + (i * 120), self.info_ptr + 20))

        # ImageDraw.Draw(self.infoview).text((50, info_ptr + 15), "비침", font=fnt, fill=(0, 0, 0))
        # ImageDraw.Draw(self.infoview).text((210, info_ptr + 15), "있음", font=fnt, fill=(0, 0, 0))
        # ImageDraw.Draw(self.infoview).text((370, info_ptr + 15), "약간", font=fnt, fill=(0, 0, 0))
        # ImageDraw.Draw(self.infoview).text((530, info_ptr + 15), "없음", font=fnt, fill=(0, 0, 0))

        self.info_ptr += 45

        # 표 두번째줄
        self.infoview.paste(self.info_table, (0, self.info_ptr))
        for i in range(0, 4):
            self.drawtext(self.infoview, list[i], 50 + (i * 160), self.info_ptr + 15)
        self.info_ptr += 100

        self.infoview.save("test_info.jpg", quallity=95)

        return self.infoview

    def info_size(self):

        # 사이즈 고시할 공간
        value = "사이즈/n어깨넓이/n가슴둘레/n소매길이/n전체길이"
        value_list = value.split("/n")

        self.size_table = Image.new("RGB", (self.base_width - 200, 40), (244, 244, 244))  # (500, 40)
        self.grey = Image.new("RGB", (self.base_width - 200, 40), (244, 244, 244))
        self.img = Image.new("RGB", (self.base_width - 200, 38), (255, 255, 255))
        self.size_table.paste(self.img, (1, 0))

        self.img = Image.open("01_data/image/SizeSpec.jpg")
        self.infoview.paste(self.img, (0, self.info_ptr))

        self.info_ptr += 80

        self.infoview.save("test_info2.jpg", quallity=95)

    def size_insert(self, value):
        value_list = value.split("/n")

        self.infoview.paste(self.grey, (0, self.info_ptr))
        num = 1
        for n in value_list:  # 사이즈 어깨넓이 등
            w, h = fnt.getsize(n)
            ImageDraw.Draw(self.infoview).text(
                ((((500 / len(value_list) * num) - (500 / len(value_list) / 2)) - w / 2), (self.info_ptr + 25 - h)), n,
                font=fnt, fill=(0, 0, 0))
            num += 1
        self.info_ptr += 40

    def info_tip(self):

        self.info_ptr += 100

        self.tag = Image.open("01_data/image/Tip.jpg")
        self.infoview.paste(self.tag, (0, self.info_ptr))
        self.info_ptr += 60

        ImageDraw.Draw(self.infoview).text((20, self.info_ptr), "-사이즈 스펙은 실측 사이즈 기준입니다.(가슴둘레는 라벨사이즈 기준)", font=fnt_tip,
                                           fill=(60, 60, 60))
        self.info_ptr += 25
        ImageDraw.Draw(self.infoview).text((20, self.info_ptr), "-사이즈는 측정 방법과 생산 과정에 따라 약간의 오차가 발생할 수 있습니다.",
                                           font=fnt_tip, fill=(60, 60, 60))
        self.info_ptr += 25
        ImageDraw.Draw(self.infoview).text((20, self.info_ptr),
                                           "-제품 안쪽 라벨에 표기된 사이즈는 표준 신체 사이즈를 표기한 것이므로, 실측사이즈와 차이가 있을 수 있습니다.",
                                           font=fnt_tip, fill=(60, 60, 60))

        self.infoview.save("test_info3.jpg", quallity=95)

    def combineImg(self):
        self.fullimage.paste(self.fullview, (0, 0))
        self.fullimage.paste(self.detailview, (0, self.fullview.height))
        self.fullimage.paste(self.product_info, (0, self.fullview.height + self.detailview.height))
        self.fullimage.paste(self.infoview, (0, self.fullview.height + self.detailview.height + self.product_info.height))

        self.fullimage.save("test_fullimage.jpg", quallity=95)

    def drawtext(self, image, text, x, y):
        ImageDraw.Draw(image).text((x, y), text, font=fnt, fill=(0, 0, 0))


if __name__ == '__main__':
    itemnumber = "PBJAX2032"
    color = "GY"

    mkImage = MakeImg()

    path = "D:\\GitHub\\ImageMaking\\01_data\\man"

    mkImage.setPath("D:/GitHub/ImageMaking/01_data/man", itemnumber)
    # mkImage.setPath("D:\GitHub\ImageMaking\01_data\man\PBJAX2032")

    mkImage.makeFV1("PBJAX2032", "GY")
    mkImage.makeDV("PBJAX2032", "GY")
    mkImage.makeInfo()
    mkImage.info_size()
    mkImage.info_tip()
    mkImage.info_product("TXBAA4403")
    mkImage.info_product("IV(아이보리)/NA(네이비)")
    mkImage.info_product("55/66")
    mkImage.info_product("봄/여름")
    mkImage.info_product("본 제품은 반드시 드라이크리닝 하십시오.(세탁라벨참고)")
    mkImage.info_product("중국")
    mkImage.info_product("[겉감]폴리에스터100%")
    mkImage.info_product("[배색]폴리에스터100%")

    mkImage.combineImg()
