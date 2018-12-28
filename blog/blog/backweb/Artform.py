
from django import forms


class AddArtForm(forms.Form):
    title = forms.CharField(min_length=3, required=True, error_messages={
        'required': '文章标题不能为空',
        'min_length': '文章标题不能少于三个字符',
    })
    desc = forms.CharField(min_length=5, required=True,
                           error_messages={
                               'required': '文章描述不能为空',
                               'min_length': '文章描述不能少于五个字符',
                           })
    content = forms.CharField(required=True, error_messages={
                                  'required': '文章内容不能为空',
                              })
    icon = forms.ImageField(required=False)
    # icon = forms.ImageField(required=True,  error_messages={
    #                               'required': '图片内容不能为空',
    #                           })
    keywords = forms.CharField(required=False)
    blogger = forms.CharField(required=False)
    publish = forms.BooleanField(required=False)


class UpdatePwd(forms.Form):
    username = forms.CharField(required=True, max_length=10, error_messages={
        'required': '用户姓名不能为空',
        'max_length': '用户名不能超过10个字符'
    })
    user = forms.CharField(required=True, max_length=10, error_messages={
        'required': '用户名不能为空',
        'max_length': '用户名不能超过20个字符'
    })
    phone = forms.CharField(required=True, max_length=11, min_length=11, error_messages={
        'required': '联系电话不能为空',
        'max_length': '联系电话为11个字符',
        'min_length': '联系电话为11个字符'
    })
    userpassword = forms.CharField(required=True, max_length=16, min_length=6, error_messages={
        'required': '密码不能为空',
        'max_length': '密码不能超过16个字符不能少于6个字符',
        'min_length': '密码不能超过16个字符不能少于6个字符'
    })
    userpassword = forms.CharField(required=True, max_length=16, min_length=6, error_messages={
        'required': '密码不能为空',
        'max_length': '密码不能超过16个字符不能少于6个字符',
        'min_length': '密码不能超过16个字符不能少于6个字符'
    })
    new_one_password = forms.CharField(required=True, max_length=16, min_length=6, error_messages={
        'required': '密码不能为空',
        'max_length': '密码不能超过16个字符不能少于6个字符',
        'min_length': '密码不能超过16个字符不能少于6个字符'
    })
    new_tow_password = forms.CharField(required=True, max_length=16, min_length=6, error_messages={
        'required': '密码不能为空',
        'max_length': '密码不能超过16个字符不能少于6个字符',
        'min_length': '密码不能超过16个字符不能少于6个字符'
    })

