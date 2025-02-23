_A='webscrape'
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from.import views
urlpatterns=[path('',views.index,name='webscraping'),path(_A,views.webscrape,name=_A),path('webscrape/data',views.webscrape_data,name='webscrape_data'),path('webscrape/export_output_to_csv/task/<str:task_run_id>',views.export_output_to_csv,name='webscrape_export_taskoutput_to_csv'),path('webscrape/export_output_to_csv/data/<int:data_id>',views.export_output_to_csv,name='webscrape_export_dataoutput_to_csv')]