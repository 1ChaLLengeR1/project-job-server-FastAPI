from config.app_config import FILE, TMP
import os
import zipfile
from PIL import Image
from io import BytesIO
from openpyxl import load_workbook
import re
import win32com.client as win32
import shutil
from config.app_config import CONVERT_XLS_TO_XLSX, START_LITERAL_COLUMN_FILE_XLSX


def extract_images_from_xlsx() -> tuple[list[dict], str, bool]:
    try:
        os.makedirs(TMP, exist_ok=True)
        data = []

        file_path, is_valid = file_name_find()
        if not is_valid:
            return data, file_path, False

        file_path = FILE / file_path

        with zipfile.ZipFile(file_path, 'r') as xlsx_zip:
            media_files = sorted(
                [f for f in xlsx_zip.namelist() if f.startswith('xl/media/')]
            )

            def extract_number_from_filename(filename):
                match = re.search(r'(\d+)', filename)
                return int(match.group(1)) if match else None

            for file_name in media_files:
                try:
                    image_data = xlsx_zip.read(file_name)
                    image = Image.open(BytesIO(image_data))

                    image_number = extract_number_from_filename(os.path.basename(file_name))

                    if image_number is None:
                        continue

                    image_name = f"image{image_number}.png"
                    save_path = os.path.join(TMP, image_name)

                    image.save(save_path, format='PNG')

                    new_image_obj = {
                        "index": image_number,
                        "name_file": image_name,
                        "url_image": save_path,
                    }
                    data.append(new_image_obj)
                except Exception as e:
                    print(f"Błąd przetwarzania obrazu {file_name}: {e}")

        return data, "", True

    except Exception as e:
        return [], str(e), False


def file_name_find(file_type: str = 'xlsx') -> tuple[str, bool]:
    try:
        if not os.path.isdir(FILE):
            return f"Ścieżka {FILE} nie jest folderem lub nie istnieje", False

        if file_type == 'xlsx':
            for file in os.listdir(FILE):
                if file.endswith(".xlsx"):
                    return file, True
        else:
            for file in os.listdir(FILE):
                if file.endswith(".xls"):
                    return file, True

        return "Brak plików .xlsx lub .xls w folderze", False
    except Exception as e:
        return str(e), False


def open_file_xlsx() -> tuple[list[dict], str, bool]:
    try:
        name_file, success = file_name_find()
        path = os.path.join(FILE, name_file)

        workbook = load_workbook(path)
        sheet = workbook.active

        headers = [cell.value for cell in sheet[START_LITERAL_COLUMN_FILE_XLSX - 1]]
        headers = [header.strip() for header in headers if header and isinstance(header, str)]

        data = []
        index = 1

        for row_idx, row in enumerate(sheet.iter_rows(min_row=10, values_only=True),
                                      start=START_LITERAL_COLUMN_FILE_XLSX):
            if not any(row):
                continue

            row_data = {headers[i]: row[i] for i in range(len(headers)) if i < len(row) and headers[i]}

            if row_data.get('Lp') == 'Lp':
                continue

            new_object = {
                'index': index,
                'column_excel': row_idx,
                'lp': row_data.get('Lp', ''),
                'name': row_data.get('Nazwa towaru', ''),
                'quantity': row_data.get('Ilość', ''),
                'ean': row_data.get('EAN', ''),
                'location': row_data.get('Lokalizacja', ''),
            }

            data.append(new_object)
            index += 1

        return data, "", True

    except Exception as e:
        return [], str(e), False


def clear_tmp_files(file_paths: list[str]) -> tuple[str, bool]:
    try:
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
        return "", True
    except Exception as e:
        return str(e), False


def clear_catalog(path_catalog) -> tuple[str, bool]:
    try:
        path_file_catalog = path_catalog
        if not path_file_catalog.exists():
            return "Katalog nie istnieje.", False

        for item in path_file_catalog.iterdir():
            if item.is_file() and not item.suffix == ".py":
                item.unlink()

            elif item.is_dir():
                shutil.rmtree(item)

        return "Katalog został wyczyszczony.", True

    except Exception as e:
        return str(e), False


def convert_xls_to_xlsx() -> tuple[str | None, bool]:
    try:
        if CONVERT_XLS_TO_XLSX is False:
            return None, True

        file_path, is_valid = file_name_find('xls')
        if not is_valid:
            return file_path, False

        file_path = FILE / file_path

        file_path_str = str(file_path)

        if not file_path_str.lower().endswith('.xls'):
            return "Podany plik nie ma rozszerzenia .xls", False

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(file_path.absolute())

        wb.SaveAs(str(file_path.absolute().with_suffix(".xlsx")), FileFormat=51)
        wb.Close()
        excel.Application.Quit()

        return None, True

    except Exception as e:
        return str(e), False
