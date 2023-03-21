import os

def listupFile(log, folder_path, ext_type='xml', filter = None):
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

def writeFile(filepath, msg):
    with open(filepath, 'wt', encoding='utf8') as f:
        f.writelines(msg)

def readFile(filepath):
    data = None
    with open(filepath, 'rt', encoding='utf8', newline='\n') as f:
        data = f.readlines()
    return data


if __name__ == '__main__':
    import jw_log
    log, logErr = jw_log.jw_make_logger('File Lib Test')
    fileList = listupFile(log, '.', 'print')
    data = readFile(fileList[0]['path'])
    print(data[0])