import json, os, shutil, html, re
from pathlib import Path
P=Path(__file__).resolve().parent.parent; O=P/'dist'; shutil.rmtree(O,ignore_errors=True); O.mkdir(); shutil.copytree(P/'public',O,dirs_exist_ok=True)
home=json.loads((P/'content/homepage.json').read_text(encoding='utf-8')); s=json.loads((P/'content/settings.json').read_text()); base=os.environ.get('SITE_URL',s['domain']).rstrip('/'); preview=os.environ.get('PRODUCTION')!='1'
e=lambda x:html.escape(str(x),quote=True)
sections=[('o-nama','O nama','Upoznajte našu crkvu'),('uzivo','Bogosluženje uživo','Budimo zajedno, gde god da ste'),('propovedi','Propovedi','Slušajte. Proučavajte. Rastite.'),('decja-sluzba','Dečja služba','Mali koraci. Velike istine.'),('omladinska-sluzba','Omladinska služba','Vera u svakodnevnom životu'),('duhovni-rast','Duhovni rast','Prostor za rast u Božijoj reči'),('biblioteka','Biblioteka','Dobri materijali. Na jednom mestu.'),('drugim-crkvama','Drugim crkvama','Resursi za zajedničko služenje'),('dogadjaji','Događaji','Vreme za zajedništvo'),('kontakt','Kontakt','Dobro došli u Jagodinu'),('newsletter','Newsletter','Prijavite se za novosti naše službe'),('podrzi-nas','Podrži nas','Podržite naš rad')]
records=[]
for f in (P/'content/posts').glob('*.json'):
 d=json.loads(f.read_text())
 if d.get('draft',True): continue
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',d['slug']): raise ValueError('Neispravan slug')
 records.append(d)
records.sort(key=lambda x:x.get('date',''),reverse=True)
nav=''.join(f'<a href="/{slug}/">{label}</a>' for slug,label,_ in [sections[i] for i in [0,2,10,11]])
urls=[]
def page(path,title,desc,body):
 url=base+'/'+path; urls.append(url); target=O/path/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
 target.write_text(f'''<!doctype html><html lang="sr-Latn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} | Evanđeoska crkva Jagodina</title><meta name="description" content="{e(desc)}"><meta name="robots" content="{'noindex,nofollow' if preview else 'index,follow'}"><link rel="canonical" href="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:locale" content="sr_RS"><meta name="theme-color" content="#b72c13"><link rel="apple-touch-icon" href="/app-icon.png"><link rel="manifest" href="/manifest.webmanifest"><link rel="icon" href="/app-icon.png"><link rel="stylesheet" href="/style.css"><script defer src="/app.js"></script><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'Church','name':s['name'],'url':base,'email':s['email']}).replace('<','\\u003c')}</script></head><body><a class="skip" href="#main">Pređi na sadržaj</a><header><a class="brand" href="/"><img class="brand-logo" src="/logo.png" alt="" width="56" height="72"><span>Evanđeoska crkva<small>J A G O D I N A</small></span></a><button class="menu" aria-expanded="false" aria-controls="nav">Meni ☰</button><nav id="nav">{nav}<a class="lang-switch" href="/en/{path}" lang="en" aria-label="Switch to English">EN</a><a class="navlive" href="/uzivo/">Prenos ↗</a></nav></header><main id="main">{body}</main><footer><div><a class="brand" href="/">Evanđeoska crkva Jagodina</a><p>Dobro došli! Zajedno slušamo i delimo Božiju reč.</p><a href="mailto:{s['email']}">{s['email']}</a></div><div><strong>Istražite</strong>{''.join(f'<a href="/{a}/">{b}</a>' for a,b,_ in sections)}</div><div><strong>Ostanimo u kontaktu</strong><p>Za informacije o poseti i bogosluženjima<br>pišite nam imejlom.</p><a href="/instalacija/">Dodajte sajt na telefon ↗</a><a href="/privatnost/">Privatnost</a><a href="/admin/">Uređivanje sadržaja ↗</a></div><aside>© {__import__('datetime').date.today().year} Evanđeoska crkva Jagodina <span>{'Privatni pregled • sadržaj je u pripremi' if preview else 'Sva prava zadržana.'}</span></aside></footer></body></html>''')
