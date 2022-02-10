//fade scroll effect
AOS.init();
// Fungsi
var ID = function (elID) {
  return document.getElementById(elID);
};

var hide = function (id) {
  return id.classList.add("d-none");
};

var show = function (id) {
  return id.classList.remove("d-none");
};

var inHtm = function (el, content) {
  return (el.innerHTML = content);
};

// Akhir Fungsi

// Deklarasi semua variabel
// yang dibutuhkan menggunakan id elemen

var emptyScrape = ID("scrapekosong");
var emptyPrediksi = ID("testkosong");
var emptyFilter = ID("filterkosong");
var emptyAnalyze = ID("analisakosong")

var btnScrapeReset = ID("btnScrapeReset");
var btnTestReset = ID("btnTestReset");
var btnFilterReset = ID("btnFilterReset");
var btnStopwordsReset = ID("btnStopwordsReset");
var btnUnigramReset = ID("btnUnigramReset");
var btnBigramReset = ID("btnBigramReset");
var btnTrigramReset = ID("btnTrigramReset");
var btnVerbReset = ID("btnVerbReset");
var btnAdjectiveReset = ID("btnAdjectiveReset");
var btnAdverbReset = ID("btnAdverbReset");
var btnNounReset = ID("btnNounReset");


var btnScrape = ID("btnScrape");
var btnTest = ID("btnTest");
var btnFilter = ID("btnFilter");
var btnStopwords = ID("btnStopwords");
var btnUnigram = ID("btnUnigram")
var btnBigram = ID("btnBigram")
var btnTrigram = ID("btnTrigram")
var btnVerb = ID("btnVerb")
var btnAdjective = ID("btnAdjective")
var btnAdverb = ID("btnAdverb")
var btnNoun = ID("btnNoun")

var spinner = ID("spinner");
var testSpinner = ID("test_spinner");

var hasilScrape = ID("hasilScrape");
var hasilTest = ID("hasilTest");
var hasilFilter = ID("hasilFilter");
var hasilAnalisis = ID("hasilAnalisis")

var grafikLoss = ID("gl");
var grafikAkurasi = ID("ga");

var formScrape = ID("formScrape");
var formTest = ID("formTest");
var formFilter = ID("formFilter");
var formStopwords = ID("formStopwords");

var cloud = ID("cloud");
var unigram = ID("unigram");
var trigram = ID("trigram");
var verb = ID("verb");
var adjective = ID("adjective");
var adverb = ID("adverb");
var noun = ID("noun");


// Akhir Deklarasi Variabel

