from .models import SiteSetting

def preloader_setting(request):
    try:
        setting = SiteSetting.objects.first()
        return {'show_preloader': setting.show_preloader if setting else True}
    except:
        return {'show_preloader': True}
