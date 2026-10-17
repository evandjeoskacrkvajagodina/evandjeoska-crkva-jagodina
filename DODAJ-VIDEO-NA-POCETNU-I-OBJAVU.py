from pathlib import Path
p=Path('scripts/build.py')
h=Path('public/_headers')
if not p.exists() or not h.exists():
    raise SystemExit('GRESKA: Otvorite glavni folder projekta (scripts/build.py i public/_headers).')
s=p.read_text(encoding='utf-8')
if 'def youtube_embed(' in s:
    raise SystemExit('Video je vec dodat u ovaj projekat; nema novih izmena.')
if 'def youtube_thumbnail(url):' not in s:
    raise SystemExit('Nedostaje prethodna ispravka za thumbnail. Nista nije promenjeno.')
start=s.find('def latest(items,label,desc):')
end=s.find('\nbody+=', start)
if start<0 or end<0: raise SystemExit('Nije nadjen blok latest; nista nije promenjeno.')
old="head(d.get('type',''),e(d['title']),e(d.get('description','')))+'<article class=\"section reading\"><p>'+e(d.get('date',''))+' · '+e(d.get('author',''))+'</p>'+text+actions+'</article>'"
if s.count(old)!=1: raise SystemExit('Nije nadjen blok pojedinacne objave; nista nije promenjeno.')
# Replace both sections atomically after validating markers.
helper='''\ndef youtube_embed(url):
    """YouTube player bez dodatnih usluga. Podrzava watch, youtu.be, live i shorts."""
    from urllib.parse import urlparse, parse_qs
    if not isinstance(url, str) or not url.strip():
        return ''
    u=urlparse(url.strip())
    host=(u.hostname or '').lower()
    parts=[a for a in u.path.split('/') if a]
    vid=''
    if host in ('youtube.com','www.youtube.com','m.youtube.com'):
        if u.path=='/watch': vid=parse_qs(u.query).get('v',[''])[0]
        elif len(parts)>1 and parts[0] in ('live','shorts','embed'): vid=parts[1]
    elif host in ('youtu.be','www.youtu.be') and parts:
        vid=parts[0]
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}',vid):
        return ''
    return ('<div class="service-video" style="aspect-ratio:16/9;width:100%;margin:16px 0 22px">'
            '<iframe loading="lazy" style="width:100%;height:100%;border:0;border-radius:12px" '
            'src="https://www.youtube-nocookie.com/embed/'+vid+'" '
            'title="Pogledajte bogosluzenje" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>')
'''
replacement='''def latest(items,label,desc):
 if items:
  d=items[0]
  video=youtube_embed(d.get('youtube',''))
  if video:
   return ('<div class="latest-card"><span class="eyebrow">'+label+'</span>'
           +video+'<h3>'+e(d['title'])+'</h3><p>'+e(d.get('description',''))
           +'</p><a href="/objave/'+e(d['slug'])+'/">Detalji bogosluzenja ↗</a></div>')
  return '<a class="latest-card" href="/objave/'+e(d['slug'])+'/"><span class="eyebrow">'+label+'</span><h3>'+e(d['title'])+'</h3><p>'+e(d.get('description',''))+'</p><b>Pročitajte više ↗</b></a>'
 return '<div class="latest-card"><span class="eyebrow">'+label+'</span><h3>Sadržaj je u pripremi.</h3><p>'+desc+'</p></div>'
'''
s=s[:start]+helper+'\n'+replacement+s[end:]
s=s.replace(old,"head(d.get('type',''),e(d['title']),e(d.get('description','')))+'<article class=\"section reading\">'+youtube_embed(d.get('youtube',''))+'<p>'+e(d.get('date',''))+' · '+e(d.get('author',''))+'</p>'+text+actions+'</article>'",1)
headers=h.read_text(encoding='utf-8')
if 'frame-src ' not in headers:
    headers=headers.replace("frame-ancestors 'none';", "frame-src https://www.youtube-nocookie.com https://www.youtube.com; frame-ancestors 'none';")
elif 'www.youtube-nocookie.com' not in headers:
    raise SystemExit('Postoji posebno frame-src pravilo. Potrebna je rucna provera, nista nije promenjeno.')
p.write_text(s,encoding='utf-8')
h.write_text(headers,encoding='utf-8')
print('USPEH: Video dodat na pocetnu stranicu i na stranicu bogosluzenja.')
print('Sledece: GitHub Desktop -> Commit to main -> Push origin.')