def empty(text):return f'<div class="empty"><span>✧</span><h3>Sadržaj je u pripremi</h3><p>{text}</p><a href="mailto:{s["email"]}">Kontaktirajte nas ↗</a></div>'
def youtube_thumbnail(url):
    """YouTube preview bez dodatnog API-ja ili plaćene usluge."""
    from urllib.parse import urlparse, parse_qs
    if not url:
        return ''
    try:
        u = urlparse(url.strip())
        host = (u.hostname or '').lower()
        parts = [x for x in u.path.split('/') if x]
        if host in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
            video_id = parse_qs(u.query).get('v', [''])[0] if u.path == '/watch' else (parts[1] if len(parts)>1 and parts[0] in ('live','shorts','embed') else '')
        elif host in ('youtu.be', 'www.youtu.be'):
            video_id = parts[0] if parts else ''
        else:
            return ''
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}', video_id):
            return ''
        return f'<img src="https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" alt="YouTube naslovna slika" loading="lazy" style="display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:12px;margin-bottom:16px">'
    except (ValueError, IndexError):
        return ''

def cards(items):
    return '<div class="results">'+''.join(
        f'<a class="result" href="/objave/{e(d["slug"])}/" data-search="{e(" ".join(str(v) for v in d.values()).lower())}" data-type="{e(d.get("type",""))}">'
        + youtube_thumbnail(d.get('youtube',''))
        + f'<span class="eyebrow">{e(d.get("type","Materijal"))} · {e(d.get("date",""))}</span><h3>{e(d["title"])}</h3><p>{e(d.get("description",""))}</p><span>Otvori materijal ↗</span></a>'
        for d in items
    )+'</div>'

def head(label,title,desc=''):return f'<section class="pagehead"><p class="eyebrow">{label}</p><h1>{title}</h1><p>{desc}</p></section>'
# Fotografije se dodaju/uklanjaju preko Pages CMS > Fotografije crkve.
# Svaki JSON zapis prikazuje jednu fotografiju. Izbrisani zapis se vise ne prikazuje.
gallery=[]
for f in (P/'content/gallery').glob('*.json'):
 d=json.loads(f.read_text(encoding='utf-8'))
 if not d.get('visible',True): continue
 path=d.get('image','')
 if not isinstance(path,str) or not path.startswith('/media/') or '"' in path: continue
 gallery.append((int(d.get('order',100)),f.name,path,d.get('title','Fotografija crkve')))
gallery.sort(key=lambda x:(x[0],x[1]))
gallery_images=''.join(f'<img class="church-photo" src="{e(path)}" alt="{e(title)}" hidden loading="eager">' for _,_,path,title in gallery)
hero=f'''<section class="hero home-hero"><div class="hero-copy"><p class="eyebrow"><span></span> EVANĐEOSKA CRKVA JAGODINA</p><h1>{e(home['title'])}<br><em>{e(home['accent'])}</em></h1><p class="hero-description">{e(home['description'])}</p><div class="buttons"><a class="button" href="/uzivo/">Pratite bogosluženje <span>↗</span></a><a class="button outline" href="/kontakt/">Posetite nas ↗</a></div></div><div class="church-photos" aria-label="Fotografije naše crkve"><div class="photo-placeholder"><span>NAŠA CRKVA</span><strong>Ovde će biti fotografije naše zajednice.</strong><small>Dodajte svoje fotografije u folder public/slike.</small></div>{gallery_images}<div class="photo-controls" hidden><button type="button" class="photo-prev" aria-label="Prethodna fotografija">‹</button><button type="button" class="photo-next" aria-label="Sledeća fotografija">›</button></div></div></section>'''
body=hero
sermons=[d for d in records if d.get('section')=='propovedi']
encouragements=[d for d in records if d.get('section')=='duhovni-rast']
def latest(items,label,desc):
 if items:
  d=items[0];return '<a class="latest-card" href="/objave/'+e(d['slug'])+'/"><span class="eyebrow">'+label+'</span><h3>'+e(d['title'])+'</h3><p>'+e(d.get('description',''))+'</p><b>Pročitajte više ↗</b></a>'
 return '<div class="latest-card"><span class="eyebrow">'+label+'</span><h3>Sadržaj je u pripremi.</h3><p>'+desc+'</p></div>'
