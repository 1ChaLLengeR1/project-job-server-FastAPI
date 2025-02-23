from fpdf import FPDF
import os
from config.app_config import DOWNLOAD, BASIC_FONT
from PIL import Image
from consumer.services.websocekt.patryk_router.pdfFilter.websocket import send_progress


def px_to_mm(px: float) -> float:
    return px * 0.2646


def truncate_text(text: str, max_width: int, pdf: FPDF, font_size: int = 8) -> str:
    pdf.set_font("CustomFont", size=font_size)
    text_width = pdf.get_string_width(text)

    if text_width <= max_width:
        return text
    truncated_text = text
    while pdf.get_string_width(truncated_text + "...") > max_width and len(truncated_text) > 1:
        truncated_text = truncated_text[:-1]

    return truncated_text + "..."


class PDF(FPDF):
    def header(self):
        self.set_font("CustomFont", size=12)
        self.cell(0, 10, "Raport produktów", ln=True, align="C")


def generate_pdf(user_id: str, data: list[dict], output_file: str) -> tuple[str, bool]:
    try:
        send_progress(user_id, 1, "Rozpoczęcie generowanie pdfa...")
        pdf = FPDF(orientation='L', unit='mm', format='A4')

        send_progress(user_id, 1, "Ładowanie fontów...")
        pdf.add_font("CustomFont", "", str(BASIC_FONT), uni=True)
        pdf.add_font("CustomFont", "B", str(BASIC_FONT), uni=True)
        pdf.add_font("CustomFont", "I", str(BASIC_FONT), uni=True)
        pdf.add_font("CustomFont", "BI", str(BASIC_FONT), uni=True)
        pdf.add_page()
        col_widths = {
            "lp": 10,
            "name": 130,
            "quantity": 10,
            "ean": 45,
            "image": 20,
            "location": 60
        }

        pdf.set_font("CustomFont", style="B", size=8)
        pdf.cell(col_widths["lp"], 10, "Lp", border=1, align="C")
        pdf.cell(col_widths["name"], 10, "Nazwa produktu", border=1, align="C")
        pdf.cell(col_widths["quantity"], 10, "Ilość", border=1, align="C")
        pdf.cell(col_widths["ean"], 10, "EAN", border=1, align="C")
        pdf.cell(col_widths["image"], 10, "Obraz", border=1, align="C")
        pdf.cell(col_widths["location"], 10, "Lokalizacja", border=1, align="C")
        pdf.ln()

        pdf.set_font("CustomFont", size=8)
        for index, row in enumerate(data, start=0):
            percent_complete = round((index + 1) / len(data) * 100, 2)
            send_progress(user_id, percent_complete, f'Tworzenie produktu: {index}')
            truncated_name = truncate_text(row.get("name", ""), max_width=125, pdf=pdf)

            pdf.cell(col_widths["lp"], 10, str(row.get("lp", "")), border=1, align="C")
            pdf.cell(col_widths["name"], 10, truncated_name, border=1)

            pdf.cell(col_widths["quantity"], 10, str(row.get("quantity", "")), border=1, align="C")
            pdf.cell(col_widths["ean"], 10, row.get("ean", ""), border=1, align="C")

            url_image = row.get("url_image", "")
            if url_image and os.path.exists(url_image):

                with Image.open(url_image) as img:
                    img_width, img_height = img.size

                img_width_mm = img_width * 0.2646
                img_height_mm = img_height * 0.2646

                max_width = col_widths["image"] - 4
                max_height = 8

                if img_width_mm > max_width:
                    scale_factor = max_width / img_width_mm
                    img_width_mm = max_width
                    img_height_mm = img_height_mm * scale_factor

                if img_height_mm > max_height:
                    scale_factor = max_height / img_height_mm
                    img_height_mm = max_height
                    img_width_mm = img_width_mm * scale_factor

                x = pdf.get_x()
                y = pdf.get_y()

                pdf.cell(col_widths["image"], 10, "", border=1)
                pdf.image(url_image, x=x + 2, y=y + 2, w=img_width_mm, h=img_height_mm)
            else:
                pdf.cell(col_widths["image"], 10, "Brak", border=1, align="C")

            pdf.cell(col_widths["location"], 10, row.get("location", "") or "", border=1, align="C")
            pdf.ln()
        send_progress(user_id, 50, f"Zakończenie tworzenia produktów...")

        output_pdf = DOWNLOAD / output_file
        pdf.output(str(output_pdf))
        print("Pdf został utworzony poprawnie!")
        return str(output_pdf), True

    except Exception as e:
        return str(e), False
