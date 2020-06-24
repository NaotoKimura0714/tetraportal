from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from . import DBmodule
import datetime
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
#from . import utils
from app.message import Message
from . import forms
from django.contrib.auth.models import User
from .models import Todo,Room
from .forms import FileForm
from django.http import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .logUtil import logUtil


# 保存するファイル名を指定
log_folder = '{0}_chat.log'.format(datetime.date.today())
# ログの初期設定を行う
logger = logUtil.setup_logger(log_folder)

 
# チャットルーム一覧
@login_required
def rooms(request): 
    # ログを出力
    logger.debug("チャットルーム一覧画面の表示")

    # チャットルーム一覧を取得
    #chat_rooms = DBmodule.DBmodule.get_chat_room()
    chat_rooms = Room.objects.all()
    return render(request, 'app/rooms.html', {'room_list':chat_rooms}) 

# チャットルーム作成
@login_required
def make_room(request, room_name):

    # チャットルームの登録
    room_id = DBmodule.DBmodule.make_chat_room(room_name)

    # リダイレクト
    response = redirect('/chat/rooms/' + room_name + '/' + str(room_id) + '/')
    return response


# チャットルーム画面
@login_required
def room(request, room_name, room_id):

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            now_date_Time = datetime.datetime.now()
            reg_date = now_date_Time.date()
            reg_time = now_date_Time.time()
            file_path = reg_date.strftime('%Y') + '/' + reg_date.strftime('%m') + '/' + reg_date.strftime('%d') + '/' + str(room_id) + '_' + room_name + '/'
            file_name = form.name()
            download_url = form.save(file_path)


            print(download_url)
            DBmodule.DBmodule.insertMessage(room_id, request.user.id, reg_date, reg_time, file_name, 1, download_url)

            room_group_name = 'chat_%s' % (room_id)
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'chat_message',
                    'message': file_name,
                    'user_name':request.user.username,
                    'kbn':'1',
                    'file_path':download_url
                }
            )

            return HttpResponse("ファイルの送信が完了")
        else:
            return HttpResponse("ファイルの送信が失敗")
    else:

        now_date = datetime.date.today()

        #print(room_name)
        room_data = Room.objects.get(id=room_id)
        print(room_data.room_name)
        print(room_data.id)

        chatlog = DBmodule.DBmodule.getMessage(room_id,now_date)

        messageLog = list()

        for row in chatlog:
            message = Message(row[0],row[1],str(row[2]),str(row[3]),row[4],row[5],row[6])
            messageLog.append(message)

        form = FileForm()

        return render(request, 'app/room.html', {
            'form': form,
            'message_log':messageLog,
            'room_name_json': mark_safe(json.dumps(room_name)),
            'room_id_json': mark_safe(room_id),
            'room_data':room_data
        })

def delete_room(request, room_id):

    del_room = Room.objects.filter(id=room_id).delete()

    return redirect('/chat/rooms/')

@login_required
def top(request):
    # ログを出力
    logger.debug("top画面の表示")
    return render(request, 'app/top.html')


#def make_qrcode(request):
#
#    onetime_pass = utils.make_onetime_pass(request.user)
#    request.session["img"] = utils.make_qrcode(onetime_pass)
#
#    return render(request, 'app/qrcode.html')


#def ashChack(request):
#    input_pass = request.POST.get('onetime-pass-input')
#    onetime_pass = utils.make_onetime_pass(request.user)
#
#    if(utils.check_onetime_pass(onetime_pass, input_pass)):
#        # リダイレクト
#        response = redirect('/chat/top/')
#        return response
#    else:
#        # リダイレクト
#        response = redirect('/login/')
#        return response

def todo_list(request):

    #todo_list = DBmodule.DBmodule.get_todo_list(request.user.id)
    todo_list = Todo.objects.filter(user_id=request.user.id).order_by('status','scheduled_start_date')
    #print(todo_list)
    for todo in todo_list:
        print(todo.todo_name)

    return render(request, 'app/todo_list.html',{'todo_list': todo_list})

def new_todo(request):
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = forms.ToDoForm(request.POST)

        if form.is_valid():

            for ele in form :
                print(ele)

            form.save()
            return redirect('/chat/todo_list/')
        else:
            print(form.errors)
            params['message'] = form.errors
            params['form'] = form

    else:
        form = forms.ToDoForm()
        form.fields['user_id'].initial = [request.user.id]
        params['form'] = form

    print("todo新規作成")

    return render(request, 'app/todo.html', params)

def delete(request):

    return redirect('/chat/todo_list/')

def complete(request):
    return redirect('/chat/todo_list/')

def todo_wbs(request):
    return render(request,'app/todo_wbs.html')

