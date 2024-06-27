import httpx, json, time, threading, random, traceback


class Tools:

    def user_id(self, user):
        headers = {'Connection': 'keep-alive','Pragma': 'no-cache','Cache-Control': 'no-cache','sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"','Accept-Language': 'en-US','sec-ch-ua-mobile': '?0','Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36','Content-Type': 'text/plain;charset=UTF-8','Client-Session-Id': '51789c1a5bf92c65','Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko','X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr','sec-ch-ua-platform': '"Windows"','Accept': '*/*','Origin': 'https://www.twitch.tv','Sec-Fetch-Site': 'same-site','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Referer': 'https://www.twitch.tv/',}
        data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
        try:
            response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
            return response.json()[0]['data']['user']['id']
        except:
            return False



class Follow:

    def __init__(self,):
        self.followed_tokens = {}

    def send_follow(self, target_id, follow_count, tokens_data):

        class Threads():
            tha = 0
            followed = 0
        
        def follow(i):
            Threads.tha = Threads.tha + 1
            
            if Threads.followed >= follow_count: return
            
            try:
                token = None; proxy = None

                for i in range(len(tokens_data)):
                    try:
                        token_id, token, token_username, proxy = random.choice(tokens_data).split("|")

                        if not token in self.followed_tokens:
                            break
                        elif not target_id in self.followed_tokens[token]:
                            break
                        else:
                            token = None
                    except:
                        pass
                if token == None:
                    return


                payload = json.dumps([
                    {
                        "operationName": "FollowUserMutation",
                        "variables": {
                        "targetId": str(target_id),
                        "disableNotifications": False
                        },
                        "extensions": {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "cd112d9483ede85fa0da514a5657141c24396efbc7bac0ea3623e839206573b8"
                        }
                        }
                    }
                    ])
                
                headers = {
                    "Api-Consumer-Type": "mobile; Android/1500000",
                    "Authorization": "OAuth " + token,
                    "Client-ID": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp",
                    "Connection": "Keep-Alive",
                    "Content-Type": "application/json",
                    "Host": "gql.twitch.tv",
                    "Transfer-Encoding": "chunked",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M) tv.twitch.android.app/15.0.0/1500000",
                    "X-APOLLO-OPERATION-NAME": "FollowUserMutation",
                    "X-App-Version": "15.0.0",
                }
                
                res = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers,proxies="http://"+proxy,timeout=40)
                print(res.text)
                
                Threads.followed = Threads.followed + 1
                
                if not token in self.followed_tokens:
                    self.followed_tokens[token] = []
                self.followed_tokens[token].append(target_id)
                

                
            except:
                traceback.print_exc()

            Threads.tha = Threads.tha - 1

        def start():
            
            count = None
            if len(tokens_data) < follow_count:
                count = len(tokens_data)
            else:
                count = follow_count
            
            for i in range(count):
                while True:
                    if Threads.followed >= count: return
                    time.sleep(0.01)
                    if Threads.tha < 20:
                        threading.Thread(
                            target=follow, args=(i,)).start()
                        break
                    else:
                        time.sleep(1)

        threading.Thread(target=start).start()









