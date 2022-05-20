import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.send({"accept": True})
        print("User connnected via Socket")
        self.accept()

    # Receive message from WebSocket
    def receive(self, text_data):
        #def ws_message(message):
        #   print "Message recieved from client side and the content is ", message.content['text']
        #   socketid = message.content['text']
        #   Group(socketid).add(message.reply_channel)
        #   log_to_terminal(socketid, {"info": "User added to the Channel Group"})

        print("Message recieved from client side and the content is ", text_data)
        socket_id = text_data
        self.socket_id = self.scope['url_route']['kwargs']['socket_id']
        async_to_sync(self.channel_layer.group_add)(
            self.socket_id,
            self.channel_name
        )
        log_to_terminal(self.socket_id, {"info": "Consumer added to the Channel Group"})

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
    }))
