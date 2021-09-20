from django.forms import ClearableFileInput, NumberInput, Select, DateInput


class CFI(ClearableFileInput):
    template_name = 'widgets/customCFI.html'

class Price(NumberInput):
    template_name = 'widgets/price.html'

class Percent(NumberInput):
    template_name = 'widgets/percent.html'

class SelectAssistant(Select):
    template_name = 'widgets/select_assistant.html'
    option_template_name = 'widgets/select_assistant_option.html'

class DatePicker(DateInput):
    template_name = 'widgets/datepicker.html'