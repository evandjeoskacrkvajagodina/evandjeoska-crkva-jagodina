# Vaš sajt — uređivanje u Visual Studio Code-u

## Šta dobijate
Kompletan izvorni kod, logo, konfiguraciju CMS-a i gotov `dist` direktorijum sajta. Nema lozinki i tokena. Projekat možete sačuvati u svom GitHub repozitorijumu, menjati i postavljati na Cloudflare Pages. GitHub i Cloudflare nalog korisnika još nisu povezani.

## Otvaranje
1. Raspakujte ZIP u jednu fasciklu, na primer `crkva-jagodina`.
2. U Visual Studio Code-u izaberite **File → Open Folder**, pa tu fasciklu.
3. Za generisanje i pregled potrebni su Python 3 i komanda `python` ili Windows launcher `py`. Na Windows-u tokom instalacije Python-a uključite dodavanje u PATH. Node i npm nisu potrebni za lokalno uređivanje.
4. Na Windows-u pokrenite `POKRENI-PREGLED.cmd`, ili u VS Code terminalu unesite `py -3 -X utf8 scripts/dev.py`. Na macOS/Linux-u koristite `python3 -X utf8 scripts/dev.py`.
5. Otvara se http://localhost:8000. Kada sačuvate izmene, generator ponovo napravi sajt; osvežite stranicu da ih vidite. Za prekid pritisnite Ctrl+C.

Lokalni pregled koristite na svom računaru. Ne postavljajte ovaj Python server kao javni produkcioni server. Za ručno otvaranje gotovog sajta koristite statički server za direktorijum `dist`; dvoklik na HTML ne podržava sve putanje i pretragu.

## Gde se šta menja

| Fajl | Šta uređujete |
| --- | --- |
| `content/homepage.json` | Glavni naslov, uvod, dugme i uvodni tekst mentorstva |
| `content/settings.json` | Imejl, vizija, podaci crkve i YouTube kanal |
| `public/style.css` | Boje, fontovi, razmaci i mobilni izgled; paleta je na početku fajla |
| `public/logo.png` | Logo bez sive pozadine; zamenite ga svojim originalnim transparentnim PNG-om kada ga budete imali |
| `public/app-icon.png` | Ikonica aplikacije, pripremljena prema logotipu |
| `scripts/build.py` | Struktura stranica i ostali tekstovi interfejsa |
| `public/app.js` | Mobilni meni i pretraga/filteri |
| `content/posts/*.json` | Propovedi, pouke, događaji i materijali |
| `.pages.yml` | Administratorski interfejs kroz Pages CMS |

Sačuvajte tekstove kao **UTF-8**. JSON zahteva dvostruke navodnike i zareze između polja. VS Code označava sintaksne greške. Ne menjajte `dist` kada želite trajne izmene: on se ponovo pravi iz izvornog koda.

## Primer objave
Napravite `content/posts/prva-pouka.json` sa sledećim sadržajem. Primer ostaje nacrt dok ne isključite draft. Primer nije poruka ili učenje crkve.

```json
{
  "title": "Naslov vaše pouke",
  "slug": "prva-pouka",
  "draft": true,
  "section": "duhovni-rast",
  "date": "2026-10-16",
  "description": "Vaš kratki opis.",
  "author": "",
  "scripture": "",
  "series": "",
  "topic": "",
  "ministry": "",
  "type": "Biblijska pouka",
  "language": "Srpski",
  "age": "",
  "youtube": "",
  "file": "",
  "body": "Vaš odobreni tekst.\n\nNovi pasus."
}
```

Odeljci: `propovedi`, `duhovni-rast`, `decja-sluzba`, `omladinska-sluzba`, `drugim-crkvama`, `dogadjaji` ili `biblioteka`. Sve objavljene stavke ulaze u biblioteku. PDF smestite u `public/media`, pa upišite putanju poput `/media/moj-materijal.pdf`. CMS omogućava isto bez ručnog pisanja JSON-a nakon povezivanja sa GitHub-om. Samo `draft: false` objavljuje stavku.

## Čuvanje na GitHub-u
U VS Code-u otvorite **Source Control**, pokrenite **Initialize Repository** ako ga nema, napravite prvi commit i izaberite **Publish to GitHub**. Preporuka je privatni repozitorijum. Ne dodajte `.env`, lozinke, tokene ni originalne video-snimke. ZIP već ima `.gitignore`. Sačuvajte `.pages.yml`, izvore i `public` direktorijum. `dist` se generiše, ne mora se čuvati u Git-u. Posle izmena napravite commit i **Sync Changes**.

## Cloudflare Pages
Povežite ovaj repozitorijum sa Pages projektom. Build command: `python3 -X utf8 scripts/build.py`; output: `dist`. Ne uključujte PRODUCTION=1 za test. Posle odobrenja i povezivanja zvaničnog domena postavite `PRODUCTION=1` i `SITE_URL=https://evandjeoskacrkvajagodina.com` i ponovo izgradite. Trenutni privatni pregled i zvanični Cloudflare projekat su odvojeni.

## Telefon i aplikacija
Ovo je izvorni kod sajta sa manifestom za PWA. Isti sajt na javnom HTTPS domenu može se dodati na početni ekran u podržanim pregledačima. Ne sadrži zasebnu Android/iOS aplikaciju za prodavnice. Ako se kasnije odlučite za njih, sadržaj, logo i dizajn mogu se ponovo koristiti, uz dodatnu izradu i podešavanje. Video-snimci i biblioteka zahtevaju internet.

## Šta je još potrebno
Potvrđena adresa, termini, zvanični YouTube kanal, stvarni materijali; prijava na vaš GitHub i Cloudflare, povezivanje CMS-a i provera uredničkog procesa. Mentorstvo trenutno vodi na kontakt imejl; termini, prijave, mentori i program nisu izmišljeni. Vizuelni pregled u pregledaču u ovom okruženju nije izvršen.
