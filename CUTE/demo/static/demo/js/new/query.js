var query = function () {
    $("div.sparql").append($("<h3>").text("SPARQL Query"));
    $("div.sparql").append($("<pre>").text(sparql));

    $all_rows_results = [];
    $all_texts_results = [];
    for (i = 0; i < results.length; i ++ ){
        text = "";
        entities_line = [];
        for (j = 0; j < $entities_count; j ++ ){
            text += "<span>" + results[i]['v' + j] + "</span>";
            entities_line.push(results[i]['v' + j]);
        }
        $all_rows_results.push(entities_line);
        $all_texts_results.push(text);

        new_tr = $('<tr>').append($('<td>').append($('<button>').text('+').attr('name', $all_rows_results.length-1).click(function () {
            name_id = parseInt(this.name);
            inner_text = $all_texts_results[name_id];
            entities_line = $all_rows_results[name_id];
            $all_rows.push(entities_line);
            $('<tr>').append($('<td>').append($('<a>').text('Delete').attr('name', $all_rows.length-1).click(function () {
                $all_rows[parseInt(this.name)] = [];
                this.closest('tr').remove();
                submit_to_server();
                return false;
            }))).append($('<td>').html(inner_text)).insertAfter($('#input_field'));
            $all_rows_results[name_id] = [];
            $all_texts_results[name_id] = "";
            this.closest('tr').remove();
            submit_to_server();
            return false;
        })).append($('<button>').text('-').attr('name', $all_rows_results.length-1).click(function () {
            name_id = parseInt(this.name);
            inner_text = $all_texts_results[name_id];
            entities_line = $all_rows_results[name_id];
            $all_rows_neg.push(entities_line);
            $('<tr>').append($('<td>').append($('<a>').text('Delete').attr('name', $all_rows_neg.length-1).click(function () {
                $all_rows_neg[parseInt(this.name)] = [];
                this.closest('tr').remove();
                submit_to_server_neg();
                return false;
            }))).append($('<td>').html(inner_text)).insertAfter($('#negvative_field'));
            $all_rows_results[name_id] = [];
            $all_texts_results[name_id] = "";
            this.closest('tr').remove();
            submit_to_server_neg();
            return false;
        }))).append($('<td>').html(text));
        all_results.push(new_tr);
        new_tr.insertAfter($('#results_field'));
    }
};