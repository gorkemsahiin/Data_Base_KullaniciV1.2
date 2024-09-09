from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager ,create_access_token ,jwt_required ,get_jwt_identity
from flask_migrate import Migrate

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key' 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1800


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kullanici_model_owner:o1Ba0DtgARUp@ep-lively-block-a57av5fv.us-east-2.aws.neon.tech/kullanici_model?sslmode=require'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Kullanici(db.Model):
    __tablename__ = 'Kullanicilar'

    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String(80), nullable=False)
    soyisim = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telno = db.Column(db.String(20), nullable=False)

@app.route('/kayit', methods=['POST'])
def kayit():
    try:
        data = request.get_json()
        isim = data.get('isim')
        soyisim = data.get('soyisim')
        email = data.get('email')
        telno = data.get('telefon numarasi')

        yeni_kullanici = Kullanici(isim=isim, soyisim=soyisim, email=email, telno=telno)
        db.session.add(yeni_kullanici)
        db.session.commit()

        return jsonify({"message": "Kayıt oldun"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/login' , methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        telno = data.get('telefon numarasi')
        isim = data.get('isim')
        soyisim = data.get('soyisim')

        kullanici = Kullanici.query.filter_by(
            email=email,
            telno=telno,
            isim=isim,
            soyisim=soyisim,
        ).first()

        if not kullanici:
            return jsonify({"msg" :"yanlıs girdiniz"}), 401
        
        access_token = create_access_token(identity=kullanici.email)

        return jsonify(access_token=access_token), 200
    
    except Exception as e:
        return jsonify({"Hata":str(e)})
    
    @app.route('/protected',methods=['GET'])
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
    
        


@app.route('/kayitgetir', methods=['GET'])
@jwt_required()
def kayitgetir():
    try:  
        kullanicilar = Kullanici.query.all()
        sonuc = []

        for kullanici in kullanicilar:
            sonuc.append({
                "isim": kullanici.isim,
                "soyisim": kullanici.soyisim,
                "email": kullanici.email,
                "telefon numarasi": kullanici.telno
            })

        return jsonify({"content": sonuc})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
        app.run(debug=True)
