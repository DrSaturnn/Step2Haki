#!/usr/bin/env python3
"""mimics.py: the single source for mimic comparison rows (hub and spoke, Jonathan 2026-10-03).

A mimic row is written ONCE here and rendered by lifechart.course_table() into every brief that uses it: the full hub
brief for a presenting complaint, and the short slice in each topic brief. The rendered row carries a hash of its HTML
(data-mrow-v), and tools/gate.py check `mimic-row` fails if a copy on the page was hand-edited or differs from another
copy. To change a row, edit it here, rebuild every brief that uses it, and ship them together.

Row fields
  name      diagnosis name (masked in study mode)
  window    the duration or course line under the name (always visible: a recall prompt)
  lines     exactly three lines, same axis order in every row: pattern or setting, core finding, deciding feature last
  course    chronic | episodic | single | lifelong | childhood   (the builder checks the strip agrees)
  segs      [(kind, a, b)] on the life-course axis in percent; kinds in lifechart.COURSE_KINDS
  marks     [x] optional brief psychotic pips drawn over the strip (borderline stress psychosis)
  src       claim sources for the ledger: page:<brief id>, or a source key in SOURCES
  status    ready | needs_source (needs_source rows refuse to render)

Life-course axis (schematic, not to scale): Child 0, Teens 20, 20s 38, 30s 62, 40s+ 84 (short labels: no collision at 390 px).
Content rule: every line traces to the existing page (page:<id>) or to a source opened 2026-10-03 (SOURCES). Vendor
explanations are paraphrased; no 10-word vendor run.
"""

AXIS = [('Child', 0), ('Teens', 20), ('20s', 38), ('30s', 62), ('40s+', 84)]

SOURCES = {
    'uw-sz': 'UWorld schizophrenia questions and article (pasted 2026-10-03; local only)',
    'uw-bpd': 'UWorld brief psychotic disorder question and article (pasted 2026-10-03; local only)',
    'uw-spd': 'UWorld schizotypal personality disorder question, cluster table (pasted 2026-10-03; local only)',
    'uw-eos': 'UWorld early-onset schizophrenia question (pasted 2026-10-03; local only)',
    'uw-sza': 'UWorld schizoaffective question and article (pasted 2026-10-03; local only)',
    'sp-pd': 'StatPearls, Personality Disorder, NBK556058: "its onset can be traced back at least to adolescence or early adulthood"',
    'sp-ppd': 'StatPearls, Paranoid Personality Disorder, NBK606107: psychotic disorders "are characterized by a period of persistent '
              'psychotic symptoms (delusions and hallucinations), which are not present in PPD"',
    'dsm-asd': 'DSM-5 autism criteria via iacc.hhs.gov: A "Persistent deficits in social communication and social interaction"; '
               'B "Restricted, repetitive patterns of behavior, interests, or activities"; C "present in the early developmental period"',
}

