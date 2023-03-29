import requests
from flask import Flask, jsonify
from threading import Thread
app = Flask('')

@app.route('/')
def home():
	return  "I'm alive"
@app.route('/link=<string:name>', methods=['GET'])
def get_name(name):
  name=name
  name=name.split('<')[1]
  name=name.split('>')[0]
  link=name.replace("+","/")
  link=f"{link}"
  BigArry={}
  def req(link):
    link=link
    if "//watching" in link:
        link=link.replace("//watching","/watching/")    
    #print(BigArry)
    hes ={'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-encoding':'gzip',
      'accept-Language':'en-US,en;q=0.9',
      'user-agent': 'Mozilla/5.0 (Windows NT 5.1; rv:32.0) Gecko/20100101 Firefox/32.0'}
    re= requests.get(link, headers=hes)
    return re.text
  def main(link):   
    if "/watching" in link:
        link=link.replace("/watching","")    
    data=req(link)
    #print(data)
    title =data.split('<title>')[1]
    title =title.split('</title>')[0]
    if ' | سيما ناو - Cima Now' in title:
        title =title.split(' | سيما ناو - Cima Now')[0]
    BigArry['title']=title
    info =data.split('<ul class="tabcontent" id="details">')[1]
    info =info.split("a></li></ul>")[0]
    try:
        story = data.split("""<meta name="description" content='""")[1]
        story =story.split("' />")[0]
    except:
        story = info.split("</i>لمحة عامة : </strong><p>")[1]
        story =story.split("</p></li>")[0]
    if "&nbsp;" in story:
        story=story.replace("&nbsp;", " ")

    BigArry['story']=story
    photo =data.split('<figure>')[1]
    photo =photo.split('</ul>')[0]
    try:
        logo= photo.split('<img  src="')[1]
        logo= logo.split('" alt="')[0]
        cover1= photo.split('<img  src="')[2]
        cover=cover1.split('" alt="')[0]
    except:    
        logo= photo.split('<img src="')[1]
        logo= logo.split('" alt="')[0]
        cover1= photo.split('<img src="')[2]
        cover=cover1.split('" alt="')[0]

    BigArry['logo']=logo
    BigArry['cover']=cover
    try:
        requ= requests.get(cover.replace("كوفر", "كلين")).reason
        if requ =="OK":
            coverMob=cover.replace("كوفر", "كلين")
            BigArry['coverMob']=coverMob
    except:
        print("No internet")




    mess=cover1.split('/release-year/')[0]
    cat=mess.split('<li><a>')[1]

    category=cat.split('</a></li>')[0]
    BigArry['category']=category

    if "مدة العرض : " in info:
        runtime =info.split('</i>مدة العرض : </strong><a>')[1]
        runtime= runtime.split('</a><li><strong>')[0]
        BigArry['runtime']=runtime

    genre=cat.split('<li>')[2]
    genre=genre.split('</li>')[0]
    BigArry['genre']=genre

    year=data.split('/release-year/')[1]
    year= year.split('/">')[0]
    BigArry['year']=year

    if "مسلسل" in title:
        series= title.split(" الحلقة")[0]
        BigArry['series']=series
        number_en=title.split(" الحلقة ")[1]
        number_en=number_en.split(" ")[0]
        BigArry['number_en']=number_en
        season =data.split('<span aria-label="season-title">')[1]
        season =season.split('الموسم')[1]
        season="الموسم"+season.split('</span>')[0]
        season=str(season)
        BigArry['season']=season




    if "الجودة : " in info:
        quality =info.split('</i>الجودة : </strong><a>')[1]
        quality= quality.split('</a></li><li><strong>')[0]
        BigArry['quality']=quality


    if "طاقم العمل : " in info:
        
        actor =info.split('</i>طاقم العمل : </strong>')[1]
        actor= actor.split('</li><li>')[0]
        try:
            actors='،'
            for i in range(6):
                actorr =actor.split('/">')[i+1]
                actorr =actorr.split('</a>')[0]
                actors+=" ، "+actorr
        except:    
            try:
                actors='،'
                for i in range(5):
                    actorr =actor.split('/">')[i+1]
                    actorr =actorr.split('</a>')[0]
                    actors+=" ، "+actorr
            except:
                try:
                    actors='،'
                    for i in range(4):
                        actorr =actor.split('/">')[i+1]
                        actorr =actorr.split('</a>')[0]
                        actors+=" ، "+actorr
                except:
                    actors='،'
                    for i in range(3):
                        actorr =actor.split('/">')[i+1]
                        actorr =actorr.split('</a>')[0]
                        actors+=" ، "+actorr

        actors=actors.replace("، ، ", "")
        BigArry['actor']=actors

    if "اخراج : " in info:
        director =info.split('</i>اخراج : </strong><a href="')[1]
        director= director.split('/">')[1]
        director= director.split('</a>')[0]
        BigArry['director']=director

    if "تأليف : " in info:    
        escritor =info.split('</i>تأليف : </strong><a href="')[1]
        escritor= escritor.split('/">')[1]
        escritor= escritor.split('</a></li></ul>')[0]
        if "</"in escritor:
            escritor=escritor.replace("</","")
        BigArry['escritor']=escritor

    if '<ul class="tabcontent" id="watch">' in data:
        trailer=data.split('<iframe src="')[1]
        trailer=trailer.split('" scrolling=')[0]
        BigArry['trailer']=trailer


  main(link)
#print(BigArry)

  
  # BigArry=BigArry.replace("ا","a0")
  # BigArry=BigArry.replace("ب","b0")
  # BigArry=BigArry.replace("ت","c0")
  # BigArry=BigArry.replace("ث","d0")
  # BigArry=BigArry.replace("ج","e0")
  # BigArry=BigArry.replace("ح","f0")
  # BigArry=BigArry.replace("خ","g0")
  # BigArry=BigArry.replace("د","h0")
  # BigArry=BigArry.replace("ذ","i0")
  # BigArry=BigArry.replace("ر","j0")
  # BigArry=BigArry.replace("ز","k0")
  # BigArry=BigArry.replace("س","l0")
  # BigArry=BigArry.replace("ش","m0")
  # BigArry=BigArry.replace("ص","n0")
  # BigArry=BigArry.replace("ض","o0")
  # BigArry=BigArry.replace("ط","p0")
  # BigArry=BigArry.replace("ظ","q0")
  # BigArry=BigArry.replace("ع","r0")
  # BigArry=BigArry.replace("غ","s0")
  # BigArry=BigArry.replace("ف","t0")
  # BigArry=BigArry.replace("ق","w0")
  # BigArry=BigArry.replace("ك","v0")
  # BigArry=BigArry.replace("ل","x0")
  # BigArry=BigArry.replace("م","y0")
  # BigArry=BigArry.replace("ن","z0")
  # BigArry=BigArry.replace("ه","m1")
  # BigArry=BigArry.replace("و","m2")
  # BigArry=BigArry.replace("ي","m3")
  # BigArry=BigArry.replace("ى","m4")
  # BigArry=BigArry.replace("ؤ","m5")
  # BigArry=BigArry.replace("ء","m6")
  # BigArry=BigArry.replace("ئ","m7")
  # BigArry=BigArry.replace("ة","m8")
  
  return jsonify(BigArry)
def run():
	app.run(host='0.0.0.0',port=8080)
t = Thread(target=run)
t.start()
