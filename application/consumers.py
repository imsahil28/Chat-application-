from django.core.exceptions import ObjectDoesNotExist   
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat.models import Profile,Message,User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.roomGroupName = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room_name = text_data_json["room_name"]
        
        await self.save_message(message, username, room_name)     

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "room_name": room_name,
            }
        )
        
    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))
    
    # @sync_to_async
    # def save_message(self, message, username, room_name):
    #    if room_name:
    #     try:
    #         room = Profile.objects.get(user=room_name)
    #         # If the profile exists, continue with further processing
    #     except ObjectDoesNotExist:
    #         # Profile doesn't exist, handle the situation accordingly
    #         # For example, you can log a message or take appropriate action
    #         print(f"Profile with user {room_name} does not exist.")
    #     else:
    #     # Handle case where room_name is empty or invalid
    #         print("Invalid room_name provided.")
    # @sync_to_async
    # def save_message(self, message, username, room_name):
    #     try:
    #         user = User.objects.get(username=username)  # Fetch the User object based on the username
    #         room = Profile.objects.get(user=room_name)  # Assuming 'user' is the field in Profile model
    #     except ObjectDoesNotExist as e:
    #         # Handle case where user or room does not exist
    #         print(f"Error occurred: {e}")
    #     else:
    #         # Both user and room exist, proceed with saving message
    #         try:
    #             Message.objects.create(user=user, room=room, content=message)
    #         except Exception as e:
    #             # Handle database operation errors
    #             print(f"Error occurred while saving message: {e}")


        
    #     Message.objects.create(user=user,room=room,content=message)
    from django.contrib.auth.models import User

    @sync_to_async
    def save_message(self, message, username, room_name):
        try:
            user = User.objects.get(username=username)  # Fetch the User object based on the username
            room = Profile.objects.get(user=user)  # Assuming 'user' is the field in Profile model
        except ObjectDoesNotExist as e:
            # Handle case where user or room does not exist
            print(f"Error occurred: {e}")
        else:
            # Both user and room exist, proceed with saving message
            try:
                Message.objects.create(user=user, room=room, content=message)
            except Exception as e:
                # Handle database operation errors
                print(f"Error occurred while saving message: {e}")
