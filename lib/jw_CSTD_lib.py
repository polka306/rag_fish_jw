import os
import os.path
import xmltodict
import dicttoxml
import json
import csv
import pickle

from pymongo import MongoClient

OBJECT_CATEGORY_TABLE = {
    'kor':{
        'sonar' : [
            '타이어',
            '스프링통발1',
            '스프링통발',
            '원형통발',
            '어망',
            '나무',
            '로프',
            
            '암반군',
            '연흔',
            '인공어초',
            '인공어초군',
            '콘크리트블럭',

            '타이어_B',
            '스프링통발1_B',
            '스프링통발_B',
            '원형통발_B',
            '어망_B',
            '나무_B',
            '로프_B',
            
            '암반군_B',
            '연흔_B',
            '인공어초_B',
            '인공어초군_B',
            '콘크리트블럭_B',
            '기타객체',
            '객체없는지형',

            '자망',
            '스프링통발2',
            '유사나무',
            '유사자망',
            '자망_B',
            '스프링통발2_B',
            '유사나무_B',
            '유사자망_B',
        ],
        'uw' : [
            '타이어',
            '스프링통발',
            '원형통발',
            '사각통발',
            '장어통발',
            '어망',
            '합판',
            '단일로프',
            '로프뭉치',

            '타이어_b',
            '스프링통발_b',
            '원형통발_b',
            '사각통발_b',
            '장어통발_b',
            '어망_b',
            '합판_b',
            '단일로프_b',
            '로프뭉치_b'
        ]
    },
    'en': {
        'sonar' : [
            'tire',
            'spring fish trap',
            'circular fish trap',
            'fish net',
            'wood',
            'rope',
            
            'bedrock group',
            'ripple marks',
            'artificial reef',
            'artificial reef group',
            'concrete block',
            'other objects',
            'no object'
        ],
        'uw' : [
            'tire',
            'spring fish trap',
            'circular fish trap',
            'rectangular fish trap',
            'eel fish trap',
            'fish net',
            'wood',
            'rope',
            'bundle of ropes'
        ]
    }
}

OBJECT_CATEGORY_TABLE2 = {
    'sonar' : [
        '타이어',
        '스프링통발1',
        '스프링통발2',
        '원형통발',
        '어망',
        '자망',
        '나무',
        '로프',
        
        '암반군',
        '연흔',
        '인공어초',
        '인공어초군',
        '콘크리트블럭',
        '유사나무',
        '유사자망'
    ],
    'uw' : [
        '타이어',
        '스프링통발',
        '원형통발',
        '사각통발',
        '장어통발',
        '어망',
        '합판',
        '단일로프',
        '로프뭉치'
    ]
}

OBJECT_CATEGORY_TABLE_EN = {
    'sonar' : {
        '타이어':('tire', 'A'),
        '스프링통발1':('spring fish trap', 'A'),
        '스프링통발':('spring fish trap', 'A'),
        '원형통발':('circular fish trap', 'A'),
        '어망':('fish net', 'A'),
        '자망':('gillnet', 'A'),
        '나무':('wood', 'A'),
        '로프':('rope', 'A'),
        
        '암반군':('bedrock group', 'A'),
        '연흔':('ripple marks', 'A'),
        '인공어초':('artificial reef', 'A'),
        '인공어초군':('artificial reef group', 'A'),
        '콘크리트블럭':('concrete block', 'A'),
        '유사나무':('similar wood', 'A'),
        '유사자망':('similar gillnet', 'A'),

        '타이어_B':('tire', 'B'),
        '스프링통발1_B':('spring fish trap', 'B'),
        '스프링통발_B':('spring fish trap', 'B'),
        '원형통발_B':('circular fish trap', 'B'),
        '어망_B':('fish net', 'B'),
        '나무_B':('wood', 'B'),
        '로프_B':('rope', 'B'),
        
        '암반군_B':('bedrock group', 'B'),
        '연흔_B':('ripple marks', 'B'),
        '인공어초_B':('artificial reef', 'B'),
        '인공어초군_B':('artificial reef group', 'B'),
        '콘크리트블럭_B':('concrete block', 'B'),
        '기타객체':('other objects', 'B'),
        '객체없는지형':('no object', 'B')
    },
    'uw' : {
        '타이어':('tire', 'A'),
        '스프링통발':('spring fish trap', 'A'),
        '원형통발':('circular fish trap', 'A'),
        '사각통발':('rectangular fish trap', 'A'),
        '장어통발':('eel fish trap', 'A'),
        '어망':('fish net', 'A'),
        '합판':('wood', 'A'),
        '단일로프':('rope', 'A'),
        '로프뭉치':('bundle of ropes', 'A'),

        '타이어_b':('tire', 'B'),
        '스프링통발_b':('spring fish trap', 'B'),
        '원형통발_b':('circular fish trap', 'B'),
        '사각통발_b':('rectangular fish trap', 'B'),
        '장어통발_b':('eel fish trap', 'B'),
        '어망_b':('fish net', 'B'),
        '합판_b':('wood', 'B'),
        '단일로프_b':('rope', 'B'),
        '로프뭉치_b':('bundle of ropes', 'B')
    }
}