body+='<section class="section watch-section"><div class="section-heading"><div><p class="eyebrow">BOGOSLUŽENJA I PROPOVEDI</p><h2>Pratite naše poslednje bogosluženje.</h2><p>Pogledajte snimke i propovedi naše crkve.</p></div><a class="button" href="/uzivo/">Bogosluženje uživo ↗</a></div><div class="latest-grid">'+latest(sermons,'POSLEDNJA PROPOVED','Ovde će se prikazati najnovija propoved kada dodamo YouTube snimak.')+'<a class="latest-card" href="/propovedi/"><span class="eyebrow">VIDEO ARHIVA</span><h3>Propovedi i prethodna bogosluženja</h3><p>Pregledajte dostupne video-snimke i biblijske poruke.</p><b>Pogledajte propovedi ↗</b></a></div></section>'
body+='<section class="section ministries-section"><div class="section-heading"><div><p class="eyebrow">MATERIJALI I SLUŽBE</p><h2>Resursi za sve generacije.</h2></div><a href="/biblioteka/">Cela biblioteka ↗</a></div><div class="ministries"><a href="/decja-sluzba/" class="kids"><span>01</span><small>DEČJI RAD</small><h3>Resursi za dečji rad</h3><p>Biblijske lekcije, aktivnosti i materijali za učitelje i roditelje.</p><b>Otvori resurse ↗</b></a><a href="/omladinska-sluzba/" class="youth"><span>02</span><small>OMLADINSKI RAD</small><h3>Resursi za omladinski rad</h3><p>Biblijske pouke, razgovori i materijali za mlade.</p><b>Otvori resurse ↗</b></a><a href="/biblioteka/" class="churches"><span>03</span><small>MUZIKA I SLAVLJENJE</small><h3>Slavljenje našeg tima</h3><p>Pesme i snimci našeg tima za slavljenje, kada ih objavimo.</p><b>Pogledaj biblioteku ↗</b></a></div></section><section class="section"><div class="section-heading"><div><p class="eyebrow">DUHOVNI RAST</p><h2>Ohrabrenja iz Božije reči.</h2></div><a href="/duhovni-rast/">Sva ohrabrenja ↗</a></div><div class="latest-grid">'+latest(encouragements,'NAJNOVIJE OHRABRENJE','Ovde ćemo objavljivati mesečna ohrabrenja i biblijska razmišljanja.')+'<a class="latest-card" href="/biblioteka/"><span class="eyebrow">BIBLIOTEKA</span><h3>Materijali za proučavanje</h3><p>Pronađite pouke i druge resurse koji će vam pomoći u proučavanju Biblije.</p><b>Istražite biblioteku ↗</b></a></div></section><section class="visit"><p class="eyebrow">DOBRO DOŠLI U JAGODINU</p><h2>Rado ćemo vas upoznati.</h2><p>Svi su dobrodošli. Kontaktirajte nas ili saznajte više o našoj crkvi.</p><a class="button" href="/kontakt/">Kontaktirajte nas ↗</a></section>'
page('','Dobro došli','Evanđeoska crkva Jagodina. Propovedamo Jevanđelje o Isusu Hristu. Svi su dobrodošli. Bog voli sve ljude.',body)
for slug,label,title in sections:
 b=head(label,title)
 if slug=='newsletter':
  b+='<section class="section reading"><h2>Newsletter</h2><p>Želite da primate novosti o našoj službi, propovedima i novim materijalima? Prijava putem imejla biće dostupna kada povežemo servis za slanje. Do tada nam možete pisati.</p><a class="button" href="mailto:'+e(s['email'])+'?subject=Newsletter%20-%20prijava">Pišite nam ↗</a></section>'
 elif slug=='podrzi-nas':
  b+='<section class="section reading"><h2>Podrži nas</h2><p>Hvala što želite da podržite službu Evanđeoske crkve Jagodina. Informacije o mogućnostima podrške objavićemo nakon potvrde zvaničnih podataka za uplatu.</p><a class="button" href="mailto:'+e(s['email'])+'?subject=Podrska%20sluzbi">Kontaktirajte nas ↗</a></section>'
 elif slug=='mentorstvo':
  b+='<section class="section mentorship-content"><div><p class="eyebrow">NAŠA VIZIJA</p><h2>'+e(s['mission'])+'</h2><p>'+e(home['mentorship_description'])+'</p></div><div class="panel"><h3>Pridružite se mentorstvu</h3><p>Pošaljite nam imejl i napišite da ste zainteresovani za mentorstvo. Kroz razgovor ćemo vam dati informacije o mogućnostima i narednim koracima.</p><a class="button" href="mailto:'+e(s['email'])+'?subject=Interesovanje%20za%20mentorstvo">Zainteresovan/a sam ↗</a><p class="note">Ovo dugme otvara vašu imejl aplikaciju. Nije automatska prijava u program.</p></div></section>'
 elif slug=='kontakt':
  b+='<section class="section contact"><div><h2>Pišite nam</h2><p>Kontakt imejl crkve</p><a class="email" href="mailto:'+s['email']+'">'+s['email']+'</a><p>Za informacije o dolasku, terminima i materijalima.</p></div><div class="panel"><h3>Posetite nas</h3><p>'+e(s.get('address') or 'Tačna adresa će biti objavljena nakon potvrde.')+'</p><h3>Raspored bogosluženja</h3><p>'+e(s.get('schedule') or 'Termini će biti objavljeni nakon potvrde. Pre dolaska kontaktirajte crkvu.')+'</p></div></section>'
 elif slug=='o-nama':
  b+='<section class="section reading"><h2>Evanđeoska crkva Jagodina</h2><p>'+e(s.get('about') or 'Dobro došli na sajt Evanđeoske crkve Jagodina. Za više informacija o crkvi i dolasku možete nam se javiti imejlom.')+'</p>'+''.join('<h3>'+t+'</h3><p>'+e(s.get(k) or 'Zvanične informacije su u pripremi.')+'</p>' for k,t in [('mission','Vizija i misija'),('beliefs','U šta verujemo'),('leadership','Rukovodstvo')])+'<a class="button" href="/kontakt/">Kako da nas posetite ↗</a></section>'
 elif slug=='uzivo':
  if s.get('youtube') and not s['youtube'].startswith('https://'): raise ValueError('YouTube kanal mora biti HTTPS link')
  b+='<section class="section">'+empty('Link ka prenosu još nije dodat. Ovaj prikaz ne označava da je bogosluženje trenutno uživo.')+'<p><a href="/propovedi/">Prethodna bogosluženja i propovedi →</a></p></section>' if not s.get('youtube') else '<section class="section"><p>Proverite dostupnost prenosa na zvaničnom kanalu.</p><a class="button" href="'+e(s['youtube'])+'">Otvorite YouTube ↗</a></section>'
 else:
  chosen=[d for d in records if slug=='biblioteka' or d.get('section')==slug]
  filters=['type','topic','ministry','language','author','age','series']
  names=['Tip materijala','Tema','Služba','Jezik','Autor / govornik','Uzrast','Serija']
  b+='<section class="section library"><label for="search">Pretražite naslove, biblijske tekstove i opise</label><input id="search" type="search" placeholder="Šta želite da proučavate?"><div class="filters">'+''.join('<label>'+name+'<select data-field="'+field+'"><option value="">Sve</option>'+''.join('<option>'+e(v)+'</option>' for v in sorted(set(d.get(field,'') for d in chosen)-{''}))+'</select></label>' for field,name in zip(filters,names))+'</div>'+ (cards(chosen) if chosen else empty('Ovde će se pojaviti zvanični sadržaji kada budu objavljeni.'))+'<p id="no-results" hidden>Nema rezultata za izabranu pretragu.</p></section>'
 page(slug+'/',label,title,b)