ROWS = {
    # ---------------- primary psychotic
    'schizophrenia': dict(
        name='Schizophrenia', window='6 months or more in all',
        lines=['Onset late teens to 20s, often after a prodrome',
               '2 or more: delusions, voices, disorganization, negative symptoms',
               'Functioning falls and stays below baseline'],
        course='chronic', segs=[('pro', 30, 38), ('act', 38, 46), ('res', 46, 100)],
        src=['page:psychosis-duration', 'uw-sz'], status='ready'),
    'schizophreniform': dict(
        name='Schizophreniform disorder', window='1 to under 6 months',
        lines=['Same symptoms as schizophrenia',
               'Functional decline not required',
               'Under 6 months in all'],
        course='single', segs=[('act', 40, 46)],
        src=['page:psychosis-duration', 'uw-bpd'], status='ready'),
    'brief-psychotic': dict(
        name='Brief psychotic disorder', window='1 day to under 1 month',
        lines=['Sudden onset, often after a marked stressor',
               '1 or more: delusions, voices, disorganization',
               'Full return to baseline within a month'],
        course='single', segs=[('act', 44, 46)],
        src=['page:psychosis-duration', 'uw-bpd'], status='ready'),
    'schizoaffective': dict(
        name='Schizoaffective disorder', window='Psychosis 2 weeks or more without mood',
        lines=['Recurrent major mood episodes with Criterion A',
               'Delusions or voices 2 weeks or more with no mood episode',
               'Mood episodes fill most of the illness'],
        course='chronic', segs=[('lop', 34, 46), ('act', 46, 50), ('lop', 50, 64), ('act', 64, 68), ('lop', 68, 84),
                                ('act', 84, 88), ('lop', 88, 100)],
        src=['page:psychosis-duration', 'uw-sza'], status='ready'),
    'delusional': dict(
        name='Delusional disorder', window='1 month or more',
        lines=['Often begins around 40',
               'One or more delusions; no prominent voices or disorganization',
               'Works and behaves normally apart from the delusion'],
        course='chronic', segs=[('only', 80, 100)],
        src=['page:psychosis-duration', 'uw-sz'], status='ready'),
    # ---------------- mood with psychosis
    'mdd-psychotic': dict(
        name='Major depressive disorder with psychotic features', window='Episodes 2 weeks or more',
        lines=['Discrete depressive episodes',
               'Low mood or anhedonia, sleep and appetite change',
               'Psychosis only inside a depressive episode'],
        course='episodic', segs=[('lo', 39, 46), ('lop', 61, 68), ('lo', 81, 88)],
        src=['page:psychosis-duration', 'page:bipolar-mania', 'uw-sza'], status='ready'),
    'bipolar-psychotic': dict(
        name='Bipolar I disorder with psychotic features', window='Manic episodes 1 week or more',
        lines=['Discrete manic episodes; depression common',
               'Elated or irritable mood, less sleep, pressured speech',
               'Psychosis only inside a mood episode'],
        course='episodic', segs=[('hi', 34, 41), ('hip', 55, 62), ('hi', 76, 83)],
        src=['page:bipolar-mania', 'page:psychosis-duration', 'uw-sz'], status='ready'),
    # ---------------- personality (no persistent psychosis)
    'paranoid-pd': dict(
        name='Paranoid personality disorder', window='Lifelong, from adolescence or early adulthood',
        lines=['Suspicious, distrustful, hypervigilant',
               'No odd beliefs, magical thinking or eccentric speech',
               'No period of persistent delusions or hallucinations'],
        course='lifelong', segs=[('trait', 24, 100)],
        src=['sp-pd', 'sp-ppd', 'uw-spd'], status='ready'),
    'schizoid-pd': dict(
        name='Schizoid personality disorder', window='Lifelong, from adolescence or early adulthood',
        lines=['Prefers to be alone; detached, little emotion',
               'No odd beliefs or eccentric behavior',
               'No hallucinations or delusions'],
        course='lifelong', segs=[('trait', 24, 100)],
        src=['sp-pd', 'uw-spd', 'uw-eos'], status='ready'),
    'schizotypal-pd': dict(
        name='Schizotypal personality disorder', window='Lifelong, from adolescence or early adulthood',
        lines=['Odd beliefs, magical thinking, eccentric dress and speech',
               'Few close relationships; paranoid ideas common',
               'Beliefs short of delusions; no frank hallucinations'],
        course='lifelong', segs=[('odd', 24, 100)],
        src=['sp-pd', 'uw-spd'], status='ready'),
    'borderline-pd': dict(
        name='Borderline personality disorder', window='Stress psychosis lasts minutes to hours',
        lines=['Unstable relationships and mood; impulsivity, self-harm',
               'Paranoia or voices under stress',
               'Clears within hours, under 24'],
        course='lifelong', segs=[('trait', 24, 100)], marks=[44, 66],
        src=['sp-pd', 'uw-spd', 'uw-bpd'], status='ready'),
    # ---------------- developmental and normal
    'autism': dict(
        name='Autism spectrum disorder', window='From the early developmental period',
        lines=['Persistent deficits in social communication',
               'Restricted, repetitive behaviors or interests',
               'No hallucinations; no decline from baseline'],
        course='childhood', segs=[('dev', 0, 100)],
        src=['dsm-asd', 'uw-eos'], status='ready'),
    'imaginary-friend': dict(
        name='Imaginary friend (normal)', window='Usually fades around age 6',
        lines=['A companion in early childhood',
               'No withdrawal and no fall in function',
               'A named voice with decline in a teen is a hallucination'],
        course='childhood', segs=[('norm', 0, 10)],
        src=['uw-eos'], status='ready'),
    # ---------------- trauma
    'acute-stress': dict(
        name='Acute stress disorder', window='3 days to 1 month after a trauma',
        lines=['Follows a traumatic event',
               'Intrusions, avoidance, dissociation, arousal',
               'Bizarre psychosis is not typical'],
        course='single', segs=[('stress', 50, 52)],
        src=['uw-bpd'], status='ready'),
    'ptsd': dict(
        name='Posttraumatic stress disorder', window='Over 1 month after a trauma',
        lines=['Follows a traumatic event',
               'Intrusions, avoidance, negative mood, arousal',
               'Lasts over a month; psychosis is not typical'],
        course='single', segs=[('stress', 50, 62)],
        src=['uw-bpd'], status='ready'),
    # ---------------- secondary
    'substance-psychosis': dict(
        name='Substance-induced psychotic disorder', window='During or soon after use',
        lines=['Drug use shown by history, exam or labs',
               'Delusions or hallucinations',
               'Usually remits once use stops'],
        course='episodic', segs=[('sub', 40, 43), ('sub', 54, 57)],
        src=['page:psychosis-duration', 'uw-sz', 'uw-bpd'], status='ready'),
    'delirium': dict(
        name='Delirium', window='Hours to days; fluctuates',
        lines=['A drug or illness as the cause',
               'Psychosis with a clouded, fluctuating sensorium',
               'Attention fails over hours to days'],
        course='single', segs=[('flux', 70, 72)],
        src=['page:delirium', 'page:psychosis-duration'], status='ready'),
    # ---------------- waiting on a source opened the day they are authored
    'ocd-poor-insight': dict(name='Obsessive-compulsive disorder, poor insight', status='needs_source'),
    'lewy-body': dict(name='Lewy body dementia', status='needs_source'),
    'postpartum-psychosis': dict(name='Postpartum psychosis', status='needs_source'),
    'grief-voice': dict(name='Hearing a dead loved one in normal grief', status='needs_source'),
}

