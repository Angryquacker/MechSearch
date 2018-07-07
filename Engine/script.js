let results = [
  {
    link: 'https://www.google.com/',
    keywords: ['google', 'search']
  },
  {
    link: 'https://www.amazon.com/',
    keywords: ['amazon', 'shop']
  },
  {
    link: 'https://www.bing.com/',
    keywords: ['bing', 'search', 'search engine']
  }
];


$(document).ready(function() {
  function search(input) {
    let final = [];
    for (let i = 0;i < results.length;i++) {
      for (let j = 0;j < results[i].keywords.length;j++) {
        if (results[i].keywords[j] == input) {
          final.push(results[i].link);
        }
      }
    }
    return final;
  }

  $('#searchBar').on('keydown', function(e) {
    if (e.which == 13) {
      let links = search(document.getElementById('searchBar').value.toLowerCase().trim());      
      if (links.length == 0) {
        $('#spinner').show();
        setTimeout(function() {
          $('#spinner').hide();
          $('section').hide();
          $('#error').show();
        }, 500);
      } else {
        $('#spinner').show();
        setTimeout(function() {
          $('#spinner').hide();
          $('section').hide();
          $('#results').show();
          console.log(links);
        }, 500);
      }
    }
  });
});