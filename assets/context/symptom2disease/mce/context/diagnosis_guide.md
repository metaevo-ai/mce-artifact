# Medical Diagnosis Symptom Guide - Error-Corrected Edition (v5)

This guide provides symptom profiles for each diagnosis, with special emphasis on error patterns identified from training data analysis.

## CRITICAL NEW RULES

### CRITICAL RULE 0: ITCHY RASH ON ARMS/FACE/BODY WITHOUT FEVER = CHICKEN POX
**Error**: Predicting allergy for itchy bumps on arms and face

**Key Pattern**:
- **Chicken Pox**: Small red bumps/rash on ARMS, FACE, or BODY + ITCHY + NO fever mentioned = CHICKEN POX
  - "Small red bumps on arms and face" = CHICKEN POX
  - "Rash on arms and neck that itches like crazy" = CHICKEN POX
  - Early chicken pox presents with rash + itching BEFORE fever develops
- **Allergy**: Itchy symptoms specifically involving EYES or THROAT (itchy eyes, scratchy throat, swollen throat)

**DECISIVE**: Itchy rash on arms/face/body WITHOUT fever = CHICKEN POX (NOT allergy)
**DECISIVE**: Itchy eyes or itchy/swollen throat = ALLERGY

**Example**:
- "Small red bumps on my arms and face. They are itchy and make my day very uncomfortable" → **CHICKEN POX** (arms + face + itchy + no fever)
- "Rash on my arms and neck that itches like crazy. Feeling really uncomfortable all day" → **CHICKEN POX** (itchy rash, no fever)
- "Red and itchy eyes, scratchy throat, sneezing, no fever" → **ALLERGY** (itchy EYES/THROAT is key)
**Error**: Predicting common cold for runny nose + sneezing + sore throat (no fever)

**Key Pattern**:
- **Allergy**: Runny nose + sneezing + sore throat WITHOUT fever = ALLERGY
- **Common Cold**: Fever PRESENT or "feeling sick" from illness
- **DECISIVE**: If NO fever is mentioned with runny/sneezing/sore throat = ALLERGY

**Example**:
- "Trouble swallowing, sore throat, running nose, sneezing a lot" → **ALLERGY** (no fever mentioned)
- "Really bad sore throat, tired, feverish, muscle aches" → **COMMON COLD** (feverish present)

### CRITICAL RULE 2: BRONCHIAL ASTHMA - THICK SALIVA/MUCUS WITHOUT COLOR IS ASTHMA
**Error**: Predicting pneumonia for thick saliva/mucus with fever and cough

**Key Pattern**:
- **Asthma**: Thick saliva/mucus + fever + cough + "hard to breathe" = ASTHMA
  - Thick SALIVA (not explicitly "colored") = Asthma
  - "Saliva also became thick" = Asthma
- **Pneumonia**: Must have COLORED (green/yellow/brown/red) phlegm = DECISIVE for pneumonia
  - Thick mucus without color specification = Asthma

**DECISIVE**: Thick saliva/mucus without color specification + fever + cough = ASTHMA
**DECISIVE**: Colored phlegm (green/yellow/brown/red) = PNEUMONIA

**Example**:
- "High fever, saliva became thick, dry cough, weakness" → **ASTHMA** (thick saliva, not colored)
- "Cough, phlegm that's a weird color, feeling run down" → **PNEUMONIA** (colored phlegm)

### CRITICAL RULE 3: ARTHRITIS vs CERVICAL SPONDYLOSIS - NECK PAIN + WALKING/STEERING DIFFICULTY = ARTHRITIS
**Errors**: 2 cases - predicting cervical spondylosis for arthritis

**Key Pattern**:
- **Arthritis**: Joint pain + neck tightness + walking difficulty + steering difficulty = ARTHRITIS
  - "Hard to move around without getting stiff" = Arthritis
  - "Painful to walk" = Arthritis
  - Neck involvement with movement difficulty = Arthritis
- **Cervical Spondylosis**: Neck pain + DIZZINESS/BALANCE issues (no walking/steering difficulty)
  - Balance problems, dizziness, unsteady walking = Cervical Spondylosis

**DECISIVE**: Neck pain + movement/walking/steering difficulty = ARTHRITIS
**DECISIVE**: Neck pain + dizziness + balance issues = CERVICAL SPONDYLOSIS

**Example**:
- "Joint pain, neck tight, hard to move around, painful to walk" → **ARTHRITIS**
- "Joint pain, neck tight, hard to move around, painful to steer car" → **ARTHRITIS**
- "Neck pain, dizzy, off balance, unsteady" → **CERVICAL SPONDYLOSIS**

### CRITICAL RULE 4: DENGUE - RASH + VOMITING + EYE PAIN = DENGUE (NOT CHICKEN POX/TYPHOID)
**Errors**: 3 cases - predicting chicken pox/typhoid for dengue

**Key Pattern**:
- **Dengue**: Rash + vomiting + appetite loss + EYE PAIN = DENGUE
  - Eye pain (behind/around eyes) is hallmark of dengue
  - Vomiting with rash + systemic symptoms = Dengue
- **Chicken Pox**: Itchy rash + fever + NO severe systemic symptoms (no eye pain, less vomiting)
- **Typhoid**: GI symptoms (stomach cramps, diarrhea) + dizziness + weakness = Typhoid

**DECISIVE**: Rash + vomiting + eye pain = DENGUE
**DECISIVE**: Rash + vomiting + stomach cramps + dizziness = TYPHOID

**Example**:
- "Vomiting, lost appetite, rashes, eye pain, can't sleep" → **DENGUE** (eye pain is key!)
- "Vomiting, stomach cramps, dizzy, weak, pain behind eyes" → **DENGUE** (eye pain + systemic)
- "Rashes all over, itchy, lost appetite, tired, something wrong" → **DENGUE** (not chicken pox - "something wrong" systemic)

### CRITICAL RULE 5: DENGUE - RASH + APPETITE LOSS + "SOMETHING WRONG" = DENGUE
**Error**: Predicting chicken pox for dengue with rash + appetite loss + exhaustion

**Key Pattern**:
- **Dengue**: Rash + appetite loss + "feel like something is wrong with my body" = DENGUE
  - Systemic feeling that "something is wrong" = Dengue
  - Chicken pox: More localized rash presentation
- **Chicken Pox**: Itchy rash + fever + NO systemic "something wrong" feeling

**DECISIVE**: Rash + appetite loss + "feel like something is wrong" = DENGUE
**DECISIVE**: Itchy rash + fever + localized symptoms = CHICKEN POX

**Example**:
- "Rashes all over, itchy, lost appetite, feel very tired, feel like something is wrong" → **DENGUE**
- "Itchy rash, lost appetite, tired" → **CHICKEN POX**

### CRITICAL RULE 6: DENGUE - RASH + RED/SWOLLEN + WORSE IN ARMS/LEGS = DENGUE
**Error**: Predicting chicken pox for dengue with rash distribution

**Key Pattern**:
- **Dengue**: Rash + red and swollen + WORSE IN ARMS AND LEGS = DENGUE
  - Rash that is "worse in some places" (arms and legs) = Dengue
- **Chicken Pox**: Generalized rash "all over body" equally

**DECISIVE**: Rash + swollen + worse in arms/legs = DENGUE
**DECISIVE**: Rash all over body uniformly = CHICKEN POX

**Example**:
- "Rash all over, red and swollen, worse in arms and legs, don't feel like eating" → **DENGUE**
- "Rash all over body, itchy, fever" → **CHICKEN POX**

### CRITICAL RULE 7: CHICKEN POX - RASH + FEVER + ITCHY + PAINFUL = DISTINGUISH CAREFULLY
**Error**: Predicting impetigo for chicken pox with itchy AND painful rash

**Key Pattern**:
- **Chicken Pox**: Rash with little bumps that are ITCHY and PAINFUL + fever + tired = CHICKEN POX
  - Can have BOTH itchy AND painful sensations (not exclusive)
  - "Little bumps" that are itchy AND painful = Chicken Pox
  - "Itchy and painful" together = Chicken Pox
- **Impetigo**: Fluid-filled blisters that are PAINFUL TO TOUCH specifically + facial location

**DECISIVE**: Rash + little bumps + itchy + painful + fever + tired = CHICKEN POX
**DECISIVE**: Fluid-filled blisters PAINFUL TO TOUCH + facial = IMPETIGO

**Example**:
- "Rash with little bumps that are itchy and painful, fever, tired" → **CHICKEN POX**
- "Rash that is red, raised, filled with fluid, painful to touch" → **IMPETIGO**

