import random
import sys
import time
import pygame

#Jocul constă în parcurgerea unei matrici, iar la fiecare pas jucătorul este întrebat în ce direcție dorește să meargă
#Acesta nu știe unde este ieșirea, astfel va trebui să parcurgă matricea
#La fiecare pas va fi o șanșă ca un monstru să îl atace. Dacă nu va avea puterea necesară, va pierde și îi va scădea din
#punctele de viață. De asemenea, la fiecare pas are o șansă de a găsi poțiuni de viață, clătite pentru putere și chei pentru
#zone întunecate

#Inițializarea jocului
pygame.init()

#Inițializarea sunetului
pygame.mixer.init()
sunet_miscare = pygame.mixer.Sound("C:/Users/mare_/Desktop/Sounds/636262__uplaod__pop-one.mp3")
sunet_lovitura = pygame.mixer.Sound("C:/Users/mare_/Desktop/Sounds/158953__carlmartin__jembay-hit-11-rim.wav")
sunet_comoara = pygame.mixer.Sound("C:/Users/mare_/Desktop/Sounds/320264__vihaleipa__tambourine-hit_03.wav")

#Definire culori
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (169, 169, 169)
WHITE = (255, 255, 255)

#Ecran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Taramul Codarii")

#Dimensiuni
cols, rows = input().split()
rows = int(rows)
cols = int(cols)

#Calculăm lungimea unei celule pentru a putea reprezenta grafic elementele
cell_size = min(screen_width // cols, screen_height // rows)

#Generarea matricei, inițializată cu 0
taramul_codarii = [[0 for i in range(cols)] for j in range(rows)]

#Generarea unei matrice cu rol de marcare a locurilor unde am fost, pentru a nu abuza
#mechanica de comori
visited = [[0 for i in range(cols)] for j in range(rows)]

#Voi genera în matrice, aleatoriu, folosind biblioteca random, coordonatele ieșirii
exit_y = random.randint(0, rows - 1)
exit_x = random.randint(0, cols - 1)

#În cazul în care ieșirea era chiar în colțul din stânga jos, aventurierul a câștigat cu usurință
if exit_x == 0 and exit_y == rows - 1:
    print("Of ce simplu! Ai avut noroc și ieșirea era chiar sub nasul tău...")
    time.sleep(10)
    sys.exit()

#Voi genera zonele întunecate
zone_intunecate = random.randint(3, int(rows * cols / 2))
for _ in range(zone_intunecate):
    x = random.randint(0, cols - 1)
    y = random.randint(0, rows - 1)
    if (x == 0 and y == rows - 1):
        zone_intunecate += 1
        continue
    taramul_codarii[y][x] = -2

#Coordonatele jucatorului
player_x = 0
player_y = rows - 1

#Voi crea un sistem de viață, de scor și putere, inițial eroul având 100 de puncte de viață, 0 scor și 1 putere
punte_de_viata = 100
putere = 1
scor = 0

#Voi implementa și timp, care dacă va ajunge la 300 îl va face pe jucător să piarda
timp = 0

#De asemenea, jucătorul va avea și un număr de chei cu care va putea deschide zonele întunecate
chei = 0

#Liste pentru comoară și monștri
iteme_cufar = ["cheie", "potiune", "clatite"]
monstri = [5, 4, 3, 2, 1]


#Funcție pentru afișarea tărâmului
def afiseaza_taram():
    screen.fill(BLACK)
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if taramul_codarii[y][x] == -2:
                pygame.draw.rect(screen, DARK_GRAY, rect)
            elif y == player_y and x == player_x:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect, 1)
    pygame.display.flip()


