from flask import Flask, render_template,request, redirect, url_for,flash, jsonify
from flask_mysqldb import MySQL 

app=Flask(__name__)
app.secret_key= "secret_key"

app.config['MYSQL_HOST'] = 'f173a5bc-69f8-488f-b6a8-f931274e57f3.ghamm-servi-5741.mysql.a.osc-fr1.scalingo-dbs.com'
app.config['MYSQL_PORT'] = 33848
app.config['MYSQL_USER'] = 'ghamm_servi_5741'
app.config['MYSQL_PASSWORD'] = 'OLlaqQ9XfUuSitHRUKL6' 
app.config['MYSQL_DB'] = 'ghamm_servi_5741'




mysql = MySQL(app)

@app.route('/T1', methods=['POST','POST'])
def receive_data(): 
    print('la fonction est deja appelée')
    data = request.get_json()
    print("Received data:", data) 
    donnees=data.values()
    _donnees=tuple(donnees)
    print("tuple de donner------------------------",_donnees)
    cur = mysql.connection.cursor()	
    cur.execute("INSERT INTO EnregistrementMoto (Nom_chauffeur, Proprietaire, Num_moteur, N_chasie, Marque, Couleur, Secteur, Tel_prop ) VALUES( %s, %s, %s, %s, %s, %s, %s, %s)",_donnees)
    mysql.connection.commit()
    # Traitez les données reçues ici selon vos besoins
    print("okokokokokok")
    return jsonify({"message": " succés"})







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
    matricules = request.args.get('matricule')
    print('ici mous somme dans get', matricules)
    tuples = (matricules)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EnregistrementMoto WHERE Num_chasie=%s", tuples)
    donnees = cur.fetchone()
    mysql.connection.commit()
    
    if donnees is None:
        donnees_list = []
    else:
        donnees_list = list(donnees)
    
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


            cur.execute("SELECT COUNT(*) FROM  EnregistrementMoto" )
            nobreDenregistrment=cur.fetchone()[0]*500
            cur.close()
            
            return render_template("shows_data.html",id_utilisateur=results[1],payement_terminaux=data, nbr_enregis=nobreDenregistrment)
    else:

      return redirect(url_for("index_acceuil"))
    
@app.route("/login_lvage")
def login_lvage():
    return render_template("login_lavage.html")


@app.route("/epargne")
def login_epargne():
    return render_template("login_epargne.html")

 
  
"""@app.route("/upload", methods =['POST'])
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
 
                 """



if __name__ =='__main__':
   
   app.run(host='0.0.0.0', port=5000)