for d in records:
 text=''.join('<p>'+e(p).replace('\n','<br>')+'</p>' for p in d.get('body','').split('\n\n'))
 actions=''
 for key,label in [('youtube','Pogledajte na YouTube-u'),('file','Otvorite / preuzmite materijal'),('drive','Otvorite PDF na Google Drive-u')]:
  u=d.get(key,'')
  if u and (u.startswith('https://') or u.startswith('/media/')): actions+=f'<p><a class="button" href="{e(u)}" rel="noopener">{label} ↗</a></p>'
 page('objave/'+d['slug']+'/',d['title'],d.get('description',''),head(d.get('type',''),e(d['title']),e(d.get('description','')))+'<article class="section reading"><p>'+e(d.get('date',''))+' · '+e(d.get('author',''))+'</p>'+text+actions+'</article>')
page('admin/','Uređivanje sadržaja','Pristup uredničkom panelu',head('UREDNICI','Uređivanje sadržaja')+'<section class="section reading"><p>Sadržaj se uređuje kroz Pages CMS, uz prijavu i odobren pristup GitHub repozitorijumu. Povezivanje repozitorijuma za ovaj projekat još nije završeno.</p><a class="button" href="https://app.pagescms.org/" rel="noopener">Otvorite Pages CMS ↗</a><p>Promene nisu moguće bez odgovarajućih dozvola. Ne unosite lozinke na ovom sajtu.</p></section>')
page('instalacija/','Sajt na telefonu','Dodajte sajt na početni ekran',head('SAJT KAO APLIKACIJA','Na vašem početnom ekranu')+'<section class="section reading"><h2>Android</h2><p>Otvorite sajt u Chrome-u. U meniju izaberite „Dodaj na početni ekran“ ili „Instaliraj aplikaciju“, ako je ponuđeno.</p><h2>iPhone i iPad</h2><p>Otvorite sajt u Safari-ju, dodirnite dugme za deljenje i izaberite „Dodaj na početni ekran“.</p><p>Za materijale i YouTube snimke potrebna je internet veza. Dostupnost instalacije zavisi od pregledača; privatni pregled može zahtevati prijavu.</p></section>')
page('privatnost/','Privatnost','Informacije o privatnosti',head('PRIVATNOST','Vaši podaci')+'<section class="section reading"><p>Ova verzija nema kontakt obrazac, naloge posetilaca niti analitičke alate. Ne tražimo podatke o deci. Kontakt putem imejla obrađuje se preko imejl servisa.</p><p>YouTube i drugi spoljni servisi otvaraju se tek izborom njihovog linka i imaju sopstvene politike privatnosti. Hosting obrađuje tehničke podatke potrebne za isporuku sajta. Privatni pregled koristi i prijavu pružaoca pregleda.</p><p>Za pitanja pišite na '+s['email']+'. Ovaj tekst treba ponovo pregledati pre dodavanja novih servisa.</p></section>')

