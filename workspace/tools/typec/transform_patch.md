# Type C transform patch (index.html, one time)

In `mnemonics()`, right after `var dl=document.createElement('dl'); dl.className='rows';` add:

    if(ul.classList.contains('mnem')) dl.classList.add('mnem');

Then paste `tools/typec/typec.css` at the end of the page's main `<style>` block.
