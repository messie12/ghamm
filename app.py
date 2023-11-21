from flask import Flask, render_template,request, redirect, url_for,flash, jsonify
from flask_mysqldb import MySQL 
import os
from datetime import datetime
from MySQLdb import IntegrityError


app=Flask(__name__)
app.secret_key= "secret_key"


app.config['MYSQL_HOST'] = 'ghamm-servi-5741.mysql.a.osc-fr1.scalingo-dbs.com'
app.config['MYSQL_PORT'] = 33773
app.config['MYSQL_USER'] = 'ghamm_servi_5741'
app.config['MYSQL_PASSWORD'] = 'OLlaqQ9XfUuSitHRUKL6' 
app.config['MYSQL_DB'] = 'ghamm_servi_5741'




mysql = MySQL(app)

from datetime import datetime  # Assurez-vous d'importer datetime

@app.route('/T1', methods=['POST'])
def receive_data():
    print('La fonction est déjà appelée')
    data = request.get_json()
    print("Received data:", data)
    donnees = data.values()
    _donnees = tuple(donnees)
    _donnees += (datetime.now(),)  # Ajoutez la date à la fin du tuple
    print("Tuple de données:", _donnees)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO EnregistrementMoto (Nom_chauffeur, Proprietaire, Num_moteur, N_chasie, Marque, Couleur, secteur, Tel_prop, Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", _donnees)
    mysql.connection.commit()
    return jsonify({"message": "Erreur : N_chasie en liste noire"})
      




@app.route('/matricule', methods=['POST'])
def receive_dat():
    print('La fonction est déjà appelée')
    data = request.get_json()

    if data is not None:
        donnees = data.values()
        _donnees = tuple(donnees) 
        print("Tuple de données ------------------------", _donnees)

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM EnregistrementMoto WHERE N_chasie=%s", _donnees)
            result = cur.fetchone()

            if result is not None:
                # Traitez les données, puis renvoyez les données en réponse
                return jsonify({'donnees': result})

        except Exception as e:
            print(e)

    # Si le matricule n'a pas été trouvé ou une erreur s'est produite
    return jsonify({'donnees': None})


@app.route('/get_donnees', methods=['GET'])
def get_donnees():
    donnees = None
    Agent1 = "AP020H02305000140"


    matricules = request.args.get('matricule')
    numero_serial = request.args.get('serials')
    print('Voici la valeur du numéro de série:', numero_serial, "Matricule:", matricules)
    try:   
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM EnregistrementMoto WHERE N_chasie = '{matricules}'")
        donnees = cur.fetchone()
    except Exception as e:
        print('Format de données invalide')
        print(f"Erreur : {str(e)}")
    
    if donnees is None:
        donnees_list = []
    else:
        donnees_list = list(donnees)
        if numero_serial == Agent1:
            print('code agent 1')
            cur = mysql.connection.cursor()
            cur.execute(f"UPDATE revendeur SET recette = recette + 1 WHERE serial = '{Agent1}'")
            mysql.connection.commit()
        elif numero_serial=='Agent2':
            print('code agent 2')
            cur = mysql.connection.cursor()
            cur.execute(f"UPDATE revendeur SET recette = recette + 1 WHERE serial = '{'Agent2'}'")
            mysql.connection.commit() 
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
        
        cur = mysql.connection.cursor()	
        cur.execute( "SELECT * FROM login WHERE Nom_utilisateur= %s AND Mot_de_passe = %s", donner)
        results = cur.fetchone() 
        print(results)       
        if results == None:
            return redirect(url_for("index_acceuil"))
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM  EnregistrementMoto  ")
            data = cur.fetchall()

            cur = mysql.connection.cursor() 
            cur.execute("SELECT * FROM  revendeur  ")
            revendeur = cur.fetchall()

 
            cur.execute("SELECT COUNT(*) FROM  EnregistrementMoto" )
            nobreDenregistrment=cur.fetchone()[0]
            cur.close()
            
            return render_template("shows_data.html",id_utilisateur=results[1],payement_terminaux=data, nbr_enregis=nobreDenregistrment, revend=revendeur)
    else:

      return redirect(url_for("index_acceuil"))
    
@app.route("/login_lvage")
def login_lvage():
    return render_template("login_lavage.html")


@app.route("/epargne")
def login_epargne():
    return render_template("login_epargne.html")

@app.route("/Apropos")
def apropos():
    return render_template("messie.html")


@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method == "POST":
        nom = request.form['conduct']
        nom_prop = request.form['prop']
        moteur = request.form['n_moteur']
        chasie = request.form['n_chasie']
        marque = request.form['marque']
        coleur = request.form['color']
        locaite = request.form['secteur']
        telephone = request.form['telephone'] 
         
        data = (nom, nom_prop, moteur, chasie, marque, coleur, locaite, telephone, datetime.now())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO EnregistrementMoto (Nom_chauffeur, Proprietaire, Num_moteur, N_chasie, Marque, Couleur, secteur,Tel_prop, Date ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
        mysql.connection.commit()
        flash("Les données sont insérées avec succès")
        return ("<h1 style ='color: red; font-size: 20px; font-weight: bold; text-align: center;'>Les données sont enregistré avec succes <h1>")
        
@app.route('/update',methods=['POST','GET'])
def update():
   if request.method == 'POST':
        ID=  request.form['id']
        nom = request.form['conduct']
        nom_prop = request.form['prop']
        moteur = request.form['n_moteur']
        chasie = request.form['n_chasie']
        marque = request.form['marque']
        coleur = request.form['color']
        localite = request.form['secteur']
        telephone = request.form['telephone']  
        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE EnregistrementMoto
               SET Nom_chauffeur = %s, Proprietaire = %s, Num_moteur= %s, N_chasie= %s, Marque= %s, Couleur= %s ,secteur= %s,Tel_prop= %s 
               WHERE id=%s """,( nom, nom_prop, moteur, chasie, marque, coleur, localite, telephone, ID))
        flash("Data Updated Successfully")
        mysql.connection.commit()   
        return ("<h1 style ='color: red; font-size: 20px; font-weight: bold; text-align: center;'>Les données sont enregistré avec succes <h1>")

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM EnregistrementMoto WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return ("SUCCES")


    
@app.route('/cloture/<id>', methods=['GET', 'POST'])
def cloture(id):
    if request.method == 'POST':
        conduct_value = request.form.get('recolte')
        cur = mysql.connection.cursor()
        cur.execute("SELECT recette FROM revendeur WHERE code_agent = %s", (id,))
        print(id)
        resultat = cur.fetchone()
        print('la valeur selection de reccette est ', (resultat[0]))
        if resultat:
             dette= int(conduct_value)
             print("la dette du client est" ,dette)
             return ("succes")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)