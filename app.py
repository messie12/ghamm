from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import os

from flask import Flask


app = Flask(__name__)
app.secret_key = "secret_key"
app.config['MYSQL_DATABASE_HOST'] = 'dfad4f63-2d70-4a76-88ab-f718d1ee1b6e.ghamm-servi-1239.mysql.a.osc-fr1.scalingo-dbs.com'
app.config['MYSQL_DATABASE_USER'] = 'ghamm_servi_1239'
app.config['MYSQL_DATABASE_PASSWORD'] = 'KC_XqKNZbq68rNpTfyWq'
app.config['MYSQL_DATABASE_DB'] = 'ghamm_servi_1239'

# Ajoutez le paramètre de connexion TLS
app.config['MYSQL_DATABASE_HOST'] += "?ssl_ca=/chemin/vers/autorite_cert.pem"

# Créez une instance MySQL en utilisant la configuration de votre application
mysql = MySQL(app)

# Exemple de route pour recevoir des données via POST
@app.route('/T1', methods=['POST'])
def receive_data():
    print('La fonction est déjà appelée')
    data = request.get_json()
    print("Received data:", data)
    donnees = data.values()
    _donnees = tuple(donnees)
    print("tuple de données ------------------------", _donnees)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO epargne_motocyclette (Nom_chauffeur, Proprietaire, Num_moteur, N_chasie, Marque, Couleur, Parking ) VALUES (%s, %s, %s, %s, %s, %s, %s)", _donnees)
    mysql.connection.commit()
    print("OK")
    return jsonify({"message": "succès"})

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
        cur.execute("SELECT * FROM epargne_motocyclette WHERE Num_moteur=%s", _donnees)
        results = cur.fetchone()
        results = list(results) if results else None
        mysql.connection.commit()
        return jsonify({'donnees': results})
    except:
        print("Le format de données est refusé")

# Autres routes...

# Exemple de route GET
@app.route('/get_donnees', methods=['GET'])
def get_donnees():
    matricules = request.args.get('matricule')
    print('ici nous sommes dans get', matricules)
    tuples = (matricules, )
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM epargne_motocyclette WHERE Num_moteur=%s", tuples)
    donnees = cur.fetchone()
    mysql.connection.commit()
    donnees_list = list(donnees) if donnees else []
    print(donnees_list)
    return jsonify(donnees_list)


@app.route('/acceuil') 
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
            cur.execute( "SELECT * FROM login WHERE nom_utilisateur=%s and mot_passe =%s", donner)
            results = cur.fetchone() 
            print(results)
            
        except:
            return 'erreur de connexion sur le serveur'
       
        if results == None:
            return redirect(url_for("traitement_epargne"))
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from epargne_motocyclette  ")
            data = cur.fetchall()


            cur.execute("SELECT COUNT(*) FROM  epargne_motocyclette" )
            nobreDenregistrment=cur.fetchone()[0]*500
            cur.close()
            
            return render_template("shows_data.html",id_utilisateur=results[0],payement_terminaux=data, nbr_enregis=nobreDenregistrment)
    else:
      return redirect(url_for("traitement_epargne"))
  
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
        cur.execute("SELECT * from epargne_motocyclette  ")
        data = cur.fetchall()
        cur.close()
        return render_template("incude_tabl.html", payement_terminaux=data )
    





@app.route("/login_lvage")
def login_lvage():
    return render_template("login_lavage.html")


@app.route("/epargne")
def login_epargne():
    return render_template("login_epargne.html")

 
          


@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        
        nom = request.form['nom']
        matric = request.form['matric']
        tel = request.form['tel']
        cur = mysql.connection.cursor()
        
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
