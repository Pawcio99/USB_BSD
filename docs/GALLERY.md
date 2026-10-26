# Dokumentacja fotograficzna USB_BSD

## Architektura publikacji

Repozytorium GitHub jest źródłem prawdy dla treści i zdjęć. GitHub Pages serwuje statyczny HTML/CSS/JavaScript. Nie ma serwera aplikacyjnego, bazy danych, formularzy ani zewnętrznych usług śledzących.

- `docs/index.html` — autorska strona i miejsca na galerie;
- `docs/assets/site.css` — projekt wizualny i responsywność;
- `docs/assets/gallery.js` — bezpieczny odczyt manifestu, odroczone ładowanie zdjęć, okno powiększenia;
- `docs/data/gallery.json` — wersjonowany katalog zdjęć;
- `docs/assets/photos/` — docelowe obrazy zatwierdzone do publikacji;
- `tools/validate_gallery.py` — kontrola schematu, nazw, rozmiarów, sygnatur i typowych metadanych;
- `.github/workflows/validate-gallery.yml` — kontrola w CI.

GitHub Pages jest statycznym hostingiem: nie uruchamia Python ani skryptów systemowych na serwerze WWW. Dodanie zdjęcia polega na zatwierdzeniu pliku i aktualizacji manifestu w Git.

## Zrzuty ekranu na FreeBSD 15.1 / GNOME

Wszystkie poniższe polecenia wykonuje użytkownik pulpitu, nie root. Operacje zapisują wyłącznie lokalne pliki PNG, nie dotykają archiwum USB.

```sh
mkdir -p "$HOME/USB_BSD-zdjecia"
command -v gnome-screenshot
echo "$XDG_SESSION_TYPE"

gnome-screenshot -d 5 -f "$HOME/USB_BSD-zdjecia/01-pulpit.png"

gio open /media
gnome-screenshot -w -d 5 -f "$HOME/USB_BSD-zdjecia/02-dysk.png"

clear
printf 'USB_BSD / FREEBSD VALIDATION\n\n'
uname -sr
ls -A /media/CHERUB_DATA >/dev/null
mount -t ext2fs | grep CHERUB_DATA
gnome-screenshot -a -f "$HOME/USB_BSD-zdjecia/03-walidacja.png"

ls -lh "$HOME/USB_BSD-zdjecia"
```

W przypadku braku `gnome-screenshot` użyj wbudowanego interfejsu Print Screen w GNOME i zapisz PNG ręcznie w tym katalogu. Nie instaluj pakietów bez oceny wpływu na system.

## Kontrola prywatności

Przed przekazaniem i przed dodaniem do publicznego repozytorium sprawdź sam obraz: nazwy prywatnych plików, zawartość terminala i przeglądarki, powiadomienia, adresy, dane uwierzytelniające, identyfikatory dysków, numery seryjne, tabliczki znamionowe, metadane lokalizacji z aparatu. Nigdy nie publikuj zdjęcia zawierającego dane wrażliwe, licząc na późniejsze usunięcie — historia Git zachowuje wcześniejsze wersje.

Obrazy będą oczyszczane i optymalizowane offline przed publikacją. Walidator identyfikuje typowe znaczniki EXIF/XMP w PNG/JPEG/WebP, ale nie rozpoznaje wszystkich możliwych metadanych ani informacji zapisanej w pikselach. Obowiązuje ręczny przegląd.

## Rejestr obrazu

Gdy zdjęcie zostanie zweryfikowane i skompresowane, dodaje się je do `docs/assets/photos/` i wpisuje do `docs/data/gallery.json`:

```json
{
  "schemaVersion": 1,
  "photos": [
    {
      "id": "01-pulpit",
      "slot": "desktop",
      "src": "assets/photos/01-pulpit.webp",
      "title": "Pulpit FreeBSD 15.1",
      "alt": "Zrzut ekranu pulpitu GNOME na stacji roboczej FreeBSD",
      "caption": "Stanowisko testowe CHERUB USB RO; widok sesji graficznej.",
      "category": "FREEBSD / GNOME"
    }
  ]
}
```

Dozwolone miejsca: `desktop`, `disk`, `validation`, `station` oraz `other`. Początkowo `photos` jest puste i strona pokazuje uczciwe symbole zastępcze, nie fotografie stockowe.

## Walidacja i publikacja

```sh
python3 tools/validate_gallery.py
node --check docs/assets/gallery.js
```

Dopiero po lokalnej walidacji, kontroli prywatności i zatwierdzeniu publikujemy zmiany. W GitHub: `Settings → Pages → Deploy from a branch → main → /docs`. Kolejne aktualizacje strony są publikowane automatycznie z tej lokalizacji po commitach (jeśli Pages jest już aktywny).

Status zrzutów oraz rzeczywistego renderowania GitHub Pages należy zawsze oceniać odrębnie. Sama poprawność plików w repozytorium nie potwierdza działania strony produkcyjnej.
