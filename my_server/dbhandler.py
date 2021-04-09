import os

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.ext.hybrid import hybrid_method
from my_server import app, db
from PIL import Image, ImageDraw
from sqlalchemy import ForeignKey
import random

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    creator = db.Column(db.String(30))
    rarity = db.Column(db.String(30))
    
    @property
    def serialize(self):
        return {
            'id':       self.id,
            'name':     self.name,
            'creator':  self.creator,
            'rarity':   self.rarity
        }

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, default=1)

    head_id = db.Column(db.Integer, ForeignKey('bit.id'))
    head = relationship('Bit', foreign_keys=[head_id])

    body_id = db.Column(db.Integer, ForeignKey('bit.id'))
    body = relationship('Bit', foreign_keys=[body_id])

    left_arm_id = db.Column(db.Integer, ForeignKey('bit.id'))
    left_arm = relationship('Bit', foreign_keys=[left_arm_id])

    right_arm_id = db.Column(db.Integer, ForeignKey('bit.id'))
    right_arm = relationship('Bit', foreign_keys=[right_arm_id])

    left_leg_id = db.Column(db.Integer, ForeignKey('bit.id'))
    left_leg = relationship('Bit', foreign_keys=[left_leg_id])

    right_leg_id = db.Column(db.Integer, ForeignKey('bit.id'))
    right_leg = relationship('Bit', foreign_keys=[right_leg_id])

    image_file = db.Column(db.String(30))

    @property
    def serialize(self):
        return {
            'id':           self.id,
            'level':        self.level,
            'image_file':   self.image_file,
            'head':         self.head.serialize,
            'body':         self.body.serialize,
            'right_arm':    self.right_arm.serialize,
            'left_arm':     self.left_arm.serialize,
            'right_leg':    self.right_leg.serialize,
            'left_leg':     self.left_leg.serialize
        }

    @property
    def toMetadata(self):
        return {
            'id':       self.id,
            'level':    self.level,
            'image_file': self.image_file,
            'attributes': [
                {
                    "trait_type": "Head", 
                    'value': self.body.name,
                },
                {
                    "trait_type": "Body",
                    'value': self.body.name
                },
                {
                    "trait_type": "Right Arm", 
                    'value': self.right_arm.name,
                },
                {
                    "trait_type": "Left Arm",
                    'value': self.left_arm.name
                },
                {
                    "trait_type": "Right Leg", 
                    'value': self.right_leg.name,
                },
                {
                    "trait_type": "Left Leg",
                    'value': self.left_leg.name
                }
            ]
        }