//! SCRAPING
$(formScrape).submit(function (e) {
  e.preventDefault();
  show(emptyScrape);
  hide(hasilScrape);
  hide(btnScrape);

  show(btnScrapeReset);
  show(spinner);

  var formData = new FormData(this);
  var xhr = $.ajax({
    url: "/twitter_data",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      obj = $.parseJSON(data);

      hide(spinner);
      hide(emptyScrape);
      show(hasilScrape);

      setupDataScrape();
            
      console.log(obj["hScrape"]);
    },
    error: function (xhr, ajaxOption, thrownError) 
    {
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnScrapeReset.onclick = function () {
    xhr.abort();
    $(formScrape)[0].reset();
    hide(btnScrapeReset);
    show(btnScrape);
  };
});
//? Akhir Proses SCRAPING

//! Akhir sCRAPING


//! Get Hasil Scraping
function setupDataScrape() {

  $('#tbScrape').DataTable({
    "ajax": {
      "url": '/hScraping',
      "dataType": "json",
      "dataSrc": "data",
      "contentType": "application/json"
    },
    
    "columns": [
      {
        "data": "created_at"
      },

      {
        "data": "id"
      },

      {
        "data": "user-screen_name"
      },
       
      {
        "data": "retweet_count"
      },

      {
        "data": "retweeted_status_screen_name"
      },

      {
        "data": "retweeted_status-text"
      },

      {
        "data": "text"
      },
      
      {
        "data": "user-location"
      }      
    ],

    "columnDefs": [{
        "className": "bolded",
        "targets": -2
      },
      {
        "className": "text-left",
        "targets": "_all"
      },
    ],
  });

}
//! END Hasil sCRAPING

// Get Table Result
function setupDataResult() {

  $('#tbResult').DataTable({
    "ajax": {
      "url": '/hpResult',
      "dataType": "json",
      "dataSrc": "data",
      "contentType": "application/json"
    },
    "columns": [
      {
        "data": "created_at"
      },

      {
        "data": "id"
      },

      {
        "data": "user-screen_name"
      },
       
      {
        "data": "retweet_count"
      },

      {
        "data": "retweeted_status_screen_name"
      },

      {
        "data": "retweeted_status-text"
      },

      {
        "data": "text"
      },
      
      {
        "data": "user-location"
      }      
    ],

    "columnDefs": [{
        "className": "text-left",
        "targets": 0
      },
      {
        "className": "text-center",
        "targets": "_all"
      },
    ],
  });
}
// END TABLE RESULT


//! Test

$(formTest).submit(function (e) {
  e.preventDefault();

  show(emptyPrediksi);
  hide(btnTest);
  hide(hasilTest);

  show(btnTestReset);
  show(testSpinner);
  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/exist_twitter",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);
      console.log(obj["prediction"]);
        
      hide(testSpinner);
      hide(emptyPrediksi);
      show(hasilTest);
      setupDataResult();
    },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: 'Terjadi Masalah :(',
        text: 'Periksa Server',
        confirmButtonText: `Oke`
      }).then((result) => {
        if (result.isConfirmed) {
          location.reload();
        }
      })
    },
  });

  btnTestReset.onclick = function () {
    xhr.abort();
    $(formTest)[0].reset();
    hide(btnTestReset);
    show(btnTest);
  };

});
//! Akhir Test


//! Filter

$(formFilter).submit(function (e) {
  e.preventDefault();
  show(emptyFilter);
  hide(hasilFilter);
  hide(btnFilter);

  show(btnFilterReset);
  show(spinner);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/filter_out",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      hide(spinner);
      hide(emptyFilter);
      show(hasilFilter);

      setupDataFilter();
      
      console.log(obj["hFilter"]);
    },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnFilterReset.onclick = function () {
    xhr.abort();
    $(formFilter)[0].reset();
    hide(btnFilterReset);
    show(btnFilter);
  };
});

//! AKHIR FILTER

//! GET TABLE FILTER
function setupDataFilter() {

  $('#tbFilter').DataTable({
    "ajax": {
      "url": '/hFilter',
      "dataType": "json",
      "dataSrc": "data",
      "contentType": "application/json"
    },
    "columns": [
      {
        "data": "created_at"
      },

      {
        "data": "id"
      },

      {
        "data": "user-screen_name"
      },
       
      {
        "data": "retweet_count"
      },

      {
        "data": "retweeted_status_screen_name"
      },

      {
        "data": "retweeted_status-text"
      },

      {
        "data": "text"
      },
      
      {
        "data": "user-location"
      }      
    ],

    "columnDefs": [
      {
        "className": "text-left",
        "targets": 0
      },
      {
        "className": "text-center",
        "targets": "_all"
      },
    ],
  });
}
// END TABLE FILTER

