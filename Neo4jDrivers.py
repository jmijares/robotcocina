from neo4j import GraphDatabase
class Neo4jDrivers:

############# init data base ##########

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

############# close data base ############

    def close(self):
        self.driver.close()

############# crear ingrediente ##################

    def incluiringrediente(self, name):
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_ingrediente, name)
    
    @staticmethod
    def _create_and_return_ingrediente(tx, name):
        tx.run("CREATE (a:Ingrediente) SET a.name = $name ", name=name)

############# crear receta ##################

    def incluirreceta(self, name, tipo, url):
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_receta, name, tipo, url)
    
    @staticmethod
    def _create_and_return_receta(tx, name, tipo, url):
        tx.run("CREATE (a:Receta) SET a.name = $name, a.tipo = $tipo, a.url=$url ", name=name, tipo=tipo, url=url)




############## borrar ingrediente #########

    def borrar_ingrediente(self, ingredienteid):
        with self.driver.session() as session:
            session.execute_write(self._borrar_ingrediente, ingredienteid)
            
    @staticmethod
    def _borrar_ingrediente(tx, ingredienteid):
        tx.run("MATCH (ingrediente:Ingrediente) where id(ingrediente) = $ingredienteid DETACH DELETE ingrediente", ingredienteid=int(ingredienteid))
        return

############## borrar todos los ingrediente #########

    def borrar_todos_los_ingredientes(self):
        with self.driver.session() as session:
            session.execute_write(self._borrar_todos_los_ingredientes)
            
    @staticmethod
    def _borrar_todos_los_ingredientes(tx):
        tx.run("MATCH (ingrediente:Ingrediente)  DELETE ingrediente")
        return





############## borrar receta #########

    def borrar_receta(self, recetaid):
        with self.driver.session() as session:
            session.execute_write(self._borrar_receta, recetaid)
            
    @staticmethod
    def _borrar_receta(tx, recetaid):
        query = "MATCH (receta:Receta) where id(receta) = $recetaid DETACH DELETE receta"
        tx.run(query, recetaid=int(recetaid))
        return
    
############## leer recetas ###############

    def leer_recetas(self, tipo, label):
        with self.driver.session() as session:
            records  = session.execute_read(self._leer_and_return_recetas,tipo, label)
        return records
               
    @staticmethod
    def _leer_and_return_recetas(tx, tipo, label):
        query = "MATCH (a:"+label+") WHERE a.tipo = $tipo RETURN id(a) AS ID, a.name AS name, a.url AS url, a.tipo AS tipo, labels(a) as label ORDER BY a.name, a.tipo"
        result = tx.run(query,tipo=tipo)
        records = list(result)  # a list of Record objects
        return records
    
    
############## leer all recetas ###############

    def leer_all_recetas(self, label):
        with self.driver.session() as session:
            records  = session.execute_read(self._leer_and_return_all_recetas, label)
        return records
               
    @staticmethod
    def _leer_and_return_all_recetas(tx, label):
        
        query = "MATCH (a:"+label+")  RETURN id(a) AS ID, a.name AS name, a.url AS url, a.tipo AS tipo, labels(a) as label ORDER BY a.name"
        result = tx.run(query)
        records = list(result)  # a list of Record objects
        return records
     
############## leer ingredientes ###############

    def leer_ingredientes(self, label):
        with self.driver.session() as session:
            records  = session.execute_read(self._leer_and_return_ingredientes, label)
        return records
               
    @staticmethod
    def _leer_and_return_ingredientes(tx, label):
        #label = "Ingrediente"
        query = "MATCH (a:"+label+")  RETURN id(a) AS ID, a.name AS name, a.idInv as idInv ORDER BY a.name"
        result = tx.run(query)
        records = list(result)  # a list of Record objects
        return records
    
