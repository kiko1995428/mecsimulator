import requests
import sys

def LINE_notify(message):
    url = "https://notify-api.line.me/api/notify"
    # LINE notifyのHPで自分用トークンを発行する必要あり
    token = 'JOUqsdscpOx1jTdEYNlUMuWXhAVrq4IX3X15PggjIXP'
    headers = {"Authorization" : "Bearer "+ token}

    args = sys.argv
    #message = "シミュレーション完了"
    #if args[0] == 1:
        #message =  '通常終了'
    #else :
        #message = '異常終了'
    payload = {"message" :  message}
    #print("111")
    #files = {"imageFile": open("/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/prototype_result.csv", "rb")}

    #r = requests.post(url ,headers = headers ,params=payload, files=files)
    r = requests.post(url, headers = headers, params=payload)

if __name__ == '__main__':
    main()