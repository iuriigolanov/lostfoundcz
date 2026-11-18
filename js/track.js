/* Lost & Found — GA4 click tracking (all pages).
   Param names deliberately avoid GA4-reserved "source"/"medium"/"campaign",
   which would overwrite the session traffic source. */
(function(){
  function t(n,p){try{if(typeof gtag==='function')gtag('event',n,p||{});}catch(e){}}
  var rules=[
    [/^tel:/i,'click_call'],
    [/(wa\.me|api\.whatsapp\.com|whatsapp:)/i,'click_whatsapp'],
    [/^mailto:/i,'click_email'],
    [/resmio\.com/i,'reserve_click'],
    [/(google\.[a-z.]+\/maps|maps\.app\.goo\.gl|goo\.gl\/maps|maps\.google\.|mapy\.(cz|com))/i,'click_directions'],
    [/instagram\.com/i,'click_instagram'],
    [/(facebook\.com|fb\.com)/i,'click_facebook'],
    [/tiktok\.com/i,'click_tiktok']
  ];
  document.addEventListener('click',function(e){
    var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;
    if(!a)return;
    var h=a.getAttribute('href')||'';
    for(var i=0;i<rules.length;i++){
      if(rules[i][0].test(h)){
        t(rules[i][1],{cta_location:(a.className||a.id||'link').toString().trim().slice(0,90),link_url:h.slice(0,200)});
        return;
      }
    }
  },true);
})();
