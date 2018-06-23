var query = function () {
    $("div.sparql").append($("<h3>").text("SPARQL Query"));
    $("div.sparql").append($("<pre>").text(sparql));

    let $all_rows_results = [];
    let $all_texts_results = [];
    for (i = 0; i < results.length; i ++ ){
        let text = "";
        let entities_line = [];
        for (j = 0; j < $entities_count; j ++ ){
            text += "<p class=\"form-control-static content result\">" + results[i]['v' + j] + "</p>";
            entities_line.push(results[i]['v' + j]);
        }
        $all_rows_results.push(entities_line);
        $all_texts_results.push(text);

        let new_positive = $('<button>').attr('type', 'button').attr('class', 'btn btn-default').append($('<span>').attr('class', 'glyphicon glyphicon-ok').css('width', '1.5rem'));
        
        let new_negative = $('<button>').attr('type', 'button').attr('class', 'btn btn-default').append($('<span>').attr('class', 'glyphicon glyphicon-remove').css('width', '1.5rem'));

        let new_tr = $('<tr>').append($('<td>').append(new_positive.attr('name', $all_rows_results.length-1).click(function () {
            let name_id = parseInt(this.name);
            let inner_text = $all_texts_results[name_id];
            let entities_line = $all_rows_results[name_id];
            $all_rows.push(entities_line);
            $('<tr>').append($('<td>').append($('<button>').append($('<span>').attr('class', 'glyphicon glyphicon-minus').css('width', '1.5rem')).attr('class', 'btn btn-default').attr('name', $all_rows.length-1).click(function () {
                if (count_all_row_pos() === 1) {
                    alert("Cannot delete the last positive examples.")
                    return false;
                }
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
        })).append(new_negative.attr('name', $all_rows_results.length-1).click(function () {
            let name_id = parseInt(this.name);
            let inner_text = $all_texts_results[name_id];
            let entities_line = $all_rows_results[name_id];
            $all_rows_neg.push(entities_line);
            $('<tr>').append($('<td>').append($('<button>').append($('<span>').attr('class', 'glyphicon glyphicon-minus').css('width', '1.5rem')).attr('class', 'btn btn-default').attr('name', $all_rows_neg.length-1).click(function () {
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
