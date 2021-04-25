import os

from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
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
    made_from = relationship("BotRelationship",)
    burnt = db.Column(db.Boolean, unique=False, default=False)

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

    @hybrid_property
    def toMetadata(self):
        attributes = [
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
        if self.head.category.id == self.body.category.id and self.head.category.id == self.left_arm.category.id and self.head.category.id == self.right_arm.category.id and self.head.category.id == self.left_leg.category.id and self.head.category.id == self.right_leg.category.id:
            attributes.append(
                {
                    "trait_type": "Complete", 
                    'value': self.body.category.name,
                }
            )
        
        return {
            'id':       self.id,
            'level':    self.level,
            'image_file': self.image_file,
            'attributes': attributes
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
            return Bot.query.filter(Bot.head_id==self.id, Bot.burnt==False).count()
        if self.part == 1:
            return Bot.query.filter(Bot.body_id==self.id, Bot.burnt==False).count()
        if self.part == 2:
            return Bot.query.filter(Bot.left_arm_id==self.id, Bot.burnt==False).count()
        if self.part == 3:
            return Bot.query.filter(Bot.right_arm_id==self.id, Bot.burnt==False).count()
        if self.part == 4:
            return Bot.query.filter(Bot.left_leg_id==self.id, Bot.burnt==False).count()
        if self.part == 5:
            return Bot.query.filter(Bot.right_leg_id==self.id, Bot.burnt==False).count()

    @property
    def serialize(self):
        return {
            'name':     self.name,
            'image':     self.image_file,
            'category':   self.category.serialize,
            'amount':   self.amount()
        }
    
def ifThenReturnSerialize(value):
    if value:
        return value.serialize()
    return None

class BotRelationship(db.Model):
    owner_id = db.Column(db.Integer, db.ForeignKey('bot.id'), primary_key=True)
    made_from_1 = db.Column(db.Integer)
    made_from_2 = db.Column(db.Integer)

    @hybrid_method
    def serialize(self):
        return {
            'owner' : self.owner_id,
            'mf_1'  : self.made_from_1,
            'mf_2'  : self.made_from_2,
            'from1': ifThenReturnSerialize(BotRelationship.query.filter(BotRelationship.owner_id==self.made_from_1).first()),
            'from2': ifThenReturnSerialize(BotRelationship.query.filter(BotRelationship.owner_id==self.made_from_2).first())
        }

def combined(owner, mf1, mf2):
    new = BotRelationship(owner_id=owner, made_from_1=mf1, made_from_2=mf2)
    get_bot(mf1).burnt = True
    get_bot(mf2).burnt = True
    db.session.add(new)
    db.session.commit()
    

def resetDB():
    db.drop_all()
    db.create_all()
    categories = [
        Category(id=0,  name="AyshaBot",    creator="AyshaArt",     rarity="Common"),
        Category(id=1,  name="Humunculus",  creator="Sander",       rarity="Common"),
        Category(id=2,  name="XR-I",        creator="TR",           rarity="Common"),
        Category(id=3,  name="TribeBot",    creator="ArtTribe",     rarity="Common"),
        Category(id=4,  name="Goblin",      creator="TR",           rarity="Common"),
        Category(id=5,  name="SmileBot",    creator="Sander",       rarity="Common"),
        Category(id=6,  name="Golem",       creator="TR",           rarity="Common"),
        Category(id=7,  name="RavenBot",    creator="Ferjart",      rarity="Common"),
        Category(id=8,  name="ArtBot",      creator="AyshaArt",     rarity="Uncommon"),
        Category(id=9,  name="XR-II",       creator="TR",           rarity="Uncommon"),
        Category(id=10, name="DemonBot",    creator="Sander",       rarity="Uncommon"),
        Category(id=11, name="PunkBot",     creator="Chabusan",     rarity="Uncommon"),
        Category(id=12, name="BugBot",      creator="ArtTribe",     rarity="Uncommon"),
        Category(id=13, name="Cyclops",     creator="TR",           rarity="Uncommon"),
        Category(id=14, name="Etherbot",    creator="Ferjart",      rarity="Uncommon"),
        Category(id=15, name="Scuboid",     creator="AyshaArt",     rarity="Rare"),
        Category(id=16, name="Weeabot",     creator="Ferjart",      rarity="Rare"),
        Category(id=17, name="Samuroid",    creator="TR",           rarity="Rare"),
        Category(id=18, name="SwampBot",    creator="Sander",       rarity="Rare"),
        Category(id=19, name="XR-800",      creator="TR",           rarity="Rare"),
        Category(id=20, name="Mantis",      creator="Chabusan",     rarity="Epic"),
        Category(id=21, name="Anubit",      creator="TR",           rarity="Epic"),
        Category(id=22, name="Onibot",      creator="ArtTribe",     rarity="Epic"),
        Category(id=23, name="SefreePoh",   creator="TR",           rarity="Epic"),
        Category(id=24, name="AlienBot",    creator="Chabusan",     rarity="Legendary"),
        Category(id=25, name="GodBot",      creator="Chabusan",     rarity="Legendary"),
        Category(id=26, name="Junkyard King",creator="MisterXCV",   rarity="Legendary"),
        
        
        

        Bit(part=0, category_id=0, name="AyshaBot Head",    coordinate="[400,530]", image_file="bit-images/aysha/head.png"),
        Bit(part=1, category_id=0, name="AyshaBot Body",    coordinate="[[360,51],[65,315],[700,315],[190,1290],[575,1290], True]", image_file="bit-images/aysha/body.png"),
        Bit(part=2, category_id=0, name="AyshaBot Left Arm",coordinate="[480,80]", image_file="bit-images/aysha/l_arm.png"),
        Bit(part=3, category_id=0, name="AyshaBot Right Arm",coordinate="[160,80]", image_file="bit-images/aysha/r_arm.png"),
        Bit(part=4, category_id=0, name="AyshaBot Left Leg",coordinate="[335,70]", image_file="bit-images/aysha/l_leg.png"),
        Bit(part=5, category_id=0, name="AyshaBot Right Leg",coordinate="[250,100]", image_file="bit-images/aysha/r_leg.png"),

        Bit(part=0, category_id=1, name="Humunculus Head",    coordinate="[260,500]", image_file="bit-images/sander2/head.png"),
        Bit(part=1, category_id=1, name="Humunculus Body",    coordinate="[[700,50],[240,350],[1180,350],[540,1130],[870,1130], True]", image_file="bit-images/sander2/body.png"),
        Bit(part=2, category_id=1, name="Humunculus Left Arm",coordinate="[370,100]", image_file="bit-images/sander2/l_arm.png"),
        Bit(part=3, category_id=1, name="Humunculus Right Arm",coordinate="[100,100]", image_file="bit-images/sander2/r_arm.png"),
        Bit(part=4, category_id=1, name="Humunculus Left Leg",coordinate="[330,90]", image_file="bit-images/sander2/l_leg.png"),
        Bit(part=5, category_id=1, name="Humunculus Right Leg",coordinate="[120,90]", image_file="bit-images/sander2/r_leg.png"),

        Bit(part=0, category_id=2, name="XR-I Head",    coordinate="[350,570]", image_file="bit-images/xr1/head.png"),
        Bit(part=1, category_id=2, name="XR-I Body",    coordinate="[[495,5],[40,250],[950,250],[330,1100],[660,1100], True]", image_file="bit-images/xr1/body.png"),
        Bit(part=2, category_id=2, name="XR-I Left Arm",coordinate="[560,500]", image_file="bit-images/xr1/l_arm.png"),
        Bit(part=3, category_id=2, name="XR-I Right Arm",coordinate="[120,500]", image_file="bit-images/xr1/r_arm.png"),
        Bit(part=4, category_id=2, name="XR-I Left Leg",coordinate="[550,120]", image_file="bit-images/xr1/l_leg.png"),
        Bit(part=5, category_id=2, name="XR-I Right Leg",coordinate="[150,130]", image_file="bit-images/xr1/r_leg.png"),

        Bit(part=0, category_id=3, name="TribeBot Head",    coordinate="[715,670]", image_file="bit-images/artribe/head.png"),
        Bit(part=1, category_id=3, name="TribeBot Body",    coordinate="[[790,60],[400,500],[1170,500],[610,1340],[970,1340], True]", image_file="bit-images/artribe/body.png"),
        Bit(part=2, category_id=3, name="TribeBot Left Arm",coordinate="[450,125]", image_file="bit-images/artribe/l_arm.png"),
        Bit(part=3, category_id=3, name="TribeBot Right Arm",coordinate="[90,135]", image_file="bit-images/artribe/r_arm.png"),
        Bit(part=4, category_id=3, name="TribeBot Left Leg",coordinate="[365,90]", image_file="bit-images/artribe/l_leg.png"),
        Bit(part=5, category_id=3, name="TribeBot Right Leg",coordinate="[190,100]", image_file="bit-images/artribe/r_leg.png"),

        Bit(part=0, category_id=4, name="Goblin Head",    coordinate="[350,475]", image_file="bit-images/xr3/head.png"),
        Bit(part=1, category_id=4, name="Goblin Body",    coordinate="[[500,75],[90,200],[930,200],[300,1120],[700,1120], True]", image_file="bit-images/xr3/body.png"),
        Bit(part=2, category_id=4, name="Goblin Left Arm",coordinate="[470,530]", image_file="bit-images/xr3/l_arm.png"),
        Bit(part=3, category_id=4, name="Goblin Right Arm",coordinate="[220,530]", image_file="bit-images/xr3/r_arm.png"),
        Bit(part=4, category_id=4, name="Goblin Left Leg",coordinate="[600,80]", image_file="bit-images/xr3/l_leg.png"),
        Bit(part=5, category_id=4, name="Goblin Right Leg",coordinate="[320,80]", image_file="bit-images/xr3/r_leg.png"),

        Bit(part=0, category_id=5, name="SmileBot Head",    coordinate="[205,455]", image_file="bit-images/sander1/head.png"),
        Bit(part=1, category_id=5, name="SmileBot Body",    coordinate="[[860,60],[290,340],[1280,490],[530,1280],[990,1280], True]", image_file="bit-images/sander1/body.png"),
        Bit(part=2, category_id=5, name="SmileBot Left Arm",coordinate="[350,130]", image_file="bit-images/sander1/l_arm.png"),
        Bit(part=3, category_id=5, name="SmileBot Right Arm",coordinate="[125,130]", image_file="bit-images/sander1/r_arm.png"),
        Bit(part=4, category_id=5, name="SmileBot Left Leg",coordinate="[290,150]", image_file="bit-images/sander1/l_leg.png"),
        Bit(part=5, category_id=5, name="SmileBot Right Leg",coordinate="[150,150]", image_file="bit-images/sander1/r_leg.png"),

        Bit(part=0, category_id=6, name="Golem Head",    coordinate="[350,600]", image_file="bit-images/xr7/head.png"),
        Bit(part=1, category_id=6, name="Golem Body",    coordinate="[[500,200],[100,270],[920,270],[370,1100],[660,1100], True]", image_file="bit-images/xr7/body.png"),
        Bit(part=2, category_id=6, name="Golem Left Arm",coordinate="[575,500]", image_file="bit-images/xr7/l_arm.png"),
        Bit(part=3, category_id=6, name="Golem Right Arm",coordinate="[120,500]", image_file="bit-images/xr7/r_arm.png"),
        Bit(part=4, category_id=6, name="Golem Left Leg",coordinate="[740,60]", image_file="bit-images/xr7/l_leg.png"),
        Bit(part=5, category_id=6, name="Golem Right Leg",coordinate="[220,60]", image_file="bit-images/xr7/r_leg.png"),

        Bit(part=0, category_id=7, name="Raven Head",    coordinate="[200,420]", image_file="bit-images/ravenbot/head.png"),
        Bit(part=1, category_id=7, name="Raven Body",    coordinate="[[540,100],[210,500],[840,500],[410,1260],[700,1260], True]", image_file="bit-images/ravenbot/body.png"),
        Bit(part=2, category_id=7, name="Raven Left Arm",coordinate="[520,80]", image_file="bit-images/ravenbot/l_arm.png"),
        Bit(part=3, category_id=7, name="Raven Right Arm",coordinate="[90,80]", image_file="bit-images/ravenbot/r_arm.png"),
        Bit(part=4, category_id=7, name="Raven Left Leg",coordinate="[430,140]", image_file="bit-images/ravenbot/l_leg.png"),
        Bit(part=5, category_id=7, name="Raven Right Leg",coordinate="[130,140]", image_file="bit-images/ravenbot/r_leg.png"),

        Bit(part=0, category_id=8, name="ArtBot Head",    coordinate="[400,660]", image_file="bit-images/aysha2/head.png"),
        Bit(part=1, category_id=8, name="ArtBot Body",    coordinate="[[765,80],[270,580],[1270,580],[620,1160],[900,1160], True]", image_file="bit-images/aysha2/body.png"),
        Bit(part=2, category_id=8, name="ArtBot Left Arm",coordinate="[370,100]", image_file="bit-images/aysha2/l_arm.png"),
        Bit(part=3, category_id=8, name="ArtBot Right Arm",coordinate="[120,100]", image_file="bit-images/aysha2/r_arm.png"),
        Bit(part=4, category_id=8, name="ArtBot Left Leg",coordinate="[440,130]", image_file="bit-images/aysha2/l_leg.png"),
        Bit(part=5, category_id=8, name="ArtBot Right Leg",coordinate="[160,140]", image_file="bit-images/aysha2/r_leg.png"),

        Bit(part=0, category_id=9, name="XR-II Head",    coordinate="[350,570]", image_file="bit-images/xr2/head.png"),
        Bit(part=1, category_id=9, name="XR-II Body",    coordinate="[[500,80],[70,255],[930,255],[300,1060],[700,1060], True]", image_file="bit-images/xr2/body.png"),
        Bit(part=2, category_id=9, name="XR-II Left Arm",coordinate="[560,500]", image_file="bit-images/xr2/l_arm.png"),
        Bit(part=3, category_id=9, name="XR-II Right Arm",coordinate="[120,500]", image_file="bit-images/xr2/r_arm.png"),
        Bit(part=4, category_id=9, name="XR-II Left Leg",coordinate="[550,120]", image_file="bit-images/xr2/l_leg.png"),
        Bit(part=5, category_id=9, name="XR-II Right Leg",coordinate="[150,130]", image_file="bit-images/xr2/r_leg.png"),

        Bit(part=0, category_id=10, name="Demon Head",    coordinate="[200,450]", image_file="bit-images/sander3/head.png"),
        Bit(part=1, category_id=10, name="Demon Body",    coordinate="[[600,70],[210,240],[1000,240],[460,1120],[740,1120], True]", image_file="bit-images/sander3/body.png"),
        Bit(part=2, category_id=10, name="Demon Left Arm",coordinate="[230,130]", image_file="bit-images/sander3/l_arm.png"),
        Bit(part=3, category_id=10, name="Demon Right Arm",coordinate="[80,130]", image_file="bit-images/sander3/r_arm.png"),
        Bit(part=4, category_id=10, name="Demon Left Leg",coordinate="[300,90]", image_file="bit-images/sander3/l_leg.png"),
        Bit(part=5, category_id=10, name="Demon Right Leg",coordinate="[130,90]", image_file="bit-images/sander3/r_leg.png"),

        Bit(part=0, category_id=11, name="Punkbot Head",    coordinate="[165,480]", image_file="bit-images/punkbot/head.png"),
        Bit(part=1, category_id=11, name="Punkbot Body",    coordinate="[[445,130],[80,350],[800,350],[220,1180],[600,1190], False]", image_file="bit-images/punkbot/body.png"),
        Bit(part=2, category_id=11, name="Punkbot Left Arm",coordinate="[380,150]", image_file="bit-images/punkbot/l_arm.png"),
        Bit(part=3, category_id=11, name="Punkbot Right Arm",coordinate="[100,160]", image_file="bit-images/punkbot/r_arm.png"),
        Bit(part=4, category_id=11, name="Punkbot Left Leg",coordinate="[315,110]", image_file="bit-images/punkbot/l_leg.png"),
        Bit(part=5, category_id=11, name="Punkbot Right Leg",coordinate="[170,110]", image_file="bit-images/punkbot/r_leg.png"),

        Bit(part=0, category_id=12, name="BugBot Head",    coordinate="[490,610]", image_file="bit-images/artribe3/head.png"),
        Bit(part=1, category_id=12, name="BugBot Body",    coordinate="[[950,120],[350,530],[1500,530],[730,1420],[1160,1420], True]", image_file="bit-images/artribe3/body.png"),
        Bit(part=2, category_id=12, name="BugBot Left Arm",coordinate="[290,160]", image_file="bit-images/artribe3/l_arm.png"),
        Bit(part=3, category_id=12, name="BugBot Right Arm",coordinate="[180,170]", image_file="bit-images/artribe3/r_arm.png"),
        Bit(part=4, category_id=12, name="BugBot Left Leg",coordinate="[400,130]", image_file="bit-images/artribe3/l_leg.png"),
        Bit(part=5, category_id=12, name="BugBot Right Leg",coordinate="[230,120]", image_file="bit-images/artribe3/r_leg.png"),

        Bit(part=0, category_id=13, name="Cyclops Head",    coordinate="[350,560]", image_file="bit-images/xr4/head.png"),
        Bit(part=1, category_id=13, name="Cyclops Body",    coordinate="[[500,100],[90,200],[930,200],[300,1120],[700,1120], True]", image_file="bit-images/xr4/body.png"),
        Bit(part=2, category_id=13, name="Cyclops Left Arm",coordinate="[470,530]", image_file="bit-images/xr4/l_arm.png"),
        Bit(part=3, category_id=13, name="Cyclops Right Arm",coordinate="[220,530]", image_file="bit-images/xr4/r_arm.png"),
        Bit(part=4, category_id=13, name="Cyclops Left Leg",coordinate="[660,80]", image_file="bit-images/xr4/l_leg.png"),
        Bit(part=5, category_id=13, name="Cyclops Right Leg",coordinate="[250,80]", image_file="bit-images/xr4/r_leg.png"),

        Bit(part=0, category_id=14, name="Etherbot Head",    coordinate="[270,450]", image_file="bit-images/etherbot/head.png"),
        Bit(part=1, category_id=14, name="Etherbot Body",    coordinate="[[430,120],[125,440],[715,440],[260,1320],[560,1320], True]", image_file="bit-images/etherbot/body.png"),
        Bit(part=2, category_id=14, name="Etherbot Left Arm",coordinate="[480,80]", image_file="bit-images/etherbot/l_arm.png"),
        Bit(part=3, category_id=14, name="Etherbot Right Arm",coordinate="[90,80]", image_file="bit-images/etherbot/r_arm.png"),
        Bit(part=4, category_id=14, name="Etherbot Left Leg",coordinate="[350,150]", image_file="bit-images/etherbot/l_leg.png"),
        Bit(part=5, category_id=14, name="Etherbot Right Leg",coordinate="[125,150]", image_file="bit-images/etherbot/r_leg.png"),

        Bit(part=0, category_id=15, name="Scuba Head",    coordinate="[320,550]", image_file="bit-images/aysha3/head.png"),
        Bit(part=1, category_id=15, name="Scuba Body",    coordinate="[[625,190],[162,435],[1100,435],[475,1090],[785,1090], True]", image_file="bit-images/aysha3/body.png"),
        Bit(part=2, category_id=15, name="Scuba Left Arm",coordinate="[390,90]", image_file="bit-images/aysha3/l_arm.png"),
        Bit(part=3, category_id=15, name="Scuba Right Arm",coordinate="[150,90]", image_file="bit-images/aysha3/r_arm.png"),
        Bit(part=4, category_id=15, name="Scuba Left Leg",coordinate="[350,140]", image_file="bit-images/aysha3/l_leg.png"),
        Bit(part=5, category_id=15, name="Scuba Right Leg",coordinate="[210,150]", image_file="bit-images/aysha3/r_leg.png"),

        Bit(part=0, category_id=16, name="Weeabot Head",    coordinate="[280,540]", image_file="bit-images/weeabot/head.png"),
        Bit(part=1, category_id=16, name="Weeabot Body",    coordinate="[[400,150],[55,450],[750,450],[260,1220],[560,1220], True]", image_file="bit-images/weeabot/body.png"),
        Bit(part=2, category_id=16, name="Weeabot Left Arm",coordinate="[550,200]", image_file="bit-images/weeabot/l_arm.png"),
        Bit(part=3, category_id=16, name="Weeabot Right Arm",coordinate="[90,200]", image_file="bit-images/weeabot/r_arm.png"),
        Bit(part=4, category_id=16, name="Weeabot Left Leg",coordinate="[380,190]", image_file="bit-images/weeabot/l_leg.png"),
        Bit(part=5, category_id=16, name="Weeabot Right Leg",coordinate="[130,190]", image_file="bit-images/weeabot/r_leg.png"),

        Bit(part=0, category_id=17, name="Samuroid Head",    coordinate="[350,620]", image_file="bit-images/xr5/head.png"),
        Bit(part=1, category_id=17, name="Samuroid Body",    coordinate="[[500,80],[95,350],[910,350],[330,1150],[670,1150], True]", image_file="bit-images/xr5/body.png"),
        Bit(part=2, category_id=17, name="Samuroid Left Arm",coordinate="[500,560]", image_file="bit-images/xr5/l_arm.png"),
        Bit(part=3, category_id=17, name="Samuroid Right Arm",coordinate="[200,570]", image_file="bit-images/xr5/r_arm.png"),
        Bit(part=4, category_id=17, name="Samuroid Left Leg",coordinate="[590,80]", image_file="bit-images/xr5/l_leg.png"),
        Bit(part=5, category_id=17, name="Samuroid Right Leg",coordinate="[230,100]", image_file="bit-images/xr5/r_leg.png"),

        Bit(part=0, category_id=18, name="SwampBot Head",    coordinate="[195,435]", image_file="bit-images/sander4/head.png"),
        Bit(part=1, category_id=18, name="SwampBot Body",    coordinate="[[640,80],[150,360],[1100,370],[480,1200],[800,1200], True]", image_file="bit-images/sander4/body.png"),
        Bit(part=2, category_id=18, name="SwampBot Left Arm",coordinate="[180,80]", image_file="bit-images/sander4/l_arm.png"),
        Bit(part=3, category_id=18, name="SwampBot Right Arm",coordinate="[90,170]", image_file="bit-images/sander4/r_arm.png"),
        Bit(part=4, category_id=18, name="SwampBot Left Leg",coordinate="[310,60]", image_file="bit-images/sander4/l_leg.png"),
        Bit(part=5, category_id=18, name="SwampBot Right Leg",coordinate="[100,70]", image_file="bit-images/sander4/r_leg.png"),

        Bit(part=0, category_id=19, name="XR-800 Head",    coordinate="[350,550]", image_file="bit-images/xr800/head.png"),
        Bit(part=1, category_id=19, name="XR-800 Body",    coordinate="[[480,30],[90,190],[870,210],[270,1140],[700,1140], False]", image_file="bit-images/xr800/body.png"),
        Bit(part=2, category_id=19, name="XR-800 Left Arm",coordinate="[490,305]", image_file="bit-images/xr800/l_arm.png"),
        Bit(part=3, category_id=19, name="XR-800 Right Arm",coordinate="[205,310]", image_file="bit-images/xr800/r_arm.png"),
        Bit(part=4, category_id=19, name="XR-800 Left Leg",coordinate="[550,75]", image_file="bit-images/xr800/l_leg.png"),
        Bit(part=5, category_id=19, name="XR-800 Right Leg",coordinate="[400,75]", image_file="bit-images/xr800/r_leg.png"),

        Bit(part=0, category_id=20, name="Mantis Head",    coordinate="[325,430]", image_file="bit-images/mantis/head.png"),
        Bit(part=1, category_id=20, name="Mantis Body",    coordinate="[[765,30],[290,290],[1200,290],[580,1130],[920,1120], True]", image_file="bit-images/mantis/body.png"),
        Bit(part=2, category_id=20, name="Mantis Left Arm",coordinate="[580,60]", image_file="bit-images/mantis/l_arm.png"),
        Bit(part=3, category_id=20, name="Mantis Right Arm",coordinate="[80,40]", image_file="bit-images/mantis/r_arm.png"),
        Bit(part=4, category_id=20, name="Mantis Left Leg",coordinate="[280,90]", image_file="bit-images/mantis/l_leg.png"),
        Bit(part=5, category_id=20, name="Mantis Right Leg",coordinate="[170,80]", image_file="bit-images/mantis/r_leg.png"),

        Bit(part=0, category_id=21, name="Anubit Head",    coordinate="[350,620]", image_file="bit-images/xr6/head.png"),
        Bit(part=1, category_id=21, name="Anubit Body",    coordinate="[[500,80],[90,240],[910,240],[330,1150],[670,1150], True]", image_file="bit-images/xr6/body.png"),
        Bit(part=2, category_id=21, name="Anubit Left Arm",coordinate="[500,380]", image_file="bit-images/xr6/l_arm.png"),
        Bit(part=3, category_id=21, name="Anubit Right Arm",coordinate="[240,380]", image_file="bit-images/xr6/r_arm.png"),
        Bit(part=4, category_id=21, name="Anubit Left Leg",coordinate="[640,100]", image_file="bit-images/xr6/l_leg.png"),
        Bit(part=5, category_id=21, name="Anubit Right Leg",coordinate="[230,100]", image_file="bit-images/xr6/r_leg.png"),

        Bit(part=0, category_id=22, name="Onibot Head",    coordinate="[520,550]", image_file="bit-images/tribe2/head.png"),
        Bit(part=1, category_id=22, name="Onibot Body",    coordinate="[[800,30],[176,385],[1436,380],[592,1080],[1040,1080], True]", image_file="bit-images/tribe2/body.png"),
        Bit(part=2, category_id=22, name="Onibot Left Arm",coordinate="[320,190]", image_file="bit-images/tribe2/l_arm.png"),
        Bit(part=3, category_id=22, name="Onibot Right Arm",coordinate="[115,190]", image_file="bit-images/tribe2/r_arm.png"),
        Bit(part=4, category_id=22, name="Onibot Left Leg",coordinate="[235,115]", image_file="bit-images/tribe2/l_leg.png"),
        Bit(part=5, category_id=22, name="Onibot Right Leg",coordinate="[220,115]", image_file="bit-images/tribe2/r_leg.png"),

        Bit(part=0, category_id=23, name="SefreePoh Head",    coordinate="[350,590]", image_file="bit-images/droid/head.png"),
        Bit(part=1, category_id=23, name="SefreePoh Body",    coordinate="[[510,120],[160,300],[860,300],[340,1170],[700,1170], True]", image_file="bit-images/droid/body.png"),
        Bit(part=2, category_id=23, name="SefreePoh Left Arm",coordinate="[510,450]", image_file="bit-images/droid/l_arm.png"),
        Bit(part=3, category_id=23, name="SefreePoh Right Arm",coordinate="[210,450]", image_file="bit-images/droid/r_arm.png"),
        Bit(part=4, category_id=23, name="SefreePoh Left Leg",coordinate="[560,130]", image_file="bit-images/droid/l_leg.png"),
        Bit(part=5, category_id=23, name="SefreePoh Right Leg",coordinate="[340,130]", image_file="bit-images/droid/r_leg.png"),

        Bit(part=0, category_id=24, name="Alienbot Head",    coordinate="[500,560]", image_file="bit-images/alienbot/head.png"),
        Bit(part=1, category_id=24, name="Alienbot Body",    coordinate="[[560,20],[190,285],[940,285],[420,1040],[660,1040], True]", image_file="bit-images/alienbot/body.png"),
        Bit(part=2, category_id=24, name="Alienbot Left Arm",coordinate="[420,120]", image_file="bit-images/alienbot/l_arm.png"),
        Bit(part=3, category_id=24, name="Alienbot Right Arm",coordinate="[110,210]", image_file="bit-images/alienbot/r_arm.png"),
        Bit(part=4, category_id=24, name="Alienbot Left Leg",coordinate="[230,130]", image_file="bit-images/alienbot/l_leg.png"),
        Bit(part=5, category_id=24, name="Alienbot Right Leg",coordinate="[60,220]", image_file="bit-images/alienbot/r_leg.png"),

        Bit(part=0, category_id=25, name="Godbot Head",    coordinate="[200,440]", image_file="bit-images/godbot/head.png"),
        Bit(part=1, category_id=25, name="Godbot Body",    coordinate="[[710,80],[230,450],[1180,450],[520,1130],[820,1130], False]", image_file="bit-images/godbot/body.png"),
        Bit(part=2, category_id=25, name="Godbot Left Arm",coordinate="[480,150]", image_file="bit-images/godbot/l_arm.png"),
        Bit(part=3, category_id=25, name="Godbot Right Arm",coordinate="[50,70]", image_file="bit-images/godbot/r_arm.png"),
        Bit(part=4, category_id=25, name="Godbot Left Leg",coordinate="[270,50]", image_file="bit-images/godbot/l_leg.png"),
        Bit(part=5, category_id=25, name="Godbot Right Leg",coordinate="[140,60]", image_file="bit-images/godbot/r_leg.png"),

        Bit(part=0, category_id=26, name="Kings Head",    coordinate="[260,475]", image_file="bit-images/king/head.png"),
        Bit(part=1, category_id=26, name="Kings Body",    coordinate="[[535,210],[170,470],[930,470],[410,1125],[650,1125], True]", image_file="bit-images/king/body.png"),
        Bit(part=2, category_id=26, name="Kings Left Arm",coordinate="[200,60]", image_file="bit-images/king/l_arm.png"),
        Bit(part=3, category_id=26, name="Kings Right Arm",coordinate="[40,40]", image_file="bit-images/king/r_arm.png"),
        Bit(part=4, category_id=26, name="Kings Left Leg",coordinate="[250,90]", image_file="bit-images/king/l_leg.png"),
        Bit(part=5, category_id=26, name="Kings Right Leg",coordinate="[75,95]", image_file="bit-images/king/r_leg.png"),
        
    ]
    db.session.bulk_save_objects(categories)
    db.session.commit()
    return Bit.query.filter_by(category_id=2, part=1).first().serialize

def create_all():
    db.create_all()

def get_bit(part, category):
    data = Bit.query.filter(Bit.category_id==category, Bit.part==part).first()
    return data

def add_bot(id, level, head_id, body_id, larm_id, rarm_id, lleg_id, rleg_id):
    print(id, level, head_id, body_id, larm_id, rarm_id, lleg_id, rleg_id)
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

    generated_image = Image.new('RGBA', (2048, 3372), (0, 0, 0, 0))
    width_to_edge = int(generated_image.size[0]/2) - int(body_img.size[0]/2)
    generated_image.paste(left_arm_img,     (width_to_edge+body_coords[1][0]-eval(left_arm.coordinate)[0], 672+body_coords[1][1]-eval(left_arm.coordinate)[1]), left_arm_img)
    generated_image.paste(right_arm_img,    (width_to_edge+body_coords[2][0]-eval(right_arm.coordinate)[0], 672+body_coords[2][1]-eval(right_arm.coordinate)[1]), right_arm_img)
    if not body_coords[5]:  generated_image.paste(body_img, (width_to_edge, 672), body_img)
    generated_image.paste(left_leg_img,     (width_to_edge+body_coords[3][0]-eval(left_leg.coordinate)[0], 672+body_coords[3][1]-eval(left_leg.coordinate)[1]), left_leg_img)
    generated_image.paste(right_leg_img,    (width_to_edge+body_coords[4][0]-eval(right_leg.coordinate)[0], 672+body_coords[4][1]-eval(right_leg.coordinate)[1]), right_leg_img)
    if body_coords[5]:      generated_image.paste(body_img, (width_to_edge, 672), body_img)
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

def decide_points(type, c_id, body=False, points=[]):
    part = get_bit(type, c_id)
    if len(points)==0:
        points = eval(part.coordinate)
    generatedImg = Image.open("my_server/static/" + part.image_file)
    draw = ImageDraw.Draw(generatedImg)
    if not body: points = [points,]
    for point in points:
        if isinstance(point, list):
            draw.ellipse((point[0]-10, point[1]-10, point[0]+10, point[1]+10), fill=(255, 0, 0))
    generatedImg.show()

def generate_random(amount):
    maxCat = 26+1
    for i in range(0, amount):
        head =      random.randrange(0, maxCat)
        body =      random.randrange(0, maxCat)
        left_arm =  random.randrange(0, maxCat)
        right_arm = random.randrange(0, maxCat)
        left_leg =  random.randrange(0, maxCat)
        right_leg = random.randrange(0, maxCat)
        add_bot(i,1, head, body, left_arm, right_arm, left_leg, right_leg)


def get_bots():
    bots = Bot.query.all()
    return bots

def get_bot(id):
    bot = Bot.query.filter(Bot.id == id).first()
    return bot
