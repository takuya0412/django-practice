from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Friend,Message
from .forms import FriendForm,FindForm,CheckForm,MessageForm
from django.db.models import Q
from django.db.models import Count,Sum,Avg,Min,Max
from django.core.paginator import Paginator

def index(request,num=1):
    #FriendモデルのQuerysetを全て取得
    data=Friend.objects.all()
    #pagenatorインスタンスを生成、モデルのインスタンスはdataから3つずつ取得
    page=Paginator(data,3)
    #テンプレート用の変数
    params={
        'title':'Test1',
        'message':'',
        #Paginatorの.get_pageメソッドで対象のページのFriendモデルインスタンスを取得
        'data':page.get_page(num),
    }
    #paramsの変数を使用してレンダリング
    return render(request,'test1/index.html',params)
    
#create model
def create(request):
    #POST送信された場合の処理
    if (request.method=='POST'):
        #Friendモデルのインスタンスを作成
        obj=Friend()
        #FriendモデルからのPOST送信された値をFriendインスタンスとして取得
        friend=FriendForm(request.POST,instance=obj)
        #formsのsaveメソッドでデータベースに保存
        friend.save()
        #もとのformに戻る
        return redirect(to='/test1')
    #テンプレート用変数
    params={
        'title':'Test1',
        
        'form':FriendForm(),
    }
    return render(request,'test1/create.html',params)
    
    
def edit(request,num):
    #引数numのQuerysetを取得
    obj=Friend.objects.get(id=num)
    if(request.method=='POST'):
    #Friendモデルのインスタンスにフォームから送信された値で再作成
        friend=FriendForm(request.POST,instance=obj)
        #データベースに保存
        friend.save()
        return redirect(to='/test1')
    params={
        'title':'test1',
        'id':num,
        #もともとデータベースに保存されている値がフォームに入力される
        'form':FriendForm(instance=obj),
    }
    return render(request,'test1/edit.html',params)

def delete(request,num):
    friend=Friend.objects.get(id=num)
    if (request.method=='POST'):
        #変数に格納していたモデルのインスタンスを削除する
        friend.delete()
        return redirect(to='/test1')
    params={
        'title':'test1',
        'id':num,
        'obj':friend,
    }
    return render(request,'test1/delete.html',params)
    
    
def find(request):
    if (request.method=='POST'):
        #検索欄から送信された値を変数へ格納
        msg=request.POST['find']
        form=FindForm(request.POST)
        #SQL文で操作対象のtableを指定
        sql='select * from test1_friend'
        #送信データが空じゃなければメソッドを追加する
        if (msg!=''):
            sql+=' where '+msg
        data=Friend.objects.raw(sql)
        msg=sql
    
    else:
        msg='search words...'
        form=FindForm()
        data=Friend.objects.all()
    params={
        'title':'test1',
        'message':msg,
        #送信されたデータは検索欄に残しておく
        'form':form,
        'data':data,
    }    
    return render(request,'test1/find.html',params)
    
def check(request):
    params={
        'title':'Test1',
        'message':'check validation',
        'form':FriendForm()
    }
    if (request.method=='POST'):
        obj=Friend()
        form=FriendForm(request.POST,instance=obj)
        #送信されたデータをフォームに残しておく
        params['form']=form
        #バリデーション実施
        if (form.is_valid()):
            params['message']='OK!'
        else:
            params['message']='no good.'
    return render(request,'test1/check.html',params)
    
def message(request,page=1):
    if (request.method=='POST'):
        obj=Message()
        form=MessageForm(request.POST,instance=obj)
        form.save()
        #新しい順に並べ替えてQuerysetを取得
    data=Message.objects.all().reverse()
    paginator=Paginator(data,5)
    params={
        'title':'Message',
        'form':MessageForm(),
        'data':paginator.get_page(page),
    }
    return render(request,'test1/message.html',params)
    