### CRITICAL RULE A: IMPETIGO - PAINFUL FLUID-FILLED BLISTERS ≠ ALL OVER BODY
**The #1 error pattern**: Predicting chicken pox when impetigo is correct

**Impetigo vs Chicken Pox Distinction**:
- **Impetigo**: Fluid-filled blisters that are **PAINFUL TO TOUCH** + NOT described as "all over body"
  - "Rash that is red, raised, and filled with fluid. Painful to touch" = IMPETIGO
  - Location not specified as "all over body" = IMPETIGO
- **Chicken Pox**: Itchy blisters + "all over body" distribution mentioned
  - "Little red spots all over body" = CHICKEN POX

**DECISIVE**: Painful fluid-filled blisters (not "all over body") = IMPETIGO

### CRITICAL RULE B: CHICKEN POX - ITCHY RASH WITHOUT FEVER
**Error**: Predicting allergy for itchy rash without fever

**Chicken Pox Pattern**:
- Itchy rash on arms/neck/body WITHOUT fever mentioned = CHICKEN POX
- Fever is NOT required to be explicitly stated for chicken pox diagnosis
- Early chicken pox can present with just rash + itching before fever develops

**DECISIVE**: Itchy rash (no fever mentioned) = CHICKEN POX (NOT allergy)

### CRITICAL RULE C: DRUG REACTION - TASTE CHANGES REQUIRE METALLIC QUALIFIER
**Error**: Predicting drug reaction for any taste change

**Drug Reaction Requirements**:
- **MUST HAVE**: "Metallic taste" specifically (not just "bad taste")
- **OR**: Flaky/peeling skin + rash
- **PLUS**: Either appetite loss OR neurological symptoms (tremors, cognitive issues)

**NOT Drug Reaction**:
- "Bad taste" without "metallic" qualifier = NOT drug reaction
- "Mouth tastes bad" + itchy throat = ALLERGY pattern

**DECISIVE**: Taste changes must be "metallic" to qualify for drug reaction

### CRITICAL RULE D: PNEUMONIA - COLORED PHLEGM IS DECISIVE
**Error**: Predicting asthma for colored phlegm symptoms

**Asthma vs Pneumonia Distinction**:
- **Asthma**: Clear/white phlegm OR no phlegm mentioned
- **Pneumonia**: "Colored" phlegm (green, yellow, brown, red) = DECISIVE for pneumonia
  - "Phlegm that's a weird color" = PNEUMONIA
  - "Thick mucus" + "colored" = PNEUMONIA

**DECISIVE**: Colored phlegm = PNEUMONIA (trumps breathing difficulty pattern)

### CRITICAL RULE E: CHICKEN POX - NAUSEA + APPETITE LOSS PATTERN
**Error**: Predicting drug reaction for rash + nausea + appetite loss

**Chicken Pox Pattern**:
- Rash + nausea + appetite loss + exhaustion = CHICKEN POX
- No metallic taste mentioned = CHICKEN POX (drug reaction requires metallic taste)
- "Feeling really sick" + rash = CHICKEN POX

**Drug Reaction Requirements**:
- Rash + appetite loss = MUST check for METALLIC TASTE
- Without metallic taste = NOT drug reaction
- Chicken pox pattern takes precedence

**DECISIVE**: Rash + nausea + appetite loss WITHOUT metallic taste = CHICKEN POX

---

## SURGICAL DISCRIMINATORS

### SURGICAL FIX 1: CHEST/BACK RASH + FLAKY SKIN = DRUG REACTION (NOT Psoriasis)

**Error Pattern**: Predicting psoriasis for rash on chest and back with flaky skin

**Key Discriminator**:
- **Drug Reaction**: Rash on chest AND back + flaky skin + itching (NOT specifically on knees/elbows)
- **Psoriasis**: MUST have location on knees and/or elbows specifically

**DECISIVE RULE**: Chest AND back rash with flaky skin = DRUG REACTION (Psoriasis requires knee/elbow location)

**Example**:
- "Rashes on my chest and back, itching all over, flaky skin that leaves marks" = **DRUG REACTION** (NOT psoriasis - no knee/elbow mention)

---

### SURGICAL FIX 2: NIGHT SYMPTOMS + STIFF NECK = ALLERGY (even with taste loss)

**Error Pattern**: Predicting common cold for stuffy nose + taste/smell loss + chest pain at night + stiff neck

**Key Discriminator**:
- **Allergy**: Chest discomfort at night + stiff neck = post-nasal drip from allergies (DECISIVE)
- **Common Cold**: Loss of taste/smell WITHOUT night chest symptoms

**DECISIVE RULE**: Chest pain/discomfort at night + stiff neck = ALLERGY (trumps taste/smell loss)

**Example**:
- "Stuffy nose, can't taste/smell, chest pain at night, stiff neck" = **ALLERGY** (night symptoms + stiff neck override taste loss)

---

### SURGICAL FIX 3: NAUSEA + VOMITING + APPETITE LOSS (NO RASH) = TYPHOID

**Error Pattern**: Predicting chicken pox for nausea + vomiting + appetite loss + weakness without rash

**Key Discriminator**:
- **Typhoid**: Nausea + vomiting + appetite loss + weakness (GI symptoms prominent) WITHOUT rash
- **Chicken Pox**: Nausea + appetite loss + exhaustion + MUST have rash

**DECISIVE RULE**: Nausea + vomiting + appetite loss + weakness WITHOUT any mention of rash = TYPHOID

**Example**:
- "Feeling really sick, nausea and vomiting, lost my appetite, feeling weak" = **TYPHOID** (GI symptoms without rash)

---

### SURGICAL FIX 4: EXPLICIT BREATHING DIFFICULTY AS PRIMARY = ASTHMA

**Error Pattern**: Predicting pneumonia for cough + explicit "hard to breathe" + thick mucus + fever

**Key Discriminator**:
- **Bronchial Asthma**: "Hard to breathe" / "trouble breathing" explicitly mentioned as PRIMARY symptom
- **Pneumonia**: Fever + thick/colored mucus + "feeling sick from infection" (breathing difficulty is secondary)

**DECISIVE RULE**: Explicit "hard to breathe" or "trouble breathing" as primary complaint = ASTHMA

**Example**:
- "Coughing a lot, hard to breathe, coughing up thick mucus, really tired, fever" = **ASTHMA** (breathing difficulty is primary)

---

## SEMANTIC SYMPTOM ESSENCES (Key Patterns to Recognize)

### ESSENCE 1: BRONCHIAL ASTHMA Pattern
**What it feels like**: Breathlessness, chest tightness, wheezing/whistling, coughing (often worse at night), tiredness from breathing effort
**Key markers**: "hard to breathe", "tight chest", "wheezing", "shortness of breath", "tired from breathing"
**Fever**: Usually ABSENT or low-grade if present
**Mucus**: Usually minimal or clear; thick PRODUCTIVE or COLORED mucus suggests pneumonia

**SEMANTIC DISTINCTION FROM PNEUMONIA**:
- Asthma = breathing difficulty as the PRIMARY symptom, cough is secondary
- Asthma = tiredness/weakness FROM the breathing effort, not from systemic infection
- Pneumonia = fever + thick/colored mucus + feeling sick from infection
- **COLORED PHLEGM = PNEUMONIA** (decisive)

**Examples**:
- "Cough for days, hard to breathe, really tired and weak" → Asthma (breathing difficulty is primary)
- "Trouble breathing, coughing a lot, feeling exhausted" → Asthma
- "Cough, colored phlegm, feeling run down" → Pneumonia (colored phlegm is decisive)

---

### ESSENCE 2: PNEUMONIA Pattern
**What it feels like**: High fever, thick/colored mucus production, feeling generally sick, weakness from infection
**Key markers**: "high fever", "thick mucus", "colored phlegm", "coughing up", "feeling sick", "saliva/mucus became thick"
**Fever**: HIGH and PROMINENT
**Mucus**: THICK and PRODUCTIVE, often COLORED (green, yellow, brown, red)

**SEMANTIC DISTINCTION FROM ASTHMA**:
- Pneumonia = fever is PRIMARY symptom, thick/colored mucus is prominent
- Pneumonia = feeling sick from infection, not just breathing effort
- **DECISIVE**: Colored phlegm = Pneumonia (regardless of breathing difficulty)
- Key question: Is the patient more bothered by fever/feeling sick, or by breathing difficulty?

---