OBJECT_CATEGORY_TABLE_EN2 = {
    'sonar' : [
        'tire',
        'spring fish trap1',
        'spring fish trap2',
        'circular fish trap',
        'fish net',
        'gillnet',
        'wood',
        'rope',
        
        'bedrock group',
        'ripple marks',
        'artificial reef',
        'artificial reef group',
        'concrete block',
        'similar wood',
        'similar gillnet'
    ],
    'uw' : [
        'tire',
        'spring fish trap',
        'circular fish trap',
        'rectangular fish trap',
        'eel fish trap',
        'fish net',
        'plywood',
        'single rope',
        'bundle of ropes'
    ]
}

UW_IMAGE_SIZE = {
    'fhd' : (1080, 1920),
    'hd' : (720, 1280),
    'sd' : (480, 640)
}

UW_LOCATION_TABLE = {
    '통영항' : ['34.837805', '128.422053'],
    '가래지구' : ['34.392521', '126.929272'],
    '고성' : ['38.490512', '128.508928'],
    '광양항' : ['34.899598', '127.674699'],
    '구룡포' : ['35.987252', '129.556157'],
    '마산항' : ['35.193589', '128.583511'],
    '부안' : ['35.807320', '126.690719'],
    '삼천포항' : ['34.922875', '128.083104'],
    '신수항' : ['35.442471', '129.358926'],
    '옥포항' : ['34.889302', '128.698264'],
    '울주군' : ['35.451632', '129.361615'],
    '울진군' : ['37.049746', '129.420208'],
    '진해항' : ['35.125470', '128.688871'],
    '태안' : ['36.731788', '126.179820'],
    '팔당호' : ['37.508226', '127.296585'],
    '속초항' : ['38.208858', '128.598288'],
    '여수' : ['34.725379', '127.665524'],
    '온산항' : ['35.441158', '129.358274'],
    '목포항' : ['34.780724', '126.385841'],
    '서귀포항' : ['33.236191', '126.565765'],
    '영덕군' : ['36.461941', '129.455171'],
    '포항시' : ['36.046488', '129.447189'],
    '무안군' : ['34.953786', '126.382841'],
    '마산리' : ['37.095888', '127.088894'],
    '발산리' : ['35.963827', '126.798446'],
    '입암리' : ['37.926182', '128.764941'],
    '제주항' : ['33.522041', '126.535568'],
    '구만리' : ['36.075787', '129.541415'],
    '대보리' : ['36.070221', '129.572125'],
    '신수도' : ['34.902706', '128.072946'],
    '서천군' : ['36.089538', '126.614597'],
    '무창포' : ['36.250198', '126.536222'],
    '연도' : ['34.440396', '127.793932'],
    '사천시' : ['34.917290', '128.074405'],
    '용기포항' : ['36.021779', '129.431396'],
    '대산항' : ['37.018013', '126.419692'],
    '대천항' : ['36.330434', '126.510896'],
    '서포리' : ['37.226203', '126.098882'],
    '비토리' : ['34.964962', '127.974974'],
    '보길도' : ['34.132881', '126.505703'],
    '영일만항' : ['36.112065', '129.435957'],
    '완도군' : ['34.269826', '126.802733'],
    '강구항' : ['36.358498', '129.394431'],
    '양포' : ['35.877411', '129.523722'],
    '죽변항' : ['37.055768', '129.421697'],
    '축산항' : ['36.509941', '129.450485'],
    '대진항' : ['38.500066', '128.428822'],
    '직산항' : ['36.724630', '129.474399'],
    '사천진항' : ['34.923494', '128.083641'],
    '지역불명' : ['0.0', '0.0']
}
UW_LOCATION_TABLE_EN = {
    '통영항' : "Tongyeong Port",
    '가래지구' : "Garae",
    '고성' : "Goseong-gun",
    '광양항' : "Gwangyang Port",
    '구룡포' : "Guryongpo",
    '마산항' : "Masan Port",
    '부안' : "Buan",
    '삼천포항' : "Samcheonpo Port",
    '신수항' : "Sinsu Port",
    '옥포항' : "Okpo Port",
    '울주군' : "Ulju-gun",
    '울진군' : "Uljin-gun",
    '진해항' : "Jinhae Port",
    '태안' : "Taean",
    '팔당호' : "Paldang Lake",
    '속초항' : "Sokcho Port",
    '여수' : "Yeosu",
    '온산항' : "Onsan Port",
    '목포항' : "Mokpo Port",
    '서귀포항' : "Seogwipo Port",
    '영덕군' : "Yeongdeok-gun",
    '포항시' : "Pohang-si",
    '무안군' : "Muan-gun",
    '마산리' : "Masan-li",
    '발산리' : "Balsan-li",
    '입암리' : "Yangyang-gun",
    '제주항' : "Jeju Port",
    '구만리' : "Guman-li",
    '대보리' : "Daebo-li",
    '신수도' : "Sinsudo",
    '서천군' : "Seocheon-gun",
    '무창포' : "Muchangpo",
    '연도' : "Yeondo",
    '사천시' : "Sacheon-si",
    '용기포항' : "Yongipo Port",
    '대산항' : "Daesan Port",
    '대천항' : "Daecheon Port",
    '서포리' : "Seopo-li",
    '비토리' : "Sacheon-si",
    '보길도' : "Bogildo",
    '영일만항' : "Yeongilman Port",
    '완도군' : "Wando-gun",
    '강구항' : "Ganggu Port",
    '양포' : "Yangpo",
    '죽변항' : "Jukbyeon Port",
    '축산항' : "Chuksan Port",
    '대진항' : "Daejin Port",
    '직산항' : "Jiksan Port",
    '사천진항' : 'Sacheon New Port',
    '지역불명' : ""
}
UW_LOCATION_TABLE2 = {
    "가래지구":{
        "idx":1,
        "en":"Garae",
        "gps":['34.392521', '126.929272']
    },
    "고성":{
        "idx":2,
        "en":"Goseong-gun",
        "gps":['38.490512', '128.508928']
    },
    "광양항":{
        "idx":3,
        "en":"Gwangyang Port",
        "gps":['34.899598', '127.674699']
    },
    "구룡포":{
        "idx":4,
        "en":"Guryongpo",
        "gps":['35.987252', '129.556157']
    },
    "마산항":{
        "idx":5,
        "en":"Masan Port",
        "gps":['35.193589', '128.583511']
    },
    "삼천포항":{
        "idx":6,
        "en":"Samcheonpo Port",
        "gps":['34.922875', '128.083104']
    },
    "신수항":{
        "idx":7,
        "en":"Sinsu Port",
        "gps":['35.442471', '129.358926']
    },
    "옥포항":{
        "idx":8,
        "en":"Okpo Port",
        "gps":['34.889302', '128.698264']
    },
    "울주군":{
        "idx":9,
        "en":"Ulju-gun",
        "gps":['35.451632', '129.361615']
    },
    "울진군":{
        "idx":10,
        "en":"Uljin-gun",
        "gps":['37.049746', '129.420208']
    },
    "진해항":{
        "idx":11,
        "en":"Jinhae Port",
        "gps":['35.125470', '128.688871']
    },
    "태안":{
        "idx":12,
        "en":"Taean",
        "gps":['36.731788', '126.179820']
    },
    "통영항":{
        "idx":13,
        "en":"Tongyeong Port",
        "gps":['34.837805', '128.422053']
    },
    "팔당호":{
        "idx":14,
        "en":"Paldang Lake",
        "gps":['37.508226', '127.296585']
    },
    "부안":{
        "idx":15,
        "en":"Buan",
        "gps":['35.807320', '126.690719']
    },
    "구만리":{
        "idx":16,
        "en":"Guman-li",
        "gps":['36.075787', '129.541415']
    },
    "대보리":{
        "idx":17,
        "en":"Daebo-li",
        "gps":['36.070221', '129.572125']
    },
    "대산항":{
        "idx":18,
        "en":"Daesan Port",
        "gps":['37.018013', '126.419692']
    },
    "대천항":{
        "idx":19,
        "en":"Daecheon Port",
        "gps":['36.330434', '126.510896']
    },
    "마산리":{
        "idx":20,
        "en":"Masan-li",
        "gps":['37.095888', '127.088894']
    },
    "목포항":{
        "idx":21,
        "en":"Mokpo Port",
        "gps":['34.780724', '126.385841']
    },
    "무안군":{
        "idx":22,
        "en":"Muan-gun",
        "gps":['34.953786', '126.382841']
    },
    "무창포":{
        "idx":23,
        "en":"Muchangpo",
        "gps":['36.250198', '126.536222']
    },
    "발산리":{
        "idx":24,
        "en":"Balsan-li",
        "gps":['35.963827', '126.798446']
    },
    "사천시":{
        "idx":25,
        "en":"Sacheon-si",
        "gps":['34.917290', '128.074405']
    },
    "서귀포항":{
        "idx":26,
        "en":"Seogwipo Port",
        "gps":['33.236191', '126.565765']
    },
    "서천군":{
        "idx":27,
        "en":"Seocheon-gun",
        "gps":['36.089538', '126.614597']
    },
    "서포리":{
        "idx":28,
        "en":"Seopo-li",
        "gps":['37.226203', '126.098882']
    },
    "속초항":{
        "idx":29,
        "en":"Sokcho Port",
        "gps":['38.208858', '128.598288']
    },
    "신수도":{
        "idx":30,
        "en":"Sinsudo",
        "gps":['34.902706', '128.072946']
    },
    "여수":{
        "idx":31,
        "en":"Yeosu",
        "gps":['34.725379', '127.665524']
    },
    "연도":{
        "idx":32,
        "en":"Yeondo",
        "gps":['34.440396', '127.793932']
    },
    "영덕군":{
        "idx":33,
        "en":"Yeongdeok-gun",
        "gps":['36.461941', '129.455171']
    },
    "영일만항":{
        "idx":34,
        "en":"Yeongilman Port",
        "gps":['36.112065', '129.435957']
    },
    "온산항":{
        "idx":35,
        "en":"Onsan Port",
        "gps":['35.441158', '129.358274']
    },
    "완도군":{
        "idx":36,
        "en":"Wando-gun",
        "gps":['34.269826', '126.802733']
    },
    "용기포항":{
        "idx":37,
        "en":"Yongipo Port",
        "gps":['36.021779', '129.431396']
    },
    "입암리":{
        "idx":38,
        "en":"Yangyang-gun",
        "gps":['37.926182', '128.764941']
    },
    "제주항":{
        "idx":39,
        "en":"Jeju Port",
        "gps":['33.522041', '126.535568']
    },
    "지역불명":{
        "idx":40,
        "en":"",
        "gps":['0.0', '0.0']
    },
    "포항시":{
        "idx":41,
        "en":"Pohang-si",
        "gps":['36.046488', '129.447189']
    },
    "강구항":{
        "idx":42,
        "en":"Ganggu Port",
        "gps":['36.358498', '129.394431']
    },
    "양포":{
        "idx":43,
        "en":"Yangpo",
        "gps":['35.877411', '129.523722']
    },
    "죽변항":{
        "idx":44,
        "en":"Jukbyeon Port",
        "gps":['37.055768', '129.421697']
    },
    "축산항":{
        "idx":45,
        "en":"Chuksan Port",
        "gps":['36.509941', '129.450485']
    },
    "대진항":{
        "idx":46,
        "en":"Daejin Port",
        "gps":['38.500066', '128.428822']
    },
    "직산항":{
        "idx":47,
        "en":"Jiksan Port",
        "gps":['36.724630', '129.474399']
    },
    "사천진항":{
        "idx":48,
        "en":"Sacheon New Port",
        "gps":['34.923494', '128.083641']
    }
}

