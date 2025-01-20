from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import Desktopdata,Desktopissue_data,HistoryField,Logfiles_data
from math import ceil
from bson import ObjectId
from datetime import datetime
from time import time
from mongoengine.errors import NotUniqueError

desktop = APIRouter()

templates = Jinja2Templates(directory="templates")

users=Logfiles_data.objects.order_by("-id")[0]

@desktop.get('/desktop_dashboard')
async def desktop_dashboard(request:Request):
    
    total_systems = Desktopdata.objects()
    assign_data = Desktopdata.objects(status="Assigned")
    issue_data = Desktopdata.objects(status="Issue")
    unassign_data = Desktopdata.objects(status="Unassigned")

 

    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': total_systems,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    
    }

    return templates.TemplateResponse('desktop_dashboard.html',content)

@desktop.post('/desktop_add_systems', response_class=HTMLResponse)
async def handle_desktop_add_systems(request: Request):
    # Extracting form data
    form_data = await request.form()
    desktopid = form_data.get('desktopid', '').upper()
    deviceid = form_data.get('deviceid', '').upper()
    productid = form_data.get('productid', '').upper()
    name = form_data.get('name', '').upper()
    manufacturer = form_data.get('manufacturer', '')
    model = form_data.get('model', '')
    configuration = form_data.get('configuration', '')
    date = form_data.get('date', '')
    status = form_data.get('status', '')
    required_fields=[desktopid,deviceid,productid,manufacturer,model,configuration,date,status]
    if(not all(required_fields)):
        message="Please enter valid fields.."
        return templates.TemplateResponse('desktop_dashboard.html', {'request': request, 'message': message})
    

    # Check for existing records
    if Desktopdata.objects(desktopid=desktopid).first():
        message = "Desktop ID already exists..."
        return templates.TemplateResponse('desktop_dashboard.html', {'request': request, 'message': message})

    if Desktopdata.objects(productid=productid).first():
        message = "Product ID already exists..."
        return templates.TemplateResponse('desktop_dashboard.html', {'request': request, 'message': message})

    try:
        # Save the desktop data
        Desktopdata(
            desktopid=desktopid,
            deviceid=deviceid,
            productid=productid,
            name=name,
            manufacturer=manufacturer,
            model=model,
            configuration=configuration,
            date=date,
            status=status
        ).save()

        # Save the history record
        HistoryField(
            laptopid=desktopid,
            name=name,
            action="Create",
            admin=users.loginid.name,
            updated_date=date,
            received_by='Rama Krishna sir',
            received_date=date
        ).save()

        # Update unassigned desktops
        Desktopdata.objects(name='').update(status="Unassigned")

    except NotUniqueError as e:
        # Handle unique constraint violations
        message = f"Error saving data: {str(e)}"
        return templates.TemplateResponse('desktop_dashboard.html', {'request': request, 'message': message})

    except Exception as e:
        # General exception handling
        message = f"Unexpected error: {str(e)}"
        return templates.TemplateResponse('desktop_dashboard.html', {'request': request, 'message': message})

    # Fetch data for the dashboard
    total_systems = Desktopdata.objects()
    assign_data = Desktopdata.objects(status="Assigned")
    issue_data = Desktopdata.objects(status="Issue")
    unassign_data = Desktopdata.objects(status="Unassigned")

    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': total_systems,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }

    return templates.TemplateResponse('desktop_dashboard.html', content)



@desktop.get("/dasktop_assign_systems", response_class=HTMLResponse)
async def desktop_assign_systems(request: Request):

    total_systems = Desktopdata.objects()
    assign_data = Desktopdata.objects(status="Assigned")
    issue_data = Desktopdata.objects(status="Issue")
    unassign_data = Desktopdata.objects(status="Unassigned")


    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': assign_data,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('desktop_dashboard.html', content)






@desktop.get("/dasktop_issue_systems", response_class=HTMLResponse)
async def desktop_issue_systems(request: Request):

    total_systems = Desktopdata.objects()
    assign_data = Desktopdata.objects(status="Assigned")
    issue_data = Desktopdata.objects(status="Issue")
    unassign_data = Desktopdata.objects(status="Unassigned")

  
    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': issue_data,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('desktop_dashboard.html', content)







