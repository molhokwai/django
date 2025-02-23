_B='chatpromptandresponse'
_A=True
from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('app','0012_remove_chatpromptandresponse_user_and_more')];operations=[migrations.AddField(model_name=_B,name='add_history',field=models.BooleanField(blank=_A,null=_A)),migrations.AddField(model_name=_B,name='history',field=models.TextField(blank=_A,null=_A))]