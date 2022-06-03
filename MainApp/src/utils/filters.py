class DescriptionFilter:
    @property
    def short_description(self):
        raise NotImplementedError


class ImageFilter:
    @property
    def show_display(self):
        raise NotImplementedError

    @property
    def show_field(self):
        raise NotImplementedError


class DatetimeFilter:
    @property
    def correct_datetime(self):
        raise NotImplementedError

class BaseFilter(DescriptionFilter, ImageFilter):
    pass
