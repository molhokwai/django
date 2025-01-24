from django_unicorn.components import LocationUpdate, UnicornView, QuerySetType
from django.shortcuts import redirect
from django.contrib import messages
from app.models import TrainingCourse, TrainingCourseSession, TaskStatus 

from enum import Enum
import copy

class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class DashboardView(UnicornView):
    """
        Description
        +    **FORMATIONS** (from _# 6261-06-21 | Mekher_)
            *    Faire une page de présentation des cours dans le style de Xyoos pour les 4, 5 cours à réaliser, sous forme de tableau pour les cours et sessions avec ces colonnes:
                +    Admin
                    -    cours | session, préparation, vidéo brute, vidéo finie, vidéo validée, implémenté dans l'application, prêt pour Whatsapp/Telegram, mis en vente (funnel)
                    -    User:
                        *    Table heading: cours
                        *    Table rows sessions
                            +    session
                                -    Free → Link to view (voir) _(sample session, bases for all)_ → light green button
                                -    Purchase → Link to view (voir) → light blue button

                    -    Voir avec les tableaux en place: https://docs.google.com/spreadsheets/d/1k0dP5f6zx9z-wVUzIvUNk3BCDHL6Xg1IkueYMOfkMso/edit?gid=298468324#gid=298468324
                    -    blurred / readonly for non admins if asset not completed
                +    Tech:
                    -    w tailwind, on @django-unicorn
                    -    Then plain html for Shopify, or shopify/liquid blocks...?

    """
    training_courses = TrainingCourse.objects.none()

    def mount(self):
        """
            Static data:
                self.trainings = [{
                    "course": {
                        "key": 1,
                        "title": "LANCER ET MONÉTISER UNE CHAÎNE YOUTUBE",
                        "status_text": "Dossier: <a href='https://drive.google.com/drive/folders/1lqATEDM4Xkmp5ZOjnbqbF_Nfz7gB_mya' target='_blank'>en ligne</a>",
                        "sessions": [
                            {
                                "title": "Introduction",
                                "status_text": "Prérequis: Créer votre email - In text format, medias to do...",
                                "preparation": TaskStatus.IN_PROGRESS,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Stratégie",
                                "status_text": "In text format, medias to do...",
                                "preparation": TaskStatus.IN_PROGRESS,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Chaîne Youtube - Metas",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "1ère Vidéo",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Publication",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Votre chaîne",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Conclusion",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }
                        ],
                    },

                    "course": {
                        "key": 2,
                        "title": "TRAINING A PROJECT MANAGER",
                        "status_text": "Dossier: <a href='https://drive.google.com/drive/u/1/folders/187MK2EMs1QjRtLgDvHnAbTFe6qU4VXBU' target='_blank'>en ligne</a>",
                        "sessions": [
                            {
                                "title": "Introduction",
                                "status_text": "Prérequis: Créer votre email - In text format, medias to do...",
                                "preparation": TaskStatus.IN_PROGRESS,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Réunions (en ligne), outils & techniques",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Chaîne Youtube - Metas",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "1ère Vidéo",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Publication",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Votre chaîne",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Conclusion",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }
                        ],
                    },
                }]

        """
        self.task_statuses = dict(zip(TaskStatus.names, TaskStatus.values))
        print(TaskStatus.__dict__.keys())
        # print(TaskStatus.map)

        self.fields = {
            "training_course":
                [f.name for f in TrainingCourse._meta.get_fields()],
            "training_course_session_":
                [f.name for f in TrainingCourseSession._meta.get_fields()],
        }
        self.load_table(force_render=True)


    def load_table(self, force_render=False):
        tcourses = TrainingCourse.objects.all().order_by("created_on")

        self.training_courses = []
        for tcourse in tcourses:
            tsessions = []
            for tsession in tcourse.trainingcoursesession_set.all():
                tsession.set_choices_display()
                tsessions.append(tsession)
                # check:
                # ----
                # for f in TrainingCourseSession._meta.get_fields():
                #     print(getattr(tsession, f.name))

            tcourse.computed_trainingcoursesessions = tsessions
            self.training_courses.append(tcourse)

        self.force_render = force_render

