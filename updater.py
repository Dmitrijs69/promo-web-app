import urllib.request
import xml.etree.ElementTree as ET
import json

# Твоя уникальная ссылка из Admitad
ADMITAD_URL = "https://export.admitad.com/ru/webmaster/websites/2948626/coupons/export/?website=2948626&region=00&language=&keyword=&code=wqcqkqe6nm&user=dmitry_ivanovbaa29&format=xml&v=1"

def update_coupons():
    print("⏳ Подключаемся к базе Admitad...")
    
    # Делаем запрос (притворяемся браузером, чтобы сервер нас не отбил)
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
        print("❌ Ошибка: Admitad вернул неверный формат данных.")
        return

    coupons_list = []

    # Проходимся по всем купонам в XML
    for coupon in root.findall('.//coupon'):
        # Ищем название магазина
        campaign = coupon.find('campaign')
        store_name = campaign.find('name').text if campaign is not None and campaign.find('name') is not None else "Неизвестный магазин"

        # Ищем сам промокод
        promocode = coupon.find('promocode')
        promocode_text = promocode.text if promocode is not None else ""
        
        # Нам нужны только реальные промокоды (отсеиваем обычные акции без кода)
        if not promocode_text or promocode_text.lower() == "не требуется":
            continue 

        # Описание скидки
        name = coupon.find('name')
        title_text = name.text if name is not None else "Скидка на заказ"
        
        # Твоя личная партнерская ссылка для заработка
        goto_link = coupon.find('goto_link')
        link_text = goto_link.text if goto_link is not None else ""

        # Упаковываем в красивый словарь
        coupons_list.append({
            "store": store_name,
            "title": title_text,
            "code": promocode_text,
            "link": link_text
        })

    print(f"✅ Найдено {len(coupons_list)} активных промокодов.")

    # Перезаписываем наш data.json
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(coupons_list, f, ensure_ascii=False, indent=4)
        print("🎉 Файл data.json успешно обновлен!")
    except Exception as e:
        print(f"❌ Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    update_coupons()