from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
                                #importamos las librerias del, framework
                                #redirect y url-form  son para hacer que si / valla a algun sitio
                                #request para procesar formularios simples



from flask_mysqldb import MySQL
from Neo4jDrivers import Neo4jDrivers
import subprocess
import os   






######### main program ###########

#inicializar instancia de flask y la guardamos en una variable

app =  Flask(__name__)

DataBase = Neo4jDrivers("bolt://localhost:7687", "neo4j", "Lupapaul5409")

app.config['MYSQL_HOST']='presario.jmijares.ml'
app.config['MYSQL_USER']='rootroot'
app.config['MYSQL_PASSWORD']='Lupapaul5409'
app.config['MYSQL_DB']='inventario'

mysql = MySQL(app) 

app.secret_key = '12345' #para uso en tokens etc


Client_ip = 'negado'




@app.route('/') #si / ejecute un metodo qeu lo definiremos aqui en este caso
                #este es un decaorador herramienta que encapsula funcionalidades                
def index(): #el nombre cualquiera para lafuncion declarad
        global Client_ip
        Client_ip = request.remote_addr
        return redirect(url_for('listarrecetas')) #si inserta solo el http va hay 

@app.route('/home')
def home():
    global Client_ip
    Client_ip = request.remote_addr
    return render_template('home.html',ip=Client_ip)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/incluiringrediente', methods=["GET", "POST"])
def incluiringrediente():
    if request.method == 'POST':
        name =request.form['nombre']
        DataBase.incluiringrediente(name=name)
        return redirect(url_for('editaringredientes',ip=Client_ip))
    return render_template('incluiringrediente.html',ip=Client_ip)

@app.route('/incluirreceta', methods=["GET", "POST"])
def incluirreceta():
    if request.method == 'POST':
        name =request.form['name']
        tipo =request.form['tipo']
        url =request.form['url']
        DataBase.incluirreceta(name=name, tipo=tipo, url=url)
        return redirect(url_for('incluirreceta',ip=Client_ip))
    return render_template('incluirreceta.html',ip=Client_ip)



@app.route('/borrar')
def borrar():
    #DataBase.borrar_nodos()
    return redirect(url_for('listar'))

@app.route('/listarrecetas')
def listarrecetas():
    recordst1 = DataBase.leer_recetas(tipo='1', label="Receta")
    recordst2 = DataBase.leer_recetas(tipo='2', label="Receta")
    recordst3 = DataBase.leer_recetas(tipo='3', label="Receta")
    return render_template('listadorecetas.html',ip=Client_ip, recordst1=recordst1, recordst2=recordst2, recordst3=recordst3)

@app.route('/listaringredientes/')
def listaringredientes():
    label = 'Ingrediente'
    records = DataBase.leer_ingredientes(label=label)
    return render_template('listadoingredientes.html',ip=Client_ip, records=records)

@app.route('/listarclase/<label>', methods=["GET", "POST"])
def listarclase(label):
    #label = 'Verduras'
    records = DataBase.leer_ingredientes(label=label)
    return render_template('listarclase.html',ip=Client_ip, label=label, records=records)

@app.route('/listarclasereceta/<label>', methods=["GET", "POST"])
def listarclasereceta(label):
    records = DataBase.leer_all_recetas(label=label)
    return render_template('listarclasereceta.html',ip=Client_ip, label=label, records=records)

@app.route('/quitarclase/<idingrediente>/<label>')
def quitarclase(idingrediente, label):
    DataBase.quitar_label_a_ingrediente(ingredienteid=int(idingrediente), label=label)
    records =  DataBase.leer_ingrediente(ingredienteid=int(idingrediente))
    return render_template('formaeditingrediente.html',ip=Client_ip, ingrediente=records[0])

@app.route('/quitarclasereceta/<recetaid>/<label>')
def quitarclasereceta(recetaid, label):
    DataBase.quitar_label_a_receta(recetaid=int(recetaid), label=label)
  #  records =  DataBase.leer_receta(recetaid=int(recetaid), label="Receta")
  #  return render_template('formaeditreceta.html',ip=Client_ip, receta=records[0])
    return redirect(url_for('getreceta',recetaid=recetaid))


@app.route('/editaringredientes/')
def editaringredientes():
    label = 'Ingrediente'
    records = DataBase.leer_ingredientes(label=label)
    return render_template('editaringredientes.html',ip=Client_ip, records=records)

@app.route('/editarrecetas/')
def editarrecetas():
    records = DataBase.leer_all_recetas(label="Receta")
    return render_template('editarrecetas.html',ip=Client_ip, records=records)


@app.route('/getingredientes/<recetaid>')
def getingredientes(recetaid):
    records =  DataBase.get_ingredientes(recetaid=int(recetaid))
    return render_template('listadoingredientesreceta.html',ip=Client_ip, receta=records[0], tipo_receta=records[1], id_receta=records[2], url_receta=records[3], ingredientes=records[4])

@app.route('/modingredientes/<recetaid>', methods=["GET", "POST"])
def modingredientes(recetaid):
    records =  DataBase.get_ingredientes(recetaid=int(recetaid))
    if request.method == 'POST':
            returnrecetaid = request.form['returnrecetaid']
            listaidingredientes = request.form.getlist('idingrediente')
            listacantidad = request.form.getlist('cantidad')
            listaunidad = request.form.getlist('unidad')
            i = 0
            while i < len(listaidingredientes):
                DataBase.act_USA(recetaid=int(returnrecetaid),
                idingrediente=int(listaidingredientes[i]),
                cantidad=listacantidad[i],
                unidad=listaunidad[i])
                i += 1
            records =  DataBase.get_ingredientes(recetaid=int(recetaid))
            return render_template('modificaringredientesreceta.html',ip=Client_ip, receta=records[0], tipo_receta=records[1], id_receta=records[2], url_receta=records[3], ingredientes=records[4])
    return render_template('modificaringredientesreceta.html',ip=Client_ip, receta=records[0], tipo_receta=records[1], id_receta=records[2], url_receta=records[3], ingredientes=records[4])


