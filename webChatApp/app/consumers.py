from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import datetime
from . import DBmodule
from django.shortcuts import redirect
import redis
 
class ChatConsumer(WebsocketConsumer):

    # Redis に接続します
    r = redis.Redis(host='localhost', port=6379, db=0)

    #接続処理
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'chat_%s_%s' % (self.room_name , self.room_id)

        print(self.room_group_name)
        print(self.user_name)
 
        # Join room group
        #ルーム毎にグループ分け（チャンネル分け）
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # 参加者リストに追加
        self.r.sadd(self.room_group_name, self.user_name)

        message = self.user_name + 'さんが入室しました。'

        # Send message to room group
        # ルームグループに参加したことを送信
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                #'date_Time': strDateTime,
                'message': message,
                'user_name':'システムログ',
                'kbn':'0',
                'file_path':''
            }
        )

 
        self.accept()
 
    #切断処理
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        #参加者リストから削除
        self.r.srem(self.room_group_name, self.user_name)

        message = self.user_name + 'さんが退室しました。'

        # Send message to room group
        # ルームグループに参加したことを送信
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                #'date_Time': strDateTime,
                'message': message,
                'user_name':'システムログ',
                'kbn':'0',
                'file_path':''
            }
        )

 
    # Receive message from WebSocket
    # webソケットからのメッセージの受信
    # メッセージを送信した時の処理
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        #strDateTime = text_data_json['date_Time']
        message = text_data_json['message']
        now_date_Time = datetime.datetime.now()

        print("ソケットから受信")
        user = DBmodule.DBmodule.get_user(self.user_name)

        room_no = self.room_id
        user_id = user[0]
        reg_date = now_date_Time.date()
        reg_time = now_date_Time.time()


#        print('room_no:' + str(room_no) + ', user_id:' + str(user_id) + ', reg_date:' + reg_date + ', :reg_time' + reg_time)
        DBmodule.DBmodule.insertMessage(room_no,user_id,reg_date,reg_time,message,0,None)
 
        # Send message to room group
        # ルームグループに受信したメッセージを送信
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                #'date_Time': strDateTime,
                'message': message,
                'user_name':self.user_name,
                'kbn':'0',
                'file_path':''
            }
        )
 
    # Receive message from room group
    # ルームグループからのメッセージを受信
    # ルームの参加者全員の画面にメッセージを反映させる処理（開いている画面分走る）
    def chat_message(self, event):
        message = event['message']
        user_name = event['user_name']
        now_date_Time = datetime.datetime.now()
        kbn = event['kbn']
        file_path = event['file_path']

        print("ルームグループから受信")

        print(self.room_name)

        user_list_bynary = list(self.r.smembers(self.room_group_name))

        user_list = []

        # redisから取得した値はバイナリなのでUTF-8にデコード
        for data in user_list_bynary:
            user_list.append(data.decode("UTF-8"))
        print(user_list)
         
        # Send message to WebSocket
        # webソケットへ受信したメッセージの送信
        self.send(text_data=json.dumps({
            'user_name':user_name,
            'time': now_date_Time.strftime('%H:%M:%S'),
            'message': message,
            'user_list':user_list,
            'kbn':kbn,
            'file_path':file_path
        }))