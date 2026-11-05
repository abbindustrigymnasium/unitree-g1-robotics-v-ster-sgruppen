# Projektplan – Unitree G1

**1. Projektets bakgrund**

Projektet genomförs av fem elever i årskurs 3 på Hitachigymnasiets spetsutbildning, på uppdrag av Västerås stad. Projektet ska presenteras den 3 december 2026 på Västerås Kongress inom ramen för evenemanget *Ett gott liv hela livet*.

**2. Projektidé och syfte**

Vår idé är att använda roboten Unitree G1 som en spelpartner. Roboten ska kunna spela enkla spel tillsammans med en människa. Projektet omfattar två spel: sten, sax, påse och tre i rad.

Under projektets gång har vi ändrat prioriteringen mellan spelen. Vi började med tre i rad som huvudfunktion, men insåg efter en tids utveckling att det skulle bli svårt att hinna färdigställa alla delar. Därför började vi även utveckla sten, sax, påse. Eftersom arbetet kunde delas upp mellan fler gruppmedlemmar bestämde vi oss sedan för att fortsätta utveckla båda spelen parallellt.

Projektets nuvarande huvudfokus är att få sten, sax, påse att fungera på den fysiska roboten. Tre i rad utvecklas samtidigt, men är inte längre ett krav för att projektet ska anses genomfört.

Projektet genomförs med fokus på trygghet, gemenskap, meningsfullhet och hälsa. Syftet är att undersöka hur en interaktiv robot kan användas för att skapa en enkel social aktivitet där en människa kan spela även när det inte finns någon annan spelpartner tillgänglig.

Projektet har även ett tekniskt syfte. Under arbetet ska gruppen få praktisk erfarenhet av:

- Robotik
- Pythonprogrammering
- ROS 2
- Kamerahantering och bildigenkänning
- Robotstyrning
- Simulering
- Integration mellan mjukvara och fysisk hårdvara

**3. Målgrupp**

Projektets huvudsakliga målgrupp är äldre personer, framför allt personer som kan ha nytta av enkla och lättillgängliga aktiviteter i vardagen.

Målgruppen behöver inte ha tidigare erfarenhet av robotar, datorer eller programmering. Spelen ska därför vara enkla att förstå och använda.

Projektet riktar sig inte till en specifik åldersgräns, utan till äldre personer som är intresserade av att prova en interaktiv aktivitet med en robot.

**4. Projektets funktion**

Projektet består av två spel: sten, sax, påse och tre i rad.

Sten, sax, påse är projektets nuvarande huvudfunktion. Tanken är att en människa ska kunna spela mot Unitree G1 genom att visa sin handgest framför robotens kamera. Roboten ska kunna identifiera gesten, genomföra sitt eget drag och avgöra vem som vinner omgången.

Kameran används för att känna igen spelarens handgest. Resultatet skickas vidare till spelets programkod, där spelreglerna avgör vinnaren. Roboten ska sedan kunna visa sin egen gest med hjälp av handen.

Tre i rad utvecklas parallellt. Där ska en människa kunna göra sitt drag på en spelplan och roboten ska kunna identifiera förändringen, bestämma sitt eget drag och genomföra det med hjälp av sin arm.

Spelet ska fortsätta tills någon av spelarna har vunnit eller tills det blir oavgjort.

Båda spelen är tänkta att kunna visas under presentationen. Beroende på hur långt utvecklingen har kommit kommer spelen att prioriteras olika. Om tre i rad inte hinner färdigställas kommer presentationen att fokusera på sten, sax, påse.

**5. Teknisk utveckling**

Utvecklingen sker främst i Python. Arbetet omfattar bland annat programmering av spelen, kamerahantering, bildigenkänning och styrning av robotens rörelser.

En stor del av den första projektperioden har gått åt till att installera och konfigurera utvecklingsmiljön samt undersöka hur robotens hårdvara fungerar. Särskilt arbetet med att hitta och etablera kommunikation med rätt anslutning till robotens hand har tagit tid.

Arbetet är uppdelat mellan gruppmedlemmarna för att spelen och robotens olika funktioner ska kunna utvecklas parallellt.

