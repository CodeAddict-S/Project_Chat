from django.db import models 

# class User(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=50)

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user_1 = models.ForeignKey('users.User', related_name='chats_initiated', on_delete=models.CASCADE)
    user_2 = models.ForeignKey('users.User', related_name='chats_received', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    from_user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Message from {self.from_user} in chat {self.chat}"






    

    






