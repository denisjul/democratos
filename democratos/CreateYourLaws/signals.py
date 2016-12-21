from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from CreateYourLaws.models import Question, Explaination, Proposition
from CreateYourLaws.models import Disclaim, Opinion, LawArticle
from CreateYourLaws.models import Note  # UserSession,
from django.contrib.auth.signals import user_logged_in, user_logged_out


@receiver(post_delete, sender=Proposition)
@receiver(post_save, sender=Proposition)
@receiver(post_delete, sender=Opinion)
@receiver(post_save, sender=Opinion)
@receiver(post_delete, sender=Disclaim)
@receiver(post_save, sender=Disclaim)
@receiver(post_delete, sender=Explaination)
@receiver(post_save, sender=Explaination)
@receiver(post_delete, sender=Question)
@receiver(post_save, sender=Question)
def autoset(sender, instance, **kwargs):
    parent = instance.content_object
    print(parent, '     ', instance, '     ', instance.id)
    parent.nb_q = parent.questions.count()
    parent.nb_exp = parent.explainations.count()
    if type(parent) is not Question:
        if ((type(parent) is not LawArticle) and
                (type(parent) is not Proposition)):
            parent.nb_dis = parent.disclaims.count()
        else:
            parent.nb_negop = parent.opinions.filter(
                positive=False).count()  # A tester
            parent.nb_posop = parent.opinions.filter(
                positive=True).count()  # Idem
            if type(parent) is LawArticle:
                parent.nb_prop = parent.propositions.count()
    parent.save()


""" OBSOLETE ???
@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    user_sessions = UserSession.objects.filter(user=user)
    print(user_sessions)
    for user_session in user_sessions:
        try:
            user_session.session.delete()
        except:
            pass
        user_session.delete()
    UserSession.objects.get_or_create(
        user=user,
        session_id=request.session.session_key
    )


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    user_sessions = UserSession.objects.filter(user=user)
    for user_session in user_sessions:
        user_session.session.delete()
        user_session.delete()"""


@receiver(post_delete, sender=Note)
@receiver(post_save, sender=Note)
def update_approbation(sender, instance, **kwargs):
    """Update the approval ratio and factor of
     a reflexion each time a models.Note is maid """
    obj = instance.content_object
    obj.up = obj.notes.filter(approve=True).count()
    obj.down = obj.notes.filter(approve=False).count()
    obj.approval_factor = obj.up - obj.down
    try:
        obj.approval_ratio = 100 * \
            (obj.approval_factor / (obj.notes.all().count()))
    except Exception:
        obj.approval_ratio = 0
    obj.save()
