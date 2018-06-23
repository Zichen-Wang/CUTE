const MAX_ROW = 6, MAX_COLUMN = 6;
var row_number = 2;
var v_number = 2;

var common_types, common_facts, common_pattern;

var sparql, results;
var negative_results;

var negative_common_types, negative_common_facts;

var cleaner = function(uri) {
    let wikicat = uri.indexOf("wikicat");
    if (wikicat != -1)
        return uri.slice(8).replace(new RegExp("_", 'g'), " ");
    let wordnet = uri.indexOf("wordnet");
    if (wordnet != -1)
        return uri.slice(8, uri.lastIndexOf("_")).replace(new RegExp("_", 'g'), " ");
    return uri.replace(new RegExp("_", 'g'), " ");
};

var all_results = [];
var $all_rows = [];
var $all_rows_neg = [];
var $entities_count = 1;

var submit_to_server = function() {
    let entities = [];
    row_number = 0;
    for (let i = 0; i < $all_rows.length; i++) {
        if ($all_rows[i].length > 0){
            entities.push($all_rows[i]);
            row_number += 1;
        }
    }

    let payload = {
        "row_number": row_number,
        "v_number": $entities_count,
        "entities": entities
    };

    let find_attributes = $.ajax({
        type: "POST",
        url: "/demo/attributes/",
        data: JSON.stringify(payload),
        dataType: "json",
        beforeSend: function() {
            $("button").attr("disabled", true);
            $("img.entity_submitting").show();
        }
    });

    let find_pattern = $.ajax({
        type: "POST",
        url: "/demo/pattern/",
        data: JSON.stringify(payload),
        dataType: "json",
        beforeSend: function() {
            $("button").attr("disabled", true);
            $("img.entity_submitting").show();
        }
    });

    $.when(find_attributes, find_pattern).then(function(attributes_data, pattern_data) {
        common_types = attributes_data[0]["types"];
        common_facts = attributes_data[0]["facts"];
        common_pattern = pattern_data[0]["pattern"];
        attributes('');
        $("button").attr("disabled", false);
        $("img.entity_submitting").hide();
    }, function(err1, err2) {
        console.log(err1);
        console.log(err2);
        $("button").attr("disabled", false);
        $("img.entity_submitting").hide();
    });
};

var submit_to_server_neg = function() {
    let entities = [];
    row_number = 0;
    for (let i = 0; i < $all_rows_neg.length; i++) {
        if ($all_rows_neg[i].length > 0){
            entities.push($all_rows_neg[i]);
            row_number += 1;
        }
    }

    let payload = {
        "row_number": row_number,
        "v_number": $entities_count,
        "entities": entities
    };

    let find_attributes = $.ajax({
        type: "POST",
        url: "/demo/attributes/",
        data: JSON.stringify(payload),
        dataType: "json",
        beforeSend: function() {
            $("button").attr("disabled", true);
            $("img.entity_submitting_neg").show();
        }
    });

    let find_pattern = $.ajax({
        type: "POST",
        url: "/demo/pattern/",
        data: JSON.stringify(payload),
        dataType: "json",
        beforeSend: function() {
            $("button").attr("disabled", true);
            $("img.entity_submitting_neg").show();
        }
    });

    $.when(find_attributes, find_pattern).then(function(attributes_data, pattern_data) {
        negative_common_types = attributes_data[0]["types"];
        negative_common_facts = attributes_data[0]["facts"];
        //common_pattern = pattern_data[0]["pattern"];
        attributes('_neg');
        $("button").attr("disabled", false);
        $("img.entity_submitting_neg").hide();
    }, function(err1, err2) {
        console.log(err1);
        console.log(err2);
        $("button").attr("disabled", false);
        $("img.entity_submitting_neg").hide();
    });
};

$(document).ready(function() {
    $("button#reset").click(function() {
        window.location.reload();
    });
});
