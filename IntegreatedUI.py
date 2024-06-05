import PySimpleGUI as sg        # Inbuilt Modules
import random                   # Inbuilt Modules
import time                     # Inbuilt Modules
from Orders import Order_Number_See, Order_Number_Change    # Custom Modules
from SQL_Link import command    # Custom Modules
import Menu                     # Custom Modules
import sys
#__________________ Some Universal Variables __________________#
Password = ""            # Used for login window
connected = False        # Used for login window
Order = {}               # Used for bill and order summary
product_name = None      # Used for order maker
orderstatus="Accepted"   # Used for order status
dict_order = {'Prepearing':20,'Cooking':40,'Ready':60,"Out For Delivery":80,"Delivered":100}    # Used for order status
modes = ['Prepearing', 'Cooking', 'Ready',"Out For Delivery","Delivered"]                       # Used for order status
gif="tick.gif"
delivery="delivery.png"
# _________________ SQL Password Checker __________________#
def login_window() :
    sg.theme("DarkGrey2")
    window = sg.Window(
        "Login",
        layout = [
            [sg.Text("Enter Password")],
            [sg.In(enable_events=False, key="-Password-",password_char="*",)],
            [sg.Button("ENTER")],
            [sg.Button("Submit",visible=False,bind_return_key=True)]
        ])

    while True :
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED :
            break

        if event in ("Submit", "ENTER"):
            global connected
            connected = command("query", values["-Password-"],"Login_Password_Checker")
            if connected is not False :
                global Password
                Password = values["-Password-"]
                break

    window.close()
    return connected

login_window()

#____________________Order status_____________#
def status() :
    global modes
    orderstatus=modes[0]
    modes=modes[1:]
    if modes == [] :
        modes = ['Prepearing','Cooking','Ready',"Out For Delivery","Delivered"]
    return orderstatus

def decider():
    global dict_order
    global orderstatus
    l=[True,False,False,True,False]
    s=random.choice(l)
    if s==True:
       orderstatus=status()
       print(orderstatus)
       win["text"].update(f"Your order Status: {orderstatus}")
       win["progress_1"].update(dict_order[orderstatus])
       win["notice"].update(visible=False)
    else:
        orderstatus="lol"
        win["notice"].update(visible=True)
    return orderstatus

#__________________ MENU CREATION __________________#
Menu.create("Raj_Restaurant.csv", Password, "Raj_Restaurant")
Menu.create("Amar_Bakery.csv", Password, "Amar_Bakery")

# Executed when Login Window is closed without entering password
if connected == False :
    sys.exit()
# Kills the program

#__________________ Main Window __________________#
sg.theme("DarkGrey2")

#___ Layout 1 Variables ___#
headings = ["Name",'Ratings']
restaurants = [["Raj Restaurant","4.5☆"],["Amar Bakery","3.0☆"]] #iske liye bhi ek data chahiye

#___ Layout 2 Variables ___#
menu_heading = ["Dish",'Price','Quantity']
menu_content = [[]]

#___ Layout 4 Variables ___#
fonts = ( ('Courier New', 24,"underline bold"))
bill_heading = ["Item Name","QTY","Price","Amount"]
bill_content = []
bill_layout = [
    [sg.Text("",key = "-Customer Name-",font=("",10,"bold"),expand_x=True,justification = "centre")],
    [sg.Text("Ph.No. ",key = "-Customer Phone Number-",font=("",10,"bold"),expand_x=True,justification = "centre")],
    [sg.Text("Order:",key = "-Bill Number-")],
    [sg.Table(values=bill_content,headings=bill_heading,header_relief="RELIEF_FLAT",expand_y=True,key="-Bill Content-",justification="c",auto_size_columns=True)],
]
options=["Scan&Pay","CashOnDelivery(COD)","NetBanking"]

#___ Tab Layout Defining ___#
layout1=[    
    [sg.Text("Restaurants",size=(30,1),font=fonts,justification="centre")],
    [sg.Table(
        values=restaurants,
        headings=headings,
        auto_size_columns=True,
        display_row_numbers=False,
        enable_events=True,
        justification="center",
        enable_click_events=True,
        expand_x=True,
        col_widths=50,
        key="-Restaurant Table-",
        row_height=45,
        header_relief="RELIEF_FLAT")
    ]
]

