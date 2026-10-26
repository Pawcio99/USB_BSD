# USB_BSD — CHERUB USB STORAGE

Autorski projekt archiwizacji i kontrolowanego dostępu do przenośnego dysku USB na FreeBSD i Ubuntu.

**Autor / opiekun:** [Pawcio99](https://github.com/Pawcio99)  
**Stan projektu:** FreeBSD: potwierdzony odczyt RO i montowanie autofs; automatyzacja cron zainstalowana, bez testu po ponownym starcie / podłączeniu; Ubuntu: kod prototypowy, bez testu na hoście.

[Strona projektu](https://pawcio99.github.io/USB_BSD/) — zacznie działać po włączeniu GitHub Pages (`main` / `docs`).

## Cele

- Jeden wymienny nośnik danych używany kolejno na wielu komputerach.
- FreeBSD 15.1: automatyzacja montowania `ext4` jako `ext2fs`, wyłącznie `read-only`, `nosuid`, `noexec`.
- Ubuntu 26.04: oddzielone przestrzenie archiwum każdego hosta; przyszłe automatyczne kopie przyrostowe.
- Brak autorun skryptów z nośnika. Skrypty instalowane lokalnie i kontrolowane przez operatora.

## Struktura

- `freebsd/` — skrypt do montowania tylko do odczytu, instrukcja oraz wzory konfiguracji. Wariant publikacyjny z lokalnym plikiem UUID nie był jeszcze testowany na FreeBSD.
- `ubuntu/` — opis planowanego prototypu CHERUB USB SYNC v1; kod wykonawczy nie został jeszcze opublikowany i nie jest zweryfikowany produkcyjnie.
- `verification/` — raporty walidacji i znane ograniczenia.
- `docs/` — statyczna strona GitHub Pages, przygotowana na fotografie.

## Status walidacji

| Test | Wynik |
|---|---|
| FreeBSD wykrywa partycję GPT/ext4 i UUID | PASS — raport operatora 2026-10-26 |
| FreeBSD uruchamia `automountd`, `autounmountd`, `devd` | PASS — raport operatora |
| FreeBSD montuje `ext2fs` z `read-only,nosuid,noexec` | PASS — wynik `mount` |
| `cherub-usb-ro` ręcznie kończy się PASS | PASS — raport operatora |
| Cron zainstalowany | PASS — odczyt konfiguracji |
| Cron uruchomił cykliczny skrypt | NOT TESTED |
| Auto-mount po ponownym włożeniu USB | NOT TESTED |
| Auto-mount po restarcie FreeBSD | NOT TESTED |
| Synchronizacja danych Ubuntu | NOT TESTED |

## Bezpieczeństwo

Kod `freebsd/cherub-usb-ro` oparto na implementacji zgłoszonej jako zainstalowana na stanowisku, zastępując przy publikacji wpisany na stałe UUID konfiguracją lokalną. Skrypt publikacyjny nie jest uniwersalnym instalatorem. Bazuje na odczycie identyfikacji przez `file` i sprawdzeniu opcji `mount`; zastosowanie na innym urządzeniu wymaga audytu. Publikowane materiały nie zawierają identyfikatora UUID użytego dysku. Nie publikuj prywatnych logów, numerów seryjnych urządzeń ani fotografii bez usunięcia metadanych i danych widocznych na ekranach.

Nie używaj `newfs`, `fsck` z naprawą ani montowania RW na podstawie tego projektu. Sprawdzaj realną integralność i odtwarzanie archiwum. Opcja `rsync` bez `--delete` nie stanowi wersjonowania.

## Licencja

Na tym etapie prawa autorskie zastrzeżone. Nie wybrano jeszcze licencji na ponowne wykorzystywanie kodu. Udostępnienie publicznego repozytorium nie oznacza nadania automatycznej licencji open-source.

## Instalacja i rozwój

FreeBSD: [procedura audytu i kontrolowanego wdrożenia](freebsd/INSTALL.md). Zmiany na hoście wymagają osobnego zatwierdzenia.
Plan Ubuntu znajduje się w `ubuntu/` i NIE są zweryfikowanym produkcyjnie systemem synchronizacji.

Strona WWW znajduje się w `docs/index.html`; galeria zdjęć pozostaje pusta do czasu dostarczenia i anonimizacji fotografii.