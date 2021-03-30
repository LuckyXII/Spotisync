from tortoise.models import Model
from tortoise import fields

class LinkedLists(Model):
    sync_from = fields.TextField(null=False)
    sync_to = fields.TextField(null=False)
    last_synced = fields.DateField(null=False, default='1992-01-01')


    class Meta:
            table='LinkedList'
            unique_together=(("sync_from", "sync_to") )

    def __str__(self):
        return self.name


class User(Model):
    client_id = fields.TextField(pk=True, null=False)
    client_secret = fields.TextField(null=False)
    client_username = fields.TextField(null=True, default=None)

    
    class Meta:
            table='User'
            unique_together=(("client_id", "client_secret") )
    
    def __str__(self):
        return self.name