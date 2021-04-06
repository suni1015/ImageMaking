"""
엑셀 데이터 파싱 클래스

"""
import pandas as pd

# 신원 코드구분 dictionary
dic_codeFormat = {
    # 1
    'A': '브랜드코드',

    # 2
    'B': '시즌',

    # 3
    'C': '대복종',

    # 4
    'D': '소복종',

    # 5
    'E': '월',

    # 6
    '0000': '숫자4자리',

    # 7
    '0': '리오더'
}

# 1 - 브랜드 dictionary --------------------------------
dic_brand = {
    "P": "SIEG",
    "F": "FAHRENHEIT",
    "B": "BESTIBELLI",
    "S": "SI",
    "V": "ISABEY",
    "T": "VIKY",
    "X": "SIWY",
    "G": "GINNASIX",
    "Q": "ICONIQ",
    "M": "MarkM	"
}

# 남성/여성 브랜드 구분 set  ----------------------
set_man = {'P', 'F', 'M', 'Q'}
set_woman = {'B', 'S', 'T', 'V', 'G'}

# 2 - 시즌 dic --------------------------------------
dic_season = {
    "C": "2021 S/S",
    "D": "2021 F/W",
    "E": "2012 S/S",
    "F": "2012 F/W",
    "G": "2013 S/S",
    "H": "2013 F/W",
    "I": "2014 S/S",
    "J": "2014 F/W",
    "K": "2015 S/S",
    "L": "2015 F/W",
    "M": "2016 S/S",
    "P": "2016 F/W",
    "Q": "2017 S/S",
    "R": "2017 F/W",
    "U": "2018 S/S",
    "W": "2018 F/W",
    "X": "2019 S/S",
    "Y": "2019 F/W",
    "A": "2020 S/S",
    "B": "2020 F/W"
}

# 3 - 대복종 dic ------------------------------------------
dic_man_category = {
    "A": "액세서리",
    "AT": "타이",
    "AG": "가방",
    "AP": "양말",
    "AL": "벨트",
    "AS": "신발",

    "B": "셔츠",
    "C": "가디건",
    "U": "니트",
    "I": "티셔츠",
    "F": "팬츠/데님",
    "D": "다운패딩",
    "E": "자켓",
    "G": "가죽자켓",
    "H": "코트",
    "L": "코트",
    "M": "점퍼",
    "N": "트렌치",
    "J": "수트자켓",
    "P": "수트팬츠",
    "V": "수트베스트"
}

dic_woman_category = {
    "A": "액세서리",
    "AP": "PANTS-레깅스",
    "AF": "스카프",
    "AS": "신발",
    "AN": "쥬얼리",
    "AZ": "쥬얼리",
    "AG": "가방",

    "B": "블라우스",
    "C": "가디건",
    "U": "니트",
    "I": "티셔츠",
    "O": "원피스",
    "F": "팬츠/데님",
    "S": "스커트",
    "D": "다운패딩",
    "E": "자켓",
    "G": "가죽자켓",
    "H": "코트",
    "L": "코트",
    "M": "점퍼",
    "N": "트렌치"
}

# 4 - 소복종 dic ------------------------------------------

# 5 - 월 dic ------------------------------------------
dic_month = {
    "A": "1월",
    "B": "2월",
    "C": "3월",
    "D": "4월",
    "E": "5월",
    "F": "6월",
    "G": "7월",
    "H": "8월",
    "I": "9월",
    "X": "10월",
    "Y": "11월",
    "Z": "12월"
}

set_spring = {"1월", "2월", "3월"}
set_summer = {"4월", "5월", "6월"}
set_fall = {"7월", "8월", "9월"}
set_winter = {"10월", "11월", "12월"}

# 6 - 품번 dic ------------------------------------------
# 랜던 숫자 4자리
# 7 - 오더 dic ------------------------------------------
# 0 : 본 오더
# 1,2 : 리오더
# A : 추가오더

# 클래스 shinwon 정의  ===================================
''' description>>
ㅇ input
  - 품번 string
ㅇ output
  - 그림 파일명
ㅇ operator
  - 품번 파싱
  - 파싱한 데이터 기반으로 엑셀에서 그림 파일명을 가져온다.
'''


