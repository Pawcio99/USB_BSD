# Ubuntu — planowany CHERUB USB SYNC

Status: NOT TESTED. Na FreeBSD zweryfikowano wyłącznie dostęp do dysku w trybie RO. Komponent Ubuntu ma docelowo wykonywać przyrostowe kopie `rsync`, oddzielnie dla każdego komputera, po sprawdzeniu UUID woluminu.

Nie uruchamiać automatycznego zapisu, dopóki nie będą gotowe testy montowania, blokady równoległej synchronizacji, obsługi odłączenia USB i odtwarzania plików. Brak opcji `--delete` nie oznacza wersjonowania kopii.

Kod prototypowy zostanie opublikowany po uzupełnieniu testów i audycie instalatora. Projekt FreeBSD pozostaje niezależny od komponentu Ubuntu.