@desktop.get("/dasktop_unassign_systems", response_class=HTMLResponse)
async def desktop_unassign_systems(request: Request):
   
    total_systems = Desktopdata.objects()
    assign_data = Desktopdata.objects(status="Assigned")
    issue_data = Desktopdata.objects(status="Issue")
    unassign_data = Desktopdata.objects(status="Unassigned")


    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': unassign_data,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('desktop_dashboard.html', content)






@desktop.get("/desktop_total_systems", response_class=HTMLResponse)
async def desktop_total_systems(request: Request):
    total_systems = Desktopdata.objects()
    assign_data = Desktopdata.objects(status="Assigned")
    issue_data = Desktopdata.objects(status="Issue")
    unassign_data = Desktopdata.objects(status="Unassigned")

    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': total_systems,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('desktop_dashboard.html', content)



# desktop edit delete and issue data 








@desktop.post('/desktop_edit_data/{data_id}', response_class=HTMLResponse)
async def handle_desktop_systems(data_id,request: Request): 
    form_data = await request.form()
    desktopid = form_data.get('desktopid').upper()
    deviceid = form_data.get('deviceid').upper()
    productid = form_data.get('productid').upper()
    name = form_data.get('name').upper()
    manufacturer = form_data.get('manufacturer')
    model = form_data.get('model')
    configuration = form_data.get('configuration')
    date = form_data.get('date')
    status = form_data.get('status')
    required_fields=[desktopid,deviceid,productid,manufacturer,model,configuration,date,status]
    if(not all(required_fields)):
        message="Please enter valid fields.."
        return templates.TemplateResponse('desktop_dashboard.html', {'request': request, 'message': message})
    data=Desktopdata.objects(id=data_id).first()
    if data:
        receive=Desktopdata.objects(id=data_id).first()
        HistoryField(
        desktopdataid=data_id,
        laptopid=desktopid,
        name=name,
        action="Edit",
        admin=users.loginid.name,
        updated_date=date,
        received_by='Rama Krishna sir',
        received_date=receive.date
        ).save()
        data.update(
        desktopid=desktopid,
        deviceid=deviceid,
        productid=productid,
        name=name,
        manufacturer=manufacturer,
        model=model,
        configuration=configuration,
        status=status
        )
        



    name_empty=Desktopdata.objects(name='')
    if name_empty:
        name_empty.update(status="Unassigned")
    data1=Desktopissue_data.objects(desktopid=desktopid,productid=productid)
    if data1:
        data.update(status="Issue")


   
    total_systems = Desktopdata.objects()
    assign_data = Desktopdata.objects(status="Assigned")
    issue_data = Desktopdata.objects(status="Issue")
    unassign_data = Desktopdata.objects(status="Unassigned")

    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': total_systems,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('desktop_dashboard.html', content)



#issue data 
def error_function(request):
    users=Desktopissue_data.objects()
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
    return templates.TemplateResponse('desktop_issues.html',content)


@desktop.get('/desktop_issue')
async def desktop_report_page(request:Request):
    return error_function(request)

@desktop.post('/desktop_issue/{data_id}')
async def issue_data(data_id,request:Request):
    form_data = await request.form()
    desktopid = form_data.get('desktopid').upper()
    productid=form_data.get('deviceid').upper()
    name = form_data.get('name').upper()
    issue = form_data.get('issue')
    date = form_data.get('date')
    status = form_data.get('status')
    required_fields=[desktopid,productid,name,issue,date,status]
    if(not all(required_fields)):
        message="Please enter valid fields.."
        return templates.TemplateResponse('desktop_dashboard.html', {'request': request, 'message': message})
    data=Desktopissue_data.objects(desktopid=desktopid,productid=productid)
    if data:
        message="already this System is present in issue data..."
        return templates.TemplateResponse('desktop_dashboard.html',{'request':request,'message':message})

    receive=Desktopdata.objects(id=data_id).first()
    HistoryField(
        desktopdataid=data_id,
        laptopid=desktopid,
        name=name,
        action="Issue",
        admin=users.loginid.name,
        updated_date=date,
        received_by='Rama Krishna sir',
        received_date=receive.date
    ).save()
    Desktopissue_data(desktopid=desktopid,
               desktopdataid=data_id,
               name=name,
               productid=productid,
               issue=issue,
               date=date,
               status=status).save()
    
    
    data=Desktopdata.objects(id=data_id).first()
    if data:
        data.update(status="Issue")


    total_systems = Desktopdata.objects()
    assign_data = Desktopdata.objects(status="Assigned")
    issue_data = Desktopdata.objects(status="Issue")
    unassign_data = Desktopdata.objects(status="Unassigned")

    content = {
        'request': request,
        'total_systems': len(total_systems),
        'assign_data': len(assign_data),
        'data': total_systems,
        'issue_data': len(issue_data),
        'unassign_data': len(unassign_data)
    }
    return templates.TemplateResponse('desktop_dashboard.html',content)



@desktop.get('/desktop_delete_issue/{data_id}')
async def delete_issue(data_id: str, request: Request):
    first = Desktopissue_data.objects(id=data_id).first()
    if first:
        Desktopdata_data = first.desktopdataid 
        HistoryField(
        desktopdataid=data_id,
        laptopid=first.desktopid,
        name=first.name,
        action="Delete",
        admin=users.loginid.name,
        updated_date=first.date,
        received_by='Rama Krishna sir',
        received_date=Desktopdata_data.date
        ).save()
        if Desktopdata_data:
            Desktopdata_data.delete()
    
    Desktopissue_data.objects(id=data_id).delete()

    return error_function(request)




@desktop.post('/desktop_update_laptop_issue_data/{data_id}')
async def desktop_update_laptop_issue_data(data_id,request:Request):
    form_data = await request.form()
    desktopid = form_data.get('desktopid').upper()
    deviceid = form_data.get('deviceid').upper()
    productid = form_data.get('productid').upper()
    name = form_data.get('name').upper()
    manufacturer = form_data.get('manufacturer')
    model = form_data.get('model')
    configuration = form_data.get('configuration')
    date = form_data.get('date')
    status = form_data.get('status')
    required_fields=[desktopid,deviceid,productid,manufacturer,model,configuration,date,status]
    if(not all(required_fields)):
        message="Please enter valid fields.."
        return templates.TemplateResponse('desktop_issues.html', {'request': request, 'message': message})
    update_data=Desktopissue_data.objects(id=data_id).first()
    if update_data:
        managedata=update_data.desktopdataid
        if managedata and status != "Issue":
            HistoryField(
                desktopdataid=data_id,
                laptopid=desktopid,
                name=name,
                action="Updated issue data",
                admin=users.loginid.name,
                updated_date=date,
                received_by='Rama Krishna sir',
                received_date=managedata.date
            ).save()
            managedata.update(status=status,desktopid=desktopid,deviceid=deviceid,productid=productid,name=name,manufacturer=manufacturer,model=model,configuration=configuration)
            
            update_data.delete()
    return error_function(request)









# desktop filters




@desktop.get('/desktop_desktopid')
async def desktop_loginid(request:Request):
    form_data=request.query_params
    loginid=form_data.get('search_element').upper()
    total_systems=Desktopdata.objects(desktopid__icontains=loginid)
    assign_data=Desktopdata.objects(status="Assigned",desktopid__icontains=loginid)
    issue_data=Desktopdata.objects(status="Issue",desktopid__icontains=loginid)
    unassign_data=Desktopdata.objects(status="Unassigned",desktopid__icontains=loginid)
    content={
        'request':request,
        'total_systems':len(total_systems),
        'assign_data':len(assign_data),
        'data':total_systems,
        'issue_data':len(issue_data),
        'unassign_data':len(unassign_data),
        'search_element':loginid
    }
    return templates.TemplateResponse('desktop_dashboard.html',content)



@desktop.get('/desktop_name_filter')
async def desktop_name_filter(request:Request):
    form_data=request.query_params
    loginid=form_data.get('search_element').upper()
    total_systems=Desktopdata.objects(name__icontains=loginid)
    assign_data=Desktopdata.objects(status="Assigned",name__icontains=loginid)
    issue_data=Desktopdata.objects(status="Issue",name__icontains=loginid)
    unassign_data=Desktopdata.objects(status="Unassigned",name__icontains=loginid)
    content={
        'request':request,
        'total_systems':len(total_systems),
        'assign_data':len(assign_data),
        'data':total_systems,
        'issue_data':len(issue_data),
        'unassign_data':len(unassign_data),
        "search_element1":loginid
    }
    return templates.TemplateResponse('desktop_dashboard.html',content)




# pagenation data



@desktop.get('/pagination_desktop_issue/{page_num}',response_class=HTMLResponse)
async def pagination(page_num:int,request:Request):
    user=Desktopissue_data.objects()
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
    return templates.TemplateResponse('desktop_issues.html',content)
