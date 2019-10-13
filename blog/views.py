from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from .forms import UserRegistrationForm
import os
from excel2json import convert_from_file
import glob
import xlrd
import xlwt
import os
from os.path import abspath
import sys
import random

import xlrd
def post_list(request):
	posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
	return render(request, 'blog/post_list.html', { 'posts' : posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})
# Create your views here.
def test(request):
    return render(request, 'blog/test.html')
def home(request):
    return render(request, 'blog/home.html')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form' : form})

def upload(request):
    path = settings.MEDIA_ROOT
    files = [f for f in glob.glob(path+ "**/*.xlsx", recursive=True)]
    for f in files:
        # f=f.split('/')[-1]
        # f_path = abspath(f)
        print(f)
        # open_file(f_path)
   
    print(os.getcwd())
    context = {}
    if request.method == 'POST':
        uploaded_file=request.FILES['document']
        print(uploaded_file.name)
        fs=FileSystemStorage()
        name=fs.save(uploaded_file.name,uploaded_file)
        file_extension = os.path.splitext(name)[1]
        if(file_extension==".pdf" or file_extension==".xlsx" ):
            context['url']=fs.url(name)
        else:
            raise forms.ValidationError('Invalid file extension')
        # print(uploaded_file.name)

        # print(uploaded_file.size)
    return render(request, 'blog/test.html',context)
from collections import defaultdict
def download(request):
    con=defaultdict(list)
    fnam={}
    if request.method == 'GET':
        path = settings.MEDIA_ROOT
        files = [f for f in glob.glob(path+ "**/*.xlsx", recursive=True)]
        for f in files:
            fnam[random.randint(1,100)]=f
            # f=f.split('/')[-1]
            # f_path = abspath(f)
            print(f)
            for i in open_file(f):
                con[random.randint(1,100000)].append(i)
        context={
                "fnam":fnam,
                "cont":dict(con),
        }
    return render(request, 'blog/test2.html',context)
def open_file(path):
#     """

#     Open and read an Excel file
#     """
#     # Open the workbook
    xl_workbook = xlrd.open_workbook(path)
    
#     # List sheet names, and pull a sheet by name
#     #

####################################################################
# data = []
# keys = [v.value for v in worksheet.row(0)]
# for row_number in range(worksheet.nrows):
#     if row_number == 0:
#         continue
#     row_data = {}
#     for col_number, cell in enumerate(worksheet.row(row_number)):
#         row_data[keys[col_number]] = cell.value
#     data.append(row_data)
#####################################################################
# with open(sys.argv[3], 'w') as json_file:
#     json_file.write(json.dumps({'data': data}))

    sheet_names = xl_workbook.sheet_names()
#     print('Sheet Names', sheet_names)
    xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
    
#     # Or grab the first sheet by index 
#     #  (sheets are zero-indexed)
#     #
    xl_sheet = xl_workbook.sheet_by_index(0)
#     print ('Sheet name: %s' % xl_sheet.name)
    
#     # Pull the first row by index
#     #  (rows/columns are also zero-indexed)
#     #
    row = xl_sheet.row(0)  # 1st row
    
#     # Print 1st row values and types
#     #
    from xlrd.sheet import ctype_text   
    
#     print('(Column #) type:value')
    for idx, cell_obj in enumerate(row):
        cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
#        print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
    
#     # Print all values, iterating through rows and columns
#     #
    num_cols = xl_sheet.ncols   # Number of columns
    for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
        print ('-'*40)
        print ('Row: %s' % row_idx)   # Print row number
        for col_idx in range(0, num_cols):  # Iterate through columns
            cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            yield('Column: [%s] cell_obj: [%s]' % (col_idx, cell_obj))

        