# English static site: translate authored interface strings, preserving untranslatable user posts.
TRANSLATIONS = {
 'O nama':'About Us','Propovedi':'Sermons','Newsletter':'Newsletter','Podrži nas':'Support Us','Prenos ↗':'Watch Live ↗',
 'Meni ☰':'Menu ☰','Pređi na sadržaj':'Skip to content','Dobro došli u':'Welcome to','Evanđeosku crkvu Jagodina.':'Evangelical Church Jagodina.',
 'Ova stranica je napravljena da se propoveda Jevanđelje o Isusu Hristu, Spasitelju sveta. Svi su dobrodošli, bez obzira na veroispovest ili nacionalnu pripadnost. Bog voli sve ljude!':'This website exists to proclaim the Gospel of Jesus Christ, the Savior of the world. Everyone is welcome, regardless of religion or nationality. God loves all people!',
 'Pratite bogosluženje':'Watch Our Service','Posetite nas':'Visit Us','Fotografije naše crkve':'Photos of our Church', 'Fotografija iz Evanđeoske crkve Jagodina':'Photo from Evangelical Church Jagodina',
 'Ovde će biti fotografije naše zajednice.':'Photos of our church community will appear here.','Dodajte svoje fotografije u folder public/slike.':'Add your photos to public/slike.',
 'BOGOSLUŽENJA I PROPOVEDI':'SERVICES AND SERMONS','Pratite naše poslednje bogosluženje.':'Watch Our Latest Service.', 'Pogledajte snimke i propovedi naše crkve.':'Watch our recorded services and sermons.', 'Bogosluženje uživo':'Watch Live',
 'POSLEDNJA PROPOVED':'LATEST SERMON','Ovde će se prikazati najnovija propoved kada dodamo YouTube snimak.':'Our latest sermon will appear here after we add a YouTube video.',
 'Sadržaj je u pripremi.':'Content coming soon.','VIDEO ARHIVA':'VIDEO ARCHIVE','Propovedi i prethodna bogosluženja':'Sermons and Past Services','Pregledajte dostupne video-snimke i biblijske poruke.':'Browse available recordings and Bible messages.','Pogledajte propovedi':'Browse Sermons',
 'MATERIJALI I SLUŽBE':'MINISTRIES AND RESOURCES','Resursi za sve generacije.':'Resources for Every Generation.','Cela biblioteka':'Full Library',
 'DEČJI RAD':'CHILDREN’S MINISTRY','Resursi za dečji rad':'Children’s Ministry Resources','Biblijske lekcije, aktivnosti i materijali za učitelje i roditelje.':'Bible lessons, activities, and resources for teachers and parents.',
 'OMLADINSKI RAD':'YOUTH MINISTRY','Resursi za omladinski rad':'Youth Ministry Resources','Biblijske pouke, razgovori i materijali za mlade.':'Bible studies, discussions, and youth resources.',
 'MUZIKA I SLAVLJENJE':'WORSHIP AND MUSIC','Slavljenje našeg tima':'Our Worship Team','Pesme i snimci našeg tima za slavljenje, kada ih objavimo.':'Songs and recordings from our worship team will appear here.',
 'Otvori resurse':'Explore Resources','Pogledaj biblioteku':'Explore Library','DUHOVNI RAST':'SPIRITUAL GROWTH','Ohrabrenja iz Božije reči.':'Encouragement from God’s Word.','Sva ohrabrenja':'All Devotionals','NAJNOVIJE OHRABRENJE':'LATEST DEVOTIONAL',
 'Ovde ćemo objavljivati mesečna ohrabrenja i biblijska razmišljanja.':'Monthly devotionals and Bible reflections will appear here.','BIBLIOTEKA':'LIBRARY','Materijali za proučavanje':'Study Resources',
 'Pronađite pouke i druge resurse koji će vam pomoći u proučavanju Biblije.':'Explore Bible study guides and other helpful resources.','Istražite biblioteku':'Explore Library',
 'DOBRO DOŠLI U JAGODINU':'WELCOME TO JAGODINA','Rado ćemo vas upoznati.':'We Would Love to Meet You.','Svi su dobrodošli. Kontaktirajte nas ili saznajte više o našoj crkvi.':'Everyone is welcome. Contact us or learn more about our church.','Kontaktirajte nas':'Contact Us',
 'Upoznajte našu crkvu':'Get to Know Our Church','Budimo zajedno, gde god da ste':'Together Wherever You Are','Slušajte. Proučavajte. Rastite.':'Listen. Study. Grow.','Mali koraci. Velike istine.':'Small Steps. Great Truths.',
 'Vera u svakodnevnom životu':'Faith in Everyday Life','Prostor za rast u Božijoj reči':'Grow in God’s Word','Dobri materijali. Na jednom mestu.':'Useful Resources in One Place.',
 'Resursi za zajedničko služenje':'Resources for Serving Together','Vreme za zajedništvo':'Time for Fellowship','Dobro došli u Jagodinu':'Welcome to Jagodina',
 'Dečja služba':'Children’s Ministry','Omladinska služba':'Youth Ministry','Duhovni rast':'Spiritual Growth','Biblioteka':'Library','Drugim crkvama':'For Other Churches','Događaji':'Events','Kontakt':'Contact',
 'Prijavite se za novosti naše službe':'Subscribe to Ministry Updates','Podržite naš rad':'Support Our Ministry',
 'Pišite nam':'Write to Us','Želite da primate novosti o našoj službi, propovedima i novim materijalima? Prijava putem imejla biće dostupna kada povežemo servis za slanje. Do tada nam možete pisati.':'Would you like updates about our ministry, sermons, and resources? Email signup will be available once a mailing service is connected. Until then, feel free to email us.',
 'Hvala što želite da podržite službu Evanđeoske crkve Jagodina. Informacije o mogućnostima podrške objavićemo nakon potvrde zvaničnih podataka za uplatu.':'Thank you for your interest in supporting Evangelical Church Jagodina. Donation details will be published once official payment information has been confirmed.',
 'Evanđeoska crkva Jagodina':'Evangelical Church Jagodina','Dobro došli! Zajedno slušamo i delimo Božiju reč.':'Welcome! Together we listen to and share God’s Word.',
 'Istražite':'Explore','Ostanimo u kontaktu':'Stay in Touch','Za informacije o poseti i bogosluženjima':'For information on visiting and services','pišite nam imejlom.':'please email us.',
 'Dodajte sajt na telefon':'Add to Home Screen','Privatnost':'Privacy','Uređivanje sadržaja':'Content Editor','Privatni pregled • sadržaj je u pripremi':'Preview • content coming soon',
 'Upoznajte našu crkvu':'Meet Our Church','Sadržaj je u pripremi':'Content Coming Soon','Ovde će se pojaviti zvanični sadržaji kada budu objavljeni.':'Official resources will appear here when published.',
 'U šta verujemo':'What We Believe','Vizija i misija':'Vision and Mission','Rukovodstvo':'Leadership','Zvanične informacije su u pripremi.':'Official details will be added soon.',
 'Kako da nas posetite':'How to Visit','Pišite nam':'Write to Us','Kontakt imejl crkve':'Church Email','Za informacije o dolasku, terminima i materijalima.':'For visiting, service times, and resources.','Raspored bogosluženja':'Service Times','Posetite nas':'Visit Us',
 'Tačna adresa će biti objavljena nakon potvrde.':'The address will be published once confirmed.', 'Termini će biti objavljeni nakon potvrde. Pre dolaska kontaktirajte crkvu.':'Service times will be published once confirmed. Please contact the church before visiting.',
 'Pretražite naslove, biblijske tekstove i opise':'Search titles, Scripture references, and descriptions','Šta želite da proučavate?':'What would you like to study?','Nema rezultata za izabranu pretragu.':'No matching resources found.',
 'Tip materijala':'Resource Type','Tema':'Topic','Služba':'Ministry','Jezik':'Language','Autor / govornik':'Author / Speaker','Uzrast':'Age Group','Serija':'Series','Sve':'All','Otvorite / preuzmite materijal':'Open / Download Resource',
 'Prijava putem imejla':'Email Signup','Na vašem početnom ekranu':'On Your Home Screen','Sajt na telefonu':'Church Website on Your Phone',
 'Sadržaj se uređuje kroz Pages CMS, uz prijavu i odobren pristup GitHub repozitorijumu. Povezivanje repozitorijuma za ovaj projekat još nije završeno.':'Content is managed through Pages CMS with authorized GitHub access. This repository has not been connected yet.',
 'Otvorite Pages CMS':'Open Pages CMS','Promene nisu moguće bez odgovarajućih dozvola. Ne unosite lozinke na ovom sajtu.':'Editing requires permission. Never enter passwords into this website.',
}
from html.parser import HTMLParser
class EnglishParser(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True); self.out=[]; self.in_script=False
 def handle_starttag(self,tag,attrs):
  if tag=='script': self.in_script=True
  items=[]
  for k,v in attrs:
   if v is None: items.append(k); continue
   if k=='href' and v.startswith('/') and not v.startswith('//') and not v.startswith('/media/') and v not in ['/style.css','/app.js','/manifest.webmanifest']:
    v='/en/'+v.lstrip('/')
   if k=='lang' and tag=='html': v='en'
   if k=='href' and 'lang-switch' in dict(attrs).get('class',''): v=v.replace('/en/en/','/') if v.startswith('/en/en/') else v
   if k=='lang' and tag=='a' and 'lang-switch' in dict(attrs).get('class',''): v='sr'
   if k=='aria-label' and v=='Switch to English':v='Prebaci na srpski'
   if k in ('content','alt','placeholder','aria-label'):v=TRANSLATIONS.get(v,v)
   items.append(k+'="'+html.escape(v,quote=True)+'"')
  self.out.append('<'+tag+(' '+' '.join(items) if items else '')+'>')
 def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs)
 def handle_endtag(self,tag): self.out.append('</'+tag+'>'); self.in_script=False if tag=='script' else self.in_script
 def handle_data(self,data):
  if self.in_script:self.out.append(data);return
  if data in TRANSLATIONS:self.out.append(TRANSLATIONS[data]);return
  m=re.match(r'^(\s*)(.*?)(\s*)$',data,flags=re.S)
  self.out.append(m[1]+TRANSLATIONS.get(m[2],m[2])+m[3] if m else data)
 def handle_entityref(self,name):self.out.append('&'+name+';')
 def handle_charref(self,name):self.out.append('&#'+name+';')
 def handle_comment(self,data):self.out.append('<!--'+data+'-->')
