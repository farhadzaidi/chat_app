import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class PublicChatConsumer(WebsocketConsumer):

    # connect to websocket
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    # disconnect from websocket
    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )


    # recieve message from websocket
    def receive(self, text_data):
        message_info = json.loads(text_data)

        # forward message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_info': message_info
            }
        )

    # receive message from room group
    def chat_message(self, event):
        message_info = json.dumps(event['message_info'])

        # send message to websocket
        self.send(text_data=message_info)


class PrivateChatConsumer(WebsocketConsumer):

    # connect to websocket
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'private_chat_{self.room_name}'

        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    # disconnect from websocket
    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )


    # recieve message from websocket
    def receive(self, text_data):
        message_info = json.loads(text_data)

        # forward message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_info': message_info
            }
        )

    # receive message from room group
    def chat_message(self, event):
        message_info = json.dumps(event['message_info'])

        # send message to websocket
        self.send(text_data=message_info)
