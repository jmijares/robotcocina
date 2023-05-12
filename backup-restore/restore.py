from Neo4jDriversSP import Neo4jDrivers


import mysql.connector

DataBase = Neo4jDrivers("bolt://localhost:7687", "neo4j", "Lupapaul5409")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Lupapaul5409",
  database="robotcocina"
)

######## Crear los ingredientes ########

DataBase.borrar_todos_los_ingredientes() #borrar todos los ingredientes

mycursor = mydb.cursor()

mycursor.execute(f"select * from ingredientes where tiporegistro = 1;") 
#mydb.commit()
ingredientes = mycursor.fetchall()
for row in ingredientes:
    idint = row[0] 
    iding = row[1]
    nameingrediente = row[3]
    idInv = row[4]
    label =[ ]
    
    mycursor1 = mydb.cursor()
    mycursor1.execute(f"select * from ingredientes where tiporegistro = 3 and  iding = {iding};") 
    for row1 in mycursor1.fetchall():
        label.append(row1[3]) 
    
    DataBase.incluiringrediente(name=nameingrediente, idInv=idInv, label=label)

    
    
############## Crear las recetas ###########

DataBase.borrar_todas_las_recetas() #borrar todos las  recetas

mycursor = mydb.cursor()

mycursor.execute(f"select * from recetas where tiporegistro = 1;") 

recetas = mycursor.fetchall()
for row in recetas:
    idint = row[0] 
    namereceta = row[2]
    tiporeceta = row[3]
    urlreceta = row[4]
    idInv = row[5]
    iding = row[1]
    label =[ ]
  
   

    mycursor1 = mydb.cursor()
    mycursor1.execute(f"select * from recetas where tiporegistro = 3 and  idInv = {idInv};") 
    for row1 in mycursor1.fetchall():
        label.append(row1[2]) 
    
    DataBase.incluirreceta(name=namereceta, tipo=tiporeceta, url=urlreceta, label=label)
    
    ##### crear las relaciones

    mycursor1 = mydb.cursor()
    mycursor1.execute(f"select * from recetas where tiporegistro = 2 and  idInv = {idInv};") 
    for row1 in mycursor1.fetchall():
        unidad = row1[6]
        cantidad = row1[7]
        nameingrediente = row1[2]
        DataBase.add_ingrediente_a_receta(namereceta=namereceta, nameingrediente=nameingrediente, cantidad=cantidad, unidad=unidad)