Minna arbetar med kamerahantering och bildigenkänning. Fokus ligger för närvarande på att identifiera handgester för sten, sax, påse och att koppla ihop kamerafunktionen med spelets övriga programkod.

Davit och Celine samarbetar kring robotens rörelser och hur dessa ska styras.

Isak arbetar med spelreglerna, spelplanen och hur robotens arm ska kunna genomföra drag i tre i rad.

Felicia undersöker befintliga projekt och kodexempel på GitHub som kan användas eller anpassas till projektet. Hon undersöker även möjligheter inom kamerahantering och bildigenkänning.

Utvecklingen sker stegvis. Först testas funktionerna separat och därefter kombineras de till ett fungerande system. Eftersom det är begränsat med tid kvar prioriteras de funktioner som krävs för att sten, sax, påse ska fungera på den fysiska roboten.

**6. Medlemmar**

| Roll        | Namn                      |
| ----------- | ------------------------- |
| Gruppmedlem | Davit Durgaryan           |
| Gruppmedlem | Celine Söderlund Eriksson |
| Gruppmedlem | Felicia Avelin            |
| Gruppmedlem | Isak Forssén              |
| Gruppmedlem | Minna Näslund             |
| Lärare      | Ahmad Alali               |

**7. Tidsplan**

Projektet har ungefär en månad kvar till redovisningen den 3 december 2026. Den återstående tiden kommer främst att användas till att färdigställa funktionerna, testa spelen och förbereda presentationen.

| Fas                            | Uppgift                                                 | Tid/status                         |
| ------------------------------ | ------------------------------------------------------- | ---------------------------------- |
| Förstudie och uppstart         | Projektplan och planering                               | Genomförd                          |
| Installation och konfigurering | Installera utvecklingsmiljö och konfigurera roboten     | Genomförd, tog mer tid än planerat |
| Robotstyrning                  | Få igång och testa robotens rörelser och hand           | Pågående                           |
| Sten, sax, påse                | Utveckla spelregler och spelprogrammering               | Pågående                           |
| Sten, sax, påse                | Kamerahantering och igenkänning av handgester           | Pågående                           |
| Sten, sax, påse                | Koppla ihop spelets olika funktioner med roboten        | Återstående                        |
| Tre i rad                      | Utveckla spelregler, spelplan och robotens rörelser     | Pågående                           |
| Tre i rad                      | Kamerahantering och identifiering av spelplanen         | Återstående                        |
| Integration och testning       | Testa spelen med den fysiska roboten                    | Återstående                        |
| Presentation                   | Förbereda och presentera projektet på Västerås Kongress | 3 december 2026                    |

Sten, sax, påse är den högsta prioriteringen under den återstående projekttiden. Tre i rad fortsätter att utvecklas parallellt, men om tiden inte räcker kommer arbetet att fokuseras på att få huvudfunktionen att fungera så stabilt som möjligt.

**8. Riskanalys**

| Risk                                                     | Konsekvens | Åtgärd                                                                                            |
| -------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------- |
| Robotens hårdvara är svår att styra                      | Hög        | Testa robotens grundläggande funktioner separat och prioritera de rörelser som behövs för spelen. |
| Kommunikation med robotens hand fungerar inte            | Hög        | Undersöka alternativa anslutningar och använda befintliga kodexempel och dokumentation.           |
| Kamerabaserad igenkänning fungerar inte tillräckligt bra | Hög        | Testa igenkänningen i olika vinklar och ljusförhållanden. Förenkla igenkänningen om det behövs.   |
| Spelets olika programdelar fungerar inte tillsammans     | Hög        | Testa funktionerna separat och koppla ihop dem stegvis.                                           |
| Tre i rad hinner inte färdigställas                      | Medel      | Prioritera sten, sax, påse och använda det som huvudspel under presentationen.                    |
| Robotens rörelser är långsamma eller opålitliga          | Medel      | Förenkla rörelserna och testa dem upprepade gånger innan presentationen.                          |
| Systemet kraschar under demonstrationen                  | Hög        | Ha en fungerande backup på dator eller iPad och en enkel plan för att starta om systemet.         |
| Användaren förstår inte hur spelen fungerar              | Medel      | Hålla instruktionerna enkla och testa spelen med personer utanför projektgruppen.                 |
| Tiden inte räcker till alla planerade funktioner         | Hög        | Prioritera sten, sax, påse och ta bort extrafunktioner som inte är nödvändiga.                    |

