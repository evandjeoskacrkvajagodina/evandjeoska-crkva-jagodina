# Počnite ovde

Za Visual Studio Code, izmene tekstova, GitHub i lokalni pregled otvorite **UPUTSTVO-ZA-UREDJIVANJE.md**. Novi vizuelni pravac koristi vaš logo i toplu crveno-narandžasto-žutu paletu na beloj podlozi. Vizija: podizanje vođa mentorisanjem.

# Evanđeoska crkva Jagodina — predaja projekta

## Status
Pripremljen statički sajt, generator sadržaja i Pages CMS konfiguracija. Spoljna GitHub/CMS/Cloudflare povezivanja i prijava urednika nisu izvršeni ni potvrđeni. Test verzija nema indeksiranje. Naziv, imejl i vizija su uneti prema korisnikovim podacima. Ostale zvanične informacije čekaju unos. Nema izmišljenih propovedi ni događaja.

## Cloudflare Pages i GitHub
1. Napravite privatni GitHub repozitorijum i prenesite sadržaj ovog projekta, uključujući `.pages.yml`. Izostavite `.openai`, `dist` i `.git`.
2. U Cloudflare Workers & Pages izaberite Pages → povezivanje postojećeg GitHub repozitorijuma. Ako je otvoren Workers ekran, prebacite se na Pages.
3. Framework: None. Build command: `python3 -X utf8 scripts/build.py`. Output: `dist`. Generator koristi Python 3 iz build okruženja; proverite uspešan build log.
4. Za probni pages.dev sajt ne postavljajte PRODUCTION=1. SITE_URL postavite na probni URL. Test verzije imaju noindex i robots Disallow.
5. Tek posle odobrenja dizajna i zvaničnih podataka dodajte domen u Pages → Custom domains. Cloudflare vodi DNS podešavanje. Ne menjajte vlasništvo domena. Proverite HTTPS.
6. Za zvanično objavljivanje postavite PRODUCTION=1 i SITE_URL=https://evandjeoskacrkvajagodina.com, ponovo izgradite sajt. Proverite canonical, sitemap i robots na domenu. Zaštitite preview deployment ako je dostupan kroz Cloudflare Access; noindex nije zaštita pristupa.

## Pages CMS: uređivanje bez koda
Otvorite https://app.pagescms.org/ i prijavite se preko GitHub-a. Odobrite pristup samo ovom repozitorijumu. Izaberite repozitorijum i granu koja se objavljuje.
U „Objave i materijali“ dodajte zapis. Unesite naslov, jedinstveni slug (npr. vera-i-nada), odeljak, datum i opis. Popunite ostala relevantna polja. Tekst je običan tekst sa praznim redom između pasusa. Dokument dodajte kroz polje Dokument. Prilozi moraju biti manji od 25 MiB; preporuka ispod 20 MiB. Potrebno je pravo objavljivanja.
Nacrt je podrazumevano uključen. Sačuvajte i proverite. Isključite Nacrt i sačuvajte za objavljivanje. Povlačenje: uključite Nacrt ili obrišite zapis. Izmena aktivira novi Cloudflare build tek kada je Git integracija povezana. Kategorije se unose u polja; filteri se automatski formiraju iz objavljenih zapisa.
Pod „Podaci crkve“ unesite odobrene podatke. Adresa se prikazuje kao tekst; Google mapa i društvene mreže još nisu povezani. YouTube kanal otvara se linkom, bez tvrdnje da je prenos trenutno uživo. U ovoj verziji nije ugrađen player niti automatsko otkrivanje prenosa.

## Obavezna provera CMS procesa nakon prijave
Napravite nacrt, potvrdite da se ne vidi. Objavite jednu odobrenu probnu objavu na test sajtu, proverite njenu stranicu i filtere, zatim je povucite i proverite novi build. Proverite PDF na telefonu. Ove provere prijave i Git webhooka još nisu izvršene.

## Google
Posle objavljivanja otvorite Google Search Console, dodajte Domain property, kopirajte prikazani TXT zapis u Cloudflare DNS i verifikujte. Pošaljite /sitemap.xml. Indeksiranje nije trenutno i pozicija nije garantovana.
Google Business Profile kreirajte samo za stvarnu lokaciju crkve koja prima posetioce i ispunjava Google uslove; koristite tačan naziv, adresu i vreme, odgovarajuću kategoriju i svoj nalog. Prođite verifikaciju koju Google zahteva. Ne unosite izmišljenu adresu. Povežite zvanični domen. Mapa se dodaje tek kada lokacija bude potvrđena.

## Rezervne kopije i oporavak
Uključite 2FA/passkeys na Google/YouTube, GitHub i Cloudflare nalozima. Recovery kodove sačuvajte van računara i naloga. Samo potrebni urednici imaju dozvole; CMS aplikacija samo za odabrani repo. Nikad ne šaljite lozinke ili tokene u chat ili kod.
GitHub istorija nije nezavisna rezervna kopija. Nedeljno napravite git bundle na eksterni disk, pa kopiju u odvojenu cloud arhivu: `git bundle create crkva-backup.bundle --all`. Iz lokalnog repoa kopirajte i originalne dokumente. Probajte oporavak: `git clone crkva-backup.bundle oporavak` i pokrenite build.
Originalne video-snimke posle svakog snimanja čuvajte lokalno, na eksternom disku i u odvojenom oblaku. YouTube služi distribuciji. Obrisani YouTube snimak se ne vraća iz Git-a; potrebno je original ponovo postaviti, ažurirati link u CMS-u i objaviti.
Vodite evidenciju: datum, naslov, govornik, YouTube URL, putanja originala, eksterni disk, cloud kopija, datum provere. Svaka tri meseca proverite otvaranje nasumične kopije. Ne aktivirajte plaćeno skladište dok ne izmerite postojeći GB i mesečni rast. Video-bitrate * sekunde / 8 daje približne bajtove; 1 sat na 10 Mb/s ≈ 4,5 GB.

## Troškovi i ograničenja (provereno 16.10.2026)
Cloudflare Pages Free: 500 buildova mesečno, do 20.000 fajlova, maksimalno 25 MiB po fajlu. Pages CMS navodi da je besplatan. GitHub i servisi mogu menjati kvote; ponovo proverite pre produkcije. Početna arhitektura ne zahteva plaćenu pretplatu; domen se obnavlja po ceni registrara. Ne uključuje velike video rezervne kopije, dodatnu pohranu ni kupovinu diska.
Izvori: https://developers.cloudflare.com/pages/platform/limits/ ; https://pagescms.org/ ; https://pagescms.org/docs/configuration/ .

## Tehničke granice
Nema service worker-a: ne keširamo zastarele prenose niti obećavamo offline sadržaj. Manifest i PNG ikonice omogućavaju dodavanje na telefon gde pregledač podržava. Nema kontakt obrasca ni prikupljanja podataka o deci. Kontakt je mailto. Sadržaj se generiše iz JSON zapisa: nije potrebno ručno pravljenje stranica. Filtriranje preuzima indeks svih objava, što je dovoljno za početnu biblioteku; za desetine hiljada zapisa planirati podeljen indeks. Rezervne video datoteke ne držati u Git repozitorijumu.
