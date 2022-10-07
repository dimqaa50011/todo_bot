from datetime import datetime


class CustomFormatters:
    @classmethod
    async def dedline_format(self, text: str):
        dedline_date, dedline_time = text.strip().split(" ")
        dedline_date = dedline_date.replace(",", ".").replace("/", ".")
        dedline_time = dedline_time.replace(".", ":").replace(",", ":")

        dedline = datetime.strptime(f"{dedline_date}.{datetime.now().year} {dedline_time}", "%d.%m.%Y %H:%M")
        return dedline