############## leer ingredientes de una receta ###############

    def get_ingredientes(self, recetaid):
        with self.driver.session() as session:
            records  = session.execute_read(self._get_ingredientes, recetaid)
        return records
               
    @staticmethod
    def _get_ingredientes(tx,recetaid):  
        result = tx.run("MATCH (a:Receta) where id(a) = $IID RETURN a.name AS name, a.tipo as tipo, id(a) as id, a.url as url", IID=recetaid)
        records = list(result)
        Name_receta = records[0]['name']
        Tipo_receta = records[0]['tipo']
        Id_receta = records[0]['id']
        Url_receta = records[0]['url']
        query = '''
            MATCH receta=({name: $Name_receta})-[r:USA]->(ingrediente) 
            RETURN ingrediente.name as name, id(ingrediente) as id, r.cantidad as cantidad, r.unidad as unidad
            ORDER BY ingrediente.name
        '''
        result = tx.run(query, Name_receta=Name_receta)
        
        records = list(result)  # a list of Record objects
        return Name_receta, Tipo_receta, Id_receta, Url_receta, records

############## leer receta de un ingrediente ###############

    def get_recetas(self, ingredienteid):
        with self.driver.session() as session:
            records  = session.execute_read(self._get_recetas, ingredienteid)
        return records
               
    @staticmethod
    def _get_recetas(tx,ingredienteid):  
        result = tx.run("MATCH (a:Ingrediente) where id(a) = $IID RETURN a.name AS name, id(a) as id", IID=ingredienteid)
        records = list(result)
        Name_ingrediente = records[0]['name']
        Id_ingrediente = records[0]['id']
        query = '''
            MATCH ingrediente=({name: $Name_ingrediente})-[r:USADO_EN]->(receta) 
            with(receta)
            MATCH (receta)-[q:USA]->(ingrediente {name: $Name_ingrediente}) 
            RETURN receta.name as name, id(receta) as id, receta.url as url, receta.tipo as tipo, q.cantidad as cantidad, q.unidad as unidad
            ORDER BY receta.name

        '''

        result = tx.run(query, Name_ingrediente=Name_ingrediente)
        
        records = list(result)  # a list of Record objects
        return Name_ingrediente, Id_ingrediente, records
    
############## leer un ingrediente ###############

    def leer_ingrediente(self, ingredienteid):
        with self.driver.session() as session:
            records  = session.execute_read(self._leer_and_return_ingrediente, ingredienteid)
        return records
               
    @staticmethod
    def _leer_and_return_ingrediente(tx, ingredienteid):
        result = tx.run("MATCH (a:Ingrediente) where id(a) = $ingredienteid RETURN id(a) AS ingredienteid, a.name AS name, a.idInv as idInv, labels(a) as label", ingredienteid=ingredienteid)
        records = list(result)  # a list of Record objects
        return records

############## leer una receta ###############

    def leer_receta(self, recetaid, label):
        with self.driver.session() as session:
            records  = session.execute_read(self._leer_and_return_receta, recetaid, label)
        return records
               
    @staticmethod
    def _leer_and_return_receta(tx, recetaid, label):
        query = "MATCH (a:"+label+") where id(a) = $recetaid RETURN  id(a) AS id, a.name AS name, a.url as url, a.tipo AS tipo, Labels(a) as label"
        result = tx.run(query, recetaid=recetaid)
        records = list(result)  # a list of Record objects
        return records
    
############## update un ingrediente ###############

    def update_ingrediente(self, ingredienteid, ingredientenombre, idInv, label):
        with self.driver.session() as session:
            session.execute_write(self._update_ingrediente, ingredienteid, ingredientenombre, idInv, label)
        return
               
    @staticmethod
    def _update_ingrediente(tx, ingredienteid, ingredientenombre, idInv, label):
        query = '''
        MATCH (a:Ingrediente) where id(a) = $ingredienteid 
        SET a.name = $ingredientenombre,
            a.idInv = $idInv
       '''
        tx.run(query, ingredienteid=ingredienteid,  ingredientenombre=ingredientenombre, idInv=idInv, label=label)
        #if label is not None:
        if len(label) >0:
            query = 'MATCH (a:Ingrediente) where id(a) = $ingredienteid SET a:'+label
            tx.run(query, ingredienteid=ingredienteid)
            
        return
    
############# quitar label a un ingrediente #########

    def quitar_label_a_ingrediente(self, ingredienteid,  label):
            with self.driver.session() as session:
                session.execute_write(self._quitar_label_a_ingrediente, ingredienteid,  label)
            return

    @staticmethod
    def _quitar_label_a_ingrediente(tx, ingredienteid, label):

        query = 'MATCH (a:Ingrediente) where id(a) = $ingredienteid REMOVE a:'+label

        tx.run(query, ingredienteid=ingredienteid)
        return
    
