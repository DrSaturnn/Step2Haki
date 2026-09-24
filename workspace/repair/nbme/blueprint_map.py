"""Phase 1: primary and secondary NBME system per brief. 'review' marks judgment calls for the user."""
M = {
# MSK
'pmr':('msk','immune',''),'biceps':('msk','',''),'cts':('msk','neuro','review: peripheral nerve could be neuro'),
'dequervain':('msk','',''),'meralgia':('neuro','msk','review: peripheral nerve'),'scaphoid':('msk','',''),
'backpain':('msk','',''),'hippos':('msk','',''),'gtps':('msk','',''),'inflam-back':('msk','immune',''),
'oa-pharm':('msk','',''),'septic-bursitis':('msk','',''),'septic-hip':('msk','',''),'synovitis':('msk','',''),
'limp':('msk','',''),'sjia':('msk','immune',''),'nursemaid':('msk','',''),'scfe':('msk','',''),
'myositis-ossificans':('msk','',''),'growing-pains':('msk','',''),'bone-tumors':('msk','',''),'scheuermann':('msk','',''),
'bs-septic-adult':('msk','',''),'bs-lbp-acute':('msk','',''),'bs-synovitis-mgmt':('msk','',''),
'bs-torticollis':('msk','newborn',''),'bs-brachial-plexus':('newborn','neuro',''),'shoulder-rom':('msk','',''),
# Pediatrics
'growth':('gen','',''),'neonatal-maternal-labs':('newborn','',''),'newborn-hormone':('newborn','',''),
'aneuploidy':('newborn','',''),'malform-syndromes':('newborn','',''),'bs-learning':('behav','',''),
'bs-nat-fracture':('multi','social','review: abuse could be coded behav or social'),'bs-shock':('multi','cv',''),
'bs-infant-feeding':('gen','gi',''),'bs-tanner':('gen','endo',''),'bs-ftt':('gen','gi',''),
'bs-preterm-followup':('newborn','gen',''),'aq-infant-hypotonia':('newborn','neuro',''),
# CV
'chf':('cv','',''),'ascvd':('cv','gen',''),'angina':('cv','',''),'ie-ppx':('cv','',''),'secondary-htn':('cv','endo',''),
'dvt':('cv','heme',''),'ped-murmur':('cv','',''),'cyanotic-chd':('cv','newborn',''),'right-murmurs':('cv','',''),
'htn-drugs':('cv','',''),'newborn-cyanosis':('newborn','cv',''),'kawasaki':('cv','multi',''),'arf':('cv','immune',''),
'myocarditis':('cv','',''),'del22q11':('newborn','immune','review: could be immune primary'),
'bs-murmur-map':('cv','',''),'bs-shunt-timing':('cv','newborn',''),
# Pulm
'copd':('resp','',''),'asthma-copd':('resp','',''),'cough':('resp','',''),'pneumoconiosis':('resp','',''),
'rhinitis':('resp','immune',''),'sinopulm-structural':('resp','immune',''),'hypoxemia-mech':('resp','',''),
'abpa':('resp','immune',''),'scd-dyspnea':('resp','heme','review: could be heme primary'),'airway':('resp','',''),
'mycoplasma':('resp','',''),'uri':('resp','',''),'asthma':('resp','',''),'bpd':('resp','newborn',''),'bs-nrd':('newborn','resp',''),
# GI
'liver-preg':('preg','gi',''),'masld':('gi','',''),'cholestasis':('gi','',''),'zenker':('gi','',''),
'infant-stool':('gi','',''),'fap':('gi','',''),'peutz-jeghers':('gi','',''),'feeding-refusal':('gi','behav','review: could be behav primary'),
'rlq-pain':('gi','',''),'peds-constipation':('gi','',''),'cyclic-vomiting':('gi','',''),'neonatal-jaundice':('newborn','gi',''),
'neonatal-bowel':('newborn','gi',''),'occult-gi-bleed':('gi','',''),'bs-galactosemia':('newborn','gi',''),
'bs-impaction':('gi','',''),'bs-tef':('newborn','gi',''),'bs-umbilical':('newborn','',''),
'bs-fat-soluble-vitamins':('multi','gi','review: nutrition coded as multisystem'),'bs-water-soluble-vitamins':('multi','gi','review: nutrition coded as multisystem'),
'bs-wilson':('gi','neuro',''),
# Renal
'pyelo':('renal','',''),'bph':('repro_m','renal',''),'nephropathy':('renal','endo',''),'hematuria':('renal','',''),
'scrotum':('repro_m','',''),'hypercalcemia':('endo','',''),'vur':('renal','',''),'peds-uti-recurrent':('renal','',''),
'enuresis':('renal','behav',''),'polyuria':('renal','endo',''),'peds-aki':('renal','',''),'nephrotic-child':('renal','',''),
'bs-puv':('renal','newborn',''),'bs-pyelo-organism':('renal','',''),'bs-incontinence':('renal','',''),'bs-enuresis':('renal','behav',''),
'bs-nephritic':('renal','',''),'bs-abdominal-mass':('renal','multi',''),'aq-puffy-eyes':('renal','',''),
# Endo
'thyroid':('endo','',''),'levo':('endo','',''),'gynecomastia':('repro_m','endo','review: breast'),'prolactin':('endo','',''),
'osteoporosis':('msk','endo',''),'preg-thyroid':('preg','endo',''),'congenital-hypothyroid':('endo','newborn',''),
'tumor-syndromes':('multi','endo','review: inherited tumor syndromes'),'precocious-puberty':('endo','',''),
'homocystinuria':('multi','msk','review: inborn error of metabolism'),'bs-dexa-highrisk':('msk','gen',''),
'bs-dm-bundle':('endo','',''),'bs-short-stature':('endo','gen',''),
# Heme
'anemia-thrombocytopenia':('heme','renal',''),'drug-hemolysis':('heme','',''),'dipstick-mismatch':('heme','renal',''),
'microcytic-anemia':('heme','',''),'factor-inhibitor':('heme','',''),'transfusion':('heme','',''),'bs-leukemia':('heme','',''),
'bs-spherocytosis':('heme','',''),'bs-sickle-trait':('heme','',''),'aq-bruising':('heme','',''),
# ID
'tb':('resp','multi',''),'meningitis':('neuro','multi',''),'hiv-vax':('immune','gen',''),'dtap':('gen','immune',''),
'cervicitis':('repro_f','',''),'ig-panel':('immune','',''),'rmsf':('multi','',''),'lymphadenitis':('heme','multi','review: lymph nodes coded lymphoreticular'),
'herpangina':('multi','gi','review: oral viral infection'),'cgd':('immune','',''),'bs-pta':('resp','',''),
'bs-torch':('newborn','multi',''),'bs-neonatal-sepsis':('newborn','multi',''),'bs-fever-rash-arthralgia':('multi','msk',''),
'bs-exanthems':('multi','skin','review: exanthems could be skin'),'bs-anaphylaxis':('immune','',''),
'bs-isolation':('gen','multi','review: infection control'),'bs-foodborne':('gi','multi',''),
'bs-febrile-infant':('multi','newborn',''),'aq-infant-fever':('multi','renal',''),
# Neuro and HEENT
'hearing':('neuro','',''),'redeye':('neuro','',''),'cluster':('neuro','',''),'sellar-mass':('neuro','endo',''),
'peds-headache-imaging':('neuro','',''),'cholesteatoma':('neuro','',''),'febrile-seizure':('neuro','',''),
'cerebral-palsy':('neuro','',''),'abrs-complications':('resp','neuro',''),'vpshunt':('neuro','',''),
'retinitis-pigmentosa':('neuro','',''),'tics':('behav','neuro','review: tic disorders'),'bs-tethered':('neuro','newborn',''),
'bs-reye':('neuro','gi',''),'bs-peds-stroke':('neuro','',''),'bs-posterior-fossa':('neuro','',''),'aq-child-headache':('neuro','',''),
# Derm
'psoriasis':('skin','',''),'cellulitis':('skin','',''),'footulcer':('skin','endo',''),'eczemaherp':('skin','',''),
'peds-alopecia':('skin','',''),'neonatal-rash':('skin','newborn',''),'diaper-dermatitis':('skin','',''),'bs-scabies':('skin','',''),
# OB/GYN
'preg-vax':('preg','gen',''),'cervical':('repro_f','',''),'pmb':('repro_f','',''),'ectopic':('preg','',''),
'hpv':('gen','repro_f',''),'adolescent-aub':('repro_f','',''),'contraception':('repro_f','',''),'fibroids':('repro_f','',''),
'teratogens':('preg','',''),'primary-amenorrhea':('repro_f','endo',''),'bs-cervical-gate':('repro_f','',''),
'bs-tdap-preg':('preg','gen',''),'bs-pid':('repro_f','',''),
# Prevention and ethics
'smoking':('gen','',''),'lipid-screen':('gen','cv',''),'preop':('gen','',''),'elder':('social','',''),
'vegan':('multi','gen','review: nutrition'),'bs-adolescent-confid':('social','',''),'bs-adolescent-vax':('gen','',''),
}
