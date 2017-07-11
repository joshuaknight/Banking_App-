import threading
import time 
import sqlite3 
import os 

class Database:    

    def __init__(self):        
        self.initial_create()

    def initial_create(self):
     #   try:   
        conn = sqlite3.connect("test.db")                 
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Account(Account_No INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Account_Name TEXT NOT NULL,Balance INTEGER NOT NULL,Date_of_creation blob NOT NULL,
            Contact_id INTEGER,customer_id INTEGER, Account_type text,user_password BLOB NOT NULL,
            joint_account boolean,foreign key (Contact_id) references Contact(ID),
            foreign key (Customer_id) references Customer(ID));
            """
        )                              

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Contact(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            ADDRESS BLOB default NULL, Phone_no integer NOT NULL,email blob default null);
            """
        )            

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Customer(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            customer_name NOT NULL,customer_age NOT NULL,customer_gender NOT NULL);
            """
        )


        conn.commit()

        conn.close()                   

       # except sqlite3.OperationalError:            
       #    print "Table can't be created"            
            

    @staticmethod
    def save_into_database(kwargs):                
        try:
            conn = sqlite3.connect("test.db")     # connect to database              

            cur = conn.execute(                     # contact_insertion 
                """ 
                INSERT INTO Contact(address,phone_no,email)
                VALUES ('{}','{}','{}'); 
                """.format(kwargs['address'],kwargs['phone_no'],kwargs['email'])
            )      
            contact_id = cur.lastrowid  # Get contact id 

            cur = conn.execute(         #customer_insertion 
                """
                INSERT INTO Customer(customer_name,customer_age,customer_gender)
                VALUES ('{}','{}','{}');  
                """.format(kwargs['name'],kwargs['age'],kwargs['gender'])
            )      
            customer_id=cur.lastrowid   # Get customer id 
            
            if_joint = lambda x: "Yes" if x else "No"      ## joint_account_check  

            password = '^' + str(customer_id) + '_' + '#' +kwargs['account_name'] + '$'
            cur = conn.execute(               # account_insertion 
                """
                INSERT INTO Account (Account_Name,Balance,contact_id,
                customer_id,Date_of_creation,account_type,joint_account,user_password)
                VALUES ('{}','{}','{}','{}','{}','{}','{}','{}');
                """.format(kwargs['account_name']+'_'+str(customer_id),
                    kwargs['balance'],contact_id,customer_id,
                    time.strftime("%D|%H:%M:%S"),
                    kwargs['account_type'],if_joint(kwargs['joint_acc']),
                    password,
                    ),
            )     
            acc_no = cur.lastrowid        
            customer_id = ''
            contact_id = ''
            conn.commit()        
            conn.close()

            return (password,acc_no) 

        except:
            print "Error Creating Account"

    @staticmethod 
    def update_ele(ac_no,balance):        
        try:
            db = sqlite3.connect('test.db')        
            cur = db.cursor()
            cur.execute(
                """ 
                UPDATE Account 
                SET balance='{}'
                where account_no='{}'
                """.format(balance,ac_no)
            )
            db.commit()
        except:
            print "Error Updating Data"            

    @staticmethod 
    def delete_account(ac_no):
        try:
            db = sqlite3.connect('test.db')
            cur = db.cursor()
            cur.execute(
                """
                    DELETE * 
                    from account 
                    where account_no = '{}';
                """.format(ac_no)
            )
            db.commit()
        
        except:            
            print "Account Cannot Be Deleted"

    
    def __str__(self):
        return "Database is located at : {}".format(os.path.abspath('')+'/test.db') 


class NotFound_Ac(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
        


class Withdraw(threading.Thread):

    def __init__(self,ac_no,money):
        threading.Thread.__init__(self)
        self.acc_no = ac_no 
        self.money = money         
        self.money_withdrawn = False 
        self.customer = None

    def run(self):
        try:
            Account.lock.acquire()
            self.customer = Account.find_acc(self.acc_no)                                            
            self.get_money()
            Account.lock.release()
        except NotFound_Ac:
            print "Account Number does not exist"


    def get_money(self):                       
        print "{} requsted amount of ${} at {}".format(self.customer[1],
                            self.money,
                            time.strftime("%H:%M:%S"))
        if self.money - self.customer[2] > 0:
            print "Insufficent Funds"
            print "Current Balance is ${}".format(self.customer[2])
        else:
            print "Money Withdraw by {} is ${}".format(str(self.customer[1]),self.money) 
            Database.update_ele(self.acc_no,self.customer[2]-self.money)
            self.money_withdrawn = True 
            print "New Balance is {}".format(self.customer[2]-self.money)
        time.sleep(4)            


class Deposit(threading.Thread):

    def __init__(self,acc_no,money):
        threading.Thread.__init__(self)
        self.acc_no  = acc_no   
        self.money = money 
        self.customer = None 
        self.money_deposited = False 

        
    def run(self):    
        Account.lock.acquire()
        self.customer = Account.find_acc(self.acc_no)                                  
        self.add_money()
        Account.lock.release()        

    def __str__(self):
        return self.money_deposited 

    
    def add_money(self):
        try:
            if not self.customer:
                raise NotFound_Ac            
            print "Current Balance is ${} as on {}".format(self.customer[2],
                                                        time.strftime("%H:%M:%S"))

            self.customer[2] += self.money                          
            Database.update_ele(self.acc_no,self.customer[2])
            self.money_deposited = True      
            print "New Balance is ${} as on {}".format(self.customer[2],
                                                time.strftime("%H:%M:%S"))
        except NotFound_Ac:
            print "Account Not Found"
        
        except:
            print "Faulty Please try Again"
        time.sleep(3)        


class Account: 

    lock = threading.Lock()      
    def __init__(self,acc_blnc, customer_name,type_acc = "saving",joint_acc = False ):
        self.acc_name = customer_name 
        self.acc_blnc = acc_blnc 
        self.type_acc = type_acc                 
        self.joint_acc = joint_acc


    @staticmethod
    def find_acc(acc_no):       
        db= sqlite3.connect("test.db", check_same_thread=False).cursor()
        db.execute(
            """
            select * from Account 
            where account_no == '{}';
            """.format(acc_no)
        )        
        tup = db.fetchall()[0]                
        tup = list(tup)
        if tup:
            return tup
        else:
            print "Account not Found"

    @staticmethod 
    def check_password(acc_no,password):
        db= sqlite3.connect("test.db", check_same_thread=False).cursor()
        db.execute(
            """
            select account_no,user_password from Account 
            where account_no == '{}' and user_password == '{}';
            """.format(acc_no,password)
        )        
        tup = db.fetchall() 
               
        tup = list(tup)        
        if tup:
            return True 
        else:
            return False 


class Contact:

    def __init__(self,address,email,phone_no):
        self.address = address
        self.email = email 
        self.phone_no = phone_no 

class Customer:

    def __init__(self,name,age,gender):
        get_gender = lambda x : "M" if x == 1 else "F" 
        self.name = name 
        self.age  = age 
        self.gender = get_gender(gender)

class CreateAccount(Account,Contact,Customer):
    def __init__(self,lis):
        Account.__init__(self,lis[7],lis[1])        # opening_balance                               
        Contact.__init__(self,lis[4],lis[5],lis[6])  #address,email,phone_no 
        Customer.__init__(self,lis[1],lis[2],lis[3]) #name,age,gender

        self.account_created = False

        dic = {
               'name' : self.name,'age' : self.age,'gender': self.gender,
               'address' : self.address,'email' : self.email,'phone_no' : self.phone_no,
               'account_name' : self.acc_name,'balance' : self.acc_blnc,
               'account_type' : self.type_acc,'joint_acc' : self.joint_acc,
              }

        try:
            tup = Database.save_into_database(dic)
            print "A/c No : {}\nGenearated Password : {}".format(tup[1],tup[0])
            self.account_created = True 

        except:
            print "Error Creating Account"            

    def __str__(self):
        if self.account_created:
            return "Account Created"
        return "Error Creating Account"            
    
class Query:        
                     
    def __init__(self,*args):                
        self.query = args[0].lower()        
        if self.query == "create":            
            print CreateAccount(args)                                    

        elif self.query == "deposit":            
            ac = Deposit(int(args[1]),int(args[2]))       
            ac.start()
            ac.join()

                    
        elif self.query == "withdraw":
            ac = Withdraw(int(args[1]),int(args[2]))
            ac.start()
            ac.join()


def main():         
    print Database()    
    while True:              
        print "\t\t1.Create Account\n\t\t2.Login"        

        no_of_tries = 0                 

        #try:            
        user_input = int(input())

        if user_input == 1:                  

            # creating account getting_input 
            # customer_details 
            cust_name = raw_input("Enter your Name ").strip()
            cust_age = int(input("Enter your Age In Numbers "))
            cust_gender = int(input("1 Male and 2 for Female "))

            # contact_details                    
            address = raw_input("Enter Address ").strip()                                                              
            email = raw_input("Enter your E-mail ").strip()              
            phone_no = int(input("Enter your Phone No "))          

            opening_blnc = int(input("Enter Opening Balance "))                

            Query("create",cust_name,cust_age,cust_gender
                    ,address,email,phone_no,
                    opening_blnc,)

        elif user_input == 2:
            ac_no = int(input("Enter A/c No "))
            password = raw_input("Enter A/c Password ").strip()                

            session = False 

            if Account.check_password(ac_no,password):
                session = True                 

            else:
                print "Password or A/C No is Invalid"

            while session:

                print "\t\t1.Deposit\n\t\t2.Withdraw\n\t\t3.Edit Account\n\t\t4.Exit"
                user_input = int(input())

                if user_input == 1:                
                    session = False         
                    # deposit                 
                    money = raw_input("Enter Money to Deposit ").strip()                               
                    Query("deposit",ac_no,money)

                elif user_input == 2:                         
                    session = False         
                    # withdraw                                
                    money = raw_input("Enter Money to withdraw ").strip()                               
                    Query("withdraw",ac_no,money)
                
                elif user_input == 3:
                    session = False         
                    #edit_account details                                         
                    #print "\t\t1.Change Password\n\t\t2.Change Name\n\t\t3.Close A/c\n\t\t4.Change Account Type"
                    #raw_input().strip()
                    
                    #   **** YET TO BUILD *****  

                elif user_input == 4:
                    return           
                
                else:
                    print "Try Again"                            
        else:
            print "Try Again"                                                        
 #       except:
#            print "User Input Should Be Integers"                

if __name__ == '__main__':
    main()
                 