class Bit(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    part = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship('Category')
    name = db.Column(db.String(30))
    coordinate = db.Column(db.String(64))
    image_file = db.Column(db.String(30))

    @hybrid_method
    def amount(self):
        if self.part == 0:
            return Bot.query.filter(Bot.head_id==self.id).count()
        if self.part == 1:
            return Bot.query.filter(Bot.body_id==self.id).count()
        if self.part == 2:
            return Bot.query.filter(Bot.left_arm_id==self.id).count()
        if self.part == 3:
            return Bot.query.filter(Bot.right_arm_id==self.id).count()
        if self.part == 4:
            return Bot.query.filter(Bot.left_leg_id==self.id).count()
        if self.part == 5:
            return Bot.query.filter(Bot.right_leg_id==self.id).count()

    @property
    def serialize(self):
        return {
            'name':     self.name,
            'image':     self.image_file,
            'category':   self.category.serialize,
            'amount':   self.amount()
        }
    

def resetDB():
    db.drop_all()
    db.create_all()
    categories = [
         Category(id=0, name="AyshaBot",    creator="AyshaArt",     rarity="Common"),
         Category(id=1, name="SmileBot",    creator="Sander",       rarity="Common"),
         Category(id=2, name="TribeBot",    creator="ArtTribe",     rarity="Uncommon"),
         Category(id=3, name="XR-I",        creator="TR",           rarity="Uncommon"),
         Category(id=4, name="XR-II",       creator="TR",           rarity="Rare"),
         Category(id=5, name="DemonBot",    creator="Sander",       rarity="Rare"),

         Bit(part=0, category_id=0, name="AyshaBot Head",    coordinate="[480,650]", image_file="bit-images/aysha/head.png"),
         Bit(part=1, category_id=0, name="AyshaBot Body",    coordinate="[[360,51],[65,315],[700,315],[190,1290],[575,1290]]", image_file="bit-images/aysha/body.png"),
         Bit(part=2, category_id=0, name="AyshaBot Left Arm",coordinate="[480,80]", image_file="bit-images/aysha/l_arm.png"),
         Bit(part=3, category_id=0, name="AyshaBot Right Arm",coordinate="[160,80]", image_file="bit-images/aysha/r_arm.png"),
         Bit(part=4, category_id=0, name="AyshaBot Left Leg",coordinate="[335,70]", image_file="bit-images/aysha/l_leg.png"),
         Bit(part=5, category_id=0, name="AyshaBot Right Leg",coordinate="[250,100]", image_file="bit-images/aysha/r_leg.png"),

         Bit(part=0, category_id=1, name="SmileBot Head",    coordinate="[205,455]", image_file="bit-images/sander1/head.png"),
         Bit(part=1, category_id=1, name="SmileBot Body",    coordinate="[[860,60],[290,340],[1280,490],[530,1280],[990,1280]]", image_file="bit-images/sander1/body.png"),
         Bit(part=2, category_id=1, name="SmileBot Left Arm",coordinate="[350,130]", image_file="bit-images/sander1/l_arm.png"),
         Bit(part=3, category_id=1, name="SmileBot Right Arm",coordinate="[125,130]", image_file="bit-images/sander1/r_arm.png"),
         Bit(part=4, category_id=1, name="SmileBot Left Leg",coordinate="[290,150]", image_file="bit-images/sander1/l_leg.png"),
         Bit(part=5, category_id=1, name="SmileBot Right Leg",coordinate="[150,150]", image_file="bit-images/sander1/r_leg.png"),

         Bit(part=0, category_id=2, name="TribeBot Head",    coordinate="[715,670]", image_file="bit-images/artribe/head.png"),
         Bit(part=1, category_id=2, name="TribeBot Body",    coordinate="[[790,60],[400,500],[1170,500],[610,1340],[970,1340]]", image_file="bit-images/artribe/body.png"),
         Bit(part=2, category_id=2, name="TribeBot Left Arm",coordinate="[360,100]", image_file="bit-images/artribe/l_arm.png"),
         Bit(part=3, category_id=2, name="TribeBot Right Arm",coordinate="[185,90]", image_file="bit-images/artribe/r_arm.png"),
         Bit(part=4, category_id=2, name="TribeBot Left Leg",coordinate="[365,90]", image_file="bit-images/artribe/l_leg.png"),
         Bit(part=5, category_id=2, name="TribeBot Right Leg",coordinate="[190,100]", image_file="bit-images/artribe/r_leg.png"),

         Bit(part=0, category_id=3, name="XR-I Head",    coordinate="[350,570]", image_file="bit-images/xr1/head.png"),
         Bit(part=1, category_id=3, name="XR-I Body",    coordinate="[[495,5],[40,250],[950,250],[330,1100],[660,1100]]", image_file="bit-images/xr1/body.png"),
         Bit(part=2, category_id=3, name="XR-I Left Arm",coordinate="[560,500]", image_file="bit-images/xr1/l_arm.png"),
         Bit(part=3, category_id=3, name="XR-I Right Arm",coordinate="[120,500]", image_file="bit-images/xr1/r_arm.png"),
         Bit(part=4, category_id=3, name="XR-I Left Leg",coordinate="[550,120]", image_file="bit-images/xr1/l_leg.png"),
         Bit(part=5, category_id=3, name="XR-I Right Leg",coordinate="[150,130]", image_file="bit-images/xr1/r_leg.png"),

         Bit(part=0, category_id=4, name="XR-2 Head",    coordinate="[350,570]", image_file="bit-images/xr2/head.png"),
         Bit(part=1, category_id=4, name="XR-2 Body",    coordinate="[[500,80],[70,255],[930,255],[300,1060],[700,1060]]", image_file="bit-images/xr2/body.png"),
         Bit(part=2, category_id=4, name="XR-2 Left Arm",coordinate="[560,500]", image_file="bit-images/xr2/l_arm.png"),
         Bit(part=3, category_id=4, name="XR-2 Right Arm",coordinate="[120,500]", image_file="bit-images/xr2/r_arm.png"),
         Bit(part=4, category_id=4, name="XR-2 Left Leg",coordinate="[550,120]", image_file="bit-images/xr2/l_leg.png"),
         Bit(part=5, category_id=4, name="XR-2 Right Leg",coordinate="[150,130]", image_file="bit-images/xr2/r_leg.png"),

         Bit(part=0, category_id=5, name="DemonBot Head",    coordinate="[260,500]", image_file="bit-images/sander2/head.png"),
         Bit(part=1, category_id=5, name="DemonBot Body",    coordinate="[[700,50],[90,350],[1330,330],[540,1130],[870,1130]]", image_file="bit-images/sander2/body.png"),
         Bit(part=2, category_id=5, name="DemonBot Left Arm",coordinate="[370,100]", image_file="bit-images/sander2/l_arm.png"),
         Bit(part=3, category_id=5, name="DemonBot Right Arm",coordinate="[100,100]", image_file="bit-images/sander2/r_arm.png"),
         Bit(part=4, category_id=5, name="DemonBot Left Leg",coordinate="[330,90]", image_file="bit-images/sander2/l_leg.png"),
         Bit(part=5, category_id=5, name="DemonBot Right Leg",coordinate="[120,90]", image_file="bit-images/sander2/r_leg.png"),
    ]
    db.session.bulk_save_objects(categories)
    db.session.commit()
    return Bit.query.filter_by(category_id=2, part=1).first().serialize

def create_all():
    db.create_all()

def get_bit(part, category):
    data = Bit.query.filter(Bit.category_id==category, Bit.part==part).first()
    return data

def add_bot(id, level, head_id, body_id, rarm_id, larm_id, lleg_id, rleg_id):
    head =      get_bit(0, head_id)
    body =      get_bit(1, body_id)
    left_arm =  get_bit(2, larm_id)
    right_arm = get_bit(3, rarm_id)
    left_leg =  get_bit(4, lleg_id)
    right_leg = get_bit(5, rleg_id)
    create_pic(id, head, body, left_arm, right_arm, left_leg, right_leg)
    
    new = Bot(id = id, level=level, head_id=head.id, body_id=body.id, right_arm_id=right_arm.id, left_arm_id=left_arm.id, left_leg_id=left_leg.id, right_leg_id=right_leg.id, image_file=str(id) + ".PNG")
    db.session.add(new)
    db.session.commit()
    return new
    
def create_pic(bot_id, head, body, left_arm, right_arm, left_leg, right_leg, debug=False):
    head_img =      Image.open("my_server/static/" + head.image_file)
    body_img =      Image.open("my_server/static/" + body.image_file)
    right_arm_img = Image.open("my_server/static/" + right_arm.image_file)
    left_arm_img =  Image.open("my_server/static/" + left_arm.image_file)
    right_leg_img = Image.open("my_server/static/" + right_leg.image_file)
    left_leg_img =  Image.open("my_server/static/" + left_leg.image_file)

    body_coords = eval(body.coordinate)
    print(body_coords[2])

    generated_image = Image.new('RGBA', (2048, 3372), (0, 0, 0, 0))
    width_to_edge = int(generated_image.size[0]/2) - int(body_img.size[0]/2)
    generated_image.paste(left_arm_img,     (width_to_edge+body_coords[1][0]-eval(left_arm.coordinate)[0], 672+body_coords[1][1]-eval(left_arm.coordinate)[1]), left_arm_img)
    generated_image.paste(right_arm_img,    (width_to_edge+body_coords[2][0]-eval(right_arm.coordinate)[0], 672+body_coords[2][1]-eval(right_arm.coordinate)[1]), right_arm_img)
    generated_image.paste(left_leg_img,     (width_to_edge+body_coords[3][0]-eval(left_leg.coordinate)[0], 672+body_coords[3][1]-eval(left_leg.coordinate)[1]), left_leg_img)
    generated_image.paste(right_leg_img,    (width_to_edge+body_coords[4][0]-eval(right_leg.coordinate)[0], 672+body_coords[4][1]-eval(right_leg.coordinate)[1]), right_leg_img)
    generated_image.paste(body_img,         (width_to_edge, 672), body_img)
    generated_image.paste(head_img,         (width_to_edge+body_coords[0][0]-eval(head.coordinate)[0], 672+body_coords[0][1]-eval(head.coordinate)[1]), head_img)

    if debug:
        generated_image.show()
    else:
        generated_image.save(os.path.join(app.root_path, "static\\bots-images\\", str(bot_id) + ".PNG"))

def debug_pic(head_id, body_id, larm_id, rarm_id, lleg_id, rleg_id):
    head =      get_bit(0, head_id)
    body =      get_bit(1, body_id)
    left_arm =  get_bit(2, larm_id)
    right_arm = get_bit(3, rarm_id)
    left_leg =  get_bit(4, lleg_id)
    right_leg = get_bit(5, rleg_id)
    create_pic(id, head, body, left_arm, right_arm, left_leg, right_leg, True)

def decide_points(type, c_id, points):
    part = get_bit(type, c_id)
    generatedImg = Image.open("my_server/static/" + part.image_file)
    draw = ImageDraw.Draw(generatedImg)
    for point in points:
        draw.ellipse((point[0]-10, point[1]-10, point[0]+10, point[1]+10), fill=(255, 0, 0))
    generatedImg.show()


def get_bots():
    bots = Bot.query.all()
    return bots

def get_bot(id):
    bot = Bot.query.filter(Bot.id == id).first()
    return bot