############# quitar label a una receta #########

    def quitar_label_a_receta(self, recetaid,  label):
            with self.driver.session() as session:
                session.execute_write(self._quitar_label_a_receta, recetaid,  label)
            return

    @staticmethod
    def _quitar_label_a_receta(tx, recetaid, label):

        query = 'MATCH (a:Receta) where id(a) = $recetaid REMOVE a:'+label

        tx.run(query, recetaid=recetaid)
        return
    
############## update una receta ###############

    def update_receta(self, recetaid, name, tipo, url, label):
        with self.driver.session() as session:
            session.execute_write(self._update_receta, recetaid, name, tipo, url, label)
        return
               
    @staticmethod
    def _update_receta(tx, recetaid, name, tipo, url, label):
        query = '''
        MATCH (a:Receta) where id(a) = $recetaid 
        SET a.name = $name,
            a.tipo = $tipo,
            a.url = $url
       '''
        tx.run(query, recetaid=recetaid,  name=name, tipo=tipo, url=url)
                #if label is not None:
        if len(label) >0:
            query = 'MATCH (a:Receta) where id(a) = $recetaid SET a:'+label
            tx.run(query, recetaid=recetaid)

        return

############# add un ingrediente a una receta ###############

    def add_ingrediente_a_receta(self, recetaid, idingrediente):
        with self.driver.session() as session:
            session.execute_write(self._add_ingrediente_a_receta, recetaid, idingrediente)
        return

    @staticmethod
    def _add_ingrediente_a_receta(tx, recetaid, idingrediente):
        query = '''
        MATCH (ingrediente: Ingrediente) WHERE id(ingrediente) = $idingrediente 
        MATCH (receta: Receta) WHERE id(receta) = $recetaid 
        CREATE (ingrediente)-[:USADO_EN ]->(receta)
        CREATE (receta)-[:USA ]->(ingrediente)
       '''
        tx.run(query, recetaid=recetaid, idingrediente=idingrediente)

        return
    
############# quitar un ingrediente a una receta ###############

    def quitar_ingrediente_a_receta(self, recetaid, idingrediente):
        with self.driver.session() as session:
            session.execute_write(self._quitar_ingrediente_a_receta, recetaid, idingrediente)
        return

    @staticmethod
    def _quitar_ingrediente_a_receta(tx, recetaid, idingrediente):

        query = '''
        MATCH (ingrediente: Ingrediente) WHERE id(ingrediente) = $idingrediente 
        MATCH (receta: Receta) WHERE id(receta) = $recetaid 
        MATCH (ingrediente)-[r:USADO_EN ]->(receta) DELETE r
       '''
        tx.run(query, recetaid=recetaid, idingrediente=idingrediente)

        query = '''
        MATCH (ingrediente: Ingrediente) WHERE id(ingrediente) = $idingrediente 
        MATCH (receta: Receta) WHERE id(receta) = $recetaid 
        MATCH (receta)-[r:USA ]->(ingrediente) DELETE r
       '''
        tx.run(query, recetaid=recetaid, idingrediente=idingrediente)


        return

############# Actualicar detos USA  ###############

    def act_USA(self, recetaid, idingrediente, cantidad, unidad):
        with self.driver.session() as session:
            session.execute_write(self._act_USA, recetaid, idingrediente, cantidad, unidad)
        return

    @staticmethod
    def _act_USA(tx, recetaid, idingrediente, cantidad, unidad):

        query = '''
        MATCH (ingrediente: Ingrediente) WHERE id(ingrediente) = $idingrediente 
        MATCH (receta: Receta) WHERE id(receta) = $recetaid 
        MATCH (receta)-[r:USA ]->(ingrediente) SET r.cantidad = $cantidad, r.unidad=$unidad
       '''
        tx.run(query, recetaid=recetaid, idingrediente=idingrediente, cantidad=cantidad, unidad=unidad)
        return
    
######### get huerfan node ############

    def huerfan(self):
        with self.driver.session() as session:
            result = session.execute_read(self._huerfan)
        return  result

    @staticmethod
    def _huerfan(tx):
        query = '''
        MATCH (x:Receta)
        WHERE NOT EXISTS ((x)-[:USA]-())
        RETURN x.name as name, id(x) as id
        '''
        result = tx.run(query)
        records = list(result)
        return records



