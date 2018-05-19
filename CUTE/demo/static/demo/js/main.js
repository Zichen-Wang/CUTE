const MAX_ROW = 6, MAX_COLUMN = 6;
var row_number = 2;
var v_number = 2;

var common_types, common_facts, common_pattern;
var selected_common_types, selected_common_facts;

var sparql, results;
var negative_results;

var negative_common_strings, negative_common_types, negative_common_facts;
var selected_negative_common_strings, selected_negative_common_types, selected_negative_common_facts;

var cleaner = function(uri) {
    let wikicat = uri.indexOf("wikicat");
    if (wikicat != -1)
        return uri.slice(8).replace(new RegExp("_", 'g'), " ");
    let wordnet = uri.indexOf("wordnet");
    if (wordnet != -1)
        return uri.slice(8, uri.lastIndexOf("_")).replace(new RegExp("_", 'g'), " ");
    return uri.replace(new RegExp("_", 'g'), " ");
};

$(document).ready(entity_recommendation);