for src in list(O.rglob('*.html')):
 if '/en/' in str(src):continue
 rel=src.relative_to(O); dst=O/'en'/rel;dst.parent.mkdir(parents=True,exist_ok=True)
 parser=EnglishParser(); source=src.read_text(encoding='utf-8')
 if rel==Path('index.html'):
  for key,key_en in [('title','title_en'),('accent','accent_en'),('description','description_en')]:
   val=e(home.get(key)); replacement=e(home.get(key_en) or home.get(key));source=source.replace(val,replacement)
 parser.feed(source)
 out=''.join(parser.out)
 # language switch on EN page must link back to corresponding SR page
 out=out.replace('href="/en/'+str(rel.parent).replace('\\','/')+'/" lang="sr"','href="/'+str(rel.parent).replace('\\','/')+'/" lang="sr"')
 out=out.replace('>EN</a>','>SR</a>')
 dst.write_text(out,encoding='utf-8')

(O/'robots.txt').write_text('User-agent: *\n'+('Disallow: /\n' if preview else 'Allow: /\nSitemap: '+base+'/sitemap.xml\n'))
(O/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+e(u)+'</loc></url>' for u in urls if '/admin/' not in u)+'</urlset>')
(O/'data.json').write_text(json.dumps(records,ensure_ascii=False))
print(f'Built {len(urls)} pages; {len(records)} published posts; preview={preview}')
