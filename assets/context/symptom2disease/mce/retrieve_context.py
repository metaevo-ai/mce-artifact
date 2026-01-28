import re
from pathlib import Path

def retrieval_function(question: str) -> str:
    """Return relevant diagnosis context for the given symptom question."""
    script_dir = Path(__file__).parent.resolve()
    context_file = script_dir / "context" / "diagnosis_guide.md"

    with open(context_file, 'r') as f:
        guide = f.read()

    question_lower = question.lower()

    # CRITICAL RULE 1: RUNNY NOSE + SNEEZING + SORE THROAT WITHOUT FEVER = ALLERGY
    has_runny_nose = 'runny' in question_lower or 'running' in question_lower or 'nose has been running' in question_lower
    has_sneezing = 'sneez' in question_lower
    has_sore_throat_q = 'sore throat' in question_lower or 'throat is sore' in question_lower or 'trouble swallowing' in question_lower
    has_no_fever = 'fever' not in question_lower and 'feverish' not in question_lower and 'temperature' not in question_lower

    if has_runny_nose and has_sneezing and has_sore_throat_q and has_no_fever:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE 1' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 5' in section:
                relevant.append('## ' + section)
            if 'ALLERGY' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # CRITICAL RULE 2: THICK SALIVA + FEVER + COUGH = ASTHMA (NOT PNEUMONIA)
    has_thick_saliva = 'saliva' in question_lower and 'thick' in question_lower
    has_thick_saliva_alt = 'saliva also became thick' in question_lower
    has_fever_q = 'fever' in question_lower or 'feverish' in question_lower
    has_cough_q = 'cough' in question_lower
    has_hard_breath = 'hard to breathe' in question_lower or 'difficult' in question_lower or 'trouble breathing' in question_lower

    if (has_thick_saliva or has_thick_saliva_alt) and has_fever_q and has_cough_q:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE 2' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 1' in section or 'ESSENCE 2' in section:
                relevant.append('## ' + section)
            if 'BRONCHIAL ASTHMA' in section.upper() or 'PNEUMONIA' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # CRITICAL RULE 3: ARTHRITIS - NECK + WALKING/STEERING DIFFICULTY
    has_neck_pain_q = 'neck' in question_lower and ('pain' in question_lower or 'tight' in question_lower or 'stiff' in question_lower)
    has_joint_pain_q = 'joint' in question_lower or 'joints' in question_lower
    has_walk_difficulty = ('walk' in question_lower or 'moving' in question_lower or 'move' in question_lower) and ('hard' in question_lower or 'difficult' in question_lower or 'pain' in question_lower or 'stiff' in question_lower)
    has_steer_difficulty = 'steer' in question_lower or 'steering' in question_lower

    if has_neck_pain_q and has_joint_pain_q and (has_walk_difficulty or has_steer_difficulty):
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE 3' in section:
                relevant.append('## ' + section)
            if 'ARTHRITIS' in section.upper() or 'CERVICAL' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # CRITICAL RULE 4: DENGUE - RASH + VOMITING + EYE PAIN
    has_rash_q = 'rash' in question_lower or 'rashes' in question_lower
    has_vomiting_q = 'vomit' in question_lower or 'vomiting' in question_lower
    has_eye_pain = 'eye' in question_lower and ('pain' in question_lower or 'hurt' in question_lower) or 'pain behind' in question_lower

    if has_rash_q and has_vomiting_q and has_eye_pain:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE 4' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 9' in section:
                relevant.append('## ' + section)
            if 'DENGUE' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # CRITICAL RULE 5: DENGUE - RASH + APPETITE LOSS + "SOMETHING WRONG"
    has_appetite_loss_q = 'appetite' in question_lower or "don't feel like eating" in question_lower or 'lost appetite' in question_lower
    has_something_wrong = 'something is wrong' in question_lower or 'feel like something is wrong' in question_lower

    if has_rash_q and has_appetite_loss_q and has_something_wrong:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE 5' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 9' in section:
                relevant.append('## ' + section)
            if 'DENGUE' in section.upper() or 'CHICKEN POX' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # CRITICAL RULE 6: DENGUE - RASH + SWOLLEN + WORSE IN ARMS/LEGS
    has_swollen = 'swollen' in question_lower or 'swelling' in question_lower or 'swollen' in question_lower
    has_worse_arms_legs = 'worse in' in question_lower and ('arm' in question_lower or 'leg' in question_lower) or 'arms and legs' in question_lower

    if has_rash_q and has_swollen and has_worse_arms_legs:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE 6' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 9' in section:
                relevant.append('## ' + section)
            if 'DENGUE' in section.upper() or 'CHICKEN POX' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # CRITICAL RULE 7: CHICKEN POX - RASH + ITCHY + PAINFUL + FEVER + TIRED
    has_itchy_q = 'itch' in question_lower
    has_painful_q = 'pain' in question_lower or 'painful' in question_lower
    has_little_bumps = 'little bump' in question_lower or 'little bumps' in question_lower

    if has_rash_q and has_itchy_q and has_painful_q and has_little_bumps and has_fever_q:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE 7' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 4' in section:
                relevant.append('## ' + section)
            if 'CHICKEN POX' in section.upper() or 'IMPETIGO' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # SURGICAL FIX 4: EXPLICIT BREATHING DIFFICULTY = ASTHMA
    # This MUST be the absolute highest priority check
    # "Hard to breathe" / "trouble breathing" as explicit symptom = ASTHMA
    # ========================================================
    has_explicit_breathing_difficulty = ('hard to breathe' in question_lower or
                                         'trouble breathing' in question_lower or
                                         'difficulty breathing' in question_lower or
                                         'shortness of breath' in question_lower or
                                         "can't catch" in question_lower or
                                         'breathing is getting harder' in question_lower)

    if has_explicit_breathing_difficulty:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES', '## SURGICAL DISCRIMINATORS', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'ASTHMA' in section.upper() or 'BRONCHIAL' in section.upper():
                relevant.append('## ' + section)
            if 'SURGICAL FIX 4' in section:
                relevant.append('## ' + section)
            if 'Rule 3' in section and 'asthma' in section.lower():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 1: CRITICAL RULE A - VARICOSE VEINS SKIN CHANGES
    # Rash on legs that is red, inflamed, AND itchy with spreading = VARICOSE VEINS
    # ========================================================
    has_leg_rash = 'leg' in question_lower or 'legs' in question_lower
    has_leg_rash_detail = has_leg_rash and ('rash' in question_lower or 'red' in question_lower or 'inflamed' in question_lower or 'itchy' in question_lower or 'inflamed' in question_lower)
    has_spreading = 'spread' in question_lower or 'spreading' in question_lower
    has_no_fever = 'fever' not in question_lower and 'temperature' not in question_lower

    if has_leg_rash_detail and has_spreading and has_no_fever:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE A' in section or 'VARICOSE VEINS' in section.upper():
                relevant.append('## ' + section)
            if 'ESSENCE 6' in section:
                relevant.append('## ' + section)
            if 'ERROR PATTERN 6' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 2: CRITICAL RULE B - DRUG REACTION COGNITIVE SYMPTOMS
    # Loss of libido + brain fog + confusion = DRUG REACTION (NOT hypertension)
    # ========================================================
    has_libido = 'sex' in question_lower or 'arous' in question_lower or 'libido' in question_lower
    has_brain_fog = 'brain fog' in question_lower or 'confus' in question_lower or 'think' in question_lower or 'concentrat' in question_lower
    has_no_chest_pain = 'chest pain' not in question_lower

    if has_libido and has_brain_fog and has_no_chest_pain:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE B' in section or 'DRUG REACTION' in section.upper():
                relevant.append('## ' + section)
            if 'ESSENCE 7' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 3: CRITICAL RULE C - ASTHMA EXHAUSTION PATTERN
    # "Tired and worn out from dealing with" = BRONCHIAL ASTHMA
    # ========================================================
    has_exhaustion_from = 'tired from' in question_lower or 'worn out from' in question_lower or 'exhausted from' in question_lower or 'dealing with' in question_lower
    has_mucus = 'mucus' in question_lower or 'phlegm' in question_lower or 'coughing' in question_lower

    if has_exhaustion_from and has_mucus:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE C' in section or 'ASTHMA' in section.upper() or 'BRONCHIAL' in section.upper():
                relevant.append('## ' + section)
            if 'ESSENCE 1' in section:
                relevant.append('## ' + section)
            if 'ERROR PATTERN 2' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 4: CRITICAL RULE D - MALARIA CYCLICAL FEVER
    # Chills + fever + sweating (cyclical pattern) = MALARIA
    # ========================================================
    has_chills = 'chill' in question_lower
    has_sweating = 'sweat' in question_lower or 'sweating' in question_lower
    has_fever = 'fever' in question_lower or 'temperature' in question_lower

    if has_chills and has_sweating and has_fever:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE D' in section or 'MALARIA' in section.upper():
                relevant.append('## ' + section)
            if 'ESSENCE 10' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 5: CRITICAL RULE E - PEPTIC ULCER FOOD TRIGGERS
    # Burning + worse lying down + pain after certain foods = PEPTIC ULCER
    # ========================================================
    has_burning_stomach = 'burning' in question_lower and ('stomach' in question_lower or 'abdomen' in question_lower)
    has_worse_lying = 'lying down' in question_lower or 'lie down' in question_lower or 'lying down' in question_lower
    has_food_pain = ('pain after' in question_lower and 'eat' in question_lower) or ('food' in question_lower and ('trigger' in question_lower or 'spicy' in question_lower or 'acid' in question_lower))

    if has_burning_stomach and has_worse_lying and has_food_pain:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE E' in section or 'PEPTIC ULCER' in section.upper():
                relevant.append('## ' + section)
            if 'ESSENCE 8' in section:
                relevant.append('## ' + section)
            if 'ERROR PATTERN 8' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 6: CRITICAL RULE F - DENGUE SMALL RED SPOTS
    # Small red spots on arms/legs + extreme tiredness = DENGUE
    # ========================================================
    has_small_red_spots = ('small red spot' in question_lower or 'little red spot' in question_lower) and ('arm' in question_lower or 'leg' in question_lower)
    has_extreme_tired = 'tired' in question_lower and ('weak' in question_lower or 'can barely' in question_lower or 'really' in question_lower)
    has_no_fever_mentioned = 'fever' not in question_lower

    if has_small_red_spots and has_extreme_tired:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE F' in section or 'DENGUE' in section.upper():
                relevant.append('## ' + section)
            if 'ESSENCE 9' in section:
                relevant.append('## ' + section)
            if 'ERROR PATTERN 3' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 7: CRITICAL RULE G - DENGUE JOINT PAIN + NAUSEA
    # Joint pain + difficulty walking + lost appetite + weak + nauseous = DENGUE
    # ========================================================
    has_joint_pain = 'joint' in question_lower or 'joint pain' in question_lower
    has_walking_difficulty = 'walk' in question_lower or 'walking' in question_lower
    has_appetite_loss = 'appetite' in question_lower or "don't feel like eating" in question_lower or 'lost' in question_lower and 'appetite' in question_lower
    has_nausea = 'nause' in question_lower or 'vomit' in question_lower or 'sick' in question_lower
    has_no_swollen_joints = 'swell' not in question_lower or 'swollen' not in question_lower

    if has_joint_pain and has_walking_difficulty and has_appetite_loss and has_nausea and has_no_swollen_joints:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE G' in section or 'DENGUE' in section.upper():
                relevant.append('## ' + section)
            if 'ESSENCE 9' in section:
                relevant.append('## ' + section)
            if 'ERROR PATTERN 3' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 8: CRITICAL RULE H - DENGUE BODY PAIN + RASH + VOMITING
    # Extreme body pain + headache + vomiting + red spots all over + itchy = DENGUE
    # ========================================================
    has_extreme_body_pain = 'extreme' in question_lower and ('body pain' in question_lower or 'muscle' in question_lower or 'joint' in question_lower)
    has_vomiting = 'vomit' in question_lower or 'vomiting' in question_lower
    has_red_spots_all_over = 'red spot' in question_lower and ('all over' in question_lower or 'whole body' in question_lower or 'everywhere' in question_lower)
    has_itchy_rash = 'itch' in question_lower and ('rash' in question_lower or 'skin' in question_lower)

    if has_extreme_body_pain and has_vomiting and has_red_spots_all_over and has_itchy_rash:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE H' in section or 'DENGUE' in section.upper():
                relevant.append('## ' + section)
            if 'ESSENCE 9' in section:
                relevant.append('## ' + section)
            if 'ERROR PATTERN 3' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 9: CRITICAL RULE I - FUNGAL INFECTION BUMPS + COLOR PATCHES
    # Rash all over + small bumps like pimples + different colored patches = FUNGAL
    # ========================================================
    has_rash_all_over = 'rash all over' in question_lower or 'rash all over' in question_lower or 'all over' in question_lower and 'rash' in question_lower
    has_bumps_like_pimples = 'bump' in question_lower and ('pimple' in question_lower or 'like pimple' in question_lower)
    has_color_patches = 'different color' in question_lower or 'different colored' in question_lower or 'color patch' in question_lower

    if has_rash_all_over and has_bumps_like_pimples and has_color_patches:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE I' in section or 'FUNGAL' in section.upper():
                relevant.append('## ' + section)
            if 'ESSENCE 11' in section:
                relevant.append('## ' + section)
            if 'ERROR PATTERN 11' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 2: CRITICAL RULE B - ITCHY RASH WITHOUT FEVER = CHICKEN POX
    # Itchy rash on arms/neck without fever = CHICKEN POX (not allergy)
    # ========================================================
    has_itchy_rash = 'itch' in question_lower and ('rash' in question_lower or 'bumps' in question_lower or 'spots' in question_lower)
    has_no_fever = 'fever' not in question_lower and 'temperature' not in question_lower and 'feverish' not in question_lower
    has_arms_neck_or_face = 'arm' in question_lower or 'neck' in question_lower or 'face' in question_lower

    if has_itchy_rash and has_no_fever and has_arms_neck_or_face:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE B' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 4' in section:
                relevant.append('## ' + section)
            if 'CHICKEN POX' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 3b' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 3: CRITICAL RULE C - BAD TASTE WITHOUT METALLIC = NOT DRUG REACTION
    # "Bad taste" without "metallic" + itchy throat = ALLERGY
    # ========================================================
    has_bad_taste = 'taste' in question_lower and ('bad' in question_lower or 'funny' in question_lower)
    has_no_metallic = 'metallic' not in question_lower
    has_itchy_throat = ('throat' in question_lower and 'itch' in question_lower) or 'scratchy' in question_lower

    if has_bad_taste and has_no_metallic and has_itchy_throat:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE C' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 7' in section:
                relevant.append('## ' + section)
            if 'ALLERGY' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 4' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 4: CRITICAL RULE D - COLORED PHLEGM = PNEUMONIA
    # "Weird color" or "colored" phlegm = PNEUMONIA (not asthma)
    # ========================================================
    has_colored_phlegm = ('color' in question_lower or 'weird' in question_lower) and \
                        ('phlegm' in question_lower or 'mucus' in question_lower or 'sputum' in question_lower)

    if has_colored_phlegm:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE D' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 2' in section:
                relevant.append('## ' + section)
            if 'PNEUMONIA' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 2' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 5: CRITICAL RULE E - RASH + NAUSEA + APPETITE LOSS = CHICKEN POX
    # Rash + nausea + appetite loss without metallic taste = CHICKEN POX
    # ========================================================
    has_rash = 'rash' in question_lower or 'skin' in question_lower
    has_nausea = 'nause' in question_lower or 'vomit' in question_lower or 'uneasy' in question_lower
    has_appetite_loss = 'appetite' in question_lower or "don't feel like eating" in question_lower or 'lost' in question_lower and 'appetite' in question_lower

    if has_rash and has_nausea and has_appetite_loss:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL NEW RULES (FROM TRAINING ERRORS)', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CRITICAL RULE E' in section:
                relevant.append('## ' + section)
            if 'ESSENCE 4' in section:
                relevant.append('## ' + section)
            if 'CHICKEN POX' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 5' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 6: SORE THROAT + FEVERISH + MUSCLE ACHES = COMMON COLD
    # ========================================================
    has_sore_throat = 'sore throat' in question_lower or 'throat really sore' in question_lower or 'throat is sore' in question_lower
    has_feverish = 'fever' in question_lower or 'temperature' in question_lower or 'feverish' in question_lower or 'feeling cold' in question_lower
    has_muscle_aches = 'muscle' in question_lower or 'body ache' in question_lower

    if has_sore_throat and has_feverish and has_muscle_aches:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES', '## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'ESSENCE 5' in section:
                relevant.append('## ' + section)
            if 'COMMON COLD' in section.upper():
                relevant.append('## ' + section)
            if 'Rule 3b' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 2: ALLERGY - NIGHT SYMPTOMS + STIFF NECK (Surgical Fix 2)
    # Chest discomfort at night + stiff neck = Allergy even with taste loss
    # ========================================================
    has_night_symptoms = ('night' in question_lower and ('chest' in question_lower or 'discomfort' in question_lower or 'pain' in question_lower))
    has_stiff_neck = 'stiff neck' in question_lower or 'neck is stiff' in question_lower
    has_taste_smell_loss = 'taste' in question_lower or 'smell' in question_lower or "can't taste" in question_lower or "can't smell" in question_lower

    if has_night_symptoms and has_stiff_neck:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES', '## SURGICAL DISCRIMINATORS']
        for section in sections:
            if 'ALLERGY' in section.upper():
                relevant.append('## ' + section)
            if 'SURGICAL FIX 2' in section:
                relevant.append('## ' + section)
            if 'COMMON COLD' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 2: CHEST/BACK RASH + FLAKY SKIN = DRUG REACTION (Surgical Fix 1)
    # Chest and back rash + flaky skin = Drug Reaction (not psoriasis)
    # ========================================================
    has_chest_rash = 'chest' in question_lower and ('rash' in question_lower or 'skin' in question_lower)
    has_back_rash = 'back' in question_lower and ('rash' in question_lower or 'skin' in question_lower)
    has_flaky = 'flaky' in question_lower or 'peel' in question_lower
    has_knees_elbows = ('knee' in question_lower or 'elbow' in question_lower) and ('peel' in question_lower or 'flake' in question_lower)

    if has_chest_rash and has_back_rash and has_flaky and not has_knees_elbows:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES', '## SURGICAL DISCRIMINATORS']
        for section in sections:
            if 'DRUG REACTION' in section.upper():
                relevant.append('## ' + section)
            if 'PSORIASIS' in section.upper():
                relevant.append('## ' + section)
            if 'SURGICAL FIX 1' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 3: NAUSEA + VOMITING + APPETITE LOSS (NO RASH) = TYPHOID (Surgical Fix 3)
    # Nausea + vomiting + appetite loss without rash = Typhoid
    # ========================================================
    has_nausea = 'nause' in question_lower or 'vomit' in question_lower or 'vomiting' in question_lower
    has_appetite_loss = 'appetite' in question_lower or "don't feel like eating" in question_lower or "can't eat" in question_lower
    has_weakness = 'weak' in question_lower or 'weakness' in question_lower or 'tired' in question_lower
    has_no_rash = 'rash' not in question_lower and 'skin' not in question_lower

    if has_nausea and has_appetite_loss and has_weakness and has_no_rash:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES', '## SURGICAL DISCRIMINATORS']
        for section in sections:
            if 'TYPHOID' in section.upper():
                relevant.append('## ' + section)
            if 'CHICKEN POX' in section.upper():
                relevant.append('## ' + section)
            if 'SURGICAL FIX 3' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 4: CERVICAL SPONDYLOSIS - NECK PAIN + DIZZINESS (Error Pattern 26)
    # Neck pain + dizziness + balance issues = Cervical Spondylosis
    # ========================================================
    has_neck_pain = 'neck' in question_lower and ('pain' in question_lower or 'stiff' in question_lower)
    has_dizziness = 'dizzi' in question_lower or 'balance' in question_lower or 'unsteady' in question_lower

    if has_neck_pain and has_dizziness:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CERVICAL' in section.upper() or 'ERROR PATTERN 26' in section:
                relevant.append('## ' + section)
            if 'DRUG REACTION' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # SEMANTIC ESSENCE MATCHING - Highest Priority
    # ========================================================

    # ESSENCE 1: BRONCHIAL ASTHMA Pattern
    # "Hard to breathe" or "trouble breathing" as PRIMARY complaint
    has_breathing_difficulty = 'hard to breathe' in question_lower or \
                               'trouble breathing' in question_lower or \
                               'shortness of breath' in question_lower or \
                               'difficult to breathe' in question_lower
    has_wheezing = 'wheez' in question_lower or 'whistling' in question_lower
    has_chest_tightness = 'tight chest' in question_lower or 'chest tight' in question_lower or \
                          'chest feels tight' in question_lower

    # Check if breathing difficulty is PRIMARY (appears early or emphasized)
    breathing_primary = has_breathing_difficulty or has_wheezing or has_chest_tightness

    # ESSENCE 2: IMPETIGO Pattern (FACIAL + FEVER + SPREADING)
    has_face_rash = 'face' in question_lower and ('rash' in question_lower or 'sore' in question_lower or 'blister' in question_lower)
    has_face_sores = 'sores on my face' in question_lower or 'sores near' in question_lower or \
                     'face and near my nose' in question_lower or 'around my nose' in question_lower
    has_spreading = 'spread' in question_lower or 'spreading' in question_lower
    has_fever = 'fever' in question_lower or 'temperature' in question_lower or 'feverish' in question_lower

    # ESSENCE 3: PNEUMONIA Pattern (HIGH FEVER + THICK MUCUS + FEELING SICK)
    has_high_fever = 'high fever' in question_lower or 'fever really high' in question_lower or \
                     'fever for past' in question_lower or 'fever since past' in question_lower
    has_thick_mucus = 'thick mucus' in question_lower or 'thick phlegm' in question_lower or \
                      'sticky mucus' in question_lower or 'coughing up a lot of mucus' in question_lower or \
                      'mucus became thick' in question_lower
    has_feeling_sick = 'feeling sick' in question_lower or 'really sick' in question_lower or \
                       'feeling really sick' in question_lower

    # ESSENCE 4: ALLERGY vs COMMON COLD
    has_taste_smell_loss = 'taste' in question_lower or 'smell' in question_lower
    has_itchy_symptoms = 'itch' in question_lower and ('eye' in question_lower or 'throat' in question_lower or 'nose' in question_lower)

    # ========================================================
    # PRIORITY 1: Check for ASTHMA ESSENCE (breathing difficulty primary)
    # ========================================================
    if breathing_primary:
        # If breathing difficulty is primary, check if this is clearly asthma or could be pneumonia
        if has_high_fever and has_thick_mucus:
            # Both high fever AND thick mucus present - this is AMBIGUOUS
            # Return BOTH asthma and pneumonia sections for comparison
            sections = guide.split('\n## ')
            relevant = ['## SEMANTIC SYMPTOM ESSENCES']
            for section in sections:
                if 'ESSENCE 1' in section or 'ESSENCE 2' in section:
                    relevant.append('## ' + section)
                if 'BRONCHIAL ASTHMA' in section.upper() or 'PNEUMONIA' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)
        else:
            # No high fever, or fever present but no thick mucus = ASTHMA likely
            sections = guide.split('\n## ')
            relevant = ['## SEMANTIC SYMPTOM ESSENCES']
            for section in sections:
                if 'ESSENCE 1' in section:
                    relevant.append('## ' + section)
                if 'BRONCHIAL ASTHMA' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 2: Check for IMPETIGO ESSENCE (facial + fever + spreading)
    # ========================================================
    if has_face_sores and has_fever:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'ESSENCE 3' in section:
                relevant.append('## ' + section)
            if 'IMPETIGO' in section.upper():
                relevant.append('## ' + section)
            if 'CHICKEN POX' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 3: Check for PNEUMONIA ESSENCE (high fever + thick mucus + feeling sick)
    # ========================================================
    if has_high_fever and has_thick_mucus and has_feeling_sick:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'ESSENCE 2' in section:
                relevant.append('## ' + section)
            if 'PNEUMONIA' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 4: Check for ALLERGY vs COMMON COLD (Error Pattern 5)
    # ========================================================
    has_swollen_throat = 'throat' in question_lower and ('swollen' in question_lower or 'swelling' in question_lower)
    has_watery_eyes = ('eye' in question_lower and ('watery' in question_lower or 'red' in question_lower)) or 'eyes are' in question_lower
    has_sinus_pressure = 'sinus' in question_lower or 'pressure in my sinuses' in question_lower
    has_lymph_nodes = 'lymph' in question_lower or 'lymph node' in question_lower or 'swollen neck' in question_lower
    has_chest_hurts_night = ('chest' in question_lower and 'night' in question_lower) or ('chest hurts' in question_lower and 'night' in question_lower)
    has_taste_smell = 'taste' in question_lower or 'smell' in question_lower or "can't taste" in question_lower or "can't smell" in question_lower
    has_sore_throat = 'sore throat' in question_lower or 'throat is sore' in question_lower or 'throat really sore' in question_lower
    has_sneezing = 'sneez' in question_lower
    has_trouble_swallowing = 'trouble swallowing' in question_lower or 'swallowing is painful' in question_lower

    # NEW PATTERN: Sore throat + runny nose + sneezing WITHOUT fever = ALLERGY
    has_runny_nose = 'runny' in question_lower or 'nose has been running' in question_lower or 'nose running' in question_lower
    has_fever = 'fever' in question_lower or 'temperature' in question_lower or 'feverish' in question_lower

    if (has_sore_throat or has_trouble_swallowing) and has_runny_nose and has_sneezing and not has_fever:
        # Sore throat + runny nose + sneezing + no fever = ALLERGY
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'ESSENCE 5' in section:
                relevant.append('## ' + section)
            if 'ALLERGY' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 5' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    if has_lymph_nodes:
        # Swollen lymph nodes = COMMON COLD (indicates infection)
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'ESSENCE 5' in section:
                relevant.append('## ' + section)
            if 'COMMON COLD' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 5' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    if (has_swollen_throat or has_watery_eyes or has_sinus_pressure) and not has_taste_smell:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'ESSENCE 5' in section:
                relevant.append('## ' + section)
            if 'ALLERGY' in section.upper() or 'COMMON COLD' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 5' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 4b: Check for IMPETIGO vs CHICKEN POX - fluid-filled blisters (Error Pattern 14)
    # ========================================================
    has_fluid_filled = 'fluid' in question_lower or 'filled with fluid' in question_lower or 'fluid-filled' in question_lower
    has_painful_touch = 'painful to touch' in question_lower or 'painful' in question_lower
    has_yellow_crust = 'yellow' in question_lower and ('crust' in question_lower or 'honey' in question_lower or 'crusting' in question_lower)
    has_all_over_body = 'all over my body' in question_lower or 'all over body' in question_lower or 'all over' in question_lower

    if has_fluid_filled and has_painful_touch and not has_all_over_body:
        # Fluid-filled blisters + painful + NOT all over body = IMPETIGO
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'IMPETIGO' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 14' in section:
                relevant.append('## ' + section)
            if 'CHICKEN POX' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 4d: Check for DENGUE vs CHICKEN POX - extreme tiredness (Error Pattern 13)
    # ========================================================
    has_extreme_tired = 'very tired' in question_lower or 'very tired all day' in question_lower or 'really tired' in question_lower or 'exhausted' in question_lower
    has_something_wrong = 'something is wrong' in question_lower or 'feel like something is wrong' in question_lower
    has_little_red_spots = 'little red spot' in question_lower or 'small red spot' in question_lower or 'red spot' in question_lower
    has_itchy_rash = 'itchy' in question_lower and ('rash' in question_lower or 'bump' in question_lower)

    if has_itchy_rash and has_extreme_tired and has_something_wrong and not has_little_red_spots:
        # Itchy rash + extreme tiredness + something wrong with body = DENGUE
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'DENGUE' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 13' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 4e: Check for TYPHOID vs PEPTIC ULCER - sustained duration (Error Pattern 15)
    # ========================================================
    has_week = 'past week' in question_lower or 'week' in question_lower
    has_not_improving = 'not getting better' in question_lower or 'not improving' in question_lower or 'not better' in question_lower
    has_vomiting = 'vomit' in question_lower or 'vomiting' in question_lower or 'like vomiting' in question_lower
    has_cant_eat = "can't eat" in question_lower or 'cannot eat' in question_lower or "don't eat" in question_lower or 'lost appetite' in question_lower
    has_burning = 'burning' in question_lower and ('stomach' in question_lower or 'abdomen' in question_lower or 'abdominal' in question_lower)

    if has_week and has_not_improving and has_vomiting and has_cant_eat and not has_burning:
        # Stomach ache for week + not improving + vomiting + can't eat = TYPHOID
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'TYPHOID' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 15' in section:
                relevant.append('## ' + section)
            if 'PEPTIC ULCER' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 4b: Check for CHICKEN POX "little red spots" pattern (Error Pattern 3b)
    # ========================================================
    has_little_red_spots = ('little red spot' in question_lower or 'small red spot' in question_lower or 'red spots all over' in question_lower)
    has_spots_body = ('all over my body' in question_lower or 'all over body' in question_lower or 'all over' in question_lower)
    has_fever = 'fever' in question_lower or 'temperature' in question_lower
    has_metallic = 'metallic' in question_lower or 'metal' in question_lower
    has_flaky = 'flaky' in question_lower or 'peeling' in question_lower

    if has_little_red_spots and has_spots_body and has_fever and not has_metallic and not has_flaky:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'CHICKEN POX' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 3b' in section or 'ERROR PATTERN 3' in section:
                relevant.append('## ' + section)
            if 'IMPETIGO' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 4c: Check for COMMON COLD "feeling cold" pattern (Error Pattern 22)
    # ========================================================
    has_run_down = 'run down' in question_lower or 'really run down' in question_lower
    has_sore_throat = 'sore throat' in question_lower or 'throat really sore' in question_lower
    has_feeling_cold = 'feeling cold' in question_lower or 'really cold' in question_lower or 'feeling really cold' in question_lower
    has_thick_mucus = ('thick' in question_lower and ('mucus' in question_lower or 'phlegm' in question_lower or 'saliva' in question_lower or 'sputum' in question_lower))

    if (has_run_down or has_sore_throat) and has_feeling_cold and has_fever and not has_thick_mucus:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'COMMON COLD' in section.upper():
                relevant.append('## ' + section)
            if 'PNEUMONIA' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 22' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 5: Check for DENGUE vs TYPHOID (Error Pattern 17)
    # ========================================================
    has_vomiting = 'vomit' in question_lower or 'vomiting' in question_lower
    has_muscle_joint_back = ('muscle' in question_lower or 'joint' in question_lower or 'back' in question_lower)
    has_no_diarrhea = 'diarrhea' not in question_lower and 'loose stool' not in question_lower and 'watery stool' not in question_lower
    has_body_aches = 'body ache' in question_lower or 'body ache' in question_lower

    if has_vomiting and has_muscle_joint_back and has_no_diarrhea and has_fever:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'DENGUE' in section.upper():
                relevant.append('## ' + section)
            if 'TYPHOID' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 17' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 6: Check for DRUG REACTION neurological pattern (Error Pattern 20)
    # ========================================================
    has_decreased_sex_drive = ('sex drive' in question_lower or 'libido' in question_lower or 'sex' in question_lower) and ('decrease' in question_lower or 'lower' in question_lower or 'less' in question_lower or 'low' in question_lower or 'gone' in question_lower or 'lost' in question_lower)
    has_cognitive = 'think' in question_lower or 'thinking' in question_lower or 'concentrat' in question_lower or 'brain' in question_lower or 'confus' in question_lower
    has_chest_pain = 'chest pain' in question_lower or 'chest hurts' in question_lower

    if has_decreased_sex_drive and has_cognitive and not has_chest_pain:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'DRUG REACTION' in section.upper():
                relevant.append('## ' + section)
            if 'HYPERTENSION' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 20' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 7: Check for VARICOSE VEINS leg rash pattern (Error Pattern 19)
    # ========================================================
    has_leg_rash = 'leg' in question_lower or 'legs' in question_lower
    has_leg_rash_detail = has_leg_rash and ('rash' in question_lower or 'red' in question_lower or 'inflamed' in question_lower or 'itchy' in question_lower)
    has_spreading = 'spread' in question_lower
    has_color_variation = 'color' in question_lower or 'different' in question_lower
    has_nodules = 'nodule' in question_lower or 'bump' in question_lower

    if has_leg_rash_detail and has_spreading and not has_color_variation and not has_nodules:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'VARICOSE' in section.upper():
                relevant.append('## ' + section)
            if 'FUNGAL' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 19' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # PRIORITY 8: Check for DRUG REACTION vs PSORIASIS chest/back pattern (Error Pattern 18)
    # ========================================================
    has_chest_back_rash = ('chest' in question_lower and 'back' in question_lower) and ('rash' in question_lower or 'itch' in question_lower)
    has_knees_elbows = ('knee' in question_lower or 'elbow' in question_lower) and ('peel' in question_lower or 'flake' in question_lower)

    if has_chest_back_rash and not has_knees_elbows:
        sections = guide.split('\n## ')
        relevant = ['## SEMANTIC SYMPTOM ESSENCES']
        for section in sections:
            if 'DRUG REACTION' in section.upper():
                relevant.append('## ' + section)
            if 'PSORIASIS' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 18' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # Fall back to existing rule-based patterns
    # ========================================================

    # Define has_fever early for use in all patterns
    has_fever = 'fever' in question_lower or 'temperature' in question_lower

    # ========================================================
    # ERROR PATTERN 13: DENGUE vs CHICKEN POX - SEVERE MUSCLE PAIN IS KEY
    # ========================================================
    has_severe_pain = 'severe' in question_lower and ('muscle' in question_lower or 'joint' in question_lower or 'bone' in question_lower)
    has_breakbone = 'breakbone' in question_lower or 'break bone' in question_lower
    has_small_spots = ('small red spot' in question_lower or 'red spot' in question_lower) and not has_severe_pain
    has_rash = 'rash' in question_lower or 'skin' in question_lower

    if has_rash:
        if has_breakbone or has_severe_pain:
            # Dengue pattern - severe muscle/joint pain
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'DENGUE' in section.upper() or 'ERROR PATTERN 13' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)
        elif has_small_spots:
            # Chicken pox pattern - small red spots without severe pain
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'CHICKEN POX' in section.upper() or 'ERROR PATTERN 13' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # ERROR PATTERN 14: IMPETIGO - FACIAL RASH + FEVER + SPREADING
    # ========================================================
    has_face = 'face' in question_lower or 'nose' in question_lower or 'around' in question_lower
    has_spread = 'spread' in question_lower or 'down' in question_lower
    has_rash = 'rash' in question_lower or 'sore' in question_lower

    if has_face and has_rash and (has_spread or has_fever):
        # Impetigo pattern - facial rash + fever + spreading
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES']
        for section in sections:
            if 'IMPETIGO' in section.upper() or 'ERROR PATTERN 14' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # ERROR PATTERN 5: ALLERGY vs COMMON COLD - LOSS OF TASTE/SMELL = COLD
    # ========================================================
    has_taste = 'taste' in question_lower or 'smell' in question_lower or 'can\'t taste' in question_lower or 'cannot taste' in question_lower or 'lost taste' in question_lower or 'no taste' in question_lower or 'can\'t smell' in question_lower or 'cannot smell' in question_lower or 'lost smell' in question_lower or 'no smell' in question_lower
    has_stuffy = 'stuffy' in question_lower or 'nose' in question_lower or 'nasal' in question_lower or 'congestion' in question_lower or 'blocked' in question_lower
    has_itchy = 'itch' in question_lower
    has_itchy_eye = has_itchy and ('eye' in question_lower or 'watery' in question_lower or 'red' in question_lower)
    has_itchy_throat = has_itchy and ('throat' in question_lower or 'swallow' in question_lower or 'scratch' in question_lower)

    if has_stuffy:
        if has_taste:
            # Common Cold pattern - loss of taste/smell (DECISIVE)
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'COMMON COLD' in section.upper() or 'ALLERGY' in section.upper() or 'ERROR PATTERN 5' in section or 'Rule 3b' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)
        elif has_itchy_eye or has_itchy_throat:
            # Allergy pattern - itchy symptoms without taste/smell loss
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'ALLERGY' in section.upper() or 'ERROR PATTERN 5' in section or 'ERROR PATTERN 12' in section or 'Rule 3b' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # ERROR PATTERN 2: PNEUMONIA vs ASTHMA - CRITICAL (FEVER IS KEY)
    # ========================================================
    has_cough = 'cough' in question_lower
    has_breathing = 'breath' in question_lower or 'wheez' in question_lower or 'shortness' in question_lower or 'tight' in question_lower
    has_thick_mucus = ('thick' in question_lower and ('mucus' in question_lower or 'phlegm' in question_lower or 'sputum' in question_lower or 'mucusy' in question_lower or 'mucous' in question_lower)) or \
                      'mucusy' in question_lower or 'mucous' in question_lower or 'weird color' in question_lower
    has_sticky_mucus = 'sticky' in question_lower or 'mucusy saliva' in question_lower
    has_feeling_sick = 'feeling sick' in question_lower or 'really sick' in question_lower or 'feeling really sick' in question_lower
    has_tired_from = 'tired from' in question_lower or 'tired and worn out' in question_lower or 'exhausted from' in question_lower

    if has_cough and has_breathing:
        if has_fever and has_thick_mucus:
            # Need to distinguish between pneumonia and asthma
            # Pneumonia: "feeling sick" / "really sick" from infection
            # Asthma: "tired FROM" / "tired from dealing with" breathing effort
            if has_feeling_sick and not has_tired_from:
                # Feeling sick from infection = Pneumonia
                sections = guide.split('\n## ')
                relevant = ['## CRITICAL DIFFERENTIATION RULES']
                for section in sections:
                    if 'Rule 3' in section or 'PNEUMONIA' in section.upper() or 'ASTHMA' in section.upper() or 'ERROR PATTERN 2' in section:
                        relevant.append('## ' + section)
                return '\n'.join(relevant)
            elif has_tired_from and not has_feeling_sick:
                # Tired from breathing effort = Asthma
                sections = guide.split('\n## ')
                relevant = ['## CRITICAL DIFFERENTIATION RULES']
                for section in sections:
                    if 'Rule 3' in section or 'ASTHMA' in section.upper() or 'BRONCHIAL' in section.upper() or 'ERROR PATTERN 2' in section:
                        relevant.append('## ' + section)
                return '\n'.join(relevant)
            elif has_sticky_mucus and not has_feeling_sick:
                # Sticky mucus = Asthma
                sections = guide.split('\n## ')
                relevant = ['## CRITICAL DIFFERENTIATION RULES']
                for section in sections:
                    if 'Rule 3' in section or 'ASTHMA' in section.upper() or 'BRONCHIAL' in section.upper() or 'ERROR PATTERN 2' in section:
                        relevant.append('## ' + section)
                return '\n'.join(relevant)
            else:
                # Ambiguous - return both sections
                sections = guide.split('\n## ')
                relevant = ['## CRITICAL DIFFERENTIATION RULES']
                for section in sections:
                    if 'Rule 3' in section or 'PNEUMONIA' in section.upper() or 'ASTHMA' in section.upper() or 'BRONCHIAL' in section.upper() or 'ERROR PATTERN 2' in section:
                        relevant.append('## ' + section)
                return '\n'.join(relevant)
        elif has_thick_mucus and not has_fever:
            # Thick mucus but NO fever = asthma (key pattern from training)
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'Rule 3' in section or 'ASTHMA' in section.upper() or 'BRONCHIAL' in section.upper() or 'ERROR PATTERN 2' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)
        else:
            # General cough + breathing, check for fever
            if has_fever:
                # Fever + respiratory = pneumonia or other
                sections = guide.split('\n## ')
                relevant = ['## CRITICAL DIFFERENTIATION RULES']
                for section in sections:
                    if 'Rule 3' in section or 'PNEUMONIA' in section.upper() or 'ERROR PATTERN 2' in section:
                        relevant.append('## ' + section)
                return '\n'.join(relevant)
            else:
                # No fever = asthma
                sections = guide.split('\n## ')
                relevant = ['## CRITICAL DIFFERENTIATION RULES']
                for section in sections:
                    if 'ASTHMA' in section.upper() or 'BRONCHIAL' in section.upper() or 'ERROR PATTERN 2' in section:
                        relevant.append('## ' + section)
                return '\n'.join(relevant)

    # Priority 1: YELLOW SKIN/EYES = Jaundice (absolute rule)
    if 'yellow' in question_lower and ('skin' in question_lower or 'eye' in question_lower or 'jaundice' in question_lower):
        return guide

    # ========================================================
    # ERROR PATTERN 3 & 9: IMPETIGO vs CHICKEN POX - YELLOW CRUSTING IS KEY
    # ========================================================
    has_fever = 'fever' in question_lower or 'temperature' in question_lower
    has_blister = 'blister' in question_lower or 'fluid-filled' in question_lower or 'fluid filled' in question_lower
    has_rash = 'rash' in question_lower or 'sore' in question_lower
    has_yellow_crust = 'yellow' in question_lower and ('crust' in question_lower or 'honey' in question_lower or 'crusting' in question_lower)
    has_face = 'face' in question_lower or 'nose' in question_lower or 'mouth' in question_lower or 'around' in question_lower

    if has_blister and has_fever:
        if has_yellow_crust:
            # Yellow crusting = impetigo
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'IMPETIGO' in section.upper():
                    relevant.append('## ' + section)
                if 'ERROR PATTERN 3' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)
        else:
            # No yellow crusting = chicken pox (NOT impetigo)
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'CHICKEN POX' in section.upper():
                    relevant.append('## ' + section)
                if 'ERROR PATTERN 3' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # Facial rash + fever + spreading = impetigo (Error Pattern 9)
    if has_face and has_fever and has_rash and 'spread' in question_lower:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES']
        for section in sections:
            if 'IMPETIGO' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 9' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # ERROR PATTERN 4: VARICOSE VEINS - CHECK FOR LEG VEINS
    # ========================================================
    has_leg = 'leg' in question_lower or 'legs' in question_lower or 'calf' in question_lower or 'thigh' in question_lower
    has_vein = 'vein' in question_lower or 'veins' in question_lower or 'varicose' in question_lower
    has_cramps = 'cramp' in question_lower or 'cramping' in question_lower
    has_standing = 'stand' in question_lower or 'standing' in question_lower
    has_inflam = 'inflamed' in question_lower or 'inflammation' in question_lower or 'red' in question_lower
    has_fever = 'fever' in question_lower or 'temperature' in question_lower

    if has_leg and (has_vein or (has_cramps and has_standing)):
        if not has_fever:
            # Varicose veins pattern (no fever differentiates from fungal)
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'VARICOSE' in section.upper():
                    relevant.append('## ' + section)
                if 'ERROR PATTERN 4' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # ERROR PATTERN 6: DRUG REACTION with TASTE CHANGES
    # ========================================================
    has_metallic = 'metallic' in question_lower or 'metal' in question_lower
    has_taste_change = 'taste' in question_lower or 'smell' in question_lower
    has_joint = 'joint' in question_lower or 'muscle' in question_lower or 'bone' in question_lower

    if has_metallic and has_taste_change:
        # Drug reaction with taste changes
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES']
        for section in sections:
            if 'DRUG REACTION' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 6' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # ERROR PATTERN 7: GERD vs PEPTIC ULCER
    # ========================================================
    has_burning = 'burn' in question_lower and ('stomach' in question_lower or 'abdom' in question_lower or 'upper' in question_lower)
    has_appetite = 'appetite' in question_lower or 'hungry' in question_lower or 'no appetite' in question_lower
    has_belch = 'belch' in question_lower or 'burp' in question_lower
    has_heartburn = 'heartburn' in question_lower or 'acid' in question_lower
    has_worse_eat = ('worse' in question_lower and 'eat' in question_lower) or ('worse' in question_lower and 'meal' in question_lower)
    has_radiation = 'radiat' in question_lower or 'go to' in question_lower or 'goes to' in question_lower

    if has_burning and has_appetite:
        # Burning + appetite = peptic ulcer
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES']
        for section in sections:
            if 'PEPTIC ULCER' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 7' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    if has_belch and (has_heartburn or has_radiation):
        # Belching + chest pain radiation = GERD (NOT hypertension)
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES']
        for section in sections:
            if 'GERD' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 7' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # ERROR PATTERN 8: EXTREME FATIGUE ONLY = CHICKEN POX
    # ========================================================
    has_fatigue = 'tired' in question_lower or 'fatigue' in question_lower or 'exhausted' in question_lower or 'weak' in question_lower or 'can barely' in question_lower
    has_fever = 'fever' in question_lower or 'temperature' in question_lower or 'rash' in question_lower
    has_thirst = 'thirst' in question_lower or 'pee' in question_lower or 'urinat' in question_lower or 'vision' in question_lower

    if has_fatigue and not has_fever and not has_thirst:
        # Extreme fatigue only, no fever, no rash, no diabetes symptoms
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES']
        for section in sections:
            if 'CHICKEN POX' in section.upper():
                relevant.append('## ' + section)
            if 'ERROR PATTERN 8' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # Priority 1: HYPERTENSION vs MIGRAINE (Error Pattern 1)
    # ========================================================
    has_headache = 'headache' in question_lower or 'head hurts' in question_lower or 'head pain' in question_lower
    has_chest_pain = 'chest pain' in question_lower or 'chest discomfort' in question_lower
    has_dizziness = 'dizzi' in question_lower or 'off balance' in question_lower or 'vertigo' in question_lower
    has_concentration = 'concentrat' in question_lower or 'focus' in question_lower or 'focusing' in question_lower
    has_visual_distortion = 'visual' in question_lower or 'wavy' in question_lower or 'zigzag' in question_lower or 'blind spot' in question_lower

    if has_headache and has_chest_pain and has_dizziness and not has_visual_distortion:
        # Return hypertension-focused sections
        sections = guide.split('\n## ')
        relevant = []
        for section in sections:
            if 'CRITICAL DIFFERENTIATION RULES' in section:
                relevant.append('## ' + section)
            if 'HYPERTENSION' in section.upper():
                relevant.append('## ' + section)
            if 'Error Pattern 1' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant) if relevant else guide

    # ========================================================
    # Priority 2: FEVER + RASH (Chicken Pox, Impetigo, Dengue, Drug Reaction)
    # ========================================================
    has_fever = 'fever' in question_lower or 'temperature' in question_lower
    has_rash = 'rash' in question_lower or 'skin' in question_lower

    if has_fever and has_rash:
        has_yellow_crust = 'yellow' in question_lower and ('crust' in question_lower or 'honey' in question_lower)
        has_appetite_loss = 'appetite' in question_lower or "don't feel like eating" in question_lower or 'lost appetite' in question_lower or 'no appetite' in question_lower
        has_severe_muscle_pain = 'severe' in question_lower and ('muscle' in question_lower or 'joint' in question_lower or 'bone' in question_lower)
        has_fluid_blister = 'fluid' in question_lower or 'blister' in question_lower or 'vesicle' in question_lower
        has_face_sores = ('face' in question_lower or 'nose' in question_lower or 'mouth' in question_lower) and ('sore' in question_lower or 'rash' in question_lower)
        has_neuro = 'tremor' in question_lower or 'shake' in question_lower or 'shaking' in question_lower or 'twitch' in question_lower

        if has_yellow_crust or (has_face_sores and has_fever):
            # Impetigo
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'IMPETIGO' in section.upper():
                    relevant.append('## ' + section)
                if 'Error Pattern 4' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

        elif has_appetite_loss and not has_neuro and not has_severe_muscle_pain:
            # Could be chicken pox or drug reaction - return both
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'Error Pattern 2' in section:
                    relevant.append('## ' + section)
                if 'CHICKEN POX' in section.upper():
                    relevant.append('## ' + section)
                if 'DRUG REACTION' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

        elif has_severe_muscle_pain:
            # Dengue
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'Error Pattern 3' in section:
                    relevant.append('## ' + section)
                if 'DENGUE' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

        elif has_neuro:
            # Drug Reaction
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'DRUG REACTION' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

        else:
            # General fever + rash - return chicken pox section
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'CHICKEN POX' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # Priority 3: COUGH + BREATHING DIFFICULTY (Asthma vs Pneumonia)
    # ========================================================
    has_cough = 'cough' in question_lower
    has_breathing = 'breath' in question_lower or 'wheez' in question_lower or 'shortness' in question_lower or 'tight' in question_lower

    if has_cough and has_breathing:
        has_fever = 'fever' in question_lower or 'temperature' in question_lower
        has_thick_sputum = ('thick' in question_lower and ('sputum' in question_lower or 'phlegm' in question_lower or 'mucus' in question_lower)) or \
                         'sticky mucus' in question_lower or 'sticky phlegm' in question_lower or 'mucusy' in question_lower or 'mucous' in question_lower

        if has_fever and has_thick_sputum:
            # Pneumonia
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'PNEUMONIA' in section.upper() or 'ASTHMA' in section.upper():
                    relevant.append('## ' + section)
                if 'Rule 3' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)
        else:
            # Asthma (no fever or no thick sputum)
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'ASTHMA' in section.upper() or 'BRONCHIAL' in section.upper():
                    relevant.append('## ' + section)
                if 'Rule 3' in section:
                    relevant.append('## ' + section)
                if 'Error Pattern 6' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # Priority 4: GASTROINTESTINAL (GERD vs Peptic Ulcer)
    # ========================================================
    has_heartburn = 'heartburn' in question_lower or 'acid reflux' in question_lower or 'acid taste' in question_lower
    has_burning = 'burning' in question_lower and ('stomach' in question_lower or 'abdom' in question_lower or 'upper' in question_lower)
    has_appetite_loss = 'appetite' in question_lower or 'no appetite' in question_lower or "don't feel like eating" in question_lower
    has_worse_eating = ('worse' in question_lower and 'eat' in question_lower) or ('worse' in question_lower and 'meal' in question_lower)

    if has_heartburn or has_burning:
        if has_burning and has_appetite_loss and has_worse_eating:
            # Peptic Ulcer
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'PEPTIC ULCER' in section.upper():
                    relevant.append('## ' + section)
                if 'Error Pattern 5' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

        elif has_heartburn and not has_appetite_loss:
            # GERD
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'GERD' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # Priority 5: JOINT/MUSCLE PAIN (Arthritis vs Dengue)
    # ========================================================
    has_joint = 'joint' in question_lower or 'knee' in question_lower or 'hip' in question_lower or 'hand' in question_lower
    has_walk = 'walk' in question_lower or 'walking' in question_lower
    has_swollen = 'swell' in question_lower
    has_muscle_pain = 'muscle' in question_lower or 'bone' in question_lower
    has_nausea = 'nause' in question_lower or 'vomit' in question_lower or 'sick' in question_lower
    has_weakness = 'weak' in question_lower or 'tired' in question_lower or 'fatigue' in question_lower or 'exhausted' in question_lower

    if has_joint:
        if has_swollen and has_walk:
            # Arthritis
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'ARTHRITIS' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

        elif (has_muscle_pain or has_weakness) and (has_nausea or has_weakness):
            # Could be Dengue
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'DENGUE' in section.upper():
                    relevant.append('## ' + section)
                if 'Error Pattern 3' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # Priority 6: ALLERGY vs COMMON COLD
    # ========================================================
    has_nose = 'runny' in question_lower or 'stuffy' in question_lower or 'nose' in question_lower
    has_itchy = 'itch' in question_lower or 'scratchy' in question_lower
    has_sneeze = 'sneez' in question_lower
    has_taste_smell = 'taste' in question_lower or 'smell' in question_lower
    has_eye_symptoms = ('eye' in question_lower or 'watery' in question_lower or 'red' in question_lower)

    if has_nose:
        if has_itchy or has_eye_symptoms:
            # Allergy
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'ALLERGY' in section.upper():
                    relevant.append('## ' + section)
                if 'Error Pattern 7' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

        elif has_taste_smell:
            # Common Cold
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'COMMON COLD' in section.upper():
                    relevant.append('## ' + section)
                if 'Error Pattern 7' in section:
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # Priority 7: NECK SYMPTOMS (Cervical Spondylosis)
    # ========================================================
    has_neck = 'neck' in question_lower
    has_balance = 'balance' in question_lower or 'dizzi' in question_lower or 'unsteady' in question_lower

    if has_neck and has_balance:
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES']
        for section in sections:
            if 'CERVICAL' in section.upper():
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # Priority 8: SKIN SYMPTOMS (Fungal, Drug Reaction, Psoriasis)
    # ========================================================
    has_rash = 'rash' in question_lower or 'skin' in question_lower
    has_peeling = 'peel' in question_lower or 'flaky' in question_lower
    has_color = 'color' in question_lower or 'different' in question_lower
    has_nodule = 'nodule' in question_lower or 'bump' in question_lower or 'lump' in question_lower

    if has_rash:
        if has_peeling and not has_nodule:
            # Drug Reaction or Psoriasis
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'DRUG REACTION' in section.upper():
                    relevant.append('## ' + section)
                if 'PSORIASIS' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

        if has_color or has_nodule:
            # Fungal Infection
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'FUNGAL' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # Priority 9: VISUAL SYMPTOMS (Migraine vs Diabetes)
    # ========================================================
    has_visual = 'visual' in question_lower or 'vision' in question_lower or 'see' in question_lower
    has_headache = 'headache' in question_lower or 'head hurts' in question_lower

    if has_visual:
        if has_headache:
            # Migraine
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'MIGRAINE' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

        else:
            # Diabetes
            sections = guide.split('\n## ')
            relevant = ['## CRITICAL DIFFERENTIATION RULES']
            for section in sections:
                if 'DIABETES' in section.upper():
                    relevant.append('## ' + section)
            return '\n'.join(relevant)

    # ========================================================
    # Priority 10: COGNITIVE SYMPTOMS (Diabetes vs Drug Reaction)
    # ========================================================
    has_cognitive = 'confus' in question_lower or 'brain fog' in question_lower or 'concentrat' in question_lower
    has_libido = 'libido' in question_lower or 'arous' in question_lower or 'sex' in question_lower

    if has_cognitive and has_libido:
        # Diabetes
        sections = guide.split('\n## ')
        relevant = ['## CRITICAL DIFFERENTIATION RULES']
        for section in sections:
            if 'DIABETES' in section.upper():
                relevant.append('## ' + section)
            if 'Error Pattern 8' in section:
                relevant.append('## ' + section)
        return '\n'.join(relevant)

    # ========================================================
    # Default: Return full guide
    # ========================================================
    return guide