# Hubs: one per presenting complaint. groups render as labelled sub-tables, in this order.
HUBS = {
    'voices': dict(
        title='Hears Voices or Holds Odd Beliefs',
        groups=[('Primary psychotic', ['schizophrenia', 'schizophreniform', 'brief-psychotic', 'schizoaffective', 'delusional']),
                ('Mood with psychosis', ['mdd-psychotic', 'bipolar-psychotic']),
                ('Personality: no persistent psychosis', ['paranoid-pd', 'schizoid-pd', 'schizotypal-pd', 'borderline-pd']),
                ('Developmental and normal', ['autism', 'imaginary-friend']),
                ('After a trauma', ['acute-stress', 'ptsd']),
                ('A drug or illness', ['substance-psychosis', 'delirium'])]),
}

# Spokes: the slice each topic brief carries (most tempting first), with the hub it links to.
SPOKES = {
    'psychosis-duration': dict(hub='voices', rows=['schizophrenia', 'delusional', 'bipolar-psychotic', 'schizotypal-pd',
                                                   'schizoid-pd', 'paranoid-pd']),
    'bipolar-mania': dict(hub='voices', rows=['bipolar-psychotic', 'schizophrenia', 'delusional', 'schizotypal-pd',
                                              'schizoid-pd', 'paranoid-pd']),
}
