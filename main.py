import json
import re
import FileHandler
import mail_sender
from Configurations import Public_Key, Private_Key
from API_Worker import WorkerAPI


if __name__ == '__main__':
    api_worker = WorkerAPI(public_key=Public_Key, private_key=Private_Key)
    api_worker.get_order_list()

    with open("Orders_list.json", "r", encoding="UTF-8") as file:
        orders_list = json.load(file)
    file_handler = FileHandler.FileHandler()

    for order in orders_list:
        path_to_zip = file_handler.download(order["download_link"], order["id"])
        filepath = False
        if path_to_zip:
            filepath = file_handler.unZIP(path_to_zip, order["id"])
        if filepath:
            size = re.search(r'(\d{2}x\d{2})', order["title"])
            size = size.group(0)
            shirina = size[0:2]
            visota = size[3:]
            params = {"id": order["id"],
                      "title": order["title"],
                      "shirina": int(shirina),
                      "visota": int(visota),
                      "filepath": filepath}
            params = json.dumps(params)
            mail_sender = mail_sender.MailSender()
            mail_sender.send_mail(to_email="someemail@gmail.com", subject=f'order_{order["id"]}', msg_body=params)
            api_worker.change_order_status(order["id"])