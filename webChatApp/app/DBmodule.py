# MySQLdb をインポート
import MySQLdb
#import pymysql.cursors

class DBmodule():

    # メッセージの保存
    def insertMessage(room_no, user_id, reg_date, reg_time, message, kbn, file_path):
        # データベース接続とカーソル生成
        connection = MySQLdb.connect(
#        connection = pymysql.connect(
            host='localhost', user='chatuser', passwd='Ch@tUser0123', db='chatdb', charset='utf8')
        cursor = connection.cursor()

        try:
            # INSERT
            cursor.execute(
                "INSERT INTO message VALUES (%(room_no)s, %(user_id)s, %(regist_date)s, %(regist_time)s, %(message)s, %(kbn)s, %(file_path)s)",
                {'room_no': room_no, 'user_id': user_id, 'regist_date':reg_date, 'regist_time':reg_time, 'message':message, 'kbn':kbn, 'file_path':file_path})
        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)

        #Commit処理
        connection.commit()
        # 接続を閉じる
        connection.close()

    # 過去メッセージ取得
    def getMessage(room_no, now_date):

        # データベース接続とカーソル生成
        connection = MySQLdb.connect(
#        connection = pymysql.connect(
            host='localhost', user='chatuser', passwd='Ch@tUser0123', db='chatdb', charset='utf8')
        cursor = connection.cursor()

        # SQLの発行
        cursor.execute('select \
                            message.room_no, \
                            user.username, \
                            message.regist_date, \
                            message.regist_time, \
                            message.message, \
                            message.kbn, \
                            message.file_path \
                        from \
                            message message \
                        inner join \
                            auth_user user \
                        on \
                            message.user_id = user.id \
                        WHERE \
                            message.room_no = %(room_no)s \
                        ORDER BY \
                            regist_date ASC, regist_time ASC',
                            {'room_no':room_no})
#        for row in cursor:
#            print(row)
        result = cursor

        # 接続を閉じる
        connection.close()

        return result

    # チャットルーム登録
    def make_chat_room(room_name):

        # データベース接続とカーソル生成
        connection = MySQLdb.connect(
#        connection = pymysql.connect(
            host='localhost', user='chatuser', passwd='Ch@tUser0123', db='chatdb', charset='utf8')
        cursor = connection.cursor()

        # チャットルームの件数取得
        #cursor.execute('SELECT max(id) FROM room')
        #result = cursor.fetchall()
        #room_no = result[0][0] + 1
        #print(room_no)


        try:
            # INSERT
            cursor.execute(
#                "INSERT INTO room VALUES (%(room_no)s, %(room_name)s)",
#                {'room_no': room_no, 'room_name': room_name})
                "INSERT INTO room VALUES (null, %(room_name)s)",
                {'room_name': room_name})
        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)

        cursor.execute('select last_insert_id()')
        result = cursor.fetchall()
        room_no = result[0][0]
        print(room_no)

        #Commit処理
        connection.commit()
        # 接続を閉じる
        connection.close()

        return room_no

    # 登録されているチャットルーム一覧を取得
    def get_chat_room():

        # データベース接続とカーソル生成
        connection = MySQLdb.connect(
#        connection = pymysql.connect(
            host='localhost', user='chatuser', passwd='Ch@tUser0123', db='chatdb', charset='utf8')
        cursor = connection.cursor()

        # SQLの発行
        cursor.execute('SELECT * FROM room order by room_no ASC')
        result = cursor

        # 接続を閉じる
        connection.close()

        return result

    def get_user(user_name):

        # データベース接続とカーソル生成
        connection = MySQLdb.connect(
#        connection = pymysql.connect(
            host='localhost', user='chatuser', passwd='Ch@tUser0123', db='chatdb', charset='utf8')
        cursor = connection.cursor()

        # SQLの発行
        cursor.execute('SELECT * FROM auth_user where username = %(user_name)s',{'user_name':user_name})
        result = cursor.fetchone()

        # 接続を閉じる
        connection.close()

        return result

    def get_todo_list(user_id):

        # データベース接続とカーソル生成
        connection = MySQLdb.connect(
#        connection = pymysql.connect(
            host='localhost', user='chatuser', passwd='Ch@tUser0123', db='chatdb', charset='utf8')
        cursor = connection.cursor()

        # SQLの発行
        cursor.execute('SELECT * FROM todo where user_id = %(user_id)s order by status ASC, start_date ASC',{'user_id':user_id})
        result = cursor.fetchall()

        # 接続を閉じる
        connection.close()

        return result