@app.route('/getrecetas/<ingredienteid>')
def getrecetas(ingredienteid):
    records =  DataBase.get_recetas(ingredienteid=int(ingredienteid))
    return render_template('listadorecetasingrediente.html',ip=Client_ip, ingrediente=records[0], id_ingrediente=records[1], recetas=records[2])


@app.route('/getingrediente/<ingredienteid>', methods=["GET", "POST"])
def getingrediente(ingredienteid):
    records =  DataBase.leer_ingrediente(ingredienteid=int(ingredienteid))
    if request.method == 'POST':
            ingredientenombre = request.form['nombre']
            idInv = request.form['idInv']          
            label =request.form['newlabel']
            if request.form.get("delete"):
                DataBase.borrar_ingrediente(ingredienteid=ingredienteid)
                return redirect(url_for('editaringredientes',ip=Client_ip))
            DataBase.update_ingrediente(ingredienteid=int(ingredienteid), ingredientenombre = ingredientenombre, idInv=idInv, label=label )
            return redirect(url_for('editaringredientes',ip=Client_ip))
    
    return render_template('formaeditingrediente.html',ip=Client_ip, ingrediente=records[0])


@app.route('/getreceta/<recetaid>', methods=["GET", "POST"])
def getreceta(recetaid):
    records =  DataBase.leer_receta(recetaid=int(recetaid), label="Receta")
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']          
        tipo =request.form['tipo']
        label =request.form['newlabel']
        if request.form.get("delete"):
             DataBase.borrar_receta(recetaid=recetaid)
             return redirect(url_for('editarrecetas',ip=Client_ip))
        DataBase.update_receta(recetaid=int(recetaid), name = name, url=url, tipo=tipo, label=label )
        #return redirect(url_for('editarrecetas',ip=Client_ip))
        return redirect(url_for('getreceta',recetaid=recetaid))
    return render_template('formaeditreceta.html',ip=Client_ip, receta=records[0])

@app.route('/agregaringredienteareceta/<recetaid>', methods=["GET", "POST"])
def agregaringredienteareceta(recetaid):
    if request.method == 'POST':
        recetaid = request.form['recetaid']
        sellist = request.form.getlist('sellist') #lsita de id de ingredientes a agregar
        for i in sellist:
            DataBase.add_ingrediente_a_receta(recetaid=int(recetaid), idingrediente=int(i))
            

        records =  DataBase.get_ingredientes(recetaid=int(recetaid))
      #  return render_template('modificaringredientesreceta.html',ip=Client_ip, receta=records[0], tipo_receta=records[1], id_receta=records[2], url_receta=records[3], ingredientes=records[4])
        return redirect(url_for('modingredientes',recetaid=recetaid))
    #2 Pasamos a pagina de seleccion todos los ingredientes
    records = DataBase.leer_ingredientes(label="Ingrediente")
  
    return render_template('selectingredientes.html', ip=Client_ip, recetaid=recetaid, records=records)

@app.route('/quitaringredienteareceta/<recetaid>/<idingrediente>')
def quitaringredienteareceta(recetaid,idingrediente):
    
    DataBase.quitar_ingrediente_a_receta(recetaid=int(recetaid), idingrediente=int(idingrediente))
   
    records =  DataBase.get_ingredientes(recetaid=int(recetaid))
   # return render_template('modificaringredientesreceta.html',ip=Client_ip, receta=records[0], tipo_receta=records[1], id_receta=records[2], url_receta=records[3], ingredientes=records[4])
    return redirect(url_for('modingredientes',recetaid=recetaid))
 

@app.route('/getproducto/<idInv>')
def getproducto(idInv):
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from Productos where id='{idInv}';") #es mejor pone los campos y el * 
    datos = cursor.fetchone()
    existencia = datos[16]/1000
    entradas = datos[7]/1000
    salidas = datos[8]/1000
    ptopedido = datos[13]/1000
    ultcosto = datos[9]/100
    ultcostodolar = datos[10]/100
    iva1 = datos[14]/100
    iva2 = datos[15]/100
    if datos==None: #si la consulta no da anada
            return render_template('404.html',ip=Client_ip)
        
    return render_template('detalle.html',ip=Client_ip, datos=datos, existencia=existencia,
                           entradas = entradas, salidas=salidas,
                           ultcosto=ultcosto, ultcostodolar=ultcostodolar,
                           ptopedido=ptopedido,
                           iva1=iva1, iva2=iva2)
    

@app.route('/backup')
def backup():
    p = "/var/www/robotcocina/backup-restore/backup.py"
    p = os.path.abspath("backup-restore/backup.py")

    result = subprocess.run(["python3", p], capture_output=True, text=True)

    err= result.returncode
    if err==0:
        return redirect(url_for('index'))
    
    flash('A ocurrido un error al ejecutar el comando Backup:'+p)
    return render_template('error.html',ip=Client_ip) 


@app.route('/huerfan')
def huerfan():
    result = DataBase.huerfan()
    return render_template('huerfan.html',ip=Client_ip, result=result)


if __name__=='__main__':
        app.run(debug=False)
        ####, host='0.0.0.0', port=5555)
