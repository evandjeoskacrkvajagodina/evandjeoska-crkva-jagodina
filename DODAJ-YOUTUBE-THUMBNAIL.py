from pathlib import Path
p = Path('scripts/build.py')
if not p.is_file():
    raise SystemExit('GRESKA: Pokreni ovu skriptu iz glavnog foldera sajta (gde su scripts i content).')
s = p.read_text(encoding='utf-8')
start = s.find('def cards(items):')
end = s.find('\ndef head(', start)
if start < 0 or end < 0:
    raise SystemExit('Nije pronađen očekivani deo koda. Ništa nije menjano.')
if 'youtube_thumbnail' in s:
    raise SystemExit('YouTube thumbnail je već dodat. Ništa nije menjano.')
replacement = '''def youtube_thumbnail(url):
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
'''
p.write_text(s[:start] + replacement + s[end:], encoding='utf-8')
print('USPEH: YouTube thumbnail dodat na kartice sa YouTube linkom.')
