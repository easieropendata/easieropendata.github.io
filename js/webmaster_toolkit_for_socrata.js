function updateItemWithSimpleCount(item, data) {
  item.text(data[0][Object.keys(data[0])[0]]);
}

function handleSimpleCount() {
  $.each($('.socrata_count'), function(item) {
    var socrataUrl = $(this).attr('data-url');
    $.get(socrataUrl, function(data) {
      updateItemWithSimpleCount($(this), data);
    });
  });
}

// Anonymous "self-invoking" function
(function() {
    // Load the script
    var script = document.createElement("SCRIPT");
    script.src = 'https://code.jquery.com/jquery-2.2.0.min.js';
    script.type = 'text/javascript';
    document.getElementsByTagName("head")[0].appendChild(script);

    // Poll for jQuery to come into existance
    var checkReady = function(callback) {
        if (window.jQuery) {
            callback(jQuery);
        }
        else {
            window.setTimeout(function() { checkReady(callback); }, 100);
        }
    };

    // Start polling...
    checkReady(function($) {
        handleSimpleCount();
    });
})();
