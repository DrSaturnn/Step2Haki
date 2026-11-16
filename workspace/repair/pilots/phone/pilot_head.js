(function(){try{var o=JSON.parse(localStorage.getItem('ph-pilot')||'{}')||{},h=document.documentElement,q=location.search;
var D={dx:'b',nav:'push',surf:'axbx24',home:'desk',tabs:'float'};
function qp(k){var m=new RegExp('[?&]'+k+'=([^&]+)').exec(q);return m?decodeURIComponent(m[1]):null;}
['layout','bars','rail','dx','home','tabs','surf','nav'].forEach(function(k){var v=qp('ph'+k)!==null?qp('ph'+k):(o[k]||D[k]);if(v)h.setAttribute('data-ph-'+k,v);});}catch(e){}})();
