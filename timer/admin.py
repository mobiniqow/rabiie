from django.contrib import admin
from django import forms
from .models import DeviceTimer


# فرم سفارشی برای نمایش روزها به صورت چک‌باکس
class DeviceTimerForm(forms.ModelForm):
    DAYS_OF_WEEK = [
        ("0", "شنبه"),
        ("1", "یکشنبه"),
        ("2", "دوشنبه"),
        ("3", "سه‌شنبه"),
        ("4", "چهارشنبه"),
        ("5", "پنج‌شنبه"),
        ("6", "جمعه"),
    ]

    days_display = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        label="روزهای فعال",
        required=True,
    )

    class Meta:
        model = DeviceTimer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DeviceTimerForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # تبدیل string 0 و 1 به لیست ایندکس‌ها
            self.initial['days_display'] = [
                str(i) for i, val in enumerate(self.instance.days) if val == "1"
            ]

    def clean(self):
        cleaned_data = super().clean()
        days_list = cleaned_data.get("days_display")
        if not days_list or len(days_list) == 0:
            raise forms.ValidationError("حداقل یک روز باید انتخاب شود.")

        days_str = "".join("1" if str(i) in days_list else "0" for i in range(7))
        cleaned_data["days"] = days_str
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        days_list = self.cleaned_data.get("days_display", [])
        instance.days = "".join("1" if str(i) in days_list else "0" for i in range(7))
        if commit:
            instance.save()
        return instance


@admin.register(DeviceTimer)
class DeviceTimerAdmin(admin.ModelAdmin):
    form = DeviceTimerForm
    list_display = (
        "id",
        "user",
        "is_active",
        "relay_port_number",
        "start_time",
        "end_time",
        "get_days_display",
        "created_at",
    )
    list_filter = ("is_active", "relay10", "relay6", "created_at", "updated_at")
    search_fields = ("user__first_name", "relay_port_number")
    readonly_fields = ("created_at", "updated_at")

    def get_days_display(self, obj):
        days_map = ["ش", "ی", "د", "س", "چ", "پ", "ج"]
        return "، ".join([days_map[i] for i in range(7) if obj.days[i] == "1"])
    get_days_display.short_description = "روزهای فعال"
