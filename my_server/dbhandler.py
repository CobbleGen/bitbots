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
        Category(id=1,  name="SmileBot",    creator="Sander",       rarity="Common"),
        Category(id=2,  name="XR-I",        creator="TR",           rarity="Common"),
        Category(id=3,  name="XR-III",      creator="TR",           rarity="Common"),
        Category(id=4,  name="SwampBot",    creator="Sander",       rarity="Common"),
        Category(id=5,  name="TribeBot",    creator="ArtTribe",     rarity="Uncommon"),
        Category(id=6,  name="Humunculus",  creator="Sander",       rarity="Uncommon"),
        Category(id=7,  name="XR-IV",       creator="TR",           rarity="Uncommon"),
        Category(id=8,  name="ArtBot",      creator="AyshaArt",     rarity="Uncommon"),
        Category(id=9,  name="Mantis",      creator="Chabusan",     rarity="Uncommon"),
        Category(id=10, name="XR-II",       creator="TR",           rarity="Rare"),
        Category(id=11, name="Golem",       creator="TR",           rarity="Rare"),
        Category(id=12, name="DemonBot",    creator="Sander",       rarity="Rare"),
        Category(id=13, name="XR-V",        creator="TR",           rarity="Epic"),
        Category(id=14, name="Unit",        creator="ArtTribe",     rarity="Epic"),
        Category(id=15, name="Anubit",      creator="TR",           rarity="Epic"),
        Category(id=16, name="PunkBot",     creator="Chabusan",     rarity="Epic"),
        Category(id=17, name="GodBot",      creator="Chabusan",     rarity="Legendary"),
        Category(id=18, name="Junkyard King",creator="Roman Ichalov",rarity="Legendary"),

        Bit(part=0, category_id=0, name="AyshaBot Head",    coordinate="[400,530]", image_file="bit-images/aysha/head.png"),
        Bit(part=1, category_id=0, name="AyshaBot Body",    coordinate="[[360,51],[65,315],[700,315],[190,1290],[575,1290], True]", image_file="bit-images/aysha/body.png"),
        Bit(part=2, category_id=0, name="AyshaBot Left Arm",coordinate="[480,80]", image_file="bit-images/aysha/l_arm.png"),
        Bit(part=3, category_id=0, name="AyshaBot Right Arm",coordinate="[160,80]", image_file="bit-images/aysha/r_arm.png"),
        Bit(part=4, category_id=0, name="AyshaBot Left Leg",coordinate="[335,70]", image_file="bit-images/aysha/l_leg.png"),
        Bit(part=5, category_id=0, name="AyshaBot Right Leg",coordinate="[250,100]", image_file="bit-images/aysha/r_leg.png"),

        Bit(part=0, category_id=1, name="SmileBot Head",    coordinate="[205,455]", image_file="bit-images/sander1/head.png"),
        Bit(part=1, category_id=1, name="SmileBot Body",    coordinate="[[860,60],[290,340],[1280,490],[530,1280],[990,1280], True]", image_file="bit-images/sander1/body.png"),
        Bit(part=2, category_id=1, name="SmileBot Left Arm",coordinate="[350,130]", image_file="bit-images/sander1/l_arm.png"),
        Bit(part=3, category_id=1, name="SmileBot Right Arm",coordinate="[125,130]", image_file="bit-images/sander1/r_arm.png"),
        Bit(part=4, category_id=1, name="SmileBot Left Leg",coordinate="[290,150]", image_file="bit-images/sander1/l_leg.png"),
        Bit(part=5, category_id=1, name="SmileBot Right Leg",coordinate="[150,150]", image_file="bit-images/sander1/r_leg.png"),

        Bit(part=0, category_id=2, name="XR-I Head",    coordinate="[350,570]", image_file="bit-images/xr1/head.png"),
        Bit(part=1, category_id=2, name="XR-I Body",    coordinate="[[495,5],[40,250],[950,250],[330,1100],[660,1100], True]", image_file="bit-images/xr1/body.png"),
        Bit(part=2, category_id=2, name="XR-I Left Arm",coordinate="[560,500]", image_file="bit-images/xr1/l_arm.png"),
        Bit(part=3, category_id=2, name="XR-I Right Arm",coordinate="[120,500]", image_file="bit-images/xr1/r_arm.png"),
        Bit(part=4, category_id=2, name="XR-I Left Leg",coordinate="[550,120]", image_file="bit-images/xr1/l_leg.png"),
        Bit(part=5, category_id=2, name="XR-I Right Leg",coordinate="[150,130]", image_file="bit-images/xr1/r_leg.png"),

        Bit(part=0, category_id=3, name="XR-III Head",    coordinate="[350,475]", image_file="bit-images/xr3/head.png"),
        Bit(part=1, category_id=3, name="XR-III Body",    coordinate="[[500,75],[90,200],[930,200],[300,1120],[700,1120], True]", image_file="bit-images/xr3/body.png"),
        Bit(part=2, category_id=3, name="XR-III Left Arm",coordinate="[470,530]", image_file="bit-images/xr3/l_arm.png"),
        Bit(part=3, category_id=3, name="XR-III Right Arm",coordinate="[220,530]", image_file="bit-images/xr3/r_arm.png"),
        Bit(part=4, category_id=3, name="XR-III Left Leg",coordinate="[600,80]", image_file="bit-images/xr3/l_leg.png"),
        Bit(part=5, category_id=3, name="XR-III Right Leg",coordinate="[320,80]", image_file="bit-images/xr3/r_leg.png"),

        Bit(part=0, category_id=4, name="SwampBot Head",    coordinate="[195,435]", image_file="bit-images/sander4/head.png"),
        Bit(part=1, category_id=4, name="SwampBot Body",    coordinate="[[640,80],[150,360],[1100,370],[480,1200],[800,1200], True]", image_file="bit-images/sander4/body.png"),
        Bit(part=2, category_id=4, name="SwampBot Left Arm",coordinate="[180,80]", image_file="bit-images/sander4/l_arm.png"),
        Bit(part=3, category_id=4, name="SwampBot Right Arm",coordinate="[90,170]", image_file="bit-images/sander4/r_arm.png"),
        Bit(part=4, category_id=4, name="SwampBot Left Leg",coordinate="[310,60]", image_file="bit-images/sander4/l_leg.png"),
        Bit(part=5, category_id=4, name="SwampBot Right Leg",coordinate="[100,70]", image_file="bit-images/sander4/r_leg.png"),

        Bit(part=0, category_id=5, name="TribeBot Head",    coordinate="[715,670]", image_file="bit-images/artribe/head.png"),
        Bit(part=1, category_id=5, name="TribeBot Body",    coordinate="[[790,60],[400,500],[1170,500],[610,1340],[970,1340], True]", image_file="bit-images/artribe/body.png"),
        Bit(part=2, category_id=5, name="TribeBot Left Arm",coordinate="[450,125]", image_file="bit-images/artribe/l_arm.png"),
        Bit(part=3, category_id=5, name="TribeBot Right Arm",coordinate="[90,135]", image_file="bit-images/artribe/r_arm.png"),
        Bit(part=4, category_id=5, name="TribeBot Left Leg",coordinate="[365,90]", image_file="bit-images/artribe/l_leg.png"),
        Bit(part=5, category_id=5, name="TribeBot Right Leg",coordinate="[190,100]", image_file="bit-images/artribe/r_leg.png"),

        Bit(part=0, category_id=6, name="Humunculus Head",    coordinate="[200,450]", image_file="bit-images/sander3/head.png"),
        Bit(part=1, category_id=6, name="Humunculus Body",    coordinate="[[600,70],[210,240],[1000,240],[460,1120],[740,1120], True]", image_file="bit-images/sander3/body.png"),
        Bit(part=2, category_id=6, name="Humunculus Left Arm",coordinate="[230,130]", image_file="bit-images/sander3/l_arm.png"),
        Bit(part=3, category_id=6, name="Humunculus Right Arm",coordinate="[80,130]", image_file="bit-images/sander3/r_arm.png"),
        Bit(part=4, category_id=6, name="Humunculus Left Leg",coordinate="[300,90]", image_file="bit-images/sander3/l_leg.png"),
        Bit(part=5, category_id=6, name="Humunculus Right Leg",coordinate="[130,90]", image_file="bit-images/sander3/r_leg.png"),

        Bit(part=0, category_id=7, name="XR-IV Head",    coordinate="[350,560]", image_file="bit-images/xr4/head.png"),
        Bit(part=1, category_id=7, name="XR-IV Body",    coordinate="[[500,100],[90,200],[930,200],[300,1120],[700,1120], True]", image_file="bit-images/xr4/body.png"),
        Bit(part=2, category_id=7, name="XR-IV Left Arm",coordinate="[470,530]", image_file="bit-images/xr4/l_arm.png"),
        Bit(part=3, category_id=7, name="XR-IV Right Arm",coordinate="[220,530]", image_file="bit-images/xr4/r_arm.png"),
        Bit(part=4, category_id=7, name="XR-IV Left Leg",coordinate="[660,80]", image_file="bit-images/xr4/l_leg.png"),
        Bit(part=5, category_id=7, name="XR-IV Right Leg",coordinate="[250,80]", image_file="bit-images/xr4/r_leg.png"),

        Bit(part=0, category_id=8, name="ArtBot Head",    coordinate="[400,660]", image_file="bit-images/aysha2/head.png"),
        Bit(part=1, category_id=8, name="ArtBot Body",    coordinate="[[765,80],[270,580],[1270,580],[620,1160],[900,1160], True]", image_file="bit-images/aysha2/body.png"),
        Bit(part=2, category_id=8, name="ArtBot Left Arm",coordinate="[370,100]", image_file="bit-images/aysha2/l_arm.png"),
        Bit(part=3, category_id=8, name="ArtBot Right Arm",coordinate="[120,100]", image_file="bit-images/aysha2/r_arm.png"),
        Bit(part=4, category_id=8, name="ArtBot Left Leg",coordinate="[440,130]", image_file="bit-images/aysha2/l_leg.png"),
        Bit(part=5, category_id=8, name="ArtBot Right Leg",coordinate="[160,140]", image_file="bit-images/aysha2/r_leg.png"),

        Bit(part=0, category_id=9, name="Mantis Head",    coordinate="[325,430]", image_file="bit-images/mantis/head.png"),
        Bit(part=1, category_id=9, name="Mantis Body",    coordinate="[[765,30],[290,290],[1200,290],[580,1130],[920,1120], True]", image_file="bit-images/mantis/body.png"),
        Bit(part=2, category_id=9, name="Mantis Left Arm",coordinate="[580,60]", image_file="bit-images/mantis/l_arm.png"),
        Bit(part=3, category_id=9, name="Mantis Right Arm",coordinate="[80,40]", image_file="bit-images/mantis/r_arm.png"),
        Bit(part=4, category_id=9, name="Mantis Left Leg",coordinate="[280,90]", image_file="bit-images/mantis/l_leg.png"),
        Bit(part=5, category_id=9, name="Mantis Right Leg",coordinate="[170,80]", image_file="bit-images/mantis/r_leg.png"),

        Bit(part=0, category_id=10, name="XR-II Head",    coordinate="[350,570]", image_file="bit-images/xr2/head.png"),
        Bit(part=1, category_id=10, name="XR-II Body",    coordinate="[[500,80],[70,255],[930,255],[300,1060],[700,1060], True]", image_file="bit-images/xr2/body.png"),
        Bit(part=2, category_id=10, name="XR-II Left Arm",coordinate="[560,500]", image_file="bit-images/xr2/l_arm.png"),
        Bit(part=3, category_id=10, name="XR-II Right Arm",coordinate="[120,500]", image_file="bit-images/xr2/r_arm.png"),
        Bit(part=4, category_id=10, name="XR-II Left Leg",coordinate="[550,120]", image_file="bit-images/xr2/l_leg.png"),
        Bit(part=5, category_id=10, name="XR-II Right Leg",coordinate="[150,130]", image_file="bit-images/xr2/r_leg.png"),

        Bit(part=0, category_id=11, name="Golem Head",    coordinate="[350,600]", image_file="bit-images/xr7/head.png"),
        Bit(part=1, category_id=11, name="Golem Body",    coordinate="[[500,200],[100,270],[920,270],[370,1100],[660,1100], True]", image_file="bit-images/xr7/body.png"),
        Bit(part=2, category_id=11, name="Golem Left Arm",coordinate="[575,500]", image_file="bit-images/xr7/l_arm.png"),
        Bit(part=3, category_id=11, name="Golem Right Arm",coordinate="[120,500]", image_file="bit-images/xr7/r_arm.png"),
        Bit(part=4, category_id=11, name="Golem Left Leg",coordinate="[740,60]", image_file="bit-images/xr7/l_leg.png"),
        Bit(part=5, category_id=11, name="Golem Right Leg",coordinate="[220,60]", image_file="bit-images/xr7/r_leg.png"),

        Bit(part=0, category_id=12, name="DemonBot Head",    coordinate="[260,500]", image_file="bit-images/sander2/head.png"),
        Bit(part=1, category_id=12, name="DemonBot Body",    coordinate="[[700,50],[240,350],[1180,350],[540,1130],[870,1130], True]", image_file="bit-images/sander2/body.png"),
        Bit(part=2, category_id=12, name="DemonBot Left Arm",coordinate="[370,100]", image_file="bit-images/sander2/l_arm.png"),
        Bit(part=3, category_id=12, name="DemonBot Right Arm",coordinate="[100,100]", image_file="bit-images/sander2/r_arm.png"),
        Bit(part=4, category_id=12, name="DemonBot Left Leg",coordinate="[330,90]", image_file="bit-images/sander2/l_leg.png"),
        Bit(part=5, category_id=12, name="DemonBot Right Leg",coordinate="[120,90]", image_file="bit-images/sander2/r_leg.png"),

        Bit(part=0, category_id=13, name="XR-V Head",    coordinate="[350,620]", image_file="bit-images/xr5/head.png"),
        Bit(part=1, category_id=13, name="XR-V Body",    coordinate="[[500,80],[95,350],[910,350],[330,1150],[670,1150], True]", image_file="bit-images/xr5/body.png"),
        Bit(part=2, category_id=13, name="XR-V Left Arm",coordinate="[500,560]", image_file="bit-images/xr5/l_arm.png"),
        Bit(part=3, category_id=13, name="XR-V Right Arm",coordinate="[200,570]", image_file="bit-images/xr5/r_arm.png"),
        Bit(part=4, category_id=13, name="XR-V Left Leg",coordinate="[590,80]", image_file="bit-images/xr5/l_leg.png"),
        Bit(part=5, category_id=13, name="XR-V Right Leg",coordinate="[230,100]", image_file="bit-images/xr5/r_leg.png"),

        Bit(part=0, category_id=14, name="Unit Head",    coordinate="[520,550]", image_file="bit-images/tribe2/head.png"),
        Bit(part=1, category_id=14, name="Unit Body",    coordinate="[[800,30],[176,385],[1436,380],[592,1080],[1040,1080], True]", image_file="bit-images/tribe2/body.png"),
        Bit(part=2, category_id=14, name="Unit Left Arm",coordinate="[320,190]", image_file="bit-images/tribe2/l_arm.png"),
        Bit(part=3, category_id=14, name="Unit Right Arm",coordinate="[115,190]", image_file="bit-images/tribe2/r_arm.png"),
        Bit(part=4, category_id=14, name="Unit Left Leg",coordinate="[235,115]", image_file="bit-images/tribe2/l_leg.png"),
        Bit(part=5, category_id=14, name="Unit Right Leg",coordinate="[220,115]", image_file="bit-images/tribe2/r_leg.png"),

        Bit(part=0, category_id=15, name="Anubit Head",    coordinate="[350,620]", image_file="bit-images/xr6/head.png"),
        Bit(part=1, category_id=15, name="Anubit Body",    coordinate="[[500,80],[90,240],[910,240],[330,1150],[670,1150], True]", image_file="bit-images/xr6/body.png"),
        Bit(part=2, category_id=15, name="Anubit Left Arm",coordinate="[500,380]", image_file="bit-images/xr6/l_arm.png"),
        Bit(part=3, category_id=15, name="Anubit Right Arm",coordinate="[240,380]", image_file="bit-images/xr6/r_arm.png"),
        Bit(part=4, category_id=15, name="Anubit Left Leg",coordinate="[640,100]", image_file="bit-images/xr6/l_leg.png"),
        Bit(part=5, category_id=15, name="Anubit Right Leg",coordinate="[230,100]", image_file="bit-images/xr6/r_leg.png"),

        Bit(part=0, category_id=16, name="Punkbot Head",    coordinate="[165,480]", image_file="bit-images/punkbot/head.png"),
        Bit(part=1, category_id=16, name="Punkbot Body",    coordinate="[[445,130],[80,350],[800,350],[220,1180],[600,1190], False]", image_file="bit-images/punkbot/body.png"),
        Bit(part=2, category_id=16, name="Punkbot Left Arm",coordinate="[380,150]", image_file="bit-images/punkbot/l_arm.png"),
        Bit(part=3, category_id=16, name="Punkbot Right Arm",coordinate="[100,160]", image_file="bit-images/punkbot/r_arm.png"),
        Bit(part=4, category_id=16, name="Punkbot Left Leg",coordinate="[315,110]", image_file="bit-images/punkbot/l_leg.png"),
        Bit(part=5, category_id=16, name="Punkbot Right Leg",coordinate="[170,110]", image_file="bit-images/punkbot/r_leg.png"),

        Bit(part=0, category_id=17, name="Godbot Head",    coordinate="[200,440]", image_file="bit-images/godbot/head.png"),
        Bit(part=1, category_id=17, name="Godbot Body",    coordinate="[[710,80],[230,450],[1180,450],[520,1130],[820,1130], False]", image_file="bit-images/godbot/body.png"),
        Bit(part=2, category_id=17, name="Godbot Left Arm",coordinate="[480,150]", image_file="bit-images/godbot/l_arm.png"),
        Bit(part=3, category_id=17, name="Godbot Right Arm",coordinate="[50,70]", image_file="bit-images/godbot/r_arm.png"),
        Bit(part=4, category_id=17, name="Godbot Left Leg",coordinate="[270,50]", image_file="bit-images/godbot/l_leg.png"),
        Bit(part=5, category_id=17, name="Godbot Right Leg",coordinate="[140,60]", image_file="bit-images/godbot/r_leg.png"),

        Bit(part=0, category_id=18, name="Kings Head",    coordinate="[200,480]", image_file="bit-images/king/head.png"),
        Bit(part=1, category_id=18, name="Kings Body",    coordinate="[[540,230],[170,470],[930,470],[410,1125],[660,1125], True]", image_file="bit-images/king/body.png"),
        Bit(part=2, category_id=18, name="Kings Left Arm",coordinate="[230,275]", image_file="bit-images/king/l_arm.png"),
        Bit(part=3, category_id=18, name="Kings Right Arm",coordinate="[140,250]", image_file="bit-images/king/r_arm.png"),
        Bit(part=4, category_id=18, name="Kings Left Leg",coordinate="[250,90]", image_file="bit-images/king/l_leg.png"),
        Bit(part=5, category_id=18, name="Kings Right Leg",coordinate="[75,95]", image_file="bit-images/king/r_leg.png"),
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
    maxCat = 18+1
    for _ in range(0, amount):
        head =      get_bit(0, random.randrange(0, maxCat))
        body =      get_bit(1, random.randrange(0, maxCat))
        left_arm =  get_bit(2, random.randrange(0, maxCat))
        right_arm = get_bit(3, random.randrange(0, maxCat))
        left_leg =  get_bit(4, random.randrange(0, maxCat))
        right_leg = get_bit(5, random.randrange(0, maxCat))
        create_pic(random.randrange(0, 99999), head, body, left_arm, right_arm, left_leg, right_leg, False)


def get_bots():
    bots = Bot.query.all()
    return bots

def get_bot(id):
    bot = Bot.query.filter(Bot.id == id).first()
    return bot
