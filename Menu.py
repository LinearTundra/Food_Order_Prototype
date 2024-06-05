from SQL_Link import command
import csv


def create(file_name: {str:"csv file"}, password: str, database:str):

    command("drop table Menu", password, database)

    with open(file_name, "r") as menu :

        reader = csv.reader(menu)
        for read in reader :
            
            if read[0].lower() == "product_id" :
                
                try :
                    command(
                        "create table Menu(Product_ID int, Product_Name varchar(30), Price int, Per varchar(10))",
                        password,
                        database
                        ) 
                except :
                    pass
                
                continue
                
            else :
                command(
                    f"insert into Menu values({int(read[0])}, '{read[1].title()}', {int(read[2])}, '{read[3].title()}')",
                    password,
                    database
                    ) 
