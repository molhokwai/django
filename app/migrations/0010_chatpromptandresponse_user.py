import django.db.models.deletion
from django.conf import settings
from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('app','0009_initial'),migrations.swappable_dependency(settings.AUTH_USER_MODEL)];operations=[migrations.AddField(model_name='chatpromptandresponse',name='user',field=models.ForeignKey(blank=True,editable=False,null=True,on_delete=django.db.models.deletion.CASCADE,related_name='user_chatpromptresponses',to=settings.AUTH_USER_MODEL))]