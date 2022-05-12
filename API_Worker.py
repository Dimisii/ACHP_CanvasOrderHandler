import traceback

import requests
import json
import hashlib


class WorkerAPI:

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.access_token = ""
        self.get_access_token()

    def get_access_token(self):
        request_token_url = "http://api.pixlpark.com/oauth/requesttoken"

        try:
            responce = requests.get(request_token_url)
            if responce.status_code == 200:
                requests_json = json.loads(responce.text)
                request_token = requests_json["RequestToken"]
            else:
                raise
        except Exception:
            print("Ошибка при получении requestToken")
            print(traceback.print_exc())
            return

        finally:
            responce.close()

        access_token_url = "http://api.pixlpark.com/oauth/accesstoken"
        access_token_params = {"oauth_token": request_token,
                               "grant_type": "api",
                               "username": self.public_key,
                               "password": hashlib.sha1(str(request_token + self.private_key).encode("UTF-8")).hexdigest()
                              }
        try:
            responce = requests.get(access_token_url, params=access_token_params)
            if responce.status_code == 200:
                requests_json = json.loads(responce.text)
                self.access_token = requests_json["AccessToken"]
            else:
                raise
        except Exception:
            print("Ошибка при получении accessToken" + responce.status_code)
            print(traceback.print_exc())
            return

        finally:
            responce.close()

    def get_order_list(self):
        orders_url = "http://api.pixlpark.com/orders"
        order_request_params = {"oauth_token": self.access_token,
                                "take": 40,
                                "status": "NotProcessed"  # NotProcessed
                               }
        try:
            responce = requests.get(orders_url, params=order_request_params)
            if responce.status_code == 200:
                json_orders = json.loads(responce.text)
                json_orders = json_orders["Result"]
                orders_list = []
                for item in json_orders:
                    if str(item["Title"]).count("Холсты на подрамнике") > 0:
                        orders_list.append({"id": f'{item["Id"]}',
                                            "title": f'{item["Title"]}',
                                            "download_link": f'{item["DownloadLink"]}'
                                            })
                with open("Orders_list.json", "w", encoding="UTF-8") as file:
                    json.dump(orders_list, file, indent=4, ensure_ascii=False)
                    print(file.name + " сохранен")

        except Exception:
            print(traceback.print_exc())
        finally:
            responce.close()

    def change_order_status(self, order_id):
        url = f"http://api.pixlpark.com/orders/{order_id}/status"
        params = {"oauth_token": self.access_token,
                 "newStatus": "DesignCoordinationComplete"}

        try:
            responce = requests.post(url, params=params)
            if responce.status_code == "200":
                print(f"Статус заказа {order_id} успешно изменен.")
        except:
            print(traceback.print_exc())
        finally:
            responce.close()