#Funcție pentru mutarea jucătorului
def mutare_jucator(directie: str) -> None:
    #Declararea globală a variabilelor
    global player_x, player_y, timp, scor, chei, punte_de_viata, putere, iteme_cufar, monstri

    #Play la sunet de fiecare dată când ne mișcăm
    sunet_miscare.play()

    #Dacă au trecut 5 ore, am pierdut :P
    if timp > 300 or punte_de_viata <= 0:
        print("Din păcate, timpul s-a scurs aventurierule, și povestea are un final nefericit..")
        print("Scorul tău: " + str(scor))
        time.sleep(10)
        sys.exit()
    elif timp >= 150:
        print("Ai grija, s-a scurs jumatate din timp...")
        time.sleep(1)

    #Verificăm direcțiile
    if directie == 'N' and player_y > 0:
        player_y -= 1
    elif directie == 'S' and player_y < rows - 1:
        player_y += 1
    elif directie == 'E' and player_x < cols - 1:
        player_x += 1
    elif directie == 'V' and player_x > 0:
        player_x -= 1
    else:
        print("Din păcate nu putem merge acolo.. :(")
        return

    #Incrementăm scorul și timpul
    scor += 1
    timp += 1

    #În cazul în care ne aflăm pe o zonă întunecată
    exista_cheie = 0
    if taramul_codarii[player_y][player_x] == -2:
        #Cum se specifică și în cerintă, dacă suntem într-o zonă întunecată, aventurierul va pierde
        #de la 5 până la 10 secunde. Am transformat secundele în minute.
        timp += random.randint(5, 10)
        print("Te afli într-o zonă întunecată, pentru a debloca această zonă ai nevoie de o cheie")
        if chei >= 1:
            print("Vrei să folosești o cheie? (DA / NU)")
            raspuns = input()
            if (raspuns == "DA"):
                print("Ai deblocat zona.")
                taramul_codarii[player_y][player_x] = 0
                time.sleep(1)
                exista_cheie = 1
                chei -= 1
            else:
                print("Nu ai de blocat zona.")
                time.sleep(1)
        else:
            print("Din păcate nu ai nicio cheie")
            time.sleep(1)
    else:
        taramul_codarii[player_y][player_x] = 0

    #Verificăm dacă am ajuns la final
    if player_x == exit_x and player_y == exit_y and taramul_codarii[player_y][player_x] != -2:
        taramul_codarii[player_y][player_x] = -1
        print("Felicitări! Ai găsit ieșirea și ai câștigat!")
        print("Scorul tău: " + str(scor))
        time.sleep(5)
        sys.exit()

    #Voi genera un numar de la 1 -> 4. Dacă acest număr este 4, jucătorul a găsit o comoară
    #Dacă zona este întunecată, nu putem accesa această zona dacă nu avem o cheie
    if (visited[player_y][player_x] <= 2) and ((taramul_codarii[player_y][player_x] == -2 and exista_cheie == 1) or taramul_codarii[player_y][player_x] != -2):
        comoara = random.randint(1, 5)
        if comoara == 5:
            sunet_comoara.play()
            print("Felicitări aventurierule! Ai găsit o comoară!")
            time.sleep(1)
            scor += 10
            item_gasit = iteme_cufar[random.randint(0, 2)]
            print("Deschizând cufărul ai găsit... " + str(item_gasit) + "! Super!")
            time.sleep(1)
            if item_gasit == "cheie":
                chei += 1
                print("Numărul de chei: " + str(chei))
                time.sleep(1)
            elif item_gasit == "potiune":
                print("Mă simt mai bine acum... +25 PUNCTE DE VIAȚĂ")
                time.sleep(1)
                punte_de_viata += 25
                if punte_de_viata > 100:
                    punte_de_viata = 100
                    print("Sunt prea plin de viata.. :D")
                    time.sleep(1)
                print("Puncte de viață: " + str(punte_de_viata))
                time.sleep(1)
            elif item_gasit == "clatite":
                print("Sunt bune clătitele, mă simt mai puternic... +1 PUTERE")
                putere += 1
                time.sleep(1)
                print("Puncte de putere: " + str(putere))
                time.sleep(1)

    #Voi aplica aceași metodă și pentru monștri
    monstru = random.randint(1, 10)
    if monstru == 10:
        print("Of ce ghinion! Un monstru te-a atacat!")
        time.sleep(1)
        print("Monstrul are " + str(monstri[-1]) + " puncte de putere")
        time.sleep(1)
        print("Tu ai " + str(putere) + " puncte de putere")
        time.sleep(1)

        if (len(monstri) != 0):
            if (monstri[-1] <= putere):
                print("Ai câștigat lupta! Super!!")
                sunet_lovitura.play()
                time.sleep(1)
                monstri.pop()
                scor += 10
            else:
                print("Ai pierdut lupta... :(")
                time.sleep(1)
                punte_de_viata -= monstri[-1] * 10
                print("Puncte de viață: " + str(punte_de_viata))
                time.sleep(1)
        else:
            print("Fiindcă ai învis deja toți monștri ai scăpat.. de data asta..")
            time.sleep(1)
    visited[player_y][player_x] += 1

#Aici introducem direcțiile
running = True
while running:
    afiseaza_taram()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mutare_jucator('N')
            elif event.key == pygame.K_DOWN:
                mutare_jucator('S')
            elif event.key == pygame.K_LEFT:
                mutare_jucator('V')
            elif event.key == pygame.K_RIGHT:
                mutare_jucator('E')
pygame.quit()