'''
    동,서,남해 구분을 위한 비교 테이블
                  |
            west  |   east
            sea   |   sea
          --------*---------
            southern sea

    * : 중심점 (35.075528, 128.012627)

    데이터 구조 : [latitude min, latitude max, longitude min, longitude max]
'''
SONAR_LCATION_TABLE = {
    '동해' : [35.075528, None, 128.012627, None],
    '남해' : [None, 35.075528, None, None],
    '서해' : [35.075528, None, None, 128.012627]
}

SONAR_LOCATION_TABLE_EN = {
    '동해' : {
        'en' : 'the East sea',
        'num' : 1
    },
    '남해' : {
        'en' : 'the South sea',
        'num' : 2
    },
    '서해' : {
        'en' : 'the West sea',
        'num' : 3
    }
}

# load config
local_cfg_path = "local.cfg"
cfg_data = {
    "db": {
        "url":"127.0.0.1:27017",
        "id":"jwkang",
        "pass":"dmsdhrfyd!210"
    }
}
if os.path.isfile(local_cfg_path) :
    with open(local_cfg_path, "r", encoding='UTF8') as cfgfile:
        cfg_data = json.load(cfgfile)

def listup_file(log, folder_path, ext_type='xml', filter = None):
    '''
    지정된 폴더 내부의 파일 리스트를 list 객체로 반환해주는 함수
    :param log: 메시지를 출력하기 위한 log 객체
    :param folder_path: 대상 폴더 전체 경로
    :param ext_type: 대상 파일 확장자 (default : xml)
    :prarm filter: 제외할 폴더나 파일
    예시1) 'X'라는 이름의 폴더 제외 {'folders':'X'}
    :return: 아래 dict 구조를 list 형태로 반환
    {
        'filename' : filename,
        'path' : full path of file,
        'filetype' : meta file type ('xml', 'json')
    }
    '''
    meta_files = []
    for rootpath, dirnames, filenames in os.walk(folder_path):
        log.debug(rootpath)
        if filter is not None and 'folders' in filter:
            if rootpath.endswith(filter['folders']):
                continue
    
        for filename in [file for file in filenames if file.endswith('.'+ext_type)] : 
            log.debug('\t'+filename)
            meta_files.append({'filename': filename, 'path': rootpath+'/'+filename, 'filetype':ext_type})

    log.info(f'file type : {ext_type}, file quantity : {len(meta_files)}')
    return meta_files

