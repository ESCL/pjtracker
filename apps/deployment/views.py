
from ..common.views.base import StandardResourceView
from .models import TimeSheet


class TimeSheetView(StandardResourceView):
    model = TimeSheet
