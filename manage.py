from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import Managedata,HistoryField,Logfiles_data
from math import ceil

dashboard = APIRouter()

templates = Jinja2Templates(directory="templates")

users=Logfiles_data.objects.order_by("-id")[0]


@dashboard.get("/")
async def read_dashboard(request:Request):
    return templates.TemplateResponse('login.html',{'request':request})

@dashboard.get('/add_systems', response_class=HTMLResponse)
async def add_systems(request: Request):
    return templates.TemplateResponse('manage.html', {'request': request})


@dashboard.get('/dashboard', response_class=HTMLResponse)
async def add_systems(request: Request):
    return templates.TemplateResponse('dashboard.html', {'request': request})

@dashboard.post('/add_systems', response_class=HTMLResponse)
async def handle_add_systems(request: Request): 
    form_data = await request.form()
    laptopid = form_data.get('laptopid').upper()
    name = form_data.get('name').upper()
    serial_no = form_data.get('serial_no')
    product = form_data.get('product')
    configuration = form_data.get('configuration')
    receiver = form_data.get('receiver')
    date = form_data.get('date')
    status = form_data.get('status')

    data=Managedata.objects(laptopid=laptopid)
    data1=Managedata.objects(serial_no=serial_no)
    required_fields=[laptopid,serial_no,product,configuration,receiver,date,status]


    if(data):
        message='laptopid already exits...'
        return templates.TemplateResponse('dashboard.html',{'request':request,'message':message})
    if(data1):
        message='serial number already exits...'
        return templates.TemplateResponse('dashboard.html',{'request':request,'message':message})
    if(all(required_fields)):
        Managedata(
        laptopid=laptopid,
        name=name,
        serial_no=serial_no,
        product=product,
        configuration=configuration,
        received_by=receiver,
        date=date,
        status=status
        ).save()
        HistoryField(
        laptopid=laptopid,
        name=name,
        action="Create",
        admin=users.loginid.name,
        updated_date=date,
        received_by=receiver,
        received_date=date
        ).save()
    
        name_empty=Managedata.objects(name='')
        if name_empty:
            name_empty.update(status="Unassigned")


   
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
    else:
        message="Please enter valid fields.."
        return templates.TemplateResponse('dashboard.html', {'request': request, 'message': message})



@dashboard.get("/assign_systems", response_class=HTMLResponse)
async def assign_systems(request: Request):

    total_systems = Managedata.objects()
    assign_data = Managedata.objects(status="Assigned")
    issue_data = Managedata.objects(status="Issue")
    unassign_data = Managedata.objects(status="Unassigned")


    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': assign_data,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('dashboard.html', content)






@dashboard.get("/issue_systems", response_class=HTMLResponse)
async def issue_systems(request: Request):

    total_systems = Managedata.objects()
    assign_data = Managedata.objects(status="Assigned")
    issue_data = Managedata.objects(status="Issue")
    unassign_data = Managedata.objects(status="Unassigned")

  
    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': issue_data,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('dashboard.html', content)







@dashboard.get("/unassign_systems", response_class=HTMLResponse)
async def unassign_systems(request: Request):
   
    total_systems = Managedata.objects()
    assign_data = Managedata.objects(status="Assigned")
    issue_data = Managedata.objects(status="Issue")
    unassign_data = Managedata.objects(status="Unassigned")


    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': unassign_data,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('dashboard.html', content)






@dashboard.get("/total_systems", response_class=HTMLResponse)
async def total_systems(request: Request):
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
