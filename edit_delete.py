from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import Signup,Managedata,Issue_data,HistoryField,Logfiles_data
from bson import ObjectId
from math import ceil

edit = APIRouter()

templates = Jinja2Templates(directory="templates")


users=Logfiles_data.objects.order_by("-id")[0]


def error_function(request):
    users=Issue_data.objects()
    page = 1
    per_page = 5
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
    return templates.TemplateResponse('report_issue.html',content)

@edit.post('/edit_data/{data_id}', response_class=HTMLResponse)
async def handle_edit_systems(data_id,request: Request): 
    form_data = await request.form()
    laptopid = form_data.get('laptopid').upper()
    name = form_data.get('name').upper()
    serial_no = form_data.get('serial_no')
    product = form_data.get('product')
    configuration = form_data.get('configuration')
    date = form_data.get('date')
    status = form_data.get('status')
    data=Managedata.objects(id=data_id).first()
    required_fields=[laptopid,serial_no,product,configuration,date,status]
    if data:
        if(not all(required_fields)):
            message="Please enter valid fields.."
            return templates.TemplateResponse('dashboard.html', {'request': request, 'message': message})
        receive=Managedata.objects(id=data_id).first()
        HistoryField(
        laptopdataid=data_id,
        laptopid=laptopid,
        name=name,
        action="Edit",
        admin=users.loginid.name,
        updated_date=date,
        received_by=receive.received_by,
        received_date=receive.date
        ).save()
        data.update(
        laptopid=laptopid,
        name=name,
        serial_no=serial_no,
        product=product,
        configuration=configuration,
        status=status
        )
        

    name_empty=Managedata.objects(name='')
    if name_empty:
        name_empty.update(status="Unassigned")
    data1=Issue_data.objects(laptopid=laptopid,serial_no=serial_no)
    if data1:
        data.update(status="Issue")


   
    total_systems = Managedata.objects()
    assign_data = Managedata.objects(status="Assigned")
    issue_data = Managedata.objects(status="Issue")
    unassign_data = Managedata.objects(status="Unassigned")

    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': total_systems,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('dashboard.html', content)


@edit.get('/issue')
async def report_page(request:Request):
    return error_function(request)

@edit.post('/issue/{data_id}')
async def issue_data(data_id,request:Request):
    form_data = await request.form()
    laptopid = form_data.get('laptopid').upper()
    name = form_data.get('name').upper()
    serial_no = form_data.get('serial_no')
    issue = form_data.get('issue')
    date = form_data.get('date')
    status = form_data.get('status')
    required_fields=[laptopid,name,serial_no,issue,date,status]
    data=Issue_data.objects(laptopid=laptopid,serial_no=serial_no).first()
    if data:
        message="already this System is present in issue data..."
        return templates.TemplateResponse('dashboard.html',{'request':request,'message':message})
    if(not all(required_fields)):
            message="Please enter valid fields.."
            return templates.TemplateResponse('dashboard.html', {'request': request, 'message': message})

    receive=Managedata.objects(id=data_id).first()
    HistoryField(
        laptopdataid=data_id,
        laptopid=laptopid,
        name=name,
        action="Issue",
        admin=users.loginid.name,
        updated_date=date,
        received_by=receive.received_by,
        received_date=receive.date
        ).save()
    Issue_data(laptopid=laptopid,
               managedataId=data_id,
               name=name,
               serial_no=serial_no,
               issue=issue,
               date=date,
               status=status).save()
    
    
    
    data=Managedata.objects(id=data_id).first()
    if data:
        data.update(status="Issue")


    total_systems = Managedata.objects()
    assign_data = Managedata.objects(status="Assigned")
    issue_data = Managedata.objects(status="Issue")
    unassign_data = Managedata.objects(status="Unassigned")

    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': total_systems,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('dashboard.html',content)



@edit.get('/delete_issue/{data_id}')
async def delete_issue(data_id: str, request: Request):
    first = Issue_data.objects(id=data_id).first()
    if first:
        managedata_data = first.managedataId
        HistoryField(
        laptopdataid=data_id,
        laptopid=first.laptopid,
        name=first.name,
        action="Delete",
        admin=users.loginid.name,
        updated_date=first.date,
        received_by=managedata_data.received_by,
        received_date=managedata_data.date
        ).save()
        if managedata_data:
            managedata_data.delete()
    
    Issue_data.objects(id=data_id).delete()

    return error_function(request)



@edit.post('/update_laptop_issue_data/{data_id}')
async def update_laptop_issue_data(data_id,request:Request):
    form_data = await request.form()
    laptopid = form_data.get('laptopid').upper()
    name = form_data.get('name').upper()
    serial_no = form_data.get('serial_no')
    product = form_data.get('product')
    configuration = form_data.get('configuration')
    date = form_data.get('date')
    status = form_data.get('status')
    required_fields=[laptopid,name,serial_no,product,configuration,date,status]
    if(not all(required_fields)):
        message="Please enter valid fields.."
        return templates.TemplateResponse('report_issue.html', {'request': request, 'message': message})
    update_data=Issue_data.objects(id=data_id).first()
    if update_data:
        managedata=update_data.managedataId
        if managedata and status != "Issue":
            HistoryField(
                laptopdataid=data_id,
                laptopid=laptopid,
                name=name,
                action="Update issue data",
                admin=users.loginid.name,
                updated_date=date,
                received_by=managedata.received_by,
                received_date=managedata.date
                ).save()
            managedata.update(status=status,laptopid=laptopid,name=name,serial_no=serial_no,product=product,configuration=configuration)
            
            update_data.delete()
    return error_function(request)





@edit.get('/pagination_laptop_issue/{page_num}',response_class=HTMLResponse)
async def pagination(page_num:int,request:Request):
    user=Issue_data.objects()
    page = page_num
    per_page = 5
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
    return templates.TemplateResponse('report_issue.html',content)