def load_meta_data(log, file):
    try:
        with open(file['path'], "r", encoding='UTF8') as metafile:
            if file['filetype'] == 'xml' or file['filetype'] == 'kml':
                data = metafile.read()
                cc = xmltodict.parse(data)
                meta_data = json.loads(json.dumps(cc))
            elif file['filetype'] == 'json':
                meta_data = json.load(metafile)
            else:
                log.critical('meta data parsing fail - %s'%file['filename'])
                meta_data = {}
    except IOError:
        log.critical('cant load meta file - %s'%file['filename'])
        meta_data = {}
    log.debug(meta_data)
    return meta_data

def save_meta_data(filepath, meta_data):    
    with open(filepath, 'w', encoding='utf-8') as result_file:
        result_file.write(xmltodict.unparse(meta_data))

def download_meta_data(log, db, src, filename):
    query = {
        f"{src}.filename":filename
    }
    meta = db.find(query)
    log.info(f"{query} : {json.dumps(meta)}")
    return meta

def upload_meta_data(log, db, src, filename, meta):
    query = {
        f"{src}.filename":filename
    }


# csv file func
def write_csv(filepath, header, body_list):    
    with open(filepath, 'wt', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if header != None:
            writer.writerow(header)
        for row in body_list:
            writer.writerow(row)

def read_csv(filepath):
    data = []    
    with open(filepath, 'rt', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def write_file(filepath, msg):
    with open(filepath, 'wt', encoding='utf8') as f:
        f.writelines(msg)

def read_file(filepath):
    data = None
    with open(filepath, 'rt', encoding='utf8', newline='\n') as f:
        data = f.readlines()
    return data

# db func
def get_db(collection):
    global cfg_data
    db_path_str = f"mongodb://{cfg_data['db']['id']}:{cfg_data['db']['pass']}@{cfg_data['db']['url']}/"
    client = MongoClient(db_path_str)
    db = client.fyddb
    return db[collection]

def make_query_sonar(filename):
    '''
    - param
    filename : sonar file name (00000000_00000_00_sonar.jpg)
    - return : query, splited number
    '''
    ext = os.path.splitext(filename)[1]
    splited_filename = os.path.splitext(filename)[0].split('_')
    query = {
        'refined.filename' : f"{splited_filename[0]}_{splited_filename[1]}{ext}"
    }
    return query, splited_filename[2]



if __name__ == "__main__":
    import jw_log
    # log, err_log = jw_log.jw_make_logger('jw_CSTD_lib')
    # file_list = listup_file(log, 'E:\\Dev\\Data\\3_verified\\수중촬영이미지\\C급 재정제\\2차\\2020-10-20(C급재정제)', 'jpg', {'folders':('X', '로프')})
    db = get_db("sonar_data")
    list = db.find()
    print(list[0])

    msg = ['test', '한글', '123']
    write_file('./test.txt', msg)
    data = read_file('./test.txt')
    print(data)

    msg = [
        ['test', '한글', '123'],
        ['test', '한글2', '1223']
    ]
    write_csv('./test.csv', None, msg)
    # data = read_csv('test.csv')
    # print(data)
