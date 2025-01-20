from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import Signup,Managedata,Desktopdata,HistoryField
from math import ceil

filter = APIRouter()

templates = Jinja2Templates(directory="templates")


@filter.get('/laptopid')
async def loginid(request:Request):
    form_data=request.query_params
    loginid=form_data.get('search_element').upper()
    total_systems=Managedata.objects(laptopid__icontains=loginid)
    assign_data=Managedata.objects(status="Assigned",laptopid__icontains=loginid)
    issue_data=Managedata.objects(status="Issue",laptopid__icontains=loginid)
    unassign_data=Managedata.objects(status="Unassigned",laptopid__icontains=loginid)
    content={
        'request':request,
        'total_systems':len(total_systems),
        'assign_data':len(assign_data),
        'data':total_systems,
        'issue_data':len(issue_data),
        'unassign_data':len(unassign_data),
        'search_element':loginid
    }
    return templates.TemplateResponse('dashboard.html',content)



@filter.get('/name_filter')
async def name_filter(request:Request):
    form_data=request.query_params
    loginid=form_data.get('search_element').upper()
    total_systems=Managedata.objects(name__icontains=loginid)
    assign_data=Managedata.objects(status="Assigned",name__icontains=loginid)
    issue_data=Managedata.objects(status="Issue",name__icontains=loginid)
    unassign_data=Managedata.objects(status="Unassigned",name__icontains=loginid)
    content={
        'request':request,
        'total_systems':len(total_systems),
        'assign_data':len(assign_data),
        'data':total_systems,
        'issue_data':len(issue_data),
        'unassign_data':len(unassign_data),
        "search_element1":loginid
    }
    return templates.TemplateResponse('dashboard.html',content)









#history filter
def error_function(request):
    users=HistoryField.objects()
    page = 1
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = ceil(len(users) / per_page)
    paginated_data = users[start:end]
    content= {
        "start":start,
        "total_pages": total_pages,
        "request":request,
        'data':paginated_data
    }
    return templates.TemplateResponse('history.html',content)


@filter.get('/history')
async def history(request:Request):
    return error_function(request)


@filter.get('/history_laptopid')
async def loginid(request:Request):
    form_data=request.query_params
    loginid=form_data.get('search_element').upper()
    data=HistoryField.objects(laptopid__icontains=loginid)
    content = {
        'request': request,
        'data':data
        
    }
    return templates.TemplateResponse('history.html',content)




@filter.get('/history_name_filter')
async def name_filter(request:Request):
    form_data=request.query_params
    loginid=form_data.get('search_element').upper()
    data=HistoryField.objects(name__icontains=loginid)
    content = {
        'request': request,
         'data':data
        
    }
    return templates.TemplateResponse('history.html',content)




@filter.get('/pagination1/{page_num}',response_class=HTMLResponse)
async def pagination(page_num:int,request:Request):
    user=HistoryField.objects()
    page = page_num
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = ceil(len(user) / per_page)
    paginated_data = user[start:end]
    content= {
        "start":start,
        "total_pages": total_pages,
        "request":request,
        'data':paginated_data
    }
    return templates.TemplateResponse('history.html',content)