// STOPWORDS CUSTOM
$(formStopwords).submit(function (e) {
  e.preventDefault();
  show(emptyAnalyze);
  hide(hasilAnalisis);
  hide(btnStopwords);

  show(btnStopwordsReset);
  show(spinner);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/stopwords",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      setupDataRT_Indegree();
      setupDataReply_Indegree();
      setupDataRT_betweeness();
      setupDataReply_betweeness();
      setupDataRatio();

      console.log(obj["locHStopwords"]);
      console.log(obj["lochRT_indegree"]);
      console.log(obj["lochReply_indegree"]);
      console.log(obj["lochRT_betweeness"]);
      console.log(obj["lochReply_betweeness"]);
      console.log(obj["lochRatio"]);

      console.log(obj["wordcloud"]);
        $(cloud).attr("src", "./static/img/grafik/" + obj["wordcloud"]);
      console.log(obj["network"]);
        $(network).attr("src", "./static/img/grafik/" + obj["network"]);
      console.log(obj["timeseries"]);
        $(timeseries).attr("src", "./static/img/grafik/" + obj["timeseries"]);
      console.log(obj["unigram"]);
        $(unigram).attr("src", "./static/img/grafik/" + obj["unigram"]);
      console.log(obj["bigram"]);
        $(bigram).attr("src", "./static/img/grafik/" + obj["bigram"]);
      console.log(obj["trigram"]);
        $(trigram).attr("src", "./static/img/grafik/" + obj["trigram"]);
      console.log(obj["verb"]);
        $(verb).attr("src", "./static/img/grafik/" + obj["verb"]);
      console.log(obj["adjective"]);
        $(adjective).attr("src", "./static/img/grafik/" + obj["adjective"]);
      console.log(obj["adverb"]);
        $(adverb).attr("src", "./static/img/grafik/" + obj["adverb"]);
      console.log(obj["noun"]);
        $(noun).attr("src", "./static/img/grafik/" + obj["noun"]);

      hide(spinner);
      hide(emptyAnalyze);
      show(hasilAnalisis);

      },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnStopwordsReset.onclick = function () {
    xhr.abort();
    $(formStopwords)[0].reset();
    hide(btnStopwordsReset);
    show(btnStopwords);
  };
});

$(formUnigram).submit(function (e) {
  e.preventDefault();
  
  hide(btnUnigram);
  show(btnUnigramReset);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/hUnigram",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      console.log(obj["unigram"]);
        $(unigram).attr("src", "./static/img/grafik/" + obj["unigram"]);

      },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnUnigramReset.onclick = function () {
    xhr.abort();
    $(formUnigram)[0].reset();
    hide(btnUnigramReset);
    show(btnUnigram);
  };
});


$(formBigram).submit(function (e) {
  e.preventDefault();
  
  hide(btnBigram);
  show(btnBigramReset);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/hBigram",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      console.log(obj["bigram"]);
        $(bigram).attr("src", "./static/img/grafik/" + obj["bigram"]);

      },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnBigramReset.onclick = function () {
    xhr.abort();
    $(formBigram)[0].reset();
    hide(btnBigramReset);
    show(btnBigram);
  };
});

$(formTrigram).submit(function (e) {
  e.preventDefault();
  
  hide(btnTrigram);
  show(btnTrigramReset);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/hTrigram",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      console.log(obj["trigram"]);
        $(trigram).attr("src", "./static/img/grafik/" + obj["trigram"]);

      },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnTrigramReset.onclick = function () {
    xhr.abort();
    $(formTrigram)[0].reset();
    hide(btnTrigramReset);
    show(btnTrigram);
  };
});

$(formVerb).submit(function (e) {
  e.preventDefault();
  
  hide(btnVerb);
  show(btnVerbReset);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/hVerb",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      console.log(obj["verb"]);
        $(verb).attr("src", "./static/img/grafik/" + obj["verb"]);

      },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnVerbReset.onclick = function () {
    xhr.abort();
    $(formVerb)[0].reset();
    hide(btnVerbReset);
    show(btnVerb);
  };
});

$(formAdjective).submit(function (e) {
  e.preventDefault();
  
  hide(btnAdjective);
  show(btnAdjectiveReset);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/hAdjective",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      console.log(obj["adjective"]);
        $(adjective).attr("src", "./static/img/grafik/" + obj["adjective"]);

      },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnAdjectiveReset.onclick = function () {
    xhr.abort();
    $(formAdjective)[0].reset();
    hide(btnAdjectiveReset);
    show(btnAdjective);
  };
});

$(formAdverb).submit(function (e) {
  e.preventDefault();
  
  hide(btnAdverb);
  show(btnAdverbReset);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/hAdverb",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      console.log(obj["adverb"]);
        $(adverb).attr("src", "./static/img/grafik/" + obj["adverb"]);

      },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnAdverbReset.onclick = function () {
    xhr.abort();
    $(formAdverb)[0].reset();
    hide(btnAdverbReset);
    show(btnAdverb);
  };
});



