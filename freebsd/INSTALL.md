# FreeBSD — procedura kontrolowana

Projekt dokumentuje instalację na FreeBSD 15.1. Publikowana wersja skryptu jest parametryzowaną adaptacją uruchomionego wcześniej na stanowisku rozwiązania. Nie zastępuj działającego skryptu bez audytu.

1. Sprawdź przez `glabel status`, `gpart show`, `file -sL /dev/gpt/primary`, `automount -L` i `mount -t ext2fs` identyfikację nośnika.
2. Zapewnij wcześniej mapę autofs odpowiadającą `auto_cherub.example`. Nie kopiuj jej w ciemno.
3. Utwórz lokalnie `/usr/local/etc/cherub-usb-ro.conf` z wierszem `CHERUB_USB_UUID=TWÓJ_UUID`; ustaw `chown root:wheel` i `chmod 600`.
4. Dopiero po zatwierdzeniu instalacji umieść `cherub-usb-ro` w `/usr/local/sbin/` z trybem 0700.
5. Wykonaj ręczny test `/usr/local/sbin/cherub-usb-ro`; zweryfikuj wpis `mount -t ext2fs` z `read-only,nosuid,noexec`.
6. Harmonogram w `cherub-usb-ro.cron.example` jest opcjonalny. Jego rzeczywiste wykonanie, hotplug i restart wymagają osobnych testów.

## Rollback

Po audycie usuń tylko pliki stworzone dla tego wdrożenia: `/usr/local/etc/cron.d/cherub-usb-ro`, `/usr/local/sbin/cherub-usb-ro`, `/usr/local/etc/cherub-usb-ro.conf`. Nie usuwaj map autofs używanych przez inne mechanizmy. Zmiany w konfiguracji dysku i montowania muszą mieć osobny plan.

Nie stosuj `newfs`, `fsck` z naprawą ani montowania RW. Prawdziwy test backupu wymaga odtworzenia danych.
