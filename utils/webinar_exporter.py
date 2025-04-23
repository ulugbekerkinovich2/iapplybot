import data
import json
from datetime import datetime
import pandas as pd
from pathlib import Path
from aiogram import Bot
from data.config import ADMINS # ID lar shu yerda bo‘lsin

DATA_DIR = Path("data")
WEBINAR_JSON_PATH = DATA_DIR / "webinar_users.json"
EXCEL_EXPORT_PATH = DATA_DIR / "webinar_export.xlsx"

def export_webinar_to_excel():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    users_by_country = {
        "italy": "Abdurakhmon Jumanazarov & Shohjahon Jonmirzayev",
        "usa": "Mahliyo Shavkatova",
        "turkey": "Gulbanu Turganbaeva",
        "nordic": "Shohjahon Jonmirzayev",
        "hungary": "Sarvinoz Yusupova",
        "germany": "Adhambek Yashnarbekov",
        "korea": "Begoyim Bekmirzaeva"
    }
    if WEBINAR_JSON_PATH.exists():
        with open(WEBINAR_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        for country, details in data.items():
            try:
                dt = datetime.fromisoformat(details.get("datetime"))
                date_str = dt.strftime("%d.%m.%Y")
                time_str = dt.strftime("%H:%M")
            except:
                continue

            for user in details.get("users", []):
                rows.append({
                    "Mentors": users_by_country.get(country, "Unknown"),
                    "Country": country.upper(),
                    "Webinar date": date_str,
                    "Webinar time": time_str,
                    "Full name": user.get("fullname", ""),
                    "Phone number": user.get("phone", ""),
                    "Degree": user.get("degree", "").capitalize(),
                    "Telegram ID": f"@{user.get('username', 'Not available')}"
                })

    df = pd.DataFrame(rows)
    with pd.ExcelWriter(EXCEL_EXPORT_PATH, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="Webinar Registration", index=False)
        worksheet = writer.sheets["Webinar Registration"]
        worksheet.cell(row=len(df) + 2, column=1).value = f"Last update: {datetime.now().strftime('%d.%m.%Y %H:%M')}"




EXCEL_EXPORT_PATH = Path("data/webinar_export.xlsx")

async def send_webinar_excel(bot: Bot):
    export_webinar_to_excel()  # 📦 Avval faylni yaratamiz

    for admin_id in ADMINS:
        try:
            await bot.send_document(
                chat_id=admin_id,
                document=EXCEL_EXPORT_PATH.open("rb"),
                caption="📊 Webinar ro'yxati eksport qilindi."
            )
            print(f"✅ Excel file sent to {admin_id}")
        except Exception as e:
            print(f"❌ Error sending to {admin_id}: {e}")