$(formNoun).submit(function (e) {
  e.preventDefault();
  
  hide(btnNoun);
  show(btnNounReset);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/hNoun",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      console.log(obj["noun"]);
        $(noun).attr("src", "./static/img/grafik/" + obj["noun"]);

      },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnNounReset.onclick = function () {
    xhr.abort();
    $(formNoun)[0].reset();
    hide(btnNounReset);
    show(btnNoun);
  };
});



function setupDataRT_Indegree() {

  $('#tbRTIndegree').DataTable({
    "paging": false,
    "searching": false,
    "ajax": {
      "url": '/hRT_indegree',
      "dataType": "json",
      "dataSrc": "data",
      "contentType": "application/json"
    },
    "columns": [
      {
        "data": "screen_name"
      },

      {
        "data": "degree"
      }   
    ],

    "columnDefs": [
      {
        "className": "text-left",
        "targets": 0
      },
      {
        "className": "text-center",
        "targets": "_all"
      },
    ],
  });
}

function setupDataReply_Indegree() {

  $('#tbReplyIndegree').DataTable({
    "paging": false,
    "searching": false,
    "ajax": {
      "url": '/hReply_indegree',
      "dataType": "json",
      "dataSrc": "data",
      "contentType": "application/json"
    },
    "columns": [
      {
        "data": "screen_name"
      },

      {
        "data": "degree"
      }   
    ],

    "columnDefs": [
      {
        "className": "text-left",
        "targets": 0
      },
      {
        "className": "text-center",
        "targets": "_all"
      },
    ],
  });
}

function setupDataRT_betweeness() {

  $('#tbRTbetweeness').DataTable({
    "paging": false,
    "searching": false,
    "ajax": {
      "url": '/hRT_betweeness',
      "dataType": "json",
      "dataSrc": "data",
      "contentType": "application/json"
    },
    "columns": [
      {
        "data": "screen_name"
      },

      {
        "data": "degree"
      }   
    ],

    "columnDefs": [
      {
        "className": "text-left",
        "targets": 0
      },
      {
        "className": "text-center",
        "targets": "_all"
      },
    ],
  });
}


function setupDataReply_betweeness() {

  $('#tbReplybetweeness').DataTable({
    "paging": false,
    "searching": false,
    "ajax": {
      "url": '/hReply_betweeness',
      "dataType": "json",
      "dataSrc": "data",
      "contentType": "application/json"
    },
    "columns": [
      {
        "data": "screen_name"
      },

      {
        "data": "degree"
      }   
    ],

    "columnDefs": [
      {
        "className": "text-left",
        "targets": 0
      },
      {
        "className": "text-center",
        "targets": "_all"
      },
    ],
  });
}

function setupDataRatio() {

  $('#tbRatio').DataTable({
    "paging": false,
    "searching": false,
    "ajax": {
      "url": '/hRatio',
      "dataType": "json",
      "dataSrc": "data",
      "contentType": "application/json"
    },
    "columns": [
      {
        "data": "screen_name"
      },

      {
        "data": "degree_rt"
      },
      
      {
        "data": "degree_reply"
      },

      {
        "data": "ratio"
      }
    ],

    "columnDefs": [
      {
        "className": "text-left",
        "targets": 0
      },
      {
        "className": "text-center",
        "targets": "_all"
      },
    ],
  });
}

$(formTimeseries).submit(function (e) {
  e.preventDefault();
  
  hide(btnTimeseries);
  show(btnTimeseriesReset);

  var formData = new FormData(this);
  
  var xhr = $.ajax({
    url: "/timeseries",
    type: "POST",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      
      obj = $.parseJSON(data);

      console.log(obj["timeseries"]);
        $(timeseries).attr("src", "./static/img/grafik/" + obj["timeseries"]);

      },
    error: function (xhr, ajaxOption, thrownError) {
      
      Swal.fire({
        icon: "error",
        title: "Proses Dibatalkan",
        confirmButtonColor: "#577EF4",
      });
      location.reload();
    }
  });

  btnTimeseriesReset.onclick = function () {
    xhr.abort();
    $(formTimeseries)[0].reset();
    hide(btnTimeseriesReset);
    show(btnTimeseries);
  };
});