from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL

import os

from flask import Flask

 
app = Flask(__name__)

app.secret_key = "secret_key"
app.config['MYSQL_HOST'] = 'f173a5bc-69f8-488f-b6a8-f931274e57f3.ghamm-servi-5741.mysql.a.osc-fr1.scalingo-dbs.com'
app.config['MYSQL_PORT'] = 33848
app.config['MYSQL_USER'] = 'ghamm_servi_5741'
app.config['MYSQL_PASSWORD'] = 'OLlaqQ9XfUuSitHRUKL6' 
app.config['MYSQL_DB'] = 'ghamm_servi_5741'


"""app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'horizon'"""




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
        cur.execute("INSERT INTO EnregistrementMoto (Nom_chauffeur, Proprietaire, Num_moteur, N_chasie, Marque, Couleur, Secteur, Tel_prop, Date) VALUES (%s, %s, %s, %s, %s, %s, %s , %s,  STR_TO_DATE('04/11/2023 04:42', '%d/%m/%Y %H:%i')))", _donnees)
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Succès"})
    except Exception as e:
        print(f'mysql: {e}')
        return jsonify({"message": "Erreur lors de l'insertion dans la base de données"})
    
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
        cur.execute("SELECT * FROM EnregistrementMoto WHERE N_chasie=%s", _donnees)
        results = cur.fetchone()
        results = list(results) if results else None
        mysql.connection.commit()
        cur.close()
        return jsonify({'donnees': results})
    except:
        print("Les formats des données sont refusé")

@app.route('/get_donnees', methods=['GET'])
def get_donnees():
    matricules = request.args.get('matricule')
    print('ici nous sommes dans get', matricules)
    tuples = (matricules, )
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EnregistrementMoto WHERE Num_moteur=%s", tuples)
    donnees = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    donnees_list = list(donnees) if donnees else []
    print(donnees_list)
    return jsonify(donnees_list)


@app.route('/') 
def index_acceuil():
    return  render_template("acceuilx.html") 


@app.route("/traitement_epargne", methods =[ 'POST'])
def traitement_epargne():
     
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

            if results!=None:
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM EnregistrementMoto  ")
                data = cur.fetchall()

                return render_template("shows_data.html",id_utilisateur=results[1] ,payement_terminaux=data,)
            else:
                return '<h1>Erreur mot de passe<h1>'
        except Exception as e:
            print(f"Erreur MySQL: {e}")
            return '<h1>Erreur de liaison avec la base de donner<h1>'
     
       
          
  




@app.route("/login_lvage")
def login_lvage():
    return render_template("login_lavage.html")


@app.route("/epargne")
def login_epargne():
    return render_template("login_epargne.html")

 
          


 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == "gunicorn.app.wsgiapp":
    from app import app  
    application = app