# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime
import json

class Account(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)

    # Field name made lowercase.
    permission = models.ForeignKey(
        'Permission', models.DO_NOTHING, db_column='PermissionID')
    # Field name made lowercase.
    username = models.CharField(
        db_column='Username', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    password = models.CharField(
        db_column='Password', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
    
    class Meta:

        db_table = 'account'


class Address(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)

    # Field name made lowercase.
    city = models.CharField(
        db_column='City', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    district = models.CharField(
        db_column='District', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    ward = models.CharField(
        db_column='Ward', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    address = models.CharField(
        db_column='Address', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.address + ', ' + self.ward + ', ' + self.district + ', ' + self.city
    class Meta:

        db_table = 'address'


class Bank(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    logo = models.CharField(
        db_column='Logo', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'bank'

    def __str__(self):
        return self.name

class Bill(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    order = models.ForeignKey(
        'Order', models.DO_NOTHING, db_column='OrderID')
    # Field name made lowercase.
    company = models.CharField(
        db_column='Company', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    tax_code = models.CharField(
        db_column='Tax_code', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    address = models.CharField(
        db_column='Address', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'bill'


class BussinessStaff(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    member = models.ForeignKey(
        'Member', models.DO_NOTHING, db_column='memberID')

    class Meta:

        db_table = 'bussiness_staff'


class Cart(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    customer = models.ForeignKey(
        'Customer', models.DO_NOTHING, db_column='CustomerID', null=True)
    # Field name made lowercase. This field type is a guess.
    is_order = models.TextField(db_column='Is_order')

    def __str__(self):
        return str(self.id)
    class Meta:

        db_table = 'cart'


class CartItem(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, db_column='CartID')
    # Field name made lowercase.
    item = models.ForeignKey('Item', models.CASCADE, db_column='ItemID')
    qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.

    class Meta:

        db_table = 'cart_item'


class Comment(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    content = models.CharField(
        db_column='Content', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    updated_date = models.DateTimeField(
        db_column='Updated_date', default=datetime.now, blank=True)

    class Meta:

        db_table = 'comment'


class Customer(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    member = models.ForeignKey(
        'Member', models.DO_NOTHING, db_column='memberID')

    def __str__(self):
        return self.member.name
    class Meta:

        db_table = 'customer'


class DeliveryAddress(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    
    # Field name made lowercase.
    address = models.ForeignKey(
        Address, models.DO_NOTHING, db_column='AddressID')
    # Field name made lowercase.
    customer = models.ForeignKey(
        Customer, models.DO_NOTHING, db_column='CustomerID')
    # Field name made lowercase.
    receiver = models.CharField(
        db_column='Receiver', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    phone = models.CharField(
        db_column='Phone', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'delivery_address'

class Discount(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    item = models.ForeignKey('Item', models.CASCADE, db_column='ItemID')
    # Field name made lowercase.
    discount_value = models.BigIntegerField(db_column='Discount_value')
    # Field name made lowercase.
    from_date = models.DateTimeField(
        db_column='From_date', blank=True, null=True)
    # Field name made lowercase.
    to_date = models.DateTimeField(db_column='To_date', blank=True, null=True)

    class Meta:

        db_table = 'discount'


class Event(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    from_date = models.DateTimeField(
        db_column='From_date', blank=True, null=True)
    # Field name made lowercase.
    to_date = models.DateTimeField(db_column='To_date', blank=True, null=True)

    class Meta:

        db_table = 'event'


class Feedback(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    customer = models.ForeignKey('Customer', models.CASCADE, db_column='CustomerID', null=True, blank=True)
    item = models.ForeignKey('Item', models.CASCADE, db_column='ItemID')
    # Field name made lowercase.
    comment = models.ForeignKey(
        Comment, models.DO_NOTHING, db_column='CommentID')
    # Field name made lowercase.
    rate_score = models.IntegerField(db_column='Rate_score')
    # Field name made lowercase.
    created_date = models.DateTimeField(
        db_column='Created_date', default=datetime.now, blank=True)

    class Meta:

        db_table = 'feedback'


class Image(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    product = models.ForeignKey(
        'Product', models.DO_NOTHING, db_column='ProductID')
    # Field name made lowercase.
    caption = models.CharField(
        db_column='Caption', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    path = models.CharField(
        db_column='Path', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'image'


class ImportFile(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    created_date = models.DateTimeField(
        db_column='Created_date', default=datetime.now, blank=True)

    class Meta:

        db_table = 'import_file'

    def __str__(self):
        return str(self.id) + ': ' + str(self.created_date)

class ImportProduct(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    product = models.ForeignKey(
        'Product', models.CASCADE, db_column='ProductID')
    # Field name made lowercase.
    import_file = models.ForeignKey(
        'ImportFile', models.DO_NOTHING, db_column='Import_fileID')
    qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.

    class Meta:

        db_table = 'import_product'

    def __str__(self):
        return str(self.product) + ': ' + str(self.qty)

class Item(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    product = models.ForeignKey(
        'Product', models.DO_NOTHING, db_column='ProductID')
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    price = models.BigIntegerField(
        db_column='Price')
    def __str__(self):
        return self.name

    class Meta:

        db_table = 'item'


class Member(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)

    account = models.ForeignKey(
        Account, models.DO_NOTHING, db_column='AccountID', null=True)

    address = models.ForeignKey(
        Address, models.DO_NOTHING, db_column='AddressID', null=True)
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    phone = models.CharField(
        db_column='Phone', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    email = models.CharField(
        db_column='Email', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    dob = models.DateField(db_column='Dob', blank=True, null=True)
    # Field name made lowercase.
    gender = models.IntegerField(db_column='Gender')
    # Field name made lowercase.
    avatar = models.CharField(
        db_column='Avatar', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
        
    class Meta:

        db_table = 'member'


class Order(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    cart = models.ForeignKey(
        'Cart', models.DO_NOTHING, db_column='CartID', null=True, blank=True)
    # Field name made lowercase.
    shipment = models.ForeignKey(
        'Shipment', models.DO_NOTHING, db_column='ShipmentID')
    payment = models.ForeignKey(
        'Payment', models.DO_NOTHING, db_column='PaymentID',null=True)

    deliveryAddress = models.ForeignKey('DeliveryAddress',models.DO_NOTHING,db_column='DeliveryAddressID', null=True, blank=True)
    # Field name made lowercase.
    created_date = models.DateTimeField(
        db_column='Created_date', default=datetime.now, blank=True)
    statusNow = models.CharField(
        db_column='Status_now', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'order'


class OrderHistory(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    member = models.ForeignKey(
        'Member', models.DO_NOTHING, db_column='MemberID',null=True)
    # Field name made lowercase.
    order = models.ForeignKey(Order, models.CASCADE, db_column='OrderID')
    # Field name made lowercase.
    status = models.CharField(
        db_column='Status', max_length=255, blank=True, null=True)
    
    # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', blank=True, null=True,auto_now_add=True)

    class Meta:

        db_table = 'order_history'


class Payment(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    paymentmethod = models.ForeignKey(
        'PaymentMethod', models.DO_NOTHING, db_column='PaymentMethodID')
    # Field name made lowercase.
   

    paymentDetail = models.ForeignKey('PaymentDetail', models.DO_NOTHING, db_column='PaymentDetailID',null=True, blank=True)

    class Meta:

        db_table = 'payment'


class PaymentDetail(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    customer_name = models.CharField(db_column='customer_name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    bank = models.ForeignKey(Bank, models.DO_NOTHING, db_column='bankID')
    # Field name made lowercase.
    card = models.CharField(
        db_column='Card', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'payment_detail'


class PaymentMethod(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    method_name = models.CharField(
        db_column='Method_name', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'payment_method'

    def __str__(self):
        return self.method_name

class PaymentmethodBank(models.Model):
    # Field name made lowercase.
    paymentmethod = models.OneToOneField(
        PaymentMethod, models.DO_NOTHING, db_column='PaymentMethodID', primary_key=True)
    # Field name made lowercase.
    bank = models.ForeignKey(Bank, models.DO_NOTHING, db_column='bankID')

    class Meta:

        db_table = 'paymentmethod_bank'
        unique_together = (('paymentmethod', 'bank'),)


class Permission(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)

    # Field name made lowercase.
    level = models.IntegerField(db_column='Level')
    # Field name made lowercase.
    description = models.CharField(
        db_column='Description', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'permission'


class Product(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    warehouse = models.ForeignKey(
        'Warehouse', models.DO_NOTHING, db_column='WarehouseID')
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)
    price = models.BigIntegerField(db_column='Price')  # Field name made lowercase.
    # Field name made lowercase.
    description = models.CharField(
        db_column='Description', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    qty_in_stock = models.IntegerField(db_column='Qty_in_stock')
    type = models.ForeignKey(
        'Type', models.DO_NOTHING, db_column='TypeID',null=True)

    class Meta:

        db_table = 'product'
    def __str__(self):
        return self.name


class Respone(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    comment = models.ForeignKey(
        Comment, models.DO_NOTHING, db_column='CommentID')
    # Field name made lowercase.
    content = models.CharField(
        db_column='Content', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    created_date = models.DateTimeField(
        db_column='Created_date', blank=True, null=True)
    # Field name made lowercase.
    updated_date = models.DateTimeField(
        db_column='Updated_date', default=datetime.now, blank=True)

    class Meta:

        db_table = 'respone'


class SalerStaff(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    member = models.ForeignKey(
        Member, models.DO_NOTHING, db_column='memberID')

    class Meta:

        db_table = 'saler_staff'


class Shipment(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    shipper = models.ForeignKey(
        'Shipper', models.DO_NOTHING, db_column='ShipperID', null=True, blank=True)
    shipmentMethod = models.ForeignKey(
        'ShipmentMethod', models.DO_NOTHING, db_column='ShipmentMethodID',null=True)

    class Meta:

        db_table = 'shipment'


class ShipmentMethod(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.

    # Field name made lowercase.
    method_name = models.CharField(
        db_column='Method_name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    duration = models.IntegerField(db_column='Duration')
    fee = models.IntegerField(db_column='Fee')  # Field name made lowercase.

    class Meta:

        db_table = 'shipment_method'


class Shipper(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    member = models.ForeignKey(
        Member, models.DO_NOTHING, db_column='memberID')

    class Meta:

        db_table = 'shipper'


class Shop(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    logo = models.CharField(
        db_column='Logo', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    address = models.CharField(
        db_column='Address', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    email = models.CharField(
        db_column='Email', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    phone = models.CharField(
        db_column='Phone', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    desc = models.CharField(
        db_column='Desc', max_length=255, blank=True, null=True)
    class Meta:

        db_table = 'shop'


class Tax(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    product = models.ForeignKey(
        Product, models.DO_NOTHING, db_column='ProductID')
    # Field name made lowercase.
    no = models.CharField(db_column='No', max_length=255,
                          blank=True, null=True)
    # Field name made lowercase.
    value = models.CharField(
        db_column='Value', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'tax'


class Policy(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    description = models.CharField(
        db_column='Description', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'policy'

class Warehouse(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    city = models.CharField(
        db_column='City', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'warehouse'

    def __str__(self):
        return self.name


class WarehouseStaff(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    import_file = models.ForeignKey(
        ImportFile, models.DO_NOTHING, db_column='Import_fileID')
    # Field name made lowercase.
    member = models.ForeignKey(
        Member, models.DO_NOTHING, db_column='memberID')

    class Meta:

        db_table = 'warehouse_staff'


class Notification(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, db_column="customerID")
    content = models.CharField(db_column='content', max_length=255, blank=True, null=True
                               )
    time = models.DateTimeField(db_column='time',default=datetime.now, null=True, blank=True)
    attach = models.CharField(db_column='attach', max_length=255, blank=True, null=True
                            )

    class Meta:

        db_table = 'notification'


class Type(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='content',
                            max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, db_column="CategoryID",null=True)

    attributes = models.ManyToManyField('Attribute',through='AttributeType')

    class Meta:

        db_table = 'type'

    def __str__(self):
        return self.name
    def toJSON(self):
        return json.dumps(self.__dict__)


class Category(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='content',
                            max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'category'
    def __str__(self):
        return self.name

class Attribute(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='name',
                            max_length=255, blank=True, null=True)
    types = models.ManyToManyField('Type',through='AttributeType')

    class Meta:

        db_table = 'attribute'
    def __str__(self):
        return self.name

class AttributeType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    type = models.ForeignKey(
        'Type', on_delete=models.CASCADE, db_column="TypeID",null=True)

    attribute = models.ForeignKey(
        'Attribute', on_delete=models.CASCADE, db_column="AttributeID",null=True)

    class Meta:

        db_table = 'attribute_type'
   
    def __str__(self):
        return  str(self.type) + ': ' +str(self.attribute)

class AttributeValue(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    attribute = models.ForeignKey(
        'Attribute', on_delete=models.CASCADE, db_column="AttributeID",null=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, db_column="ProductID",null=True)
    value = models.CharField(db_column='value',
                            max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'attribute_value'

    def __str__(self) :
        return '{' + str(self.product) + ',' + str(self.attribute) + '}' + ':' + self.value