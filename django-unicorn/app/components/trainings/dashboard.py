from django_unicorn.components import LocationUpdate, UnicornView, QuerySetType
from django.shortcuts import redirect
from django.contrib import messages
from app.models import Book

from enum import Enum
import copy

class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class TaskStatus(Enum):
    TODO = "↗"
    IN_PROGRESS = "~"
    IN_VALIDATION = "..."
    ON_HOLD = "|"
    COMPLETED = "✓"
    STOPPED = "✗"
    WHEN_FREE = "☴"


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
    trainings = None

    def mount(self):        
        self.trainings = [{
            "course": {
                "title": "LANCER ET MONÉTISER UNE CHAÎNE YOUTUBE",
                "status_text": "",
                "sessions": [{
                    "title": "Introduction",
                    "status_text": "Prérequis: Créer votre email - In text format, medias to do...",
                    "preparation": TaskStatus.IN_PROGRESS.value,
                    "course_media_raw": TaskStatus.TODO.value,
                    "course_media_final": TaskStatus.TODO.value,
                    "course_media_validated": TaskStatus.TODO.value,
                    "implemented_in_app": TaskStatus.TODO.value,
                    "ready_for_whats_and_gram": TaskStatus.TODO.value,
                    "in_sales_funnel": TaskStatus.TODO.value,
                }, {
                    "title": "Stratégie",
                    "status_text": "In text format, medias to do...",
                    "preparation": TaskStatus.IN_PROGRESS.value,
                    "course_media_raw": TaskStatus.TODO.value,
                    "course_media_final": TaskStatus.TODO.value,
                    "course_media_validated": TaskStatus.TODO.value,
                    "implemented_in_app": TaskStatus.TODO.value,
                    "ready_for_whats_and_gram": TaskStatus.TODO.value,
                    "in_sales_funnel": TaskStatus.TODO.value,
                }, {
                    "title": "Chaîne Youtube - Metas",
                    "status_text": "",
                    "preparation": TaskStatus.COMPLETED.value,
                    "course_media_raw": TaskStatus.IN_VALIDATION.value,
                    "course_media_final": TaskStatus.TODO.value,
                    "course_media_validated": TaskStatus.TODO.value,
                    "implemented_in_app": TaskStatus.TODO.value,
                    "ready_for_whats_and_gram": TaskStatus.TODO.value,
                    "in_sales_funnel": TaskStatus.TODO.value,
                }, {
                    "title": "1ère Vidéo",
                    "status_text": "",
                    "preparation": TaskStatus.COMPLETED.value,
                    "course_media_raw": TaskStatus.IN_VALIDATION.value,
                    "course_media_final": TaskStatus.TODO.value,
                    "course_media_validated": TaskStatus.TODO.value,
                    "implemented_in_app": TaskStatus.TODO.value,
                    "ready_for_whats_and_gram": TaskStatus.TODO.value,
                    "in_sales_funnel": TaskStatus.TODO.value,
                }, {
                    "title": "Publication",
                    "status_text": "",
                    "preparation": TaskStatus.COMPLETED.value,
                    "course_media_raw": TaskStatus.IN_VALIDATION.value,
                    "course_media_final": TaskStatus.TODO.value,
                    "course_media_validated": TaskStatus.TODO.value,
                    "implemented_in_app": TaskStatus.TODO.value,
                    "ready_for_whats_and_gram": TaskStatus.TODO.value,
                    "in_sales_funnel": TaskStatus.TODO.value,
                }, {
                    "title": "Votre chaîne",
                    "status_text": "",
                    "preparation": TaskStatus.COMPLETED.value,
                    "course_media_raw": TaskStatus.IN_VALIDATION.value,
                    "course_media_final": TaskStatus.TODO.value,
                    "course_media_validated": TaskStatus.TODO.value,
                    "implemented_in_app": TaskStatus.TODO.value,
                    "ready_for_whats_and_gram": TaskStatus.TODO.value,
                    "in_sales_funnel": TaskStatus.TODO.value,
                }, {
                    "title": "Conclusion",
                    "status_text": "",
                    "preparation": TaskStatus.COMPLETED.value,
                    "course_media_raw": TaskStatus.IN_VALIDATION.value,
                    "course_media_final": TaskStatus.TODO.value,
                    "course_media_validated": TaskStatus.TODO.value,
                    "implemented_in_app": TaskStatus.TODO.value,
                    "ready_for_whats_and_gram": TaskStatus.TODO.value,
                    "in_sales_funnel": TaskStatus.TODO.value,
                }],
            },
        }]
        self.load_table()


    def load_table(self, force_render=False):
        self.force_render = force_render

