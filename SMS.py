import requests

def Send(Msg):
        servicePlanId = "cb4fdf231564494eb6b1b169a1e32112"
        apiToken = "d40a02ff64f0497294e479fd76ef2bde"
        sinchNumber = "447520662174"
        toNumber = "+918367739052"
        url = "https://us.sms.api.sinch.com/xms/v1/" + servicePlanId + "/batches"

        payload = {
          "from": sinchNumber,
          "to": [
           toNumber
          ],
          "body": Msg
        }

        headers = {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + apiToken
        }

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()
        print(data)
