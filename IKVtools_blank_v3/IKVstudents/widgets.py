from django.forms import NumberInput, Select, DateInput, SelectMultiple



class Price(NumberInput):
    template_name = 'widgets/price.html'

class SelectAssistant(Select):
    template_name = 'widgets/select_assistant.html'
    option_template_name = 'widgets/select_assistant_option.html'

class DatePicker(DateInput):
    template_name = 'widgets/datepicker.html'

class Hours(NumberInput):
    template_name = 'widgets/hours.html'

class CSM(SelectMultiple):
    template_name = 'widgets/select_assistant.html'
    option_template_name = 'widgets/select_assistant_option.html'

    class Meta:
        verbose_name = "Betreuer"
        verbose_name_plural = "Betreuer"