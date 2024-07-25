import os
import requests



class Oanda_client:

    def __init__(self):
        self.oanda_api_key = os.getenv('OANDA_API_KEY')
        self.oanda_acc_id=os.getenv('OANDA_ACC_ID')
    def get_price(self,instrument):


        # Oanda API endpoint for fetching the current price of an instrument
        url = f"https://api-fxpractice.oanda.com/v3/accounts/{self.oanda_acc_id}/pricing?instruments={instrument}"

        # Headers including the authorization token
        headers = {
            "Authorization": f"Bearer {self.oanda_api_key}",
        }

        # Make the request to Oanda API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            prices = data.get('prices', [])
            if prices:
                current_price = prices[0]
                bid = current_price.get('bids', [{}])[0].get('price')
                ask = current_price.get('asks', [{}])[0].get('price')

                return {"status_code": response.status_code,
                        "message": "Price requested successfully",
                        "data":
                            {"instrument":instrument,
                            "bid_price":bid,
                            "ask_price":ask}
                        }
        else:
            return {"status_code":response.status_code,
                    "message":response.text,
                    "data":{}
                    }


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    oanda=Oanda_client()
    response=oanda.get_price('US30_USD')

    if response['status_code']==200:
        print(f"{response['message']}, {response['data']['bid_price']},{response['data']['ask_price']}")
    else:
        print(f"{response['message']}")