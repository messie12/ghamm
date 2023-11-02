from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv


load_dotenv()

import os

from flask import Flask

 
app = Flask(__name__)
app.secret_key = "secret_key"

app.config['MYSQL_DATABASE_HOST'] = os.environ.get('DB_HOST')
app.config['MYSQL_DATABASE_USER'] = os.environ.get('DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('DB_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('DB_NAME')
app.config['MYSQL_DATABASE_PORT'] = 33848  

mysql = MySQL()
mysql.init_app(app)

'''app=Flask(__name__)
app.secret_key= "secret_key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'horizon'
'''




# Créez une instance MySQL en utilisant la configuration de votre application
mysql = MySQL(app)

# Exemple de route pour recevoir des données via POST
@app.route('/T1', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("Received data:", data)
    donnees = data.values()
    _donnees = tuple(donnees)
    print("tuple de données ------------------------", _donnees)
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO EnregistrementMoto (Nom_chauffeur, Proprietaire, Num_moteur, N_chasie, Marque, Couleur, Secteur, Tel_prop ) VALUES (%s, %s, %s, %s, %s, %s, %s , %s)", _donnees)
        mysql.connection.commit()
        print("OK")
        return jsonify({"message": "succès"})
    except:
        print('les requettes provenant des terminaux ne trouve pas la base de donnée')
# Exemple de route pour recevoir des données via POST
@app.route('/matricule', methods=['POST'])
def receive_dat():
    print('La fonction est déjà appelée')
    data = request.get_json()
    print("Received data:", data)
    donnees = data.values()
    _donnees = tuple(donnees)
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM EnregistrementMoto WHERE Num_moteur=%s", _donnees)
        results = cur.fetchone()
        results = list(results) if results else None
        mysql.connection.commit()
        return jsonify({'donnees': results})
    except:
        print("Les formats des données sont refusé")

# Autres routes...

# Exemple de route GET
@app.route('/get_donnees', methods=['GET'])
def get_donnees():
    matricules = request.args.get('matricule')
    print('ici nous sommes dans get', matricules)
    tuples = (matricules, )
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EnregistrementMoto WHERE Num_moteur=%s", tuples)
    donnees = cur.fetchone()
    mysql.connection.commit()
    donnees_list = list(donnees) if donnees else []
    print(donnees_list)
    return jsonify(donnees_list)


@app.route('/') 
def index_acceuil():
    return  render_template("acceuilx.html") 


@app.route("/traitement_epargne", methods =[ 'POST','GET'])
def traitement_epargne():
     
    if request.method == "POST":
        donne_form_log_epgne = request.form
        nom=donne_form_log_epgne.get('identifiant')
        passe=donne_form_log_epgne.get('motdepasse')
        donner=(nom,passe)
        
        try:
            cur = mysql.connection.cursor()	
            print(donner)
            cur.execute( "SELECT * FROM login WHERE Nom_utilisateur=%s and Mot_de_passe =%s", donner)
            results = cur.fetchone() 
            print("okkookkook",results)
            
        except Exception as e:
            print(f"Erreur MySQL: {e}")
            return '<h1>Erreur de liaison avec la base de donner<h1>'
       
        if results == None: 
            return redirect(url_for("index_acceuil"))
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from EnregistrementMoto  ")
            data = cur.fetchall()


            cur.execute("SELECT COUNT(*) FROM  EnregistrementMoto" )
            nobreDenregistrment=cur.fetchone()[0]*500
            cur.close()
            
            return render_template("shows_data.html",id_utilisateur=results[1],payement_terminaux=data, nbr_enregis=nobreDenregistrment)
    else:
      return redirect(url_for("index_acceuil"))   
  
@app.route("/upload", methods =['POST'])
def epargn_upload():
    if request.method == "POST":
        donne_form_base = request.form
        print(donne_form_base)
        return"les donnees sont envoyer avec succes "
    else:
        return redirect(url_for("index_acceuil"))
       


@app.route('/donnees', methods =["GET"] )
def Data():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from EnregistrementMoto  ")
        data = cur.fetchall()
        cur.close()
        return render_template("incude_tabl.html", payement_terminaux=data )
    





@app.route("/login_lvage")
def login_lvage():
    return render_template("login_lavage.html")


@app.route("/epargne")
def login_epargne():
    return render_template("login_epargne.html")

 
          


@app.route('/inserts', methods = ['POST'])
def insert():

    if request.method == "POST":
        
        conduct = request.form['conduct']
        prop = request.form['prop']
        moteur = request.form['n_moteur']
        chasie = request.form['n_chasie']
        marque = request.form['marque']
        coul = request.form['coul']
        secteur = request.form['secteur']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        _donnes= (conduct, prop, moteur, chasie, marque, coul,secteur, phone )
        cur.execute("INSERT INTO EnregistrementMoto (Nom_chauffeur, Proprietaire, Num_moteur, N_chasie, Marque, Couleur, Secteur, tel_prop ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", _donnes)
        mysql.connection.commit()
        flash("les données sont inseré avec succes")
        

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
 try:
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM compt_client WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Data'))
 except: 
    return"la supression de cette compte entrainera les pertes de donnés de payement" 
    
    
@app.route('/update',methods=['POST','GET'])
def update():
   if request.method == 'POST':
        id_data= request.form['id']
        nom = request.form['nom']
        matric = request.form['matric']
        tel = request.form['tel']
        print(request.form)
        num_compt = request.form['num_compt'] 
        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE compt_client
               SET Nom = %s, Matricule = %s, Telephone = %s 
               WHERE id=%s """,( nom, matric, tel, num_compt, id_data,))
        flash("Data Updated Successfully")
        mysql.connection.commit()   
        return redirect(url_for('Data'))


@app.route('/detail/<string:id_data>')
def detail_clent(id_data):
        cur = mysql.connection.cursor()
        cur.execute("""SELECT p.* FROM paiements p JOIN compt_client c ON c.id = %s""" % (id_data))

        donne = cur.fetchall()
        cur.close()
        global shared_variable 
        don_client =list(donne)
        print(donne)          
        return render_template('detail.html',details=donne)

@app.route('/payement', methods = ['POST',"GET"])
def payement():
     if request.method == "POST":
        num_carnet = request.form['num_carnet']
        payement = request.form['payement']
        id_datas= request.form ['id']
        print(num_carnet,payement)
        print("voici",id_datas)
        flash("Record Has Been Deleted Successfully")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO paiements(Numerocarnet, Montantpayer, client_id) VALUES (%s, %s, %s)", (num_carnet, payement, id_datas))
        mysql.connection.commit()
        return redirect(url_for("Data"))
 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
