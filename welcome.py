import mysql.connector as connector

amount = 0
price = {'Rice': 60, 'Wheat': 45, 'Barley': 100, 'Maize': 50, 'Oats': 40}
up_pw = {'Divya':'laxmi','Karthigayinee':'karthi','Dheeksha':'dheeksha'}

mydb = connector.connect(host='localhost', user='root', passwd='')
boo = mydb.cursor()


def insertion():
    name = input('Enter name: ')
    product = input('Enter product name: ').capitalize()
    qty = int(input('Enter quantity: '))
    boo.execute(f"select quantity from visible where product='{product}'")
    a=boo.fetchall()
    if a==None or len(a) == 0:
        boo.execute(f"insert into visible (product,quantity,price) values('{product}',{qty},{price[product]})")
    else:
        newqty=int(a[0][0])+qty
        boo.execute(f"update visible set quantity={newqty} where product='{product}'")

    boo.execute(f"insert into internal (name,product,quantity) values('{name}','{product}',{qty})")
    mydb.commit()
    print('Thank you\nLets stay connected\nKindly continue your beloved service\n')


def order():
    print('Products available: ')
    print('(S.no, Product, Qty, Price)')
    boo.execute("select * from visible")
    data=boo.fetchall()
    printing(data)
    global amount
    ans = 'y'
    amount = 0
    while ans.lower() == 'y':
        product1 = input('Enter product name: ').capitalize()
        boo.execute(f"select quantity from visible where product='{product1}'")
        available=boo.fetchall()
        if len(available) == 0:
            print('unavailable')
        else:
            qty1 = int(input('Enter quantity: '))
            if available[0][0]<qty1:
                print('Sorry Available quantity is: ',qty1)
            boo.execute(f"insert into new (product,quantity,price) values ('{product1}',{qty1},{price[product1] * qty1})")
            boo.execute(f"insert into placed_orders (product,quantity,price) values ('{product1}',{qty1},{price[product1] * qty1})")
            amount = amount + price[product1] * qty1
            updation((int(available[0][0])-qty1),product1)
        ans = input('Continue ordering "y" or "n": ')
        mydb.commit()

    print('ITEMS PURCHASED: ')
    boo.execute("select product,quantity,price from new")
    display = boo.fetchall()
    printing(display)
    print()

    boo.execute('delete from new')
    mydb.commit()


def confirm(i):
    global amount
    if i == '2':
        print('Market price is: ',amount)
        print()
        amount = amount - (amount * 0.2)
        print('Dear customer PDS will be getting a discount of 20% !!!')
        print('Total amount to be paid is: ', amount)
    elif i == '3':
        print('Market price is: ', amount)
        amount = amount - (amount * 0.1)
        print('Dear customer NGO will be getting a discount of 10% !!!')
        print('Total amount to be paid is: ', amount)
    else:
        print('Total amount to be paid is: ', amount)
    print('Dear customer confirm your order...')
    confirmation = input('Enter confirmation- "y" or "n": ')
    print()
    if confirmation.lower() == 'y':
        customer = input('Enter your name: ')
        phone = input('Enter your Phone number: ')
        boo.execute(f"insert into orders (name,phone_number) values ('{customer}','{phone}')")
        print('Order placed successfully')
        print('Collect at venue: PALANGANATHAM (warehouse)')
        print('Date : Within two days\nTime: 9.00am to 4.00pm')
        print('Thankyou visit again!')
        mydb.commit()
    else:
        pass


def updation(newqty,product1):

    boo.execute(f"update visible set quantity={newqty} where product='{product1}'")
    mydb.commit()


def check():
    print('Yes have a look!')
    boo.execute("select * from visible")
    x1 = boo.fetchall()
    boo.execute("select * from internal")
    x2 = boo.fetchall()
    boo.execute("select * from orders")
    x3 = boo.fetchall()
    boo.execute("select * from placed_orders")
    x4= boo.fetchall()

    print('Visible table:')
    printing(x1)
    print('Internal table:')
    printing(x2)
    print('Orders table:')
    printing(x3)
    print('Placed_orders: ')
    printing(x4)


def descc():
    print('Yes have a look!')
    boo.execute("desc visible")
    y1 = boo.fetchall()
    boo.execute("desc internal")
    y2 = boo.fetchall()
    boo.execute("desc orders")
    y3 = boo.fetchall()
    print('Visible table:')
    printing(y1)
    print('Internal table:')
    printing(y2)
    print('Orders table:')
    printing(y3)


def printing(var):
    for row in var:
        print(row)


def main():
    boo.execute("use farmportal")
    boo.execute('create table if not exists internal(S_no integer auto_increment,Name char(25),Product char(20),Quantity integer,primary key(S_no))')
    boo.execute('create table if not exists visible (S_no integer auto_increment,Product char(25),Quantity integer,price integer,primary key(S_no))')
    boo.execute('create table if not exists orders (S_no integer auto_increment,Name char(25),Phone_number char(10),primary key(S_no))')
    boo.execute('create table if not exists new (S_no integer auto_increment,Product char(25),Quantity integer,price integer,primary key(S_no))')
    boo.execute('create table if not exists placed_orders (S_no integer auto_increment,Product char(25),Quantity integer,price integer,primary key(S_no))')
    print("Welcome to the farm portal!")
    print("A Co-operative initiative from the farmers")
    print("Everyone working together for the greater working of all!")
    print()

    while (True):
        print('Opt Your choice here: ')
        print('     1)Farmer')
        print('     2)PDS')
        print('     3)NGO')
        print('     4)Wholesale')
        print('     5)Admin')
        print('     6)EXIT')
        i = input('Which category do you belong to: ')

        if i == '1':
            insertion()

        elif i == '2' or i == '3' or i == '4':
            order()
            confirm(i)

        elif i == '5':
            up=input('Enter user name: ')
            if up in up_pw:
                pw=input('Enter password: ')
                if up_pw[up]==pw:
                    print('a)Checking\nb)Manage')
                    choicee = input('Enter a or b: ')
                    if choicee == 'a':
                        check()
                    else:
                        descc()
                else:
                    print('Incorrect password')
            else:
                print("Invalid username !!!")
        else:
            print('Good bye!...Come again!')
            return


if __name__ == '__main__':
    main()