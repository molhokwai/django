_A='chatpromptandresponse'
from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('app','0011_chatpromptandresponse_think')];operations=[migrations.RemoveField(model_name=_A,name='user'),migrations.AddField(model_name=_A,name='user_id',field=models.IntegerField(blank=True,editable=False,null=True))]