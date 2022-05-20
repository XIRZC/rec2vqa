from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


channel_layer = get_channel_layer()

def log_to_terminal(socket_id, message):
    async_to_sync(channel_layer.group_send)(
        str(socket_id),
        {
            'type': 'chat_message',
            'message': message
        }
    )