### ESSENCE 3: IMPETIGO Pattern (vs Chicken Pox)
**What it feels like**: Sores/weeping blisters on face (around nose/mouth), yellow crusting/honey-colored crust, fever
**Key markers**: "sores near nose", "weeping fluid", "yellow crust", "face rash", "spreading to arms/legs", "PAINFUL to touch"
**Location**: FACE/NOSE/MOUTH is critical
**Pain**: Vesicles are PAINFUL to touch (NOT itchy like chicken pox)

**SEMANTIC DISTINCTION FROM CHICKEN POX**:
- Impetigo = FACIAL location (around nose/mouth) + fever OR PAINFUL vesicles
- Impetigo = "PAINFUL TO TOUCH" vesicles (key differentiator)
- Chicken Pox = generalized/all over body rash
- If sores are specifically "on face" or "near nose" → Impetigo
- If blisters are "PAINFUL TO TOUCH" (not itchy) → Impetigo
- Yellow crusting CONFIRMS Impetigo but NOT REQUIRED if other signs present

**Examples**:
- "Rash on my face and near my nose, spreading down arms and legs" → Impetigo (facial + spreading)
- "Sores on my face, weeping clear fluid, high fever" → Impetigo (facial + fever)
- "Rash that is red, raised, and filled with fluid. Painful to touch, fever" → **IMPETIGO** (painful vesicles)

---

### ESSENCE 4: CHICKEN POX Pattern
**What it feels like**: Itchy rash, fluid-filled blisters (vesicles), fever, tiredness, nausea, appetite loss
**Key markers**: "itchy rash", "fluid-filled blisters", "red spots", "all over body", "nausea", "exhaustion"
**Location**: Usually generalized (all over body)
**Key Feature**: Itchy (NOT painful) vesicles

**SEMANTIC DISTINCTION FROM IMPETIGO**:
- Chicken Pox = ITCHY vesicles (NOT painful to touch)
- Chicken Pox = generalized rash, not specifically facial
- Chicken Pox = vesicles/blisters in different stages
- Chicken Pox = Can present with nausea + appetite loss + exhaustion

**CRITICAL PATTERNS**:
1. Itchy rash WITHOUT fever mentioned = CHICKEN POX (not allergy)
2. Rash + nausea + appetite loss + exhaustion = CHICKEN POX (not drug reaction)
3. "Little red spots all over body" + fever = CHICKEN POX
4. WITHOUT metallic taste + rash + systemic symptoms = CHICKEN POX

---

### ESSENCE 5: ALLERGY vs COMMON COLD
**ALLERGY Essence**: Itchy symptoms (itchy eyes, itchy/scratchy throat), sneezing, runny/stuffy nose, NO fever, symptoms triggered by allergens
**COMMON COLD Essence**: Runny/stuffy nose, sore throat, cough, LOSS OF TASTE/SMELL, NO fever usually

**Key Distinction**:
- ITCHY (eyes, throat) + runny nose = Allergy
- LOSS OF TASTE/SMELL + stuffy nose = Common Cold (DECISIVE)
- **FEVER PRESENT = NOT ALLERGY** (fever always means infection)

---

### ESSENCE 6: TYPHOID vs MALARIA vs DENGUE
**TYPHOID**: Fever (sustained, several days), stomach pain, diarrhea/constipation, nausea, appetite loss
**MALARIA**: High fever, CHILLS, SWEATING (cyclical pattern), headache, muscle aches
**DENGUE**: High fever, SEVERE muscle/joint pain ("breakbone"), pain behind eyes, rash

**Key Distinctions**:
- Stomach pain + diarrhea + fever = Typhoid (NOT malaria)
- Fever + chills + sweating = Malaria
- Fever + SEVERE muscle/joint pain = Dengue

---

### ESSENCE 7: DRUG REACTION vs ALLERGY
**DRUG REACTION**: Metallic taste, flaky/peeling skin, rash + appetite loss OR neurological symptoms
**ALLERGY**: Itchy symptoms, sneezing, runny nose, NO metallic taste, NO taste changes

**Key Distinction**:
- **"Metallic taste" = Drug Reaction** (NOT allergy)
- "Bad taste" without "metallic" = NOT Drug Reaction (consider allergy)
- Itchy throat/eyes without taste changes = Allergy
- **CRITICAL**: Taste changes MUST be "metallic" to qualify for drug reaction

---

### ESSENCE 8: VARICOSE VEINS
**What it feels like**: Leg pain, cramps (worse when standing), skin changes near veins (redness, itching, inflammation), visible twisted veins
**Key markers**: "legs", "veins", "cramps", "red", "itchy", "inflamed", "spreading", "standing"
**Key Feature**: Leg location + skin changes near veins + NO fever

**SEMANTIC DISTINCTION FROM FUNGAL INFECTION**:
- Varicose Veins = Rash on legs + red/inflamed/itchy + spreading + NO fever
- Fungal Infection = Bumps like pimples + different colored patches + spreading

---

### ESSENCE 9: DENGUE
**What it feels like**: Sudden high fever, SEVERE muscle and joint pain ("breakbone fever"), pain behind the eyes, rash, headache
**Key markers**: "severe muscle pain", "joint pain", "breakbone", "high fever", "small red spots", "rash", "vomiting"
**Fever**: HIGH and SUDDEN
**Pain**: SEVERE muscle/joint pain is HALLMARK symptom

**SEMANTIC DISTINCTION FROM CHICKEN POX**:
- Dengue = SEVERE muscle/joint pain (breakbone) + rash + fever
- Chicken Pox = Itchy fluid-filled blisters + fever (no severe pain)
- Dengue = Small red spots without blisters (distinguishes from chicken pox)

**SEMANTIC DISTINCTION FROM ARTHRITIS**:
- Dengue = Joint pain + systemic symptoms (nausea, vomiting, weakness) + NO swollen joints
- Arthritis = Joint pain + SWOLLEN JOINTS + walking difficulty

---

### ESSENCE 10: MALARIA
**What it feels like**: Cyclical fever (chills → fever → sweating), headache, muscle aches, vomiting, generalized itching
**Key markers**: "chills", "sweating", "cyclical", "high fever", "vomiting", "itchy all over"
**Fever**: CYCLICAL pattern (alternating chills and sweating)

**SEMANTIC DISTINCTION FROM DENGUE**:
- Malaria = Chills + fever + sweating (cyclical) + NO severe muscle pain
- Dengue = SEVERE muscle/joint pain + rash + fever (no cyclical pattern)

---

### ESSENCE 11: FUNGAL INFECTION
**What it feels like**: Itchy rash with texture variation (bumps like pimples), different colored patches, spreading pattern
**Key markers**: "bumps like pimples", "different color", "colored patches", "spreading", "itchy rash"
**Key Feature**: Texture variation (bumps) + color variation + NO fever

**SEMANTIC DISTINCTION FROM CHICKEN POX**:
- Fungal = Bumps like pimples + different colored patches + spreading
- Chicken Pox = Fluid-filled blisters (NOT bumps) + fever

---

### ESSENCE 12: PEPTIC ULCER
**What it feels like**: Burning upper abdominal pain, appetite changes (loss or abnormal hunger), pain worse when eating, nausea
**Key markers**: "burning stomach", "burning abdomen", "pain after eating", "appetite loss", "loose stools after eating"
**Pain Trigger**: Food (eating makes it worse)

**SEMANTIC DISTINCTION FROM GERD**:
- Peptic Ulcer = Burning + appetite changes + pain after eating
- GERD = Heartburn + worse lying down + food triggers (regurgitation pattern)

---

## CRITICAL DIFFERENTIATION RULES (ALWAYS CHECK FIRST)

### CRITICAL RULE A: VARICOSE VEINS SKIN CHANGES
**Rash on legs that is red, inflamed, AND itchy with spreading = VARICOSE VEINS (NOT fungal infection)**

Key differentiators:
- Leg location (especially calves/thighs)
- Red, inflamed appearance
- Itchy (not just painful or burning)
- Spreading pattern
- NO fever
- May have visible varicose veins mentioned

**EXAMPLE PATTERN:**
- "Rash on legs that is red, inflamed, and itchy. It is spreading" = VARICOSE VEINS

### CRITICAL RULE B: DRUG REACTION - COGNITIVE SYMPTOMS
**Loss of libido + brain fog + confusion = DRUG REACTION (NOT hypertension)**

Key differentiators:
- Loss of interest in sex/arousal
- Brain fog (difficulty thinking clearly)
- Confusion
- NO chest pain, NO dizziness, NO high blood pressure symptoms
- NO metallic taste mentioned

