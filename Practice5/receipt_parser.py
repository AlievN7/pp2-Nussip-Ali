import re, json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()


#Дата, время
dateq = re.search(r"(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
if dateq:
    print(f"Дата: {dateq.group(1)}, Время: {dateq.group(2)}")


#Названия, цена
prodpr = re.findall(r"^\d+\.\n(.+)\n.*x\s+([\d\s,]+)", text, flags=re.M)
items_list = []

for item in prodpr:
    name = item[0].strip()
    price = item[1].strip()
    items_list.append({"product_name": name, "price": price})
    
    
#Способ оплаты, сумма
pay_info = re.search(r"(.+):\n([\d\s,]+)\nИТОГО:", text)
if pay_info:
    payment_method = pay_info.group(1).strip()
    total_amount = pay_info.group(2).strip()
    print(f"Метод: {payment_method}")
    print(f"Итого к оплате: {total_amount}")
    

receipt_data = {
    "date": dateq.group(1) if dateq else None,
    "time": dateq.group(2) if dateq else None,
    "payment_method": payment_method,
    "total_amount": total_amount,
    "items": items_list 
}


print(json.dumps(receipt_data, indent=4, ensure_ascii=False))