from Neo4jDriversSP import Neo4jDrivers


import mysql.connector

DataBase = Neo4jDrivers("bolt://jmijares.ml:7687", "neo4j", "yout password")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="your mysql password",
  database="robotcocina"
)


mycursor = mydb.cursor()

mycursor.execute(f"delete from recetas;") 
mydb.commit()
recordst = DataBase.leer_recetas(tipo='1', label="Receta")
recordst = recordst + DataBase.leer_recetas(tipo='2', label="Receta")
recordst = recordst + DataBase.leer_recetas(tipo='3', label="Receta")


for  i in recordst:
    ID=i['ID']
    name = i['name']
    tipo = i['tipo']
    url = i['url']
    label = i['label'] 
        
    ingredientes =  DataBase.get_ingredientes(recetaid=int(ID))

    sql = "insert into recetas (tiporegistro,name,tipo,url, idInv) values (%s, %s, %s, %s, %s)"
    val = ('1',  name, tipo, url, ID)
    mycursor.execute (sql, val)
    mydb.commit()
    
   
    k=0 
    while k<len(ingredientes[4]):

      name = ingredientes[4][k]['name']
      unidad = ingredientes[4][k]['unidad']
      cantidad = ingredientes[4][k]['cantidad']
      k=k+1
    

      sql = "insert into recetas (tiporegistro, name, unidad, cantidad, idInv) values (%s, %s, %s, %s, %s)"
      val = ('2',  name, unidad, cantidad, ID)
      mycursor.execute (sql, val)
      mydb.commit()

    k=0 
    while k<len(label):
      
      sql = "insert into recetas (tiporegistro, name,  idInv) values (%s, %s, %s)"
      val = ('3',  label[k],  ID)
      mycursor.execute (sql, val)
      mydb.commit()
      k = k + 1
    
    
##### now with ingredientess


mycursor = mydb.cursor()

mycursor.execute(f"delete from ingredientes;") 
mydb.commit()
recordst = DataBase.leer_ingredientes(label='Ingrediente')



for  i in recordst:
  ID=i['ID']  #id interno de neo4j
  name = i['name']
  idInv = i['idInv']
  label = i['label']

  recetas =     DataBase.get_recetas(ingredienteid=int(ID))


  sql = "insert into ingredientes (tiporegistro,name,idInv, iding) values (%s, %s,  %s, %s)"
  val = ('1',  name, idInv, ID)
  mycursor.execute (sql, val)
  mydb.commit()
  
 
  k=0 
  while k<len(recetas[2]):

    name = recetas[2][k]['name']
    idInv = recetas[2][k]['id']  #ahora sera el id de la receta 
    k=k+1
  

    sql = "insert into ingredientes (tiporegistro, name,  idInv, iding) values (%s, %s, %s, %s)"
    val = ('2',  name,  idInv, ID)
    mycursor.execute (sql, val)
    mydb.commit()

  k=0 
  while k<len(label):
    
    sql = "insert into ingredientes (tiporegistro, name,  idInv, iding) values (%s, %s, %s, %s)"
    val = ('3',  label[k], idInv, ID)
    mycursor.execute (sql, val)
    mydb.commit()
    k = k + 1
    