**EXAMPLE PATTERN:**
- "Not interested in sex anymore, hard to get aroused, brain fog, feel confused" = DRUG REACTION

### CRITICAL RULE C: ASTHMA - EXHAUSTION FROM SYMPTOMS
**"Tired and worn out from dealing with" breathing symptoms = BRONCHIAL ASTHMA (NOT pneumonia)**

Key differentiators:
- "Tired/worn out FROM dealing with" symptoms (not "feeling sick FROM")
- High fever might be present but NOT with "feeling sick"
- Mucus coughing
- Focus on breathing effort exhaustion

**EXAMPLE PATTERN:**
- "Tired and weak, hard to deal with symptoms, coughing up mucus" = BRONCHIAL ASTHMA

### CRITICAL RULE D: MALARIA - CYCLICAL FEVER PATTERN
**Chills + fever + sweating (cyclical pattern) = MALARIA (NOT dengue)**

Key differentiators:
- Chills AND fever AND sweating together
- Itchy all over (generalized pruritus)
- Cyclical pattern (alternating chills and sweating)
- NO severe muscle/joint pain (distinguishes from dengue)

**EXAMPLE PATTERN:**
- "Itchy all over, chills, vomiting, high fever, sweating a lot, headache, nauseous, sore muscles" = MALARIA

### CRITICAL RULE E: PEPTIC ULCER - BURNING + FOOD TRIGGERS
**Burning in stomach + worse lying down + pain after certain foods = PEPTIC ULCER (NOT GERD)**

Key differentiators:
- Burning feeling in stomach (not just heartburn)
- Worse when lying down (gravity affects healing)
- Pain after eating certain foods (spicy/acidic)
- Loose stools after trigger foods

**EXAMPLE PATTERN:**
- "Burning feeling in stomach worse when lying down, pain after eating certain foods, loose stools" = PEPTIC ULCER

### CRITICAL RULE F: DENGUE - SMALL RED SPOTS WITHOUT ITCHY RASH
**Small red spots on arms/legs + extreme tiredness = DENGUE (NOT chicken pox)**

Key differentiators:
- Small red spots (not itchy blisters)
- Extreme tiredness/fatigue
- Arms and legs location
- NO fever mentioned (distinguishes from chicken pox which usually has fever)

**EXAMPLE PATTERN:**
- "Really tired and weak, can't get enough sleep, small red spots on arms and legs" = DENGUE

### CRITICAL RULE G: DENGUE - JOINT PAIN + NAUSEA + WEAKNESS
**Joint pain + difficulty walking + lost appetite + weak + nauseous = DENGUE (NOT arthritis)**

Key differentiators:
- Joint pain with systemic symptoms (nausea, weakness)
- Lost appetite
- Weak feeling
- NO swollen joints mentioned (would suggest arthritis)
- Nausea present

**EXAMPLE PATTERN:**
- "Joint pain, hard to walk, lost appetite, weak, nauseous" = DENGUE

### CRITICAL RULE H: DENGUE - EXTREME BODY PAIN + RASH + VOMITING
**Extreme body pain + headache + vomiting + red spots all over + itchy = DENGUE (NOT chicken pox)**

Key differentiators:
- Extreme body pain (not just rash)
- Headache present
- Vomiting present
- Red spots ALL OVER (not just local)
- Itchy rash
- Systemic symptoms (body pain, headache)

**EXAMPLE PATTERN:**
- "Extreme body pain, headache, vomiting, red spots all over, very itchy" = DENGUE

### CRITICAL RULE I: FUNGAL INFECTION - BUMPS + COLOR PATCHES
**Rash all over + red and itchy + small bumps like pimples + strange patches of different color = FUNGAL INFECTION (NOT chicken pox)**

Key differentiators:
- Small bumps like pimples (NOT fluid-filled blisters)
- Strange patches of different color
- All over body distribution
- NO fever mentioned
- Texture variation (bumps + patches)

**EXAMPLE PATTERN:**
- "Rash all over, red and itchy, small bumps like pimples, strange patches of different color" = FUNGAL INFECTION

### Rule 1: YELLOW SKIN/EYES
- **If yellow skin or yellow eyes is present → Jaundice** (regardless of other symptoms)

### Rule 2: VISUAL SYMPTOMS + HEADACHE
- **If visual DISTORTION (blurry, wavy, zigzag, blind spots) + headache → Migraine**
- **If visual PROBLEMS (blurry, unclear) + NO headache + fatigue + dizziness → Diabetes**
- **NOT GERD** even if acid reflux is present - headache with visual changes = migraine

### Rule 3: FEVER + RESPIRATORY SYMPTOMS
- **If fever + thick sputum + productivel cough → Pneumonia**
  - CRITICAL: "Thick sputum" must be explicitly described
  - **CRITICAL: Colored phlegm (green, yellow, brown, red) = PNEUMONIA**
- **If NO fever + gradual onset + runny nose + sore throat → Common Cold**
- **If wheezing + NO fever + NO thick sputum → Bronchial Asthma**
- **KEY: Cough + breathing difficulty + NO FEVER = Bronchial Asthma (NOT pneumonia)**
- **CRITICAL: If fever is NOT explicitly stated, assume NO FEVER and predict Asthma**
- **IMPORTANT: Thick/colored mucus alone is NOT enough for pneumonia - must have fever or feeling sick**

