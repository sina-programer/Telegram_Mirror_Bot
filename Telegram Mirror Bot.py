from time import sleep
from json import loads                               
from urllib.request import urlopen         
from urllib.parse import quote, unquote 

class Bot:
    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot{}/'.format(token)
    
    def start(self, delay=3):
        if self.check_token():
            while True:        
                if self.check_update():
                    self.message  = self.updates['result'][0]['message'] 
                    self.chat_id = str(self.message['chat']['id'])
                    
                    if 'text' in self.message:
                        self.send_message()   
                    else:
                        self.offset()
                
                sleep(delay)
                
        else:
            print('token is invalid')
    
    def send_message(self):
        message  = self.set_message()
        resp = urlopen(self.url + 'sendMessage?chat_id={}&text={}'.format(self.chat_id, message))
        check = loads(self.decode_utf8(resp)) 
        if check['ok']:
            self.offset()   
            
    def set_message(self):
        txt  = quote(self.message['text'].encode('utf-8'))
        return txt
            
    def offset(self):
        update_id = self.updates['result'][0]['update_id'] 
        urlopen(self.url + 'getUpdates?offset={}'.format(update_id + 1))
        
    def check_update(self):
        self.updates = loads(self.decode_utf8(urlopen(self.url + 'getUpdates')))                                  
        state  = len(self.updates['result'])  
        return state

    def check_token(self):
        result = loads(self.decode_utf8(urlopen(self.url + 'getme')))
        state = result['ok'] and result['result']['is_bot']
        return state
    
    def decode_utf8(self, resp):
        decoded = ''
        for line in resp:
            decoded += line.decode('utf-8')
        return decoded
    
    
TOKEN = 'your token'

if __name__ == "__main__":
    bot = Bot(TOKEN)
    bot.start()