layout2=[
    [sg.Text("Menu",font=("Cooper Black",30,"bold"),justification="center",size=(20,1))],
    [sg.Table(
        values=menu_content,
        headings=menu_heading,
        auto_size_columns=True,
        display_row_numbers=False,
        enable_events=True,
        justification="center",
        right_click_selects=True,
        expand_x=True,
        col_widths=50,
        row_height=35,
        header_relief="RELIEF_FLAT",
        change_submits=True,
        key="-Menu Table-")
    ],
    [sg.Button("-"), sg.Text("0",key="-Quantity-"), sg.Button("+"),sg.Button("CONFIRM")],
    [sg.Text("Select Atleast 1 Item To Proceed **",text_color="Red",visible=False,font=("",10,"italic"),k="-No Order-")]
]

layout3=[
    [sg.Frame("",
        [
            [sg.Text("Customer Details",justification="centre",size=(15,1),font=("Cooper Black",30,"underline"))],
            [sg.Frame("",
                [
                    [
                        sg.Text("Name:",font=("Adobe Kaiti Std R",12,"bold"),text_color="#ff668c"),
                        sg.Input(size=(50,50,),key='Name',enable_events=True,pad=((45,3), 3))
                    ],
                    [sg.Text("This field is compulsory**",text_color="Red",visible=False,font=("",10,"italic"),k="NameWarning")],
                    [
                        sg.Text("PhoneNo:",font=("Adobe Kaiti Std R",12,"bold"),text_color="#ff668c"),
                        sg.Input(size=(50,50),key='Phone',enable_events=True,pad=((20,3), 3))
                    ],
                    [sg.Text("Enter 10 Digit Number**",visible=False,font=("",10,"italic"),k="PhoneWarning",text_color="Red")],
                    [
                        sg.Text('Address:',font=("Adobe Kaiti Std R",12,"bold",),text_color="#ff668c"),
                        sg.Input(size=(50,50),key='Address',enable_events=True,pad=((29,3), 3))
                    ],
                    [sg.Text("This field is compulsory**",text_color="Red",visible=False,font=("",10,"italic"),k="AddressWarning")]
                ]
            )],
            [sg.B("Submit",bind_return_key=True)]
        ],
        expand_x=True,
        expand_y=True,
        element_justification="c"
    )]
]

layout4=[
    [sg.Text("Payment Method :",font=('Courier New', 15,"underline bold",),key="-Payment Method Specifications-",visible=False)],
    [sg.Text("Select Payment Method",font=('Courier New', 15,"underline bold",),key="-Select Payment Method-")],
    [sg.Combo(options,"---Select---",change_submits=True,enable_events=True,k='Method',visible=True),sg.B("ConfirmPayment",visible=False)],
    [sg.Text("Restaurant Name",size=(27,1),justification = "centre",font=("Adobe Caslon Pro Bold",17,"bold"),key="-Restaurant Name-",)],
    [sg.Text("Date",key="-Date-")],
    [sg.Frame(
        "Invoice",
        bill_layout,
        expand_y=True,
        font=fonts,
        title_location="n",
        relief="groove"),
        sg.Column(
            [
                [
                    sg.Push(),
                    sg.Push(),
                    sg.Image(filename="QRcode.png",visible=False,k="qrcode",expand_x=True),
                ],
                [
                    sg.Push(),
                    sg.Push(),
                    sg.Image(filename=delivery,visible=False,k="check",background_color="white")
                ],
                [
                    sg.Frame("",
                        [   
                            [sg.Button("",k="SBI",visible=False,size=(15,5),image_filename="sbi.png",button_color="white")],
                           [ sg.Button("",k="Kotak",visible=False,image_filename="kotak.png",expand_x=True,button_color="white")]
                        ],
                        visible=False,
                        k="NetFrame"
                    )
                ]
            ],
            vertical_scroll_only=True
        )
    ]  
]

OrderStatuslayout=[[sg.Frame("Check Your Order Status",[[],
    [sg.T(f"Your order Status: {orderstatus}",k="text",font=("",14))],
    [sg.ProgressBar(max_value=100,size=(20,20),k="progress_1",),sg.Image(filename=gif,k="g",visible=False,right_click_menu=['UNUSED', ['Exit']])],
    [sg.B("check current status"),sg.T("No update yet",visible=False,k="notice")],
    [sg.Button("New Order",visible=False)] ],expand_x=True,vertical_alignment="centre",font=("Adobe Caslon Pro Bold",20,'underline bold'),title_location="n",expand_y=True)]
]

#___ Tab Grouping ___#
tabGroup=[
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("Restaurants",layout1,key="TAB 0",),
                    sg.Tab("Orders",layout2,key="TAB 1",visible=False),
                    sg.Tab("CustomerDetails",layout3,key="TAB 2",visible=False),
                    sg.Tab("Bill&Payments",layout4,key="TAB 3",visible=False),
                    sg.Tab("Order Status",OrderStatuslayout,key="TAB 4",visible=False)
                ]
            ],
            title_color='lightgrey',
            tab_background_color="Black",
            selected_title_color="DarkGrey",
            selected_background_color="lightgrey"
        )
    ]
]
jm=[
   [sg.Push(), sg.T("Made With ♥ by Aman,Sam & Vishesh",font=("",5))]
    ]