class Shinwon:
    """
    브랜드코드(0),시즌(1),대복종(2),소복종(3),월(4),숫자4자리(5), -(9), 리오더(10)
    """
    df_all_data = None
    str_poombun = None
    # df_product_info = None
    dic_product = {}  # 빈 딕셔너리 만들기. 의류정보 결과물을 저장할 공간이다.
    dic_product_set = {}  # 빈 딕셔너리 만들기. 의류정보 결과물을 저장할 공간이다.  SET 용 공간
    size_count = None       # 이 제품의 사이즈 개수를 저장한다. (55사이즈, 66사이즈 --> 2개)
    list_poombun = None
    bSET_poombun = False

    def __init__(self, ):
        return

    def set_poombun(self, str_poombun):
        self.str_poombun = str_poombun

    def decode_poombun(self):
        """
        brand => self.str_poombun[0]
        season => self.str_poombun[1]
        category_big => self.str_poombun[2]
        category_small => self.str_poombun[3]
        month => self.str_poombun[4]
        number => self.str_poombun[5:9]
        reorder => self.str_poombun[10:]
        """

        # 브랜드
        if self.str_poombun[0] in dic_brand:
            # self.brand = dic_brand[self.str_poombun[0]]
            self.dic_product['브랜드'] = dic_brand[self.str_poombun[0]]
            # print('브랜드 : ', self.brand)
        else:
            print('ERR : 브랜드 코드')
            #return -1, 'ERR : 브랜드 코드'

        # 남성/여성 구분
        if self.str_poombun[0] in set_man:
            # self.sex = '남성'
            self.dic_product['성별'] = '남성'
            # print('성별 : ', self.sex)
        elif self.str_poombun[0] in set_woman:
            # self.sex = '여성'
            self.dic_product['성별'] = '여성'
            # print('성별 : ', self.sex)
        else:
            print('ERR : 성별1')

        # 시즌
        if self.str_poombun[1] in dic_season:
            # self.season = dic_season[self.str_poombun[1]]
            self.dic_product['시즌'] = dic_season[self.str_poombun[1]]
            # print('시즌 : ', self.season)
        else:
            print('ERR : 시즌 코드')

        # 대복종 (남성/여성, 액서서리/기타 구분)
        '''품번 코드가 A로 시작하면 액서서리로서 코드가 2글자이며, 그외에는 1글자 코드 처리하면 된다.'''
        tmp_code = self.str_poombun[2:4] if self.str_poombun[2] == 'A' else self.str_poombun[2]

        if '성별' in self.dic_product:
            if self.dic_product['성별'] == '남성':
                if tmp_code in dic_man_category:
                    # self.category_big = dic_man_category[tmp_code]
                    self.dic_product['대복종'] = dic_man_category[tmp_code]
                    # print('복종 : ', self.category_big)
                else:
                    print('ERR : 대복종 코드')

            elif self.dic_product['성별'] == '여성':
                if tmp_code in dic_woman_category:
                    # self.category_big = dic_woman_category[tmp_code]
                    self.dic_product['대복종'] = dic_woman_category[tmp_code]
                    # print('복종 : ', self.category_big)
                else:
                    print('ERR : 대복종 코드')
            else:
                print('ERR : 성별2')

        # 소복종

        # 월
        if self.str_poombun[4] in dic_month:
            # self.month = dic_month[self.str_poombun[4]]
            self.dic_product['월'] = dic_month[self.str_poombun[4]]
            # print('월 : ', self.month)
        else:
            print('ERR : 월 코드')

    def decode_poombun_set(self):
        """
        brand => self.str_poombun[0]
        season => self.str_poombun[1]
        category_big => self.str_poombun[2]
        category_small => self.str_poombun[3]
        month => self.str_poombun[4]
        number => self.str_poombun[5:9]
        reorder => self.str_poombun[10:]
        """

        # 브랜드
        if self.str_poombun[0] in dic_brand:
            # self.brand = dic_brand[self.str_poombun[0]]
            self.dic_product_set['브랜드'] = dic_brand[self.str_poombun[0]]
            # print('브랜드 : ', self.brand)
        else:
            print('ERR : 브랜드 코드')
            #return -1, 'ERR : 브랜드 코드'

        # 남성/여성 구분
        if self.str_poombun[0] in set_man:
            # self.sex = '남성'
            self.dic_product_set['성별'] = '남성'
            # print('성별 : ', self.sex)
        elif self.str_poombun[0] in set_woman:
            # self.sex = '여성'
            self.dic_product_set['성별'] = '여성'
            # print('성별 : ', self.sex)
        else:
            print('ERR : 성별1')

        # 시즌
        if self.str_poombun[1] in dic_season:
            # self.season = dic_season[self.str_poombun[1]]
            self.dic_product_set['시즌'] = dic_season[self.str_poombun[1]]
            # print('시즌 : ', self.season)
        else:
            print('ERR : 시즌 코드')

        # 대복종 (남성/여성, 액서서리/기타 구분)
        '''품번 코드가 A로 시작하면 액서서리로서 코드가 2글자이며, 그외에는 1글자 코드 처리하면 된다.'''
        tmp_code = self.str_poombun[2:4] if self.str_poombun[2] == 'A' else self.str_poombun[2]

        if '성별' in self.dic_product_set:
            if self.dic_product_set['성별'] == '남성':
                if tmp_code in dic_man_category:
                    # self.category_big = dic_man_category[tmp_code]
                    self.dic_product_set['대복종'] = dic_man_category[tmp_code]
                    # print('복종 : ', self.category_big)
                else:
                    print('ERR : 대복종 코드')

            elif self.dic_product_set['성별'] == '여성':
                if tmp_code in dic_woman_category:
                    # self.category_big = dic_woman_category[tmp_code]
                    self.dic_product_set['대복종'] = dic_woman_category[tmp_code]
                    # print('복종 : ', self.category_big)
                else:
                    print('ERR : 대복종 코드')
            else:
                print('ERR : 성별2')

        # 소복종

        # 월
        if self.str_poombun[4] in dic_month:
            # self.month = dic_month[self.str_poombun[4]]
            self.dic_product_set['월'] = dic_month[self.str_poombun[4]]
            # print('월 : ', self.month)
        else:
            print('ERR : 월 코드')

    def print_poombun(self):
        print("품번 : ", self.str_poombun)

    def print_product_info(self):
        for key, value in self.dic_product.items():
            print('*', key, '-', value)

    def openFile_clothInfo(self, str_file_path):
        """
        # 경로 예제
        base_dir = 'D:/00_WORK/00_github/imageMaking/01_data/woman'
        excel_file = '20201223여성정보고시.xlsx'  # 'sales_per_region.xlsx'
        excel_dir = os.path.join(base_dir, excel_file)
        """

        # Input : Excel 파일 (의류정보고시) ======================
        idx_col = '품번'  # ini 파일입력 되도록 수정해야 함. (ini 파일은 변경이 예상되는 것들을 별도 입력 가능하도록 한 것임.

        self.df_all_data = pd.read_excel(str_file_path,  # write your directory here
                                         sheet_name=0,  # 시트이름을 쓰거나 index
                                         #dtype={'기준\n사이즈': str},
                                         #converters={'기준\n사이즈' : str},
                                         # names = ['region', 'sales_representative', 'sales_amount'],
                                         header=0,  # dictionary type
                                         # index_col=idx_col,
                                         na_values='NaN',
                                         thousands=',',
                                         nrows=100,     # 정보고시 파일은 100개까지만 읽어들인다.
                                         comment='#')
        #print(self.df_all_data)

        print('Info : 엑셀에 기록된 품번 리스트 출력')
        self.list_poombun = self.df_all_data['품번']
        print(len(self.list_poombun))
        for poombun in self.list_poombun:
            print(poombun)

        return


    def parse_excel_data(self):
        # 품번이 입력되었는지 예외처리할것
        if not self.str_poombun:
            print('ERR : 품번 정보가 없습니다.')
            return False

        df_all = self.df_all_data

        # df 데이터 처리 테스트 코드
        row_condition = df_all['품번']
        #col_condition1 = ['브랜드', '관리코드', '상품분류코드', '상품명', '컬러', '시즌', '소재', '실측사이즈(cm)']
        #col_condition2 = ['브랜드', '관리코드', '컬러', '시즌', '소재', '실측사이즈(cm)']
        #df_product_info = df_all.loc[row_condition == self.str_poombun, col_condition2]  # 행/열 조건 삽입하여 데이터 추출

        df_product_info = df_all[row_condition == self.str_poombun]  # 행 조건만 삽입하여 데이터 추출
        #print(type(df_product_info.columns))

        if df_product_info.empty:
            print('ERR : 입력한 품번은 정보고시 파일에 존재하지 않습니다.')
            return False

        self.dic_product['상품명'] = df_all.loc[row_condition == self.str_poombun, '상품명'].values[0]
        self.dic_product['컬러'] = df_all.loc[row_condition == self.str_poombun, '컬러'].values[0]
        self.dic_product['세탁방법'] = df_all.loc[row_condition == self.str_poombun, '세탁방법'].values[0]
        self.dic_product['원산지'] = df_all.loc[row_condition == self.str_poombun, '원산지'].values[0]
        self.dic_product['소재'] = df_all.loc[row_condition == self.str_poombun, '소재'].values[0]
        self.dic_product['상품특성'] = df_all.loc[row_condition == self.str_poombun, '상품특성'].values[0]
        self.dic_product['제조원'] = df_all.loc[row_condition == self.str_poombun, '제조원'].values[0]
        self.dic_product['제조월'] = df_all.loc[row_condition == self.str_poombun, '제조월'].values[0]
        self.dic_product['기준\n사이즈'] = df_all.loc[row_condition == self.str_poombun, '기준\n사이즈'].values[0]
        self.dic_product['실측사이즈(cm)'] = df_all.loc[row_condition == self.str_poombun, '실측사이즈(cm)'].values[0]

        # 칼럼 이름이 없어서 수작업으로 파싱.
        for i, item in enumerate(df_product_info.columns):
            print(i, item)
            if item == '상품특성':
                col_idx1 = i + 1            # 상품특성의 값은 (엑셀상의) 다음칼럼에 있다.(칼럼 이름이 없어서 수작업 처리함)
            elif item == '실측사이즈(cm)':
                col_idx2 = i + 1            # 실측사이즈 값은 (엑셀상의) 다음칼럼에 있다.(칼럼 이름이 없어서 수작업 처리함)

        print('상품특성의 값이 있는 칼럼 인덱스 : ', col_idx1)
        print('실측사이즈 값이 있는 칼럼 인덱스 : ', col_idx2)

        #print(df_product_info.iloc[:, col_idx1].values[0])
        self.dic_product['상품특성 값'] = df_product_info.iloc[:, col_idx1].values[0]

        # 사이즈 개수 세기
        token = ['/', ',']
        self.size_count = 1     # 최소 1개이므로.
        for tk in token:
            self.size_count += self.dic_product['기준\n사이즈'].count(tk)
        print('사이즈 개수 : ', self.size_count)

        for i in range(self.size_count):
            str_key = "사이즈%d" % i
            self.dic_product[str_key] = df_product_info.iloc[:, col_idx2+i].values[0]

        return True


    def parse_excel_data_set(self):
        # 품번이 입력되었는지 예외처리할것
        if not self.str_poombun:
            print('ERR : 품번 정보가 없습니다.')
            return False

        df_all = self.df_all_data

        # df 데이터 처리 테스트 코드
        row_condition = df_all['품번']

        df_product_info = df_all[row_condition == self.str_poombun]  # 행 조건만 삽입하여 데이터 추출
        #print(type(df_product_info.columns))

        if df_product_info.empty:
            print('ERR : 입력한 품번은 정보고시 파일에 존재하지 않습니다.')
            return False

        self.dic_product_set['상품명'] = df_all.loc[row_condition == self.str_poombun, '상품명'].values[0]
        self.dic_product_set['컬러명 ( 한글/영문 )'] = df_all.loc[row_condition == self.str_poombun, '컬러명 ( 한글/영문 )'].values[0]
        self.dic_product_set['세탁방법'] = df_all.loc[row_condition == self.str_poombun, '세탁방법'].values[0]
        self.dic_product_set['원산지'] = df_all.loc[row_condition == self.str_poombun, '원산지'].values[0]
        self.dic_product_set['소재'] = df_all.loc[row_condition == self.str_poombun, '소재'].values[0]
        self.dic_product_set['제조원'] = df_all.loc[row_condition == self.str_poombun, '제조원'].values[0]
        self.dic_product_set['제조월'] = df_all.loc[row_condition == self.str_poombun, '제조월'].values[0]
        self.dic_product_set['사이즈'] = df_all.loc[row_condition == self.str_poombun, '사이즈'].values[0]

        ''' 엑셀에 아래 포맷으로 저장되어 있음
        상의
        
         95, 97,100,103,105,110
        
        하의
        
         74, 78, 82, 86, 90, 94
        '''
        if(self.dic_product_set['사이즈'].split('\n')[0] == '상의'):
            self.dic_product_set['사이즈_상의'] = self.dic_product_set['사이즈'].split('\n')[2]
        if (self.dic_product_set['사이즈'].split('\n')[4] == '하의'):
            self.dic_product_set['사이즈_하의'] = self.dic_product_set['사이즈'].split('\n')[6]

        return True

    def get_product_info(self):
        if self.bSET_poombun == False:
            return self.dic_product         # 일반 품번
        else:
            return self.dic_product_set     # Set 품번

    def clear_product_info(self):
        self.dic_product.clear()

    def get_size_cnt(self):
        return self.size_count

    def get_list_poombun(self):
        return self.list_poombun


"""
if __name__ == '__main__':
    # 판다스 Dataframe 많은 데이터 출력하기
    pd.set_option('display.max_row', 500)
    pd.set_option('display.max_columns', 100)

    # Input : 품번 =======================================
    sw_obj = Shinwon('SBOCZ2965')  # sw_obj = Shinwon('BYJAX1234-0')
    sw_obj.print_poombun()

    sw_obj.decode_poombun()
    # sw_obj.print_product_info()

    # 파일 오픈  (의류정보고시,Excel) ======================
    sw_obj.openFile_clothInfo()

    # 원하는 품번(ROW)의 행 정보 출력
    sw_obj.parse_excel_data()
    sw_obj.print_product_info()
"""
