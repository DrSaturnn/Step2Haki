(function(){try{var o=JSON.parse(localStorage.getItem('ph-pilot')||'{}')||{},h=document.documentElement,q=location.search;
function qp(k){var m=new RegExp('[?&]'+k+'=([^&]+)').exec(q);return m?decodeURIComponent(m[1]):null;}
['layout','bars','rail','dx'].forEach(function(k){var v=qp('ph'+k)!==null?qp('ph'+k):o[k];if(v)h.setAttribute('data-ph-'+k,v);});}catch(e){}})();