**9. Fallback-lösning**

Eftersom projektet innehåller både mjukvara och fysisk robotik finns det en risk att alla funktioner inte hinner bli färdiga till presentationsdagen. Därför finns en alternativ plan för att kunna genomföra demonstrationen även om vissa delar inte fungerar.

Den huvudsakliga fallback-lösningen är att fokusera helt på sten, sax, påse om tre i rad inte hinner färdigställas.

Om robotens fysiska hand inte fungerar som planerat kan en enklare lösning användas där spelet genomförs med hjälp av en skärm eller annan visuell presentation.

Vi undersöker även möjligheten att lägga till en röstfunktion till sten, sax, påse. Roboten skulle exempelvis kunna säga vilken gest den väljer eller kommentera resultatet av en omgång. Detta skulle kunna bidra till en mer interaktiv upplevelse och samtidigt knyta an till kommunens krav på trygghet, gemenskap, meningsfullhet och hälsa.

Prioriteringen är:

1. Fungerande sten, sax, påse på den fysiska roboten.
2. Fungerande sten, sax, påse med enklare visuell eller digital backup.
3. Tre i rad på den fysiska roboten om tiden och de tekniska förutsättningarna tillåter det.
4. Eventuella extrafunktioner, exempelvis röstfunktion.

**10. Presentation på Västerås Kongress**

Projektet ska presenteras den 3 december 2026 på Västerås Kongress inom ramen för evenemanget *Ett gott liv hela livet*.

Huvudfokus för presentationen är Unitree G1 och dess funktion som spelpartner. Besökarna ska få möjlighet att se hur roboten spelar sten, sax, påse och, om utvecklingen tillåter det, tre i rad.

Under presentationen på scen kommer gruppen att ge en kort demonstration av något av spelen. Vilket spel som visas beror på vilket som fungerar bäst och är mest färdigutvecklat vid presentationstillfället.

I montern kommer båda spelen att visas om de tekniska förutsättningarna tillåter det. För att kunna demonstrera båda spelen planeras en lösning där besökarna kan välja mellan spelen eller där spelen visas vid olika tillfällen.

En demonstration kan gå till på följande sätt:

- Besökarna får en kort förklaring av projektet.
- Robotens funktion och spelen visas.
- Besökaren får möjlighet att spela mot roboten.
- Vid sten, sax, påse visar besökaren sin handgest framför kameran. Roboten identifierar gesten, genomför sitt eget drag och presenterar resultatet.
- Vid tre i rad gör besökaren sitt drag på spelplanen. Roboten identifierar draget, bestämmer sitt eget drag och genomför det.
- Efter demonstrationen kan projektgruppen förklara hur roboten, programmeringen och kamerahanteringen fungerar.

Om tre i rad inte fungerar tillräckligt bra på presentationsdagen kommer demonstrationen i stället att fokusera på sten, sax, påse.

**11. Sammanfattning**

Unitree G1 är ett projekt där fem elever från Hitachigymnasiets spetsutbildning utvecklar en robot som kan fungera som spelpartner. Projektet genomförs på uppdrag av Västerås stad och ska presenteras den 3 december 2026 på Västerås Kongress.

Projektet omfattar två spel: sten, sax, påse och tre i rad. Under projektets gång har prioriteringen förändrats och sten, sax, påse har blivit huvudfokus. Detta beror framför allt på projektets tidsram och de tekniska utmaningar som uppstått under utvecklingen.

Arbetet omfattar bland annat Pythonprogrammering, kamerahantering, bildigenkänning och styrning av robotens rörelser. Gruppmedlemmarna arbetar med olika delar av systemet som sedan ska kombineras till en fungerande helhet.

Målet är att få sten, sax, påse att fungera på den fysiska roboten. Tre i rad utvecklas parallellt och kommer att visas om tiden och de tekniska förutsättningarna tillåter det.

Om tre i rad inte hinner färdigställas kommer sten, sax, påse att utgöra projektets huvudsakliga demonstration. Målet är att skapa en interaktiv spelpartner som kan bidra till gemenskap, meningsfullhet och en rolig aktivitet för äldre personer.