FinalLayout=tabGroup+jm

#___ Window Execution ___#
win=sg.Window("FOOD ORDER ",FinalLayout)
while True:

    events,inputs=win.read(10)
    win["g"].update_animation_no_buffering(gif, time_between_frames=100)

    if events in [sg.WIN_CLOSED,"Exit"]:
            break

    #___ Payment Method Selector ___#
    if events=="Method":

        win["ConfirmPayment"].update(visible=True)

        if inputs["Method"]=="Scan&Pay":
            win["qrcode"].update(visible=True)
            win["NetFrame"].hide_row()
        else:
            win["qrcode"].update(visible=False)

        if inputs["Method"]=="NetBanking":
            win["NetFrame"].unhide_row()
            win["SBI"].unhide_row()
            win["Kotak"].unhide_row()
            win["NetFrame"].update(visible=True)
            win["Kotak"].update(visible=True)
            win["SBI"].update(visible=True)
        else:
            win["Kotak"].hide_row()
            win["SBI"].hide_row()
            win["NetFrame"].hide_row()
            win["NetFrame"].update(visible=False)
            win["Kotak"].update(visible=False)
            win["SBI"].update(visible=False)

        if inputs["Method"]=="CashOnDelivery(COD)":
            win["NetFrame"].hide_row()
            win["check"].update(visible=True)
        else:
            win["check"].update(visible=False)

        Payment_Method = inputs["Method"]

    #___ Payment Confirmation ___#
    if events=="ConfirmPayment":
        win["-Payment Method Specifications-"].update(f"Payment Method : {Payment_Method}")
        win["-Payment Method Specifications-"].update(visible=True)
        win["-Select Payment Method-"].update(visible=False)
        win["ConfirmPayment"].update(visible=False)
        win["Method"].update(visible=False)
        win["TAB 2"].update(visible=False)
        win["TAB 4"].select()

    #___ Restaurant Selector ___#
    if events=="-Restaurant Table-":

        if inputs["-Restaurant Table-"] == [0]:
            win["-Restaurant Name-"].update("Raj Restaurant")
            database = "Raj_Restaurant"
            menu = [[i[0], f"Rs. {str(i[1])} per {i[2]}", 0]
                    for i in command("select Product_Name, Price, Per from Menu", Password, database)]
            win["-Menu Table-"].update(values=menu)
            menu_content = [[i[0],i[1]] for i in command("select Product_Name, Price from Menu", Password, database)]

        if inputs["-Restaurant Table-"] == [1]:
            win["-Restaurant Name-"].update("Amar Bakery")
            database = "Amar_Bakery"
            menu = [[i[0], f"Rs. {str(i[1])} per {i[2]}", 0]
                    for i in command("select Product_Name, Price, Per from Menu", Password, database)]
            win["-Menu Table-"].update(values=menu)
            menu_content = [[i[0],i[1]] for i in command("select Product_Name, Price from Menu", Password, database)]
        
        Order_Number_Change(Order_Number_See()+1)
        order_number = Order_Number_See()
        win["-Bill Number-"].update(f"Order Number : {order_number}")
        command(
            f"create table order{order_number}(Product_Name varchar(30), Price int, Quantity int, Amount int)",
            Password, database=database)

        win["TAB 1"].select()
        now=1

    #___ Menu Item Selector ___#
    if events == "-Menu Table-" and inputs["-Menu Table-"] != [] :

        product_name = menu_content[inputs["-Menu Table-"][0]][0]
        product_price = menu_content[inputs["-Menu Table-"][0]][1]

        if product_name in Order :
            win["-Quantity-"].update(f"{Order[product_name]}")
        else :
            win["-Quantity-"].update('0')

    #___ Order Maker ___#
    if events in ["-", "+"] :
        
        if product_name == None :
            continue

        if events == "+" :
            if product_name not in Order :
                command(
                    f"insert into order{order_number} values('{product_name}', {product_price},1,{product_price})",
                    Password, database
                    )
                Order[product_name] = 1
            else :
                command(
                    f"update order{order_number} set quantity = quantity + 1, amount = price * quantity where product_name = '{product_name}'",
                    Password, database
                    )
                Order[product_name] += 1

        if events == "-" :
            if product_name in Order and Order[product_name] > 1 :
                command(
                    f"update order{order_number} set quantity = quantity - 1, amount = price * quantity where product_name = '{product_name}'",
                    Password, database
                    )
                Order[product_name] -= 1
            elif product_name in Order and Order[product_name] <= 1 :
                command(
                    f"delete from order{order_number} where product_name = '{product_name}'",
                    Password, database
                    )
                Order.pop(product_name)

        if product_name in Order :
            win["-Quantity-"].update(f"{Order[product_name]}")
        else :
            win["-Quantity-"].update('0')

        menu = [
            [i[0], f"Rs. {str(i[1])} per {i[2]}", Order[i[0]]] 
            if i[0] in Order else [i[0], f"Rs. {str(i[1])} per {i[2]}", 0]
            for i in command("select Product_Name, Price, Per from Menu", Password, database)
        ]
        win["-Menu Table-"].update(values = menu )

        if len(Order) != 0 :
            win["-No Order-"].update(visible=False)

    #___ Confirm Order ___#
    if events == "CONFIRM" :

        if len(Order) == 0 :
            win["-No Order-"].update(visible=True)
            continue
        
        Order_Summary = command(f"select Product_Name, Quantity, Price, Amount from order{order_number}", Password, database)
        summary_list = []

        for i in Order_Summary:
            summary_list.append(list(i))
            Total = command(f"select sum(amount) from order{order_number}",Password,database)
        summary_list.extend([[],["Total","","",Total[0][0]]])

        Table=[
            [sg.Table(
                headings=["Name", "Quantity","Rate", "Amount"],
                values = summary_list,
                justification="c",
                auto_size_columns=True)],
            [sg.Button("Confirm")],
            [sg.Button("Cancel")]
        ]

        window2=sg.Window('Order Summary',Table,keep_on_top=True)
        while True:
            
            events, values = window2.read()
            if events in [sg.WIN_CLOSED,"Cancel"]:
                break
            if events=="Confirm":
                sg.popup("Order Saved Succesfully",keep_on_top=True)
                win["TAB 2"].select()
                win["TAB 0"].update(visible=False)
                win["TAB 1"].update(visible=False)
                break

        window2.close()

    #___ CUSTOMER DETAILS ___#
    if events=="Phone" :
        if inputs["Phone"][-1] not in '1,2,3,4,5,6,7,8,9,0':
            win["Phone"].update('')
        if len(inputs["Phone"])>10 or (len(inputs["Phone"]))<10:
            if len(inputs["Phone"])>10:
                win["Phone"].update(inputs["Phone"][:10])
            win["PhoneWarning"].update(visible= True)
            win["Phone"].update(text_color="Black")
        if len(inputs["Phone"])==10:
            win["PhoneWarning"].hide_row()
            win["Phone"].update(text_color="Green")
    
                
    if events=="Submit" and inputs["Address"]=="" and inputs["Name"]=="" :

        if inputs["Name"]=="":
            win["NameWarning"].update(visible=True)
        else:
            win["NameWarning"].hide_row()
            
        if inputs["Phone"]=="":
            win["PhoneWarning"].update(visible=True)
        else:
            win["PhoneWarning"].hide_row()

        if inputs["Address"]=="":
            win["AddressWarning"].update(visible=True)
        else:
            win["AddressWarning"].hide_row()

        
    if events=="Submit" and inputs["Address"]!="" and inputs["Name"]!="" :
        Date=time.asctime().split()
        win["-Customer Phone Number-"].update(f"Ph.No. {inputs['Phone']}")
        win["-Date-"].update(f"{Date[2]} {Date[1]} {Date[-1]}")
        win["-Bill Content-"].update(values = summary_list)
        win["-Customer Name-"].update(inputs["Name"])
        win["NameWarning"].hide_row()
        win["PhoneWarning"].hide_row()
        win["AddressWarning"].hide_row()
        win["TAB 2"].update(visible=False)
        win["TAB 3"].select()
    
    #___ Order Status ___#
    if events=="check current status":
        O_status = decider()
        if O_status == "Delivered" :
            win["check current status"].update(visible = False)
            win["g"].update(visible=True)
            win["New Order"].update(visible = True)

    #___ New Order ___#
    if events == "New Order" :

        Order = {}

        win["progress_1"].update(0)
        win["Address"].update("")
        win["Phone"].update("")
        win["Name"].update("")
        win["TAB 0"].select()
        win["g"].update(visible=False)
        win["-Quantity-"].update('0')
        win["-Select Payment Method-"].update(visible=True)
        win["check current status"].update(visible = True)
        win["Method"].update(visible=True)
        win["ConfirmPayment"].update(visible=True)
        win["-Payment Method Specifications-"].update(visible=False)
        win["New Order"].update(visible = False)
        win["TAB 3"].update(visible=False)
        win["TAB 4"].update(visible=False)

win.close()
