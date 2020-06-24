
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Todo
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

EMPTY_CHOICES = (
    ('', '-'*10),
)

STATUS_CHOICES = (
    ('0', '未実施'),
    ('1', '作業中'),
    ('2', '完了')
)

def user_choice():

    user_list = User.objects.all()
    choice1 = []
    for user_row in user_list:
        choice1.append((user_row.id,user_row.username))

    return choice1


class ToDoForm(forms.ModelForm):
    user_id = forms.ChoiceField(
        label = 'ユーザID',
        widget=forms.Select,
        choices=user_choice(),
        required=True)

    todo_name = forms.CharField(
        label='作業名',
        max_length=45,
        required=True,
        widget=forms.TextInput()
    )

    regist_date = forms.DateField(
        label='登録日',
        required=False,
        input_formats=[
            '%Y-%m-%d',  # 2010-01-01
            '%Y/%m/%d',  # 2010/01/01
        ]
    )

    remark = forms.CharField(
        label='備考',
        max_length=300,
        required=False,
        widget=forms.TextInput()
    )

    scheduled_start_date = forms.DateField(
        label='開始予定日',
        required=True,
        input_formats=[
            '%Y-%m-%d',  # 2010-01-01
            '%Y/%m/%d',  # 2010/01/01
        ]
    )

    start_date = forms.DateField(
        label='開始日',
        required=False,
        input_formats=[
            '%Y-%m-%d',  # 2010-01-01
            '%Y/%m/%d',  # 2010/01/01
        ]
    )

    expected_end_date = forms.DateField(
        label='終了予定日',
        required=True,
        input_formats=[
            '%Y-%m-%d',  # 2010-01-01
            '%Y/%m/%d',  # 2010/01/01
        ]
    )

    end_date = forms.DateField(
        label='終了日',
        required=False,
        input_formats=[
            '%Y-%m-%d',  # 2010-01-01
            '%Y/%m/%d',  # 2010/01/01
        ]
    )

    status = forms.ChoiceField(
        label='ステータス',
        widget=forms.Select,
        choices=EMPTY_CHOICES + STATUS_CHOICES,
        required=True,
    )

    class Meta:
        model = Todo
        fields = ('user_id',
                  'todo_name',
                  'regist_date',
                  'status',
                  'scheduled_start_date',
                  'expected_end_date',
                  'start_date',
                  'end_date',
                  'remark')


class FileForm(forms.Form):

    file = forms.FileField(label='ファイル')

    def save(self, file_path):
        upload_file = self.cleaned_data['file']
        print(upload_file.name)
        file_name = default_storage.save(file_path + upload_file.name, upload_file)
        return default_storage.url(file_name)

    def name(self):
        upload_file = self.cleaned_data['file']
        return upload_file.name