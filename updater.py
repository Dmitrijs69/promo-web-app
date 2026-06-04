import urllib.request
import xml.etree.ElementTree as ET
import json

ADMITAD_URL = "https://export.admitad.com/ru/webmaster/websites/2948626/coupons/export/?website=2948626&region=00&language=&keyword=&code=wqcqkqe6nm&user=dmitry_ivanovbaa29&format=xml&v=1"

def update_coupons():
    print("⏳ Подключаемся к базе Admitad...")
    req = urllib.request.Request(ADMITAD_URL, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        response = urllib.request.urlopen(req)
        xml_data = response.read()
    except Exception as e:
        print(f"❌ Ошибка при скачивании: {e}")
        return

    print("⚙️ Анализируем данные...")
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError:
        print("❌ Ошибка parsing XML.")
        return

    coupons_list = []

    for coupon in root.findall('.//coupon'):
        campaign = coupon.find('campaign')
        store_name = campaign.find('name').text if campaign is not None and campaign.find('name') is not None else "Магазин"
        
        promocode = coupon.find('promocode')
        promocode_text = promocode.text if promocode is not None else ""
        
        if not promocode_text or promocode_text.lower() == "не требуется":
            continue 

        name = coupon.find('name')
        title_text = name.text if name is not None else "Скидка"
        
        goto_link = coupon.find('goto_link')
        link_text = goto_link.text if goto_link is not None else ""

        coupons_list.append({
            "brand": store_name,
            "title": title_text,
            "description": "Акция от рекламодателя",
            "code": promocode_text,
            "discount": "Скидка",
            "link": link_text
        })

    if len(coupons_list) == 0:
        print("⚠️ Офферы еще на модерации. Генерируем тестовые карточки...")
        coupons_list = [
            {
                "brand": "Яндекс Еда (Тест)",
                "title": "Скидка на первый заказ",
                "description": "Проверка авто-обновления. Код скопируется, ссылка откроется!",
                "code": "YANDEX500",
                "discount": "500 руб",
                "link": "https://ya.ru"
            },
            {
                "brand": "Самокат (Тест)",
                "title": "Минус 200 руб на продукты",
                "description": "Тестовая карточка.",
                "code": "SAMOKAT200",
                "discount": "200 руб",
                "link": "https://google.com"
            }
        ]
    else:
        print(f"✅ Найдено {len(coupons_list)} активных промокодов.")

    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(coupons_list, f, ensure_ascii=False, indent=4)
        print("🎉 Файл data.json успешно обновлен!")
    except Exception as e:
        print(f"❌ Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    update_coupons()