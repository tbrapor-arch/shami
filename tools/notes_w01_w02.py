"""Lesson notes for weeks 1–2, in the Tsheh-tû format: one note per point, tied to a line,
with the expression in Arabic and transcription, a topic, and every cited word written {Arabic|transcription}.
Run once: python3 tools/notes_w01_w02.py  (rewrites the notes: blocks of W01.yaml and W02.yaml)."""
import json, re

G, V, C, S = "grammar", "vocab", "culture", "sound"
N = {
"L001": [
 (1, "اِنْتَ آدَم؟", "ʔinte ʔādam?", G, "No verb 'to be' in the present: two words side by side make a sentence. {أنا آدَم|ʔana ʔādam} 'I am Adam', {اِنْتَ سامي؟|ʔinte Sāmi?} 'are you Sāmi?'. A question keeps the same words; only the voice rises at the end. MSA works the same way: {أَنا آدَمُ|ʔanā ʔādamu}."),
 (1, "اِنْتَ", "ʔinte", G, "{اِنْتَ|ʔinte} 'you' to a man. To a woman: {اِنْتي|ʔinti} (lesson 5). Damascus says ʔinte where MSA says {أَنْتَ|ʔanta}."),
 (2, "اي", "ʔē", V, "{اي|ʔē} 'yes', the everyday word; you will also hear {إيه|ʔēh}. MSA {نَعَم|na3am} sounds formal. 'No' is {لأ|laʔ} (lesson 5)."),
 (3, "اِبْن عَمَّك", "ʔibn 3ammak", C, "Literally 'son of your father's brother'. Arabic names each cousin by the exact link: {عَمّ|3amm} is a father's brother, {خال|xāl} a mother's brother, so {اِبْن خالَك|ʔibn xālak} is a cousin on your mother's side. The ending -ak is 'your' (to a man)."),
 (3, "الحَمْدِلله عَالسَّلامة", "il-ḥamdilla 3as-salāme", C, "'Praise God for your safe arrival': the fixed greeting for anyone back from a journey or recovering from an illness. {الحَمْدِلله|il-ḥamdilla} 'thank God' on its own is also the usual answer to 'how are you?' (lesson 2)."),
 (4, "الله يْسَلّمَك", "ʔalla ysallmak", C, "The fixed reply: 'God keep you safe'. To a woman: {الله يْسَلّمِك|ʔalla ysallmik}. Many Syrian formulas come in pairs like this; learn the greeting and its reply together."),
 (5, "أَهْلا وْسَهْلا فيك", "ʔahla w-sahla fīk", V, "'Welcome'. {فيك|fīk} 'in you' makes it personal: 'welcome to you'. The reply is {أَهْلا فيك|ʔahla fīk}."),
 (5, "بِالشّام", "biš-Šām", C, "{الشّام|iš-Šām} is what Syrians call Damascus, and more widely the whole Levant. The map name is {دِمَشْق|Dimašq} (Bridge 1). {بْ|b-} 'in' joins the article: {بِالشّام|biš-Šām} 'in Damascus'."),
],
"L002": [
 (1, "أَهْلين عَمّو", "ʔahlēn 3ammo", C, "{أَهْلين|ʔahlēn} 'hi', a friendly form of {أَهْلا|ʔahla}. The uncle calls Adam {عَمّو|3ammo} 'uncle', and Adam calls him {عَمّو|3ammo} back (line 2). Older relatives address children by their own title: it is affectionate, not a mistake."),
 (1, "كيفَك", "kīfak", G, "{كيف|kīf} 'how' takes the ending of the person asked: {كيفَك|kīfak} to a man, {كيفِك|kīfik} to a woman (line 4), {كيفْكُن|kīfkun} to several people (line 6). The same endings mean 'your' on nouns: {عَمَّك|3ammak}, {عَمِّك|3ammik}."),
 (2, "مْنيح، الحَمْدِلله", "mnīḥ, il-ḥamdilla", G, "{مْنيح|mnīḥ} 'fine, good'. A woman answers {مْنيحة|mnīḥa} (line 5): the adjective agrees with the speaker. The ة is said -a here because of the ḥ before it (lesson 7)."),
 (3, "تَمام", "tamām", V, "{تَمام|tamām} 'perfect, all good': a very common answer to 'how are you?', and also 'OK, fine'."),
 (3, "هَيّ مَرْت عَمَّك", "hayy mart 3ammak", G, "{هَيّ|hayy} 'this (f)' introduces a woman: {هَيّ لينا|hayy Līna} 'this is Līna'. {مَرْت عَمَّك|mart 3ammak} 'your uncle's wife': {مَرَة|mara} 'woman, wife' shows a t before another noun (see lesson 3)."),
 (6, "يا اِبْني", "yā ʔibni", C, "{يا|yā} is used to call someone: {يا آدَم|yā ʔādam}. {اِبْني|ʔibni} 'my son' is how an older woman speaks to any young man she is fond of. {شَباب|šabāb} 'young people' is the usual 'guys'."),
 (6, "تْفَضَّلو", "tfaḍḍalu", V, "'Please, go ahead': come in, sit down, help yourselves. To one man {تْفَضَّل|tfaḍḍal}, to one woman {تْفَضَّلي|tfaḍḍali}, to several {تْفَضَّلو|tfaḍḍalu}. You will hear it many times a day."),
],
"L003": [
 (1, "يا تيتا", "yā tēta", C, "Tēta calls Adam {تيتا|tēta}, as his uncle called him {عَمّو|3ammo} in lesson 2: the grown-up gives the child her own title. Tēta is this family's word for grandmother; many Damascenes say {سِتّي|sitti} 'my grandmother'."),
 (1, "بَيْتي… بَيْتَك", "bēti… bētak", G, "'My' is -i, 'your' is -ak to a man and -ik to a woman: {بَيْت|bēt} 'house', {بَيْتي|bēti} 'my house', {بَيْتَك|bētak}, {بَيْتِك|bētik} 'your house'. {هادا|hāda} 'this' goes with masculine words; MSA {هٰذا|hādhā} (Bridge 1)."),
 (1, "هَلَّق", "hallaʔ", S, "Sound of the week: ق. Damascus does not say q; it says ʔ, a catch in the throat like the break in 'uh-oh'. The spelling keeps ق: {هَلَّق|hallaʔ} 'now'. MSA {قَهْوة|qahwa} 'coffee' is Shami {قَهْوة|ʔahwe} (lesson 8)."),
 (2, "شو حِلو!", "šū ḥilu!", G, "{شو|šū} 'what' also makes exclamations: {شو حِلو!|šū ḥilu!} 'how beautiful!'. {حِلو|ḥilu} 'nice, beautiful, sweet', feminine {حِلْوة|ḥilwe}."),
 (3, "هَوْن… هْنيك", "hōn… hnīk", V, "{هَوْن|hōn} 'here', {هْنيك|hnīk} 'there'. No verb is needed: {هَوْن المَطْبَخ|hōn il-maṭbax} 'here is the kitchen'."),
 (4, "وهَيّ؟", "w-hayy?", G, "{هَيّ|hayy} is 'this' for a feminine word. Adam says {وهَيّ؟|w-hayy?} because he points at a {أوضة|ʔūḍa} 'room', which is feminine. For a masculine word: {هادا|hāda}."),
 (5, "أوضِة أَبوك", "ʔūḍit ʔabūk", G, "'Your father's room': the thing first, the owner second, side by side. A word ending in ة then shows a hidden t: {أوضة|ʔūḍa} becomes {أوضِة|ʔūḍit}. The t also appears before an ending: {أوضْتَك|ʔūḍtak} 'your room'. {أَبوك|ʔabūk} 'your father': after a vowel, 'your' is just -k."),
],
"L004": [
 (1, "شو هاد؟", "šū hād?", G, "{شو|šū} 'what' starts the question; nothing else changes. {هاد|hād} is the everyday short form of {هادا|hāda}; both are right."),
 (2, "ياسْمين", "yāsmīn", C, "Jasmine climbs the walls of the old courtyard houses; Damascus is often called 'the city of jasmine'."),
 (2, "البَحْرة", "il-baḥra", C, "{البَحْرة|il-baḥra}: the fountain basin in the middle of a Damascene courtyard (from {بَحْر|baḥr} 'sea'). The house itself is a {بَيْت عَرَبي|bēt 3arabi} 'Arab house'."),
 (3, "مين", "mīn", V, "The question words so far: {شو|šū} 'what', {مين|mīn} 'who', {وَيْن|wēn} 'where' (line 5), {كيف|kīf} 'how' (lesson 2). They come first."),
 (3, "بِالصّورة", "biṣ-ṣūra", G, "'The' is {ال|il-}, joined to the word. Before t, d, s, z, š, ṣ, ḍ, ṭ, ẓ, n, r, l (and often j) the l copies the next sound: il + ṣūra → {الصّورة|iṣ-ṣūra}, il + Šām → {الشّام|iš-Šām}. Elsewhere it stays: {البَحْرة|il-baḥra}. These are the 'sun letters'."),
 (4, "جِدّي وجِدَّك", "jiddi w-jiddak", V, "{جِدّ|jidd} 'grandfather', with 'my' and 'your'. Līna says 'my grandfather and yours': they share him, since their fathers are brothers."),
 (4, "الله يِرْحَمو", "ʔalla yirḥamo", C, "'God have mercy on him': said each time you mention someone who has died. For a woman: {الله يِرْحَمْها|ʔalla yirḥamha}."),
 (6, "بِالمَطْبَخ", "bil-maṭbax", G, "{بْ|b-} 'in' joins the article: b + il-maṭbax → {بِالمَطْبَخ|bil-maṭbax}. Still no verb: {تيتا بِالمَطْبَخ|tēta bil-maṭbax} 'Tēta is in the kitchen'."),
],
"L005": [
 (1, "جوعان", "jū3ān", G, "Words for a passing state often end in -ān: {جوعان|jū3ān} 'hungry', {تَعْبان|ta3bān} 'tired', {نَعْسان|na3sān} 'sleepy'. Feminine -e, plural -īn: {تَعْبانة|ta3bāne}, {تَعْبانين|ta3bānīn}."),
 (2, "لأ", "laʔ", V, "{لأ|laʔ} 'no', with a clear catch in the throat at the end. 'Yes' is {اي|ʔē}."),
 (2, "مو جوعان", "mū jū3ān", G, "{مو|mū} is 'not' before anything that is not a verb: {مو جوعان|mū jū3ān} 'not hungry', {مو هَوْن|mū hōn} 'not here', {مو أنا|mū ʔana} 'not me'. Verbs take {ما|mā} (lesson 6)."),
 (2, "شْوَيّ", "šwayy", G, "{شْوَيّ|šwayy} 'a little' and {كْتير|ktīr} 'very, a lot' (line 4) usually follow the adjective: {تَعْبان شْوَيّ|ta3bān šwayy}, {نَعْسان كْتير|na3sān ktīr}. ktīr can also come first: {كْتير حِلو|ktīr ḥilu}."),
 (3, "وِلّا", "willa", V, "{وِلّا|willa} 'or' in a question that offers a choice: {تَعْبان وِلّا نَعْسان؟|ta3bān willa na3sān?}."),
 (4, "واِنْتي", "w-ʔinti", G, "{اِنْتي|ʔinti} 'you' to a woman, and her adjective is feminine too: {اِنْتي تَعْبانة؟|ʔinti ta3bāne?}."),
 (5, "أَبَداً", "ʔabadan", V, "{أَبَداً|ʔabadan} 'not at all, never', after a negative: {مو تَعْبانة أَبَداً|mū ta3bāne ʔabadan}. One of the few Shami words that keep the MSA ending -an."),
],
"L006": [
 (1, "عَنْدَك", "3andak", G, "There is no verb 'to have': you say 'at me'. {عَنْد|3and} + ending: {عَنْدي|3andi} 'I have', {عَنْدَك|3andak} 'you have' (to a man), {عَنْدِك|3andik} (to a woman)."),
 (1, "إخْوِة", "ʔixwe", V, "{إخْوِة|ʔixwe} 'brothers', and for a mixed family 'brothers and sisters'. One brother: {أَخّ|ʔaxx}; one sister: {إخْت|ʔixt}."),
 (2, "ما عَنْدي", "mā 3andi", G, "'I don't have': {ما عَنْدي|mā 3andi}. {ما|mā} negates verbs and the verb-like words {عَنْد|3and} and {في|fī}; {مو|mū} (lesson 5) negates the rest."),
 (3, "في", "fī", G, "{في|fī} 'there is, there are' and {ما في|mā fī} 'there isn't, there aren't' never change: {في مَطَر|fī maṭar}, {ما في ياسْمين|mā fī yāsmīn}."),
 (4, "بَسّ", "bass", V, "{بَسّ|bass} 'but'; also 'only' and 'enough!'. One of the commonest words in Shami."),
 (5, "يا حَرام", "yā ḥarām", C, "Sympathy: 'poor thing', 'what a pity'."),
 (5, "إلَك", "ʔilak", G, "{إل|ʔil-} + ending: 'belongs to, is for'. {إلي|ʔili} 'mine, for me', {إلَك|ʔilak} 'yours'. It is warmer than {عَنْدَك|3andak}: Tēta is saying the house is his."),
],
"L008": [
 (1, "شو بِدّْكُن؟", "šū biddkun?", G, "{بِدّ|bidd-} + an ending means 'want'. It works like {عَنْد|3and} (lesson 6): {بِدّي|biddi} 'I want', {بِدَّك|biddak} (to a man), {بِدِّك|biddik} (to a woman), {بِدّْكُن|biddkun} (to several). It is not a verb, so it never takes b-, and it is negated with mā: {ما بِدّي|mā biddi}."),
 (2, "قَهْوة", "ʔahwe", C, "MSA {قَهْوة|qahwa}, with ق said ʔ. Syrian coffee is boiled Turkish-style in a small pot, often with cardamom, and served in tiny cups."),
 (3, "كَمان", "kamān", V, "{كَمان|kamān} 'also, too', and 'more, again': {كَمان قَهْوة|kamān ʔahwe} 'another coffee'."),
 (3, "سادة", "sāde", C, "{سادة|sāde} 'plain' means no sugar. Ask for {وَسَط|wasaṭ} for a little sugar, {حِلْوة|ḥilwe} for sweet."),
 (4, "تْنين قَهْوة", "tnēn ʔahwe", G, "To order, the number comes first with a singular word: {تْنين قَهْوة|tnēn ʔahwe} 'two coffees', {تْلاتة مَيّ|tlāte mayy} 'three waters'. {واحِد|wāḥid} and {تْنين|tnēn} keep this form even before a feminine word like ʔahwe. Numbers 1–10 are below the dialogue."),
 (4, "إذا بِتْريد", "ʔiza bitrīd", V, "Literally 'if you want': the everyday 'please'. To a woman: {إذا بِتْريدي|ʔiza bitrīdi}. {مِن فَضْلَك|min faḍlak} works too."),
 (5, "أَمْرَك", "ʔamrak", C, "'Your order': what a waiter or shopkeeper says as he takes your request. {شي تاني؟|šī tāni?} 'anything else?': {شي|šī} 'something', {تاني|tāni} 'other'."),
 (6, "واحِد كْنافة", "wāḥid knāfe", C, "{كْنافة|knāfe}: warm cheese pastry soaked in syrup, the classic Damascus dessert. Again number + singular: {واحِد كْنافة|wāḥid knāfe}."),
],
"L009": [
 (1, "وَيْن رايِح؟", "wēn rāyiḥ?", G, "'Going', right now. {رايِح|rāyiḥ} is a verb-adjective (a participle), so it changes like {تَعْبان|ta3bān}: {رايِح|rāyiḥ} (m), {رايْحة|rāyḥa} (f), {رايْحين|rāyḥīn} (pl, line 4). {وَيْن رايِح؟|wēn rāyiḥ?} is the everyday 'where are you off to?'."),
 (2, "عَالسّوق", "3as-sūʔ", G, "{عَ|3a-} 'to, onto' fuses with the article: 3a + is-sūʔ → {عَالسّوق|3as-sūʔ}; 3a + il-bēt → {عَالبَيْت|3al-bēt} 'home'. {سوق|sūʔ} is MSA sūq, ق said ʔ."),
 (2, "بِدّي شوف", "biddi šūf", G, "After {بِدّي|biddi} the verb comes with no b-. For 'I' it is the bare stem: {بِدّي شوف|biddi šūf} 'I want to see', {بِدّي روح|biddi rūḥ} 'I want to go'."),
 (2, "سوق الحَميدِيّة", "sūʔ il-Ḥamīdiyye", C, "The great covered market of old Damascus, under a high iron roof, running from the citadel to the Umayyad Mosque."),
 (3, "لَحالَك", "la-ḥālak", V, "'On your own'. With other endings: {لَحالي|la-ḥāli} 'on my own', {لَحالِك|la-ḥālik} (to a woman), {لَحالْها|la-ḥālha} 'on her own'."),
 (4, "مَعي", "ma3i", V, "{مَع|ma3} 'with' takes endings: {مَعي|ma3i} 'with me', {مَعَك|ma3ak} 'with you'."),
 (5, "بَعْدين", "ba3dēn", V, "{بَعْدين|ba3dēn} 'then, after that, later'."),
 (6, "بِدّْنا نْروح", "biddna nrūḥ", G, "'We want to go'. For 'we' the verb starts with n-: {نْروح|nrūḥ}. {بِدّْنا|biddna} is bidd + -na 'our'."),
 (6, "لَعَنْد تيتا", "la-3and tēta", G, "{عَنْد تيتا|3and tēta} is 'at Tēta's (place)'. With {لَ|la-} 'to' in front, it becomes 'to Tēta's'."),
],
"L010": [
 (1, "شو بْتْحِبّ تاكُل", "šū btḥibb tākul", G, "Two verbs in a row: the first takes b-, the second does not. {بْتْحِبّ تاكُل|btḥibb tākul} 'you like to eat'. On its own, 'you eat' is {بْتاكُل|btākul}."),
 (2, "بْحِبّ", "bḥibb", G, "b- marks the ordinary present. For 'I' it is b- + the stem: {بْحِبّ|bḥibb} 'I like, I love'. {حَبّ|ḥabb} covers both 'like' and 'love'. The full table is below the dialogue."),
 (2, "كِلّ شي", "kill šī", V, "{كِلّ|kill} 'every, all' + {شي|šī} 'thing' = 'everything'. {كِلّ يوم|kill yōm} 'every day'."),
 (2, "الكِبّة", "il-kibbe", C, "{كِبّة|kibbe}: balls of bulgur and minced meat stuffed with more meat and pine nuts, a Damascus speciality."),
 (3, "بيحِبّ المَحْشي", "biḥibb il-maḥši", G, "'He likes': b- and the y- of 'he' merge into bi-: {بيحِبّ|biḥibb}. 'You like' and 'she likes' sound the same: {بْتْحِبّ|btḥibb} (line 5). {المَحْشي|il-maḥši}: courgettes, aubergines or vine leaves stuffed with rice and often meat."),
 (4, "ما بْحِبّ", "mā bḥibb", G, "Verbs are negated with {ما|mā}, like {عَنْد|3and} and {في|fī}: {ما بْحِبّ|mā bḥibb} 'I don't like'."),
 (4, "اللَّحْمة", "il-laḥme", V, "{لَحْمة|laḥme} 'meat', {خُضْرة|xuḍra} 'vegetables', {حُمُّص|ḥummuṣ} 'hummus, chickpeas'. Food you speak of in general takes the article: {بْحِبّ الحُمُّص|bḥibb il-ḥummuṣ} 'I like hummus'."),
 (5, "الحِلو", "il-ḥilu", V, "{حِلو|ḥilu} 'nice, sweet'; {الحِلو|il-ḥilu} 'the sweet (thing)' is dessert."),
 (6, "صَحْتين", "ṣaḥtēn", C, "'Two healths': said to people who are eating. The answer is {عَلى قَلْبَك|3ala ʔalbak} 'on your heart' (to a woman {عَلى قَلْبِك|3ala ʔalbik}). {عَالطّاوْلة|3aṭ-ṭāwle} 'on the table'."),
],
"L011": [
 (1, "بْتِشْتِغِل", "btištiɣil", G, "'You work'. {اِشْتَغَل|ištaɣal} 'to work': {بِشْتِغِل|bištiɣil} 'I work' (line 2), {بْتِشْتِغِل|btištiɣil} 'you work' or 'she works', {بْيِشْتِغِل|byištiɣil} 'he works'."),
 (2, "أنا مُهَنْدِس", "ʔana muhandis", G, "No word for 'a': {أنا مُهَنْدِس|ʔana muhandis} 'I'm an engineer', {هِيّ دْكتورة|hiyye doktōra} 'she's a doctor'."),
 (2, "بالمَزّة", "bil-Mazze", C, "{المَزّة|il-Mazze}, in west Damascus: a modern district of flats and offices, where Sāmi's family lives."),
 (3, "بْتِشْتِغْلي", "btištiɣli", G, "To a woman the verb adds -i, and the vowel before it drops: {بْتِشْتِغِل|btištiɣil} → {بْتِشْتِغْلي|btištiɣli}."),
 (4, "بِدْرُس طِبّ", "bidrus ṭibb", V, "{دَرَس|daras} 'to study': {بِدْرُس|bidrus} 'I study'. {طِبّ|ṭibb} is medicine as a subject; a doctor is usually {دْكتور|doktōr}. {الجامْعة|il-jām3a} 'the university'."),
 (5, "بْمَكْتَبة", "b-maktabe", V, "{مَكْتَبة|maktabe} 'library' or 'bookshop', from the root k-t-b 'write', like {كْتاب|ktāb} 'book' and {كَتَب|katab} 'he wrote' (lesson 12)."),
 (5, "فَرَنْسي وسوري", "faransi w-sūri", G, "Nationalities end in -i, and -iyye for a woman: {سوري|sūri} / {سوريّة|sūriyye}, {فَرَنْسي|faransi} / {فَرَنْسيّة|faransiyye}. More in the table below."),
 (6, "يَعْني", "ya3ni", V, "Literally 'it means': the everyday 'so, I mean, that is'. You will hear it in almost every sentence. {نُصّ|nuṣṣ} 'half'."),
 (6, "شامي", "šāmi", C, "{شامي|šāmi} 'from iš-Šām': Damascene, and more loosely Syrian or Levantine. It is also the name of this course."),
],
"L012": [
 (1, "صَباح الخير", "ṣabāḥ il-xēr", C, "'Morning of goodness'. The answer swaps in another nice word: {صَباح النّور|ṣabāḥ in-nūr} 'morning of light' (line 2)."),
 (1, "شو عْمِلْت", "šū 3milt", G, "The past. -t is the ending for 'I' and for 'you' (to a man): {عْمِلْت|3milt} 'I did' or 'you did'; context decides. {عِمِل|3imil} 'he did'. The full table is below the dialogue."),
 (1, "مْبارِح", "mbāriḥ", V, "{مْبارِح|mbāriḥ} 'yesterday'. {اليوم|il-yōm} 'today', {بُكْرا|bukra} 'tomorrow'."),
 (2, "رِحْت", "riḥt", G, "{راح|rāḥ} 'he went' shortens its ā before an ending that starts with a consonant: {رِحْت|riḥt} 'I went'. {شاف|šāf} 'he saw' does the same: {شِفْت|šift} (line 3)."),
 (4, "الجامِع الأُمَوي", "il-Jāmi3 il-ʔUmawi", C, "The Umayyad Mosque, at the end of the Ḥamīdiyye souk, built in the early 8th century on the site of a church and, before that, a Roman temple."),
 (4, "بوظة عَنْد بَكْداش", "būẓa 3and Bakdāš", C, "{بوظة|būẓa}: Damascus ice cream, pounded and stretched, flavoured with mastic and rolled in pistachios. {بَكْداش|Bakdāš}, in the Ḥamīdiyye souk, is the most famous place for it. {أَكَلْت|ʔakalt} 'I ate'."),
 (5, "أَحْلى شي!", "ʔaḥla šī!", V, "'The nicest thing': a warm 'how lovely!'. {أَحْلى|ʔaḥla} 'nicer, nicest', from {حِلو|ḥilu}. {لَأَبوك|la-ʔabūk} 'to your father'."),
 (6, "كَتَبْتِلّو", "katabtillo", G, "-lo 'to him' sticks onto the verb, with an i to link: {كَتَبْت|katabt} + -lo → {كَتَبْتِلّو|katabtillo} 'I wrote to him'. {بِاللّيْل|bil-lēl} 'at night'."),
 (6, "ما رَدّ", "mā radd", G, "The past is negated with {ما|mā} too: {ما رَدّ|mā radd} 'he didn't answer'."),
],
"L013": [
 (1, "قَدّيش", "ʔaddēš", G, "{قَدّيش|ʔaddēš} 'how much?' for prices and amounts. For things you count, use {كَم|kam} + a singular noun: {كَم شال؟|kam šāl?} 'how many scarves?'."),
 (1, "هالشّال", "haš-šāl", G, "{هَـ|hal-} is a short 'this', glued on like the article: {هالبَيْت|hal-bēt} 'this house'. It merges with sun letters as {ال|il-} does: {هالشّال|haš-šāl}."),
 (1, "عَمّو", "3ammo", C, "The polite way to address an older man you don't know, such as a shopkeeper: 'uncle'. For an older woman: {خالة|xāle} 'aunt'."),
 (2, "لَإلِك؟", "la-ʔilik?", C, "'For you?': the seller's classic line, to make a price sound like a favour. {إلِك|ʔilik} is ʔil- + -ik (lesson 6)."),
 (2, "تْلاتين أَلْف", "tlātīn ʔalf", G, "From 11 up, the noun after a number stays singular: {تْلاتين أَلْف|tlātīn ʔalf} 'thirty thousand', {خَمْسين ليرة|xamsīn lēra} 'fifty pounds'. The numbers are below the dialogue."),
 (3, "غالي", "ɣāli", V, "{غالي|ɣāli} 'expensive', and also 'dear, precious'. 'Cheap' is {رْخيص|rxīṣ}."),
 (4, "مَعْقول؟", "ma3ʔūl?", V, "'Reasonable?', here 'are you serious?'. MSA {مَعْقول|ma3qūl}, ق said ʔ."),
 (4, "خَمْسة وعِشْرين", "xamsa w-3išrīn", G, "Units come first, as in German: 'five and twenty' = 25."),
 (6, "مْنِعْرِف نْفاصِل", "mni3rif nfāṣil", G, "{فاصَل|fāṣal} 'to bargain'. {مْنِعْرِف نْفاصِل|mni3rif nfāṣil} 'we know (how to) bargain': 'we' with b- is m(i)n-, and the second verb has no b-. In the souk, the first price opens a conversation."),
],
}

def block(notes):
    out = ["    notes:"]
    for line, ar, tr, topic, text in notes:
        out.append(f"      - {{line: {line}, ar: {json.dumps(ar, ensure_ascii=False)}, tr: {json.dumps(tr, ensure_ascii=False)}, topic: {topic}, text: {json.dumps(text, ensure_ascii=False)}}}")
    return "\n".join(out)

for f in ("lessons/W01.yaml", "lessons/W02.yaml"):
    s = open(f, encoding="utf-8").read()
    for lid, notes in N.items():
        m = re.search(rf"  - id: {lid}\n(.*?)(?=\n  - id: |\Z)", s, re.S)
        if not m: continue
        body = m.group(1)
        new = re.sub(r"    notes:\n(?:      - .*\n)+", block(notes) + "\n", body, count=1)
        assert new != body, lid
        s = s[:m.start(1)] + new + s[m.end(1):]
    open(f, "w", encoding="utf-8").write(s)
print("ok")
