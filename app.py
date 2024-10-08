from flask import Flask, render_template,request, redirect, url_for,flash, jsonify
from flask_mysqldb import MySQL 
import os
from datetime import datetime
from MySQLdb import IntegrityError


app=Flask(__name__)
app.secret_key= "secret_key"

app.config['MYSQL_HOST'] ='ghamm-servi-3432.mysql.a.osc-fr1.scalingo-dbs.com'
app.config['MYSQL_PORT'] =34233
app.config['MYSQL_USER'] = 'ghamm_servi_3432'
app.config['MYSQL_PASSWORD'] = '2rLkyXj1hEA-XNyvQDCA' 
app.config['MYSQL_DB'] = 'ghamm_servi_3432'


mysql = MySQL(app)

def custom_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0  # ou une valeur par défaut appropriée
    

# Ajoutez la fonction personnalisée au contexte de l'application
app.jinja_env.globals['custom_int'] = custom_int



from datetime import datetime  # Assurez-vous d'importer datetime

@app.route('/T1', methods=['POST'])
def receive_data():
    print('La fonction est déjà appelée')
    
    # Récupérer les données JSON
    data = request.get_json()
    print("Données reçues:", data)
    
    # Obtenir les valeurs des données sous forme de tuple
    donnees = data.values()
    Tdonnees = tuple(donnees)
    
    # Obtenir la date actuelle
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Ajouter la date au tuple
     # Tdonnees = _donnees + (date,)
    
    print("Tuple de données:", Tdonnees)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO enregistrementmoto (Nom_chauffeur, Proprietaire, Num_moteur, N_chasie, Plaque, Marque, Couleur, secteur, Tel_prop) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", Tdonnees)
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
            cur.execute("SELECT * FROM enregistrementmoto WHERE N_chasie=%s", _donnees)
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
    liste_serial=[]
    chasie = request.args.get('matricule')
    numero_serial = request.args.get('serials')
    donnees = None
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM revendeur ")
    revendeurs= cur.fetchall()
    mysql.connection.commit()
    cur.close()
    for revendeur in revendeurs :
        liste_serial.append(revendeur[3])
        print(revendeur[3])
    
    print(liste_serial)
    print(numero_serial) 
    print(liste_serial[2])
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM enregistrementmoto WHERE N_chasie = '{chasie}'")
    donnees = cur.fetchone()
    print(donnees)
      
    if donnees is None:
        listDon = []
    else:

        cur = mysql.connection.cursor()
        cur.execute("UPDATE enregistrementmoto SET cout_total = cout_total + 500, copteur_versement = copteur_versement + 1, date_lates_paye = %s WHERE N_chasie = %s", (datetime.now(), chasie))
        mysql.connection.commit()
        print(f'taille de la liste est {len(liste_serial)}')
    
    for i in range(len(liste_serial)):
            for liste in liste_serial:
              if liste== numero_serial:
                    print(f'serial POS {i} est {liste}')
                    cur = mysql.connection.cursor()
                    cur.execute(f"UPDATE revendeur SET recette = recette + 500 WHERE  serial = '{liste}'")
                    mysql.connection.commit()
                    cur.close()    
            
                    print('je suis la')
                    listDon= list(donnees)
                    return jsonify(listDon)    
            else:
                    return jsonify('')   
              
                
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
            cur.execute( "SELECT * FROM login WHERE Nom_utilisateur= %s AND Mot_de_passe = %s", donner)
            results = cur.fetchone() 
            print(results)
        except Exception as e:  
            return f"Exeception :{e} "     
        if results == None:
            return redirect(url_for("index_acceuil"))
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM  enregistrementmoto")
            data = cur.fetchall()

           
            cur.execute("SELECT * FROM  revendeur  ")
            revendeur = cur.fetchall()
            print("voici tout le revendeur",revendeur)

 
            cur.execute("SELECT COUNT(*) FROM  enregistrementmoto" )
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
        plaque = request.form['plaque'] 
        marque = request.form['marque']
        coleur = request.form['color']
        locaite = request.form['secteur']
        telephone = request.form['telephone'] 
         
        data = (nom, nom_prop, moteur, chasie, plaque, marque, coleur, locaite, telephone)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO enregistrementmoto (Nom_chauffeur, Proprietaire, Num_moteur, N_chasie, Plaque, Marque, Couleur, secteur, Tel_prop) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", data)

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
        cur.execute(""" UPDATE enregistrementmoto
               SET Nom_chauffeur = %s, Proprietaire = %s, Num_moteur= %s, N_chasie= %s, Marque= %s, Couleur= %s ,secteur= %s,Tel_prop= %s 
               WHERE id=%s """,( nom, nom_prop, moteur, chasie, marque, coleur, localite, telephone, ID))
        flash("Data Updated Successfully")
        mysql.connection.commit()   
        return ("<h1 style ='color: red; font-size: 20px; font-weight: bold; text-align: center;'>Les données sont enregistré avec succes <h1>")

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM enregistrementmoto WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return ("SUCCES")


    
@app.route('/cloture/<int:id>', methods=['GET', 'POST'])
def cloture(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("SELECT recette FROM revendeur WHERE id = %s", (id,))
        rect=cur.fetchone()
        fraisVerser =(request.form.get('recolte'))
        recet=rect[0]
        print("la recette est",rect)
        print("frais a remettre",fraisVerser)
        
        if recet >= 500:
                fraisVerser=int(fraisVerser)
                print(type(rect))
                print(type(fraisVerser))
                if fraisVerser > recet:
                    return "operation_invalide. le montant que vous inserez est trop a la recette de ce commisionnaire" 
                venteJourne = recet - fraisVerser       
                cur.execute(f"UPDATE revendeur SET Dette = Dette +{venteJourne} WHERE id = '{id}'")
                mysql.connection.commit()
                cur.execute("UPDATE revendeur SET recette = %s WHERE id = %s", (0, id))
                mysql.connection.commit()
                print("la dette du client est" , venteJourne)

        else:
             return("aucune recette pour ce commitionaire")
    return {"message": "Erreur : l'utilisateur POS n'a pas recette"} 


@app.route('/desctivePOS/<int:id>', methods=['GET', 'POST'])
def desctivePOS(id):
    if request.method == 'POST':
        fraisVerser =(request.form.get('numPOS'))
        print(fraisVerser, type(fraisVerser))
        if fraisVerser== "0":
            fraisVerser="*"
            cur = mysql.connection.cursor()
            cur.execute("SELECT serial FROM revendeur WHERE id = %s", (id,))
            serial= cur.fetchone()
            serial= serial[0]+str(fraisVerser)
            cur.execute("UPDATE revendeur SET serial = %s WHERE id = %s", (serial, id))
            mysql.connection.commit()
            cur.close()
            print(serial)
            return 'le POS désactiver avec succes '
        elif fraisVerser=="1":
            cur = mysql.connection.cursor()
            cur.execute("SELECT serial FROM revendeur WHERE id = %s", (id,))
            serial= cur.fetchone()
            serial= serial[0].replace('*', '')
            cur.execute("UPDATE revendeur SET serial = %s WHERE id = %s", (serial, id))
            mysql.connection.commit()
            cur.close()
            print(serial)
            return 'le POS activé avec succes '
        else:
            return ' Apuyez sur 0 ou 1 activez soit des activez le POS'

       

        
        

    return 'pos('+ str(id) +')desactivé'


from flask import render_template

@app.route('/detail/<int:id_data>')
def afficher_details_client(id_data):
    print(id_data)
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Nom_chauffeur, cout_total, copteur_versement, date_lates_paye FROM enregistrementmoto WHERE id= %s", (id_data,))
        details = cur.fetchone()
         # Convertir le champ Decimal en une chaîne de caractères formatée
        cout_total_str = "{:,}".format(details[1])  # Utilisez la virgule comme séparateur de milliers

        # Mettez à jour les détails avec la version formatée de cout_total
        details = (details[0], cout_total_str, details[2], details[3])

        print("voici la où extraire les infos détaillées", details)
        return render_template("detail.html", details=details)
    except:
        details = (details[0], 0 , details[2], details[3])
        return render_template("detail.html", details=details)
        
   

from flask import render_template, request, redirect, url_for

@app.route("/cotisation", methods=['POST', 'GET'])
def cotisation():
    if request.method == 'POST':
        chasie = request.form['chasi']
        if len(chasie)!=5:
          return (f'Le numero de chasie doive contenir que "5" caractere numerique. vous vous avez saisi "{len(chasie)}".  modifier puis ressayer ')       
        
        try:   
            cur = mysql.connection.cursor()
            cur.execute(f"SELECT * FROM enregistrementmoto WHERE N_chasie = '{chasie}'")
            donnees = cur.fetchone()
            if donnees is None:
                print('Le numero de chasie n\'a pas été trouvé.')
                # Rediriger l'utilisateur vers une page informant que le numéro de châssis n'a pas été trouvé
                return ('Le numero de chasie n\'a pas été trouvé.')
            else:
                print(donnees)
                # Afficher les données dans la page facture.html
                return render_template("facture.html", data=donnees)
        except:
             # Rediriger l'utilisateur vers une page informant qu'une erreur s'est produite
            return jsonify({"message": "Erreur : N_chasie en liste noire"})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