### Rule 3b: ALLERGY vs COMMON COLD - DECISIVE SYMPTOMS
- **LOSS OF TASTE OR SMELL = COMMON COLD** (trumps all other respiratory symptoms)
- **ITCHY EYES or ITCHY/SCRATCHY THROAT + NO taste/smell loss = Allergy**
- **CRITICAL**: When BOTH are present (stuffy nose + itchy throat + can't taste), Common Cold wins
- **CRITICAL**: "Scratchy throat" alone without "itchy" = not definitive, use other symptoms
- **FEVER PRESENT = NOT ALLERGY** (fever always indicates infection)

### Rule 4: FEVER + RASH PATTERNS
- **If yellow honey-colored crusting + fluid-filled sores → Impetigo** (especially around nose/mouth)
  - MANDATORY: Yellow crusting must be PRESENT for impetigo diagnosis
  - **CRITICAL: PAINFUL TO TOUCH vesicles = IMPETIGO** (even without yellow crusting)
  - Without yellow crusting + NOT painful + "all over body" = chicken pox
- **If vesicles (fluid-filled blisters) in different stages + fever → Chicken Pox**
  - Can present with just fever + fluid-filled blisters (without "different stages" mentioned)
- **If widespread rash + fever + SEVERE muscle/joint pain ("breakbone") → Dengue**
- **If fever + muscle pain (SEVERE) + pain behind eyes + itching → Dengue**
- **If fever + chills + cyclical sweating → Malaria** (NOT dengue unless severe muscle pain prominent)
- **If fever + rash + SEVERE appetite loss + vomiting + skin peeling → Drug Reaction**
- **If fever + rash + nausea + appetite loss + exhaustion WITHOUT metallic taste → Chicken Pox**

### Rule 5: GASTROINTESTINAL DIFFERENTIATION
- **If heartburn + acid taste + worse lying down → GERD**
- **If burning upper abdominal pain + appetite loss + pain WORSE WHEN EATING → Peptic Ulcer Disease**
- **If belching + chest pain radiating to arm/jaw/neck + pressure → GERD** (NOT hypertension)
- **If constant hunger + stomach cramps + bloating after eating → Peptic Ulcer Disease** (NOT GERD)
- **Key difference**: GERD has heartburn/regurgitation; Peptic Ulcer has meal-related pain + appetite changes
- **CRITICAL: Burning stomach + appetite loss = Peptic Ulcer (NOT GERD)**

### Rule 6: NECK VS OTHER JOINT SYMPTOMS
- **If neck stiffness + neck pain + balance issues → Cervical Spondylosis**
- **If joint pain in knees/hips/hands + difficulty walking + SWOLLEN JOINTS → Arthritis**
- **If joint/muscle pain + weakness + nausea + NO swollen joints → Consider Dengue**
- **CRITICAL: Joint pain + swollen joints + walking difficulty = Arthritis (NOT cervical spondylosis)**
- **CRITICAL: Stiff neck + joint pain + difficulty steering/walking = Arthritis**

### Rule 7: SKIN RASH CRITICAL DISTINCTIONS
- **Impetigo**: Yellow honey-colored crusting + weeping sores (face around mouth/nose) + fever
  - MANDATORY: Yellow crusting required OR PAINFUL vesicles
  - **KEY: Painful to touch vesicles = IMPETIGO**
  - Without yellow crusting + PAINFUL = consider impetigo
- **Chicken Pox**: Fluid-filled vesicles at different stages OR generalized itchy rash + fever
  - Can present WITHOUT "different stages" mentioned
  - **KEY: Itchy rash WITHOUT fever mentioned = CHICKEN POX**
  - **KEY: Rash + nausea + appetite loss + exhaustion = CHICKEN POX**
- **Drug Reaction**: Rash + APPETITE LOSS + systemic symptoms OR neurological symptoms (tremors, shaking)
  - **CRITICAL: MUST HAVE metallic taste OR flaky skin + rash**
  - **CRITICAL: "Bad taste" without "metallic" = NOT Drug Reaction**
- **Dengue**: Rash with SEVERE muscle/joint pain ("breakbone fever")
- **Fungal Infection**: Color variation + spreading + nodules/bumps that expand (NO fever typically)
- **Varicose Veins**: Enlarged/twisted/noticeable blood vessels in legs + cramps + skin changes near veins (NO fever)
  - Key: Leg veins + redness/itching/inflammation near veins + cramps when standing

### Rule 8: TASTE SYMPTOMS
- **If metallic taste + taste/smell changes + joint/muscle pain → Drug Reaction**
  - Metallic taste is a neurological symptom
  - **CRITICAL: "Metallic" qualifier is REQUIRED for drug reaction**
- **If "bad taste" without "metallic" + itchy throat → Allergy** (NOT drug reaction)
- **If loss of taste/smell + stuffy nose + NO itchy symptoms → Common Cold**
- **If itchy eyes/throat + sneezing + NO fever → Allergy**

### Rule 9: FATIGUE PATTERNS
- **If extreme fatigue ONLY (no fever, no rash, no other symptoms) → Consider Chicken Pox**
  - Early chicken pox can present with just fatigue before rash appears
- **If fatigue + thirst + frequent urination + vision changes → Diabetes**

---

## HIGH-IMPACT ERROR PATTERNS (From Training Analysis)

These patterns caused the most misclassifications. Master these discriminators.

### ERROR PATTERN 1: HEADACHE + CHEST PAIN + DIZZINESS + CONCENTRATION ISSUES = HYPERTENSION

**Common Error**: Predicting Migraine or GERD for this symptom cluster

**Key Discriminator**:
- **Hypertension**: Headache + chest pain + dizziness + trouble concentrating (NO fever, NO rash, NO skin symptoms)
- **Migraine**: Visual DISTORTION (wavy/zigzag) + headache (visual changes are REQUIRED)
- **GERD**: Belching + chest pain radiating to arm/jaw + heartburn/acid taste (use for belching cases)

**Example**:
- "Trouble concentrating, headaches, chest pain, dizziness, off balance" → **Hypertension**
- "Belching, chest pain goes to arm/jaw/neck, pressure in chest" → **GERD** (NOT hypertension)

---

### ERROR PATTERN 2: PNEUMONIA vs ASTHMA - COLORED PHLEGM IS DECISIVE

**Common Errors**: Predicting Pneumonia when Asthma is correct (3+ errors)

**Key Discriminator - CRITICAL REFINEMENT**:
- **ASTHMA**: Explicit breathing difficulty (hard to breathe, difficulty breathing, shortness of breath, can't catch breath) + clear/white/minimal phlegm
- **Pneumonia**: High fever + thick/colored mucus + "feeling really sick" from infection
  - **DECISIVE**: Colored phlegm (green, yellow, brown, red) = PNEUMONIA
  - **DECISIVE**: "Phlegm that's a weird color" = PNEUMONIA
- **Bronchial Asthma**: Breathing difficulty is PRIMARY complaint, cough is secondary
  - KEY: "Dry cough and difficulty in breathing" = Asthma (explicit breathing difficulty)

**CRITICAL DISTINCTION**:
- **"Colored phlegm"** = **PNEUMONIA** (decisive, regardless of other symptoms)
- **"Hard to breathe" + clear phlegm/no fever** = **ASTHMA**

**PATTERN RECOGNITION**:
- **"Phlegm that's a weird color" + cough + feeling run down** = **PNEUMONIA**
- **"Dry cough and difficulty in breathing"** = **ASTHMA** (explicit breathing difficulty)
- **"Hard to breathe" or "shortness of breath" explicitly mentioned + clear phlegm** = **ASTHMA**

**RULE REFINEMENT**:
1. If "breathing difficulty" / "shortness of breath" / "hard to breathe" explicitly mentioned:
   - If NO fever + NO colored/thick mucus → **Asthma**
   - If colored/thick mucus present → **Pneumonia** (colored phlegm is decisive)
2. If NO explicit breathing difficulty mentioned:
   - If colored phlegm → **Pneumonia**
   - If "feeling really sick" + fever + thick mucus → **Pneumonia**

**WHY MODEL FAILS**: The model sees "fever + mucus" and predicts pneumonia. It misses that colored phlegm is the key differentiator from asthma.

**CRITICAL**: COLORED PHLEGM = PNEUMONIA

---

### ERROR PATTERN 3: PAINFUL FLUID-FILLED BLISTERS = IMPETIGO, NOT CHICKEN POX

**Common Errors**: Predicting Chicken Pox when Impetigo is correct (2 errors)

**Key Discriminator - ABSOLUTE RULE**:
- **IMPETIGO**: Fluid-filled blisters that are **PAINFUL TO TOUCH** + NOT described as "all over body"
  - **"Painful to touch" is the key differentiator**
  - "Rash that is red, raised, and filled with fluid. Painful to touch" = IMPETIGO
  - Location not specified as "all over body" = IMPETIGO
- **CHICKEN POX**: Itchy blisters + "all over body" distribution OR generalized itchy rash
  - "Itchy rash" without "painful to touch" = CHICKEN POX

**CRITICAL DECISION TREE**:
1. **Fluid-filled blisters that are PAINFUL TO TOUCH?** → **IMPETIGO**
2. **"All over body" rash + fever + itchy?** → **CHICKEN POX**
3. **Yellow honey-colored crusting on sores?** → **IMPETIGO** (confirms)

**Examples - LEARN THE PATTERN**:
- "Rash on my skin that is red, raised, and filled with fluid. Painful to touch and I have a fever" → **IMPETIGO** (painful vesicles, not "all over body")
- "Rash all over my body, fever, headache, feeling sick" → **CHICKEN POX** (generalized)

**CRITICAL**: Painful to touch vesicles = IMPETIGO
**CRITICAL**: Itchy (not painful) vesicles = CHICKEN POX

---

### ERROR PATTERN 3b: CHICKEN POX - ITCHY RASH WITHOUT FEVER

**Common Errors**: Predicting Allergy for itchy rash without fever mentioned

**Key Discriminator**:
- **Chicken Pox**: Itchy rash on arms/neck/body + NO fever explicitly mentioned
  - Itchy rash can be chicken pox even without fever being mentioned
  - Early chicken pox can present with just rash + itching
- **Allergy**: Itchy symptoms + NO fever (itchy eyes, scratchy throat)

**DECISIVE RULE**: Itchy rash on arms/neck (without mention of "itchy eyes/throat" or fever) = CHICKEN POX

**Examples**:
- "I have a rash on my arms and neck that itches like crazy. I've been feeling really uncomfortable all day" → **CHICKEN POX** (NOT allergy)
- "Stuffy nose, red and itchy eyes, scratchy throat, no fever" → **Allergy**

**WHY MODEL FAILS**: The model assumes "no fever = allergy" but itchy rash on arms/neck can be chicken pox.

**CRITICAL**: Itchy rash without fever mentioned = CHICKEN POX (NOT allergy)

---

### ERROR PATTERN 4: DRUG REACTION REQUIRES METALLIC TASTE

**Common Errors**: Predicting Drug Reaction for any taste change

**Key Discriminator - ABSOLUTE RULE**:
- **Drug Reaction**:
  1. "Metallic taste" specifically (NOT just "bad taste")
  2. OR flaky/peeling skin + rash
  3. PLUS either appetite loss OR neurological symptoms
- **NOT Drug Reaction**:
  - "Bad taste" without "metallic" qualifier
  - Itchy throat + bad taste = ALLERGY pattern

**DECISIVE RULE**: "Metallic taste" = Drug Reaction, "bad taste" = NOT Drug Reaction

**Examples**:
- "I'm always tired, my mouth tastes bad, and my throat itches. My muscles are hot and painful" → **ALLERGY** (bad taste without "metallic")
- "Metallic taste, sense of taste and smell changed, joint and muscle pain" → **Drug Reaction** (metallic taste)

**WHY MODEL FAILS**: The model sees any taste change and predicts drug reaction. It misses that "metallic" qualifier is required.

**CRITICAL**: Taste changes MUST be "metallic" for drug reaction

---

### ERROR PATTERN 5: CHICKEN POX - NAUSEA + APPETITE LOSS PATTERN

**Common Errors**: Predicting Drug Reaction for rash + nausea + appetite loss

**Key Discriminator - ABSOLUTE RULE**:
- **Chicken Pox**: Rash + nausea + appetite loss + exhaustion + NO metallic taste
  - Systemic symptoms (nausea, appetite loss) are common in chicken pox
  - "Feeling really sick" + rash = CHICKEN POX
- **Drug Reaction**: Rash + APPETITE LOSS + metallic taste OR flaky skin
  - Metallic taste is REQUIRED for drug reaction diagnosis

**DECISIVE RULE**: Rash + nausea + appetite loss WITHOUT metallic taste = CHICKEN POX

**Examples**:
- "I've been feeling really sick lately. I've been having a lot of nausea and I feel really uneasy. I've also noticed some rashes on my arms and legs. I've lost my appetite and I feel exhausted every day" → **CHICKEN POX** (NOT drug reaction)
- "Rash + nausea + appetite loss + metallic taste" → Drug Reaction

**WHY MODEL FAILS**: The model sees "rash + appetite loss" and predicts drug reaction. It misses that metallic taste is required.

**CRITICAL**: Rash + nausea + appetite loss WITHOUT metallic taste = CHICKEN POX

---

### ERROR PATTERN 6: VARICOSE VEINS PRESENTATION

**Common Errors**: Predicting Fungal Infection for varicose veins

**Key Discriminator**:
- **Varicose Veins**: Leg veins + skin redness/itching/inflammation near veins + cramps (worse when standing) + NO fever
- **Fungal Infection**: Spreading rash + color variation + nodules (NO fever typically)

**Examples**:
- "Rash on legs, red inflamed itchy, spreading, cramps, pain when standing" → **Varicose Veins**
- "Different colored patches, nodules that expand, spreading rash, no fever" → **Fungal Infection**

**CRITICAL**: "Veins" + "legs" + skin changes near veins = varicose veins

---

### ERROR PATTERN 7: ALLERGY vs COMMON COLD - COMPREHENSIVE RULES

**Common Errors**: Predicting Common Cold when Allergy is correct (2+ errors), and vice versa

**Key Discriminator - ABSOLUTE RULE**:
- **FEVER PRESENT = NOT ALLERGY** (Fever always indicates infection, not allergy)
- **LOSS OF TASTE OR SMELL = COMMON COLD** (this trumps other respiratory symptoms)
- **ITCHY SYMPTOMS (eyes, throat) + NO fever = Allergy**

**ALLERGY PATTERN RECOGNITION**:
- **NO FEVER** (critical differentiator)
- **Swollen throat** causing breathing difficulty = ALLERGY
- **Red and watery eyes** = ALLERGY (not cold - cold doesn't affect eyes like this)
- **Sinus pressure + swollen lymph nodes + no fever** = ALLERGY
- **Chest hurts at night** = ALLERGY (allergies often worse at night due to post-nasal drip)
- **Stiff neck** can indicate swollen lymph nodes from allergic inflammation
- **Tickle/scratchy/itchy in throat** = ALLERGY (not definitive alone, but supportive)

**COMMON COLD PATTERN RECOGNITION**:
- **FEVER** is common (ALLERGY NEVER HAS FEVER)
- **Loss of taste or smell** = DECISIVE for cold
- **Feeling cold and shivery** = cold symptom
- **Feeling miserable/exhausted from illness** = cold symptom
- **Sore throat + fever + cough** = cold
- **SWOLLEN LYMPH NODES + feverish/fatigue** = COMMON COLD (lymph nodes indicate infection)

**CRITICAL DECISION TREE**:
1. **FEVER PRESENT?** → If YES → **COMMON COLD** (not allergy, regardless of other symptoms)
2. **NO FEVER + Loss of taste/smell?** → **COMMON COLD**
3. **SWOLLEN LYMPH NODES present?** → **COMMON COLD** (lymph nodes indicate infection, not allergy)
4. **NO FEVER + NO loss of taste/smell + NO swollen lymph nodes + ITCHY symptoms (eyes, scratchy throat, swollen throat)?** → **ALLERGY**
5. **NO FEVER + NO loss of taste/smell + Chest pain at night?** → **ALLERGY** (post-nasal drip)

**CRITICAL NEW RULE**: Sore throat + runny nose + sneezing WITHOUT fever = ALLERGY
**CRITICAL NEW RULE**: Swollen lymph nodes = COMMON COLD (lymph nodes indicate infection, not pure allergy)

**Examples - LEARN THE PATTERN**:
- "Stuffy nose, can't taste or smell, chest pain at night, stiff neck" → **COMMON COLD** (FEVER implied, loss of taste/smell present)
- "Sore throat, coughing, stuffy nose, sinus pressure, feeling miserable, exhausted" → **COMMON COLD** (FEVER implied by "feeling miserable/exhausted", no loss of taste/smell but sick feeling suggests cold)
- "Stuffy nose, red and itchy eyes, scratchy throat, no fever" → **ALLERGY** (no fever, itchy symptoms)
- "Throat swollen, can't breathe well, chest hurts at night, no fever" → **ALLERGY** (swollen throat + night symptoms)

**WHY MODEL FAILS**: The model doesn't prioritize FEVER as the absolute allergy-ruling-out factor. It also misses that chest pain at night and stiff neck are allergy indicators (lymph node swelling/post-nasal drip).

**CRITICAL**: FEVER ALWAYS MEANS NOT ALLERGY. If fever is mentioned or strongly implied ("feeling miserable/exhausted from illness"), predict common cold over allergy.

---

### ERROR PATTERN 8: BURNTING STOMACH + APPETITE LOSS + WORSE WHEN EATING = PEPTIC ULCER

**Common Errors**: Predicting GERD for peptic ulcer, or missing peptic ulcer entirely

**Key Discriminator**:
- **Peptic Ulcer**: Burning upper abdominal pain + APPETITE LOSS + pain WORSE WHEN EATING + nausea
- **GERD**: Heartburn + acid taste + worse when lying down + belching + chest pain radiation

**Examples**:
- "Burning sensation in upper abdomen, frequently nauseous, heartburn, indigestion" → **Peptic Ulcer**
- "Stomach pain, hard to sleep, anxious, no appetite" → **Peptic Ulcer**
- "Constant hunger, stomach cramps, bloated and gassy after eating" → **Peptic Ulcer** (NOT GERD)
- "Belching, chest pain goes to arm/jaw/neck, pressure in chest" → **GERD**

**CRITICAL**: Burning stomach + appetite changes = Peptic Ulcer (NOT GERD)
**CRITICAL**: Belching + chest pain radiation = GERD (NOT hypertension)

---

### ERROR PATTERN 9: EXTREME FATIGUE ONLY = CONSIDER CHICKEN POX

**Common Errors**: Predicting Diabetes for extreme fatigue without other symptoms

**Key Discriminator**:
- **Chicken Pox**: Extreme fatigue ONLY (no fever, no rash mentioned) + no other diagnosis fits
  - Early chicken pox can present with just fatigue before rash appears
- **Diabetes**: Fatigue + thirst + frequent urination + vision changes (MUST have these)

**Examples**:
- "Really tired and weak, can barely get out of bed, trouble staying awake" → **Chicken Pox** (NOT diabetes - no polyuria/polydipsia/vision changes)
- "Thirsty, pee a lot, dizzy, confused, lost vision" → **Diabetes**

**CRITICAL**: Fatigue alone with no other symptoms = consider chicken pox (early presentation)

---

### ERROR PATTERN 10: FACIAL RASH + FEVER + SPREADING = IMPETIGO

**Common Errors**: Predicting Fungal Infection for impetigo

**Key Discriminator**:
- **Impetigo**: Facial rash (around nose/mouth) + fever + spreading
- **Fungal Infection**: Spreading rash + color variation + nodules (NO fever typically)

**Examples**:
- "Rash on face and near nose, spreading down arms and legs, fever" → **Impetigo** (NOT fungal)
- "Different colored patches, nodules that expand, spreading rash, no fever" → **Fungal Infection**

**CRITICAL**: Facial rash + fever = impetigo (NOT fungal)

---

### ERROR PATTERN 11: PSORIASIS VS FUNGAL INFECTION - LOCATION + TEXTURE MATTERS

**Common Errors**: Predicting Fungal Infection when Psoriasis is correct

**Key Discriminator**:
- **Psoriasis**: Dry/flaky/peeling skin on KNEES and ELBOWS specifically + red scaly patches
  - "Skin on my knees and elbows is peeling off" = Psoriasis
  - "Red, scaly patches" + location on knees/elbows = Psoriasis
  - "Dry and flaky" + joint pain = Psoriasis (NOT drug reaction)
- **Fungal Infection**: Spreading rash + color variation + nodules/bumps that expand
  - NO fever typically
  - Nodules that expand/grow = Fungal

**Critical Examples**:
- "Rash on my skin that is itchy and irritating. It is also flaky...worse at night" → **Psoriasis** (NOT fungal - flaky and worse at night)
- "Skin is dry and flaky, joints in pain, skin on knees and elbows peeling off" → **Psoriasis**
- "Itching all over, red scaly patches, bumps that look like small nodules" → **Fungal Infection**

**CRITICAL**: Peeling/flaky skin on knees/elbows = Psoriasis (NOT fungal infection)
**CRITICAL**: Psoriasis can cause joint pain (psoriatic arthritis variant)

---

### ERROR PATTERN 12: DIABETES - THIRST + URINATION = DIABETES EVEN WITH OTHER SYMPTOMS

**Common Errors**: Predicting Drug Reaction when Diabetes is correct

**Key Discriminator**:
- **Diabetes**: Thirst + frequent urination + (any of: fatigue, dizziness, blurry vision)
  - Thirst + urination is the HALLMARK combination
  - Even with neurological symptoms like tremors or taste changes, if thirst + urination present → Diabetes first
- **Drug Reaction**: Metallic taste + taste/smell changes + joint/muscle pain + NO fever/rash
  - Metallic taste is a neurological symptom
  - Fever can be present in drug reactions

**DIABETES PATTERN**:
- **Thirst + frequent urination** = DECISIVE for diabetes
- **No thirst + no frequent urination** = NOT diabetes

**Examples**:
- "Tremors, muscle twitching, decreased sense of smell or taste, fatigued, rapid heartbeat, THIRST, urinate frequently" → **Diabetes**
- "Feeling thirsty and hungry, tired" → **Diabetes**

**CRITICAL**: Thirst + frequent urination = Diabetes (even with other symptoms)

---

### ERROR PATTERN 13: FEVER + PROMINENT NEUROLOGICAL SYMPTOMS = DRUG REACTION

**Common Errors**: Predicting Diabetes when Drug Reaction is correct (1 error)

**Key Discriminator**:
- **Drug Reaction**: Fever + PROMINENT NEUROLOGICAL/Cognitive symptoms (foggy head, can't think straight, lightheaded) + NO thirst/urination
  - Neurological/cognitive symptoms are the PRIMARY presentation
  - Fever indicates drug reaction (not infection)
  - NO thirst or frequent urination rules out diabetes
- **Diabetes**: Thirst + frequent urination + (fatigue, dizziness, blurry vision)
  - NO fever typically
  - Thirst/urination is REQUIRED

**DRUG REACTION PATTERN**:
- **Fever + foggy head + can't think straight + lightheaded** = Drug Reaction
- **No thirst + no frequent urination** = Drug Reaction (rules out diabetes)
- **Prominent cognitive impairment** = Drug Reaction

**Examples - LEARN THE PATTERN**:
- "Fever + lightheaded + heart pounding + head foggy + can't think straight + everything looks blurry" → **Drug Reaction** (NO thirst/urination mentioned, prominent neurological symptoms)
- "Thirsty, pee a lot, dizzy, confused, lost vision" → **Diabetes**

**CRITICAL**: Fever + cognitive impairment (foggy head, can't think straight) + NO thirst/urination = Drug Reaction
**CRITICAL**: Diabetes REQUIRES thirst + frequent urination. Without them, don't predict diabetes.

---

## DISEASE-SPECIFIC CRITERIA

### Bronchial Asthma
**Core Symptoms:**
- Wheezing or whistling sound when breathing
- Shortness of breath or difficulty breathing
- Chest tightness
- Cough (often worse at night)

**Must Have:**
- NO fever (asthma never has fever)
- Breathing difficulty without thick/colored sputum production
- Clear, white, or minimal phlegm

**Must NOT Have:**
- Fever
- Colored/thick sputum (that would be pneumonia)

**Training Pattern:** Cough + breathing difficulty + NO fever explicitly stated = Asthma

---

### Chicken Pox
**Core Symptoms:**
- Itchy red rash (can be generalized)
- Fluid-filled vesicles (may be at different stages)
- Fever
- Tiredness/malaise
- Nausea, appetite loss

**Key Patterns:**
- **CAN present with just rash + fever** (appetite loss NOT required)
- **CAN present with itchy rash WITHOUT fever being mentioned**
- **CAN present with just extreme fatigue (early presentation before rash)**
- **CAN present with nausea + appetite loss + exhaustion (systemic pattern)**
- Rash is the PRIMARY symptom
- **MUST NOT HAVE**: Metallic taste (that would be drug reaction)

**Must NOT Have:**
- Yellow honey-colored crusting (that would be impetigo)
- SEVERE muscle/joint "breakbone" pain (that would be dengue)
- **Metallic taste** (that would indicate drug reaction)

---

### Dengue
**Core Symptoms:**
- Sudden high fever
- SEVERE muscle and joint pain ("breakbone fever")
- Pain behind the eyes
- Rash (often itchy)
- Headache
- Weakness, nausea, vomiting

**Key Pattern:**
- **SEVERE muscle/joint pain is the HALLMARK symptom**
- Systemic symptoms (weakness, nausea) are prominent

**Must Have:**
- SEVERE muscle/joint pain (described as severe, terrible, breakbone)

---

### Drug Reaction
**Core Symptoms:**
- Rashes (widespread)
- Flaky or peeling skin
- Itching

**Additional Symptoms (when present):**
- APPETITE LOSS (STRONG indicator)
- Neurological: Tremors, shaking, metallic taste
- Cognitive: Foggy thinking, can't concentrate
- Systemic: Fever, fatigue, headache, vomiting

**Must Have:**
- **SKIN INVOLVEMENT** (rash, peeling, itching) - REQUIRED (unless taste changes + neurological symptoms)
- **PLUS either appetite loss OR neurological symptoms**
- **PLUS: Metallic taste specifically** (NOT just "bad taste")

**Training Pattern:** Metallic taste + taste/smell changes + joint pain = Drug Reaction

**Must NOT Have:**
- Just cognitive symptoms without skin involvement or metallic taste
- "Bad taste" without "metallic" qualifier

---

### Fungal Infection
**Core Symptoms:**
- Red, itchy rash
- Spreading rash
- Different colored patches
- Nodules or bumps that expand/grow

**Key Patterns:**
- **Nodules that expand = Fungal Infection**
- **Different colored patches = Fungal Infection**
- NO fever typically
- NO yellow crusting (that would be impetigo)
- NO varicose veins (that would be varicose veins)

**Must Have:**
- Spreading OR color variation OR expanding nodules

**Must NOT Have:**
- Leg veins + skin changes near veins (that would be varicose veins)
- Yellow crusting (that would be impetigo)

---

### Gastroesophageal Reflux Disease (GERD)
**Core Symptoms:**
- Heartburn
- Acid taste in mouth
- Worse when lying down or bending over
- Chest discomfort

**Key Patterns:**
- Heartburn is the PRIMARY symptom
- Belching + chest pain radiation to arm/jaw/neck
- NO appetite loss required
- Pain related to position (lying down)

**Must Have:**
- Heartburn OR acid taste OR belching with chest pain radiation

**Must NOT Have:**
- Burning pain + appetite loss + worse when eating (that would be peptic ulcer)

**Training Pattern:** Belching + chest pain radiating = GERD (NOT hypertension)

---

### Hypertension
**Core Symptoms:**
- Headache (often described as band-like)
- Chest pain
- Dizziness
- Trouble concentrating or focusing

**Key Patterns:**
- NO skin involvement
- NO fever
- NO respiratory symptoms
- NO belching or heartburn
- Cardiovascular symptom cluster

**Must Have:**
- At least 2-3 of: headache, chest pain, dizziness, concentration issues

**Must NOT Have:**
- Belching (that would be GERD)
- Heartburn (that would be GERD)

---

### Impetigo
**Core Symptoms:**
- Weeping/oozing sores
- Yellow honey-colored crusting
- Often on face (around mouth/nose)
- Fever (when systemic involvement)

**Key Patterns:**
- **YELLOW CRUSTING is the HALLMARK** - REQUIRED for diagnosis
- **PAINFUL TO TOUCH vesicles = IMPETIGO** (even without yellow crusting)
- Facial location is common
- Fever indicates more severe infection

**CRITICAL:** WITHOUT yellow crusting + PAINFUL vesicles → Consider impetigo
**CRITICAL:** WITHOUT yellow crusting + ITCHY vesicles → Chicken pox

**Must Have:**
- Yellow crusting OR painful vesicles on face

---

### Peptic Ulcer Disease
**Core Symptoms:**
- Burning upper abdominal pain
- Appetite loss (or constant hunger with eating changes)
- Pain WORSE WHEN EATING
- Nausea
- Bloating after eating

**Key Patterns:**
- Burning + appetite loss = Peptic Ulcer
- Pain related to meals (eating makes it worse)
- Constant hunger with post-meal bloating

**Must Have:**
- Burning pain AND appetite changes (loss or abnormal hunger)

**Must NOT Have:**
- Only heartburn without appetite loss (that would be GERD)
- Belching as primary symptom (that would be GERD)

---

### Psoriasis
**Core Symptoms:**
- Red, scaly patches on skin
- Dry, flaky, or peeling skin
- Often on knees, elbows, scalp, or lower back
- Itching (can be severe)
- Can cause joint pain (psoriatic arthritis)

**Key Patterns:**
- **Peeling/flaky skin on KNEES and ELBOWS = Psoriasis**
- "Skin on my knees and elbows is peeling off" = Psoriasis
- Can present WITHOUT fever (unlike fungal infection which also has no fever but different presentation)
- Worse at night is common

**Must Have:**
- Dry/flaky/peeling skin OR red scaly patches
- Location on extensor surfaces (knees, elbows) is typical

**Must NOT Have:**
- Spreading rash with color variation (that would be fungal)
- Nodules that expand/grow (that would be fungal)
- Yellow crusting (that would be impetigo)

---

### Typhoid
**Core Symptoms:**
- Sustained fever (often for several days)
- Diarrhea (or alternating diarrhea/constipation)
- Stomach pain/ache
- Nausea and vomiting
- Loss of appetite
- Weakness and fatigue

**Key Patterns:**
- **Diarrhea + stomach pain + sustained duration (several days) = Typhoid**
- "Diarrhea for a few days" = sustained duration
- Can include mild fever
- Alternating bowel movements common

**Must Have:**
- Diarrhea (or bowel changes) + stomach pain

**Must NOT Have:**
- Only burning pain + appetite loss (that would be peptic ulcer)
- Heartburn/regurgitation (that would be GERD)

---

### Migraine
**Core Symptoms:**
- Severe headache (often one-sided)
- Visual disturbances - can be blurry, wavy, zigzag, blind spots
- Nausea and vomiting
- Sensitivity to light and sound

**Key Patterns:**
- **Visual problems (NOT just distortion) + headache = Migraine**
  - "Blurry vision" with headache = Migraine (even with acid reflux)
  - Visual problems don't require "distortion" description
- **Visual aura** (seeing zigzag lines, flashing lights, blind spots) is classic
- Can coexist with other symptoms (GI, neck stiffness) but headache + visual = migraine

**Must Have:**
- Headache + visual problems (any type: blurry, unclear, distorted)

**Must NOT Have:**
- Only headache without visual problems (consider tension headache or other)
- Only heartburn/acid reflux without headache (that would be GERD)

---

### Varicose Veins
**Core Symptoms:**
- Enlarged, twisted, or noticeable blood vessels in legs
- Leg pain, worse when standing for long periods
- Cramps (especially at night or after standing)
- Skin changes near veins (redness, itching, inflammation)

**Key Patterns:**
- NO fever (important differentiator from infection)
- Leg veins are the PRIMARY clue
- Skin changes near veins (NOT general spreading rash)
- Cramps when standing

**Must Have:**
- Leg veins + at least one of: skin changes near veins, cramps, pain when standing

**Must NOT Have:**
- General spreading rash with color variation (that would be fungal)
- Yellow crusting (that would be impetigo)

---

## QUICK REFERENCE DECISION TREE

1. **Yellow skin/eyes?** → **JAUNDICE**

2. **Headache + ANY visual problems (blurry, unclear, distorted)?** → **MIGRAINE**
   - **CRITICAL**: Visual problems don't need to be "distortion" - blurry alone = migraine
   - Even with acid reflux/indigestion present = migraine
   - Visual PROBLEMS (blurry) + NO headache + fatigue + dizziness? → **DIABETES**

3. **Cough + breathing difficulty + EXPLICIT breathing difficulty mentioned + clear phlegm?** → **BRONCHIAL ASTHMA**
   - **Cough + breathing difficulty + NO explicit breathing difficulty + fever + COLORED/thick mucus + feeling sick?** → **PNEUMONIA**

4. **Fluid-filled blisters that are PAINFUL TO TOUCH (not "all over body")?** → **IMPETIGO**
   - Itchy rash (no fever mentioned) + NOT painful to touch? → **CHICKEN POX**

5. **Itchy rash WITHOUT fever mentioned?** → **CHICKEN POX** (NOT allergy)

6. **Rash + nausea + appetite loss + exhaustion WITHOUT metallic taste?** → **CHICKEN POX** (NOT drug reaction)

7. **"Bad taste" without "metallic" qualifier + itchy throat?** → **ALLERGY** (NOT drug reaction)

8. **"Metallic taste" + taste/smell changes + joint pain?** → **DRUG REACTION**

9. **Colored phlegm (green, yellow, brown, red) + cough + fever/feeling sick?** → **PNEUMONIA**

10. **Stuffy/runny nose + chest discomfort AT NIGHT + stiff neck?** → **ALLERGY**
    - **CRITICAL**: Night symptoms + stiff neck = allergy (trumps taste/smell loss)
    - Loss of taste/smell + NO night symptoms + NO lymph nodes? → **COMMON COLD**

11. **Neck pain + dizziness + balance issues?** → **CERVICAL SPONDYLOSIS**
    - **CRITICAL**: Neck + dizziness = cervical spondylosis regardless of cough/other symptoms

12. **Yellow honey-colored crusting + facial sores + fever?** → **IMPETIGO**
    - Rash + fever + SEVERE muscle/joint pain? → **DENGUE**
    - Rash + fever + APPETITE LOSS prominent? → **DRUG REACTION** (check for metallic taste first)

13. **Burning stomach + appetite loss + worse when eating?** → **PEPTIC ULCER**
    - Heartburn + worse lying down? → **GERD**
    - Belching + chest pain radiating to arm/jaw? → **GERD** (NOT hypertension)

14. **Joint pain + SWOLLEN JOINTS + walking difficulty?** → **ARTHRITIS**
    - Joint/muscle pain + weakness + nausea + NO swollen joints? → **DENGUE**

15. **Rash + spreading + color variation + nodules?** → **FUNGAL INFECTION**
    - Leg veins + skin changes near veins + cramps + NO fever? → **VARICOSE VEINS**

16. **Headache + chest pain + dizziness + concentration issues (no fever, no rash)?** → **HYPERTENSION**

17. **Stuffy nose + loss of taste/smell (no itchy symptoms)?** → **COMMON COLD**
    - Runny nose + ITCHY eyes/throat + sneezing (no fever)? → **ALLERGY**

18. **Extreme fatigue ONLY (no other symptoms)?** → **CHICKEN POX** (consider early presentation)

---

## FORMAT REQUIREMENTS

When providing diagnosis, use this EXACT format:
```
[DIAGNOSIS]diagnosis_name[/DIAGNOSIS]
```

Where diagnosis_name is lowercase:
- "migraine" not "Migraine"
- "gastroesophageal reflux disease" not "GERD"
- "bronchial asthma" not "Asthma"
- "urinary tract infection" not "UTI"

Common correct formats:
- [DIAGNOSIS]migraine[/DIAGNOSIS]
- [DIAGNOSIS]hypertension[/DIAGNOSIS]
- [DIAGNOSIS]bronchial asthma[/DIAGNOSIS]
- [DIAGNOSIS]urinary tract infection[/DIAGNOSIS]
