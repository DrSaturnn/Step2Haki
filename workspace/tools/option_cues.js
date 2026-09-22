/* Evaluate this expression in the rendered study page after its MCQs initialize.
   It reads the DOM only. It is an authoring diagnostic, not a runtime dependency.
   Length = normalized label text in JavaScript string characters, excluding A/B/C.
   This measures textual length, not rendered pixel width or clinical validity. */
(() => {
  const rows = [];
  const seen = new Set(), duplicateItemIds = [];
  document.querySelectorAll('.brief .mcq').forEach(q => {
    if (q.closest('.scalepeek')) return;
    const key = Number(q.dataset.a);
    const buttons = [...q.querySelectorAll('.opts > button')];
    if (!Number.isInteger(key) || key < 0 || key >= buttons.length || buttons.length < 2) return;
    const id = q.dataset.itemId || null;
    if (id && seen.has(id)) duplicateItemIds.push(id);
    if (id) seen.add(id);
    const labels = buttons.map(button => {
      const copy = button.cloneNode(true);
      copy.querySelectorAll('.k').forEach(letter => letter.remove());
      return copy.textContent.replace(/\s+/g, ' ').trim();
    });
    rows.push({id, brief: q.closest('.brief').id, status: q.dataset.itemStatus || null, key, labels});
  });
  function summarize(items) {
    let unique = 0, tied = 0, credit = 0, keyCharacters = 0, otherCharacters = 0, otherCount = 0;
    items.forEach(row => {
      const lengths = row.labels.map(label => label.length);
      const maximum = Math.max(...lengths), ties = lengths.filter(length => length === maximum).length;
      if (lengths[row.key] === maximum) {
        credit += 1 / ties;
        if (ties === 1) unique++; else tied++;
      }
      keyCharacters += lengths[row.key];
      otherCharacters += lengths.reduce((a, b) => a + b, 0) - lengths[row.key];
      otherCount += lengths.length - 1;
    });
    const n = items.length;
    return {n, uniquelyLongestKey: unique, keyTiedForLongest: tied,
      uniquelyLongestKeyPercent: n ? 100 * unique / n : null,
      randomTieLongestStrategyPercent: n ? 100 * credit / n : null,
      meanKeyCharacters: n ? keyCharacters / n : null,
      meanDistractorCharacters: otherCount ? otherCharacters / otherCount : null};
  }
  const briefIds = [...new Set(rows.map(row => row.brief))];
  return {
    method: 'Normalized option text; unique maxima and ties reported separately. Longest-choice score uses random tie-breaking. Missing status is not assumed ready.',
    all: summarize(rows), ready: summarize(rows.filter(row => row.status === 'ready')),
    missingStatus: rows.filter(row => row.status === null).length, duplicateItemIds,
    byBrief: Object.fromEntries(briefIds.map(id => [id, summarize(rows.filter(row => row.brief === id))])),
    reviewCandidates: rows.filter(row => {
      const lengths = row.labels.map(label => label.length);
      return lengths[row.key] > Math.max(...lengths.filter((_, index) => index !== row.key));
    })
  };
})()
