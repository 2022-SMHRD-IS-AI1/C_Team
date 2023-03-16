import zipfile
import os

def zip_folder(folder_path, output_path):
    """
    폴더를 압축하는 함수
    :param folder_path: 압축할 폴더 경로
    :param output_path: 압축 파일 경로
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

if __name__ == '__main__':
    folder_path = '/path/to/folder'
    output_path = '/path/to/output.zip'
    zip_folder(folder_path, output_path)