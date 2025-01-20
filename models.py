from mongoengine import Document,connect,StringField,EmailField,IntField,DateField,DateTimeField,ReferenceField
import mongoengine

connect('dashboard',host="mongodb+srv://dattisai02:Dkumar02@cluster0.efrhv.mongodb.net/",ssl=True)


class Signup(Document):
    name=StringField()
    email=StringField()
    password=StringField()
    role=StringField()
    reason=StringField()
    status=StringField(default="Active")
    Date=DateTimeField()



class Managedata(Document):
    laptopid=StringField(unique=True)
    name=StringField()
    serial_no=StringField(unique=True)
    product=StringField()
    configuration=StringField()
    received_by=StringField(default=None)
    date=StringField(default=None)
    status=StringField()


class Issue_data(Document):
    managedataId=ReferenceField(Managedata)
    laptopid=StringField()
    name=StringField()
    serial_no=StringField()
    issue=StringField()
    date=StringField()
    status=StringField()


class Logfiles_data(Document):
    loginid=ReferenceField(Signup)
    date=DateTimeField()


class Super_admin(Document):
    email=StringField()
    password=StringField()



class Desktopdata(Document):
    desktopid=StringField(unique=True)
    deviceid=StringField()
    productid=StringField(unique=True)
    manufacturer=StringField()
    model=StringField()
    configuration=StringField()
    name=StringField()
    date=StringField(default=None)
    status=StringField()


class Desktopissue_data(Document):
    desktopdataid=ReferenceField(Desktopdata)
    desktopid=StringField()
    productid=StringField()
    name=StringField()
    issue=StringField()
    date=StringField(default=None)
    status=StringField()



class HistoryField(Document):
    desktopdataid=ReferenceField(Desktopdata)
    laptopdataid=ReferenceField(Managedata)
    desktopid=StringField()
    laptopid=StringField()
    name=StringField()
    admin=StringField()
    action=StringField()
    updated_date=StringField()
    received_date=StringField()
    received_by=StringField()

    