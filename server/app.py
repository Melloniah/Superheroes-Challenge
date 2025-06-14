from flask import Flask
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
# connection string to the datbase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
# Prevent SQLAlchemy from tracking all modifications in orde to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

#DISPLAY ALL HEROES
@app.route('/heroes', methods=['GET'])
def get_all_heroes():
    try:
        heroes=Hero.query.all()

        return jsonify([hero.Serialize() for hero in heroes]), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve heroes", "message": str(e)}), 500 



#SEARCH HEROES BY ID
@app.route('/heroes/<int=id>', methods=['GET'])  
def get_heroes_by_id(id):
    try:
        hero=Hero.query.get(id)
        if not hero:
            return  jsonify({"error": "Hero not found"}), 404

        return jsonify(hero.Serialize()), 200
    except Exception as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500    



#DISPLAY ALL POWERS
@app.route('/powers', methods=['GET'])
def get_all_powers(): 
    try:
        powers=Power.query.all()
        return jsonify([power.Serialize() for power in powers]), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve any powers", "message": str(e)}), 500

#SEARCH POWERS BY ID
@app.route('/powers/<int=id>', methods=['GET'])  
def get_powers_by_id(id):
    try:
        power=Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404

        return jsonify(power.Serialize()), 200
    except Exception as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500     
        
#PATCH FOR POWERS/ID
@app.route('/powers/<int:id>'methods=['PATCH'])  
def update_power_description(id):
    power=Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    try:
        data=request.get_json()
        new_description=data.get('description')

        if not new_description or len(new_description)<10:
            return jsonify({"errors": ["Description must be at least 10 characters."]}), 400

        power.description=new_description
        db.session.commit()
         
        return jsonify(power.Serialize()), 200 
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400    


#POST FOR HEROPOWER
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()

        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        if not strength or not power_id or not hero_id:
            return jsonify({"errors": ["All fields (strength, power_id, hero_id) are required."]}), 400

        # Validating relationships
        power = Power.query.get(power_id)
        hero = Hero.query.get(hero_id)

        if not power or not hero:
            return jsonify({"errors": ["Invalid hero_id or power_id."]}), 400

        hero_power = HeroPower(
            strength=strength,
            hero_id=hero_id,
            power_id=power_id
        )

        db.session.add(hero_power)
        db.session.commit()

        # Respond with nested hero and power data
        response = {
            "id": hero_power.id,
            "hero_id": hero_id,
            "power_id": power_id,
            "strength": strength,
            "hero": hero.Serialize(),   
            "power": power.Serialize()  
        }

        return jsonify(response), 201

    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400




if __name__ == '__main__':
    app.run(port=5555, debug=True)