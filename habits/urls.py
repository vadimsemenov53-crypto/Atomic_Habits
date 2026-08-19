from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet

app_name = HabitsConfig.name

router = SimpleRouter()
router.register("", HabitViewSet, basename="habits_data")

urlpatterns = []

urlpatterns += router.